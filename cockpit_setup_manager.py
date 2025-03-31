#!/usr/bin/env python3

import os
import subprocess
import sys
import shutil

def check_root():
    if os.geteuid() != 0:
        print("Este script deve ser executado como root ou com privilégios de sudo.")
        sys.exit(1)

def get_distro():
    try:
        if os.path.exists("/etc/os-release"):
            with open("/etc/os-release") as f:
                for line in f:
                    if line.startswith("ID="):
                        distro = line.strip().split("=")[1].replace('"', '').lower()
                        if distro in ["rocky"]:
                            return "centos"
                        return distro
        return None
    except Exception as e:
        print(f"Erro ao detectar a distribuição: {e}")
        sys.exit(1)

def run_command(command, description=None, exit_on_error=False):
    if description:
        print(f"[*] {description}")
    try:
        result = subprocess.run(command, shell=True, check=False, 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            error_msg = result.stderr.decode().strip()
            if error_msg:
                print(f"[!] Erro: {error_msg}")
            if exit_on_error:
                sys.exit(result.returncode)
            return False
        return True
    except Exception as e:
        print(f"[!] Exceção ao executar comando: {e}")
        if exit_on_error:
            sys.exit(1)
        return False

def is_cockpit_installed():
    # Verificar via pacotes
    distro = get_distro()
    if distro in ["ubuntu", "debian"]:
        return run_command("dpkg -l cockpit 2>/dev/null | grep -q '^ii'", 
                         "Verificando pacote cockpit")
    elif distro in ["centos", "fedora", "rocky"]:
        return run_command("rpm -q cockpit >/dev/null 2>&1", 
                         "Verificando pacote cockpit")
    
    # Verificar arquivos importantes
    return os.path.exists("/usr/libexec/cockpit-ws") or os.path.exists("/usr/sbin/cockpit-ws")

def is_cockpit_active():
    result = subprocess.run("systemctl is-active cockpit.socket", shell=True, 
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0

def is_cockpit_enabled():
    result = subprocess.run("systemctl is-enabled cockpit.socket", shell=True, 
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0

def manage_cockpit_service():
    active = is_cockpit_active()
    enabled = is_cockpit_enabled()
    
    ip_address = subprocess.getoutput("hostname -I | awk '{print $1}'")
    
    if not active:
        resposta = input("[?] Cockpit não está ativo. Deseja ativá-lo? (s/n): ").strip().lower()
        if resposta == "s":
            run_command("systemctl enable --now cockpit.socket", "Ativando cockpit.socket")
            print("=" * 40)
            print(f"Cockpit ativado! Acesse: https://{ip_address}:9090")
            print("=" * 40)
    else:
        print("[*] Cockpit já está ativo e rodando")
        print(f"[*] Acesse: https://{ip_address}:9090")
        resposta = input("[?] Deseja reiniciar o serviço? (s/n): ").strip().lower()
        if resposta == "s":
            run_command("systemctl restart cockpit.socket", "Reiniciando cockpit.socket")

def install_cockpit(distro):
    print("=" * 40)
    print("Instalando o Cockpit...")
    print("=" * 40)

    success = True
    if distro in ["ubuntu", "debian"]:
        success &= run_command("apt-get update", "Atualizando repositórios")
        success &= run_command("apt-get -y install cockpit cockpit-pcp", "Instalando cockpit")
    elif distro in ["centos", "rocky"]:
        success &= run_command("yum -y install epel-release", "Instalando EPEL")
        success &= run_command("yum -y install cockpit cockpit-pcp", "Instalando cockpit")
    elif distro == "fedora":
        success &= run_command("dnf -y install cockpit", "Instalando cockpit")

    if success:
        manage_cockpit_service()
    else:
        print("[!] Falha na instalação do Cockpit")

def remove_cockpit(distro):
    print("=" * 40)
    print("Removendo o Cockpit...")
    print("=" * 40)
    
    # Parar serviços
    run_command("systemctl stop cockpit.socket cockpit.service", "Parando serviços")
    run_command("systemctl disable cockpit.socket cockpit.service", "Desativando serviços")
    
    # Remover pacotes principais sem usar wildcard
    if distro in ["ubuntu", "debian"]:
        run_command("apt-get -y remove --purge cockpit cockpit-pcp", "Removendo pacotes principais")
        run_command("apt-get -y autoremove", "Limpando dependências")
    elif distro in ["centos", "rocky", "fedora"]:
        run_command("yum -y remove cockpit cockpit-pcp", "Removendo pacotes principais")
        run_command("yum -y autoremove", "Limpando dependências")
    
    # Lista de diretórios a serem removidos
    cockpit_dirs = [
        "/etc/cockpit",
        "/usr/share/cockpit",
        "/usr/lib/cockpit",
        "/usr/libexec/cockpit",
        "/var/lib/cockpit"
    ]
    
    # Verificar quais diretórios existem
    existing_dirs = [d for d in cockpit_dirs if os.path.exists(d)]
    
    if existing_dirs:
        print("\n[!] Os seguintes diretórios foram encontrados:")
        for directory in existing_dirs:
            print(f"    - {directory}")
        
        resposta = input("\n[?] Deseja remover estes diretórios? (s/n): ").strip().lower()
        if resposta == "s":
            for directory in existing_dirs:
                try:
                    shutil.rmtree(directory)
                    print(f"[+] Removido diretório: {directory}")
                except Exception as e:
                    print(f"[!] Erro ao remover {directory}: {e}")
        else:
            print("[*] Diretórios não foram removidos.")
    else:
        print("[*] Nenhum diretório encontrado.")

    print("=" * 40)
    print("Remoção concluída!")
    print("=" * 40)

def main():
    check_root()
    distro = get_distro()

    if not distro:
        print("[!] Não foi possível detectar a distribuição")
        sys.exit(1)

    if distro not in ["debian", "ubuntu", "centos", "rocky", "fedora"]:
        print(f"[!] Distribuição não suportada: {distro}")
        sys.exit(1)

    if is_cockpit_installed():
        print("[*] Cockpit está instalado")
        resposta = input("[?] Deseja (1) remover, (2) ativar ou (3) cancelar? [1/2/3]: ").strip()
        
        if resposta == "1":
            remove_cockpit(distro)
        elif resposta == "2":
            manage_cockpit_service()
        else:
            print("[*] Operação cancelada.")
    else:
        resposta = input("[?] Cockpit não está instalado. Deseja instalá-lo? (s/n): ").strip().lower()
        if resposta == "s":
            install_cockpit(distro)
        else:
            print("[*] Operação cancelada.")

if __name__ == "__main__":
    main()