#!/bin/bash
set -e

echo "=========================================================="
echo " INICIANDO SIMULAÇÃO DE AMBIENTE AWS EC2 NO DOCKER"
echo " SO: Amazon Linux 2023 | Orquestração de Ciclo de Vida"
echo "=========================================================="

# 1. Validação de Arquitetura e Arquivos de Sistema
echo "[Teste 1/4] Verificando integridade dos scripts e configs do Systemd..."
if [ ! -f "systemd/bot-orquestrado.service" ] || [ ! -f "systemd/instalar.sh" ]; then
    echo "❌ FALHA: Arquivos em systemd/ ausentes ou corrompidos!"
    exit 1
fi
echo "✅ Arquivos do Systemd validados com sucesso."

# 2. Validação de Credenciais
echo "[Teste 2/4] Verificando variáveis de ambiente..."
if [ -z "$TOKEN_API" ] || [ -z "$CHAT_ID" ]; then
    echo "❌ FALHA: TOKEN_API ou CHAT_ID não fornecidos ao container!"
    exit 1
fi
echo "✅ Variáveis de ambiente carregadas."

# 3. Tratamento de Sinais de Desligamento da VM (SIGTERM = Stop na AWS, SIGINT = Ctrl+C)
shutdown_handler() {
    echo ""
    echo "=========================================================="
    echo " 🛑 [Simulação AWS EC2] Sinal de Desligamento Recebido!"
    echo " (Simulando sinal ACPI Shutdown da AWS / ExecStopPost)"
    echo "=========================================================="
    
    echo "Disparando sinalizador de encerramento..."
    if ! python3 src/sinalizador.py stop; then
        echo "❌ TESTE FALHOU: O sinalizador não conseguiu notificar o shutdown no Telegram!"
        exit 1
    fi
    
    if [ -n "$BOT_PID" ]; then
        echo "Encerrando processo do chatbot ..."
        kill -TERM "$BOT_PID" 2>/dev/null || true
        wait "$BOT_PID" 2>/dev/null || true
    fi
    
    echo "✅ [Sucesso] Ciclo de desligamento concluído com sucesso."
    exit 0
}

trap shutdown_handler SIGTERM SIGINT

# 4. Sinal de Inicialização da Infraestrutura (Simula ExecStartPre do Systemd)
echo "[Teste 3/4] Disparando sinal de Boot (ExecStartPre)..."
if ! python3 src/sinalizador.py start; then
    echo "❌ TESTE FALHOU: O sinalizador de Boot não conseguiu notificar no Telegram!"
    exit 1
fi
echo "✅ Notificação de Boot entregue no Telegram."

# 5. Inicialização do Chatbot (Simula ExecStart do Systemd)
echo "[Teste 4/4] Iniciando chatbot interativo (ExecStart)..."
echo "O bot está online! Envie mensagens no Telegram para testar a comunicação."
echo "Para simular o desligamento da EC2, pressione Ctrl + C ou envie 'docker stop'."
echo "----------------------------------------------------------"

python3 src/test_bot.py &
BOT_PID=$!

# Aguarda o processo em primeiro plano sem travar o trap
wait "$BOT_PID"
