# Cockpit Setup Manager

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Cockpit](https://img.shields.io/badge/Cockpit-0066CC?style=for-the-badge&logo=cockpit&logoColor=white)
![Debian](https://img.shields.io/badge/Debian-A81D33?style=for-the-badge&logo=debian&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![CentOS](https://img.shields.io/badge/Cent%20OS-262577?style=for-the-badge&logo=centos&logoColor=white)
![Fedora](https://img.shields.io/badge/Fedora-294172?style=for-the-badge&logo=fedora&logoColor=white)
![Rocky Linux](https://img.shields.io/badge/Rocky%20Linux-10B981?style=for-the-badge&logo=rockylinux&logoColor=white)

Script Python para instalar ou remover o **Cockpit**, ferramenta de administração web para servidores Linux.

## 📋 Funcionalidades

✔️ Detecta automaticamente sua distribuição Linux  
✔️ Instala o Cockpit com todos os componentes essenciais  
✔️ Remove completamente o Cockpit e seus arquivos residuais  
✔️ Configura automaticamente o serviço para iniciar com o sistema  
✔️ Exibe o URL de acesso após instalação  

## 🐧 Distribuições Suportadas

- **Debian**
- **Ubuntu**
- **CentOS**
- **Rocky Linux**
- **Fedora**

## ⚙️ Pré-requisitos

- Python 3.x
- Privilégios root/sudo
- Conexão com a internet (para instalar pacotes)

## 🚀 Como Usar

1. Clone o repositório ou baixe o script:
   ```bash
   git clone https://github.com/jwsallesbr/cockpit-setup-manager.git
   cd cockpit-setup-manager
   ```
2. Torne o script executável:
   ```bash
   chmod +x cockpit-setup-manager.py
   ```
3. Execute como root/sudo:
   ```bash
   sudo ./cockpit-setup-manager.py
      ```

Siga as instruções para:

   Instalar
   <img src="install.png">

   Ativar
   <img src="activate.png">

   Remover
   <img src="remove.png">
   

🌐 Após a instalação, o serviço será ativado e a interface poderá ser acessada via web:
```
https://<IP-DO-SERVIDOR>:9090
```
