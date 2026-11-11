#!/bin/bash
# Script utilitário para instalar o bot no Systemd
# Funciona automaticamente em Amazon Linux 2023 (ec2-user), Ubuntu (ubuntu) ou qualquer Linux.

set -e

USUARIO_ATUAL=$(whoami)
DIRETORIO_PROJETO=$(pwd)

echo "=== Configurando Servico Systemd Nativo ==="
echo "Detectado Usuario: $USUARIO_ATUAL"
echo "Detectado Diretorio: $DIRETORIO_PROJETO"

# Gera o arquivo de serviço sob medida para a máquina atual
cat <<EOF | sudo tee /etc/systemd/system/bot-orquestrado.service > /dev/null
[Unit]
Description=Telegram Bot com Orquestracao Nativa Systemd
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=${USUARIO_ATUAL}
WorkingDirectory=${DIRETORIO_PROJETO}

# 1. Sinal de Boot
ExecStartPre=${DIRETORIO_PROJETO}/.venv/bin/python ${DIRETORIO_PROJETO}/src/sinalizador.py start

# 2. Chatbot interativo
ExecStart=${DIRETORIO_PROJETO}/.venv/bin/python ${DIRETORIO_PROJETO}/src/test_bot.py

# 3. Sinal de Shutdown
ExecStopPost=${DIRETORIO_PROJETO}/.venv/bin/python ${DIRETORIO_PROJETO}/src/sinalizador.py stop

Restart=on-failure
RestartSec=5
TimeoutStopSec=30
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target
EOF

# Registra e ativa o serviço
sudo systemctl daemon-reload
sudo systemctl enable bot-orquestrado
sudo systemctl start bot-orquestrado

echo "=== Sucesso! Servico bot-orquestrado ativado e em execucao ==="
sudo systemctl status bot-orquestrado --no-pager
