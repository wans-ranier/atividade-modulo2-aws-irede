# Bot Telegram com Orquestração Nativa (Amazon Linux 2023 / AWS EC2) 🤖☁️

Este repositório contém a implementação de um **Bot no Telegram** em Python assíncrono (`python-telegram-bot`), configurado para rodar na nuvem em uma instância **Amazon Linux 2023 (EC2)** com **Orquestração Nativa de Ciclo de Vida via Systemd**.

---

## 🎯 Funcionalidades Principais

1. **Chatbot com Whitelist Restrita:** O bot só responde ao seu `CHAT_ID` autorizado. Mensagens de estranhos são descartadas silenciosamente sem consumir processamento ou expor dados.
2. **Monitoramento Nativo de Infraestrutura:** Avisa no Telegram quando a máquina virtual da AWS ligou (boot) e quando está sendo desligada (shutdown), sem custos extras e sem necessidade de credenciais de IAM (Zero IAM).

---

## 🏗️ Como Funciona a Orquestração no Amazon Linux 2023

Delegamos o controle do ciclo de vida ao **Systemd (PID 1)** do Amazon Linux:

```text
                  ┌────────────────────────────────────────────────────────┐
                  │                 LINUX SYSTEMD (PID 1)                  │
                  │                                                        │
  [Start Instance]│  1. [ExecStartPre]  ──► Dispara src/sinalizador.py     │
  na AWS Console  │         │               (Notifica: "🟢 EC2 Ligou")     │
                  │         ▼                                              │
                  │  2. [ExecStart]     ──► Mantém src/test_bot.py ativo   │
                  │         │               (Ouve apenas seu CHAT_ID)      │
                  │         ▼                                              │
   [Stop Instance]│  3. [ExecStopPost]  ──► Dispara src/sinalizador.py     │
  na AWS Console  │                         (Notifica: "🔴 EC2 Desligando")│
                  └────────────────────────────────────────────────────────┘
```

---

## 🔒 Configurações de Privacidade e Segurança

### 1. No `@BotFather` (Telegram)
Para garantir máxima privacidade antes de subir para a nuvem:
* Abra a conversa com o `@BotFather` e envie `/mybots`.
* Selecione seu bot e vá em **Bot Settings**:
  * **Group Privacy (`/setprivacy`):** Mantenha como **ENABLED** (impede o bot de ver mensagens em grupos).
  * **Allow Groups (`/setjoingroups`):** Configure como **DISABLED** (ninguém poderá adicionar seu bot em grupos).

### 2. No Firewall da AWS (Security Group)
* **Entrada (Inbound):** Apenas porta **22 (SSH)** restrita ao seu endereço IP.
* **Saída (Outbound):** Porta **443 (HTTPS)** aberta para `0.0.0.0/0` (necessária para o Long Polling com `api.telegram.org`).

---

## 🧪 Teste Local com Docker (Amazon Linux 2023)

Antes de enviar para a AWS, você pode testar o comportamento exatamente como rodará na EC2 usando o Docker no seu PC:

```bash
# 1. Constrói a imagem do Amazon Linux 2023 com seu projeto
docker build -t bot-amazonlinux .

# 2. Roda o container passando seu arquivo .env
docker run -it --rm --env-file .env bot-amazonlinux
```

> 📱 **Teste o isolamento:** Envie mensagens pelo Telegram. O bot responderá apenas para você!

---

## 🚀 Implantação Definitiva na AWS EC2

### 1. Conectar na EC2 e Atualizar o Sistema (Amazon Linux 2023)
```bash
sudo dnf update -y
sudo dnf install -y python3 python3-pip git
```

### 2. Clonar o Repositório e Preparar o Ambiente
```bash
git clone https://github.com/wans-ranier/atividade-modulo2-aws-irede.git
cd atividade-modulo2-aws-irede
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configurar o Arquivo `.env` na EC2
```bash
nano .env
```
Cole suas credenciais:
```env
USER_NAME="seu_usuario_bot"
NAME="papagaio"
LINK="https://t.me/seu_bot"
TOKEN_API="SEU_TOKEN_GERADO_NO_BOTFATHER"
CHAT_ID="SEU_CHAT_ID_NUMERICO"
```
*(Salve com `Ctrl + O`, `Enter` e saia com `Ctrl + X`)*.

### 4. Ativar o Serviço no Systemd com 1 Comando
O instalador detecta automaticamente o usuário `ec2-user` e os caminhos:
```bash
chmod +x systemd/instalar.sh
./systemd/instalar.sh
```

### 5. Simulação via Docker do Ciclo de Vida da Ec2
Passo 1: construir a imagem 
```bash
docker build -t bot-amazonlinux .
```
Passo 2: Rodar a simulação completa
```bash
docker run -it --rm --name ec2-simulada --env-file .env bot-amazonlinux
```

---

## 🎮 Comandos Úteis na EC2

* **Ver o status do serviço:** `sudo systemctl status bot-orquestrado`
* **Ver os logs ao vivo:** `journalctl -u bot-orquestrado -f`
* **Reiniciar o bot:** `sudo systemctl restart bot-orquestrado`
* **Parar o bot:** `sudo systemctl stop bot-orquestrado`
