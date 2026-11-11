import os
import sys
import asyncio
import logging
from dotenv import load_dotenv
from telegram import Bot

# Carrega configurações do .env
load_dotenv()

TOKEN = os.getenv("TOKEN_API")
if TOKEN:
    TOKEN = TOKEN.strip("\"' ")

CHAT_ID = os.getenv("CHAT_ID") or os.getenv("MEU_CHAT_ID")
if CHAT_ID:
    CHAT_ID = CHAT_ID.strip("\"' ")

# Silencia logs desnecessários
logging.basicConfig(level=logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)


async def disparar_sinal(etapa: str):
    """Envia uma notificação direta e objetiva de ciclo de vida para o Telegram."""
    if not TOKEN or not CHAT_ID:
        print("❌ [Sinalizador] Erro Crítico: TOKEN_API ou CHAT_ID ausentes no .env!", file=sys.stderr)
        sys.exit(1)

    bot = Bot(token=TOKEN)
    try:
        if etapa == "start":
            msg = "🟢 [Serviço] Ambiente EC2 preparado e operacional. Iniciando bot..."
            await bot.send_message(chat_id=CHAT_ID, text=msg)
            print("✅ [Sinalizador] Sinal de inicialização (Boot) entregue com sucesso no Telegram.")
        elif etapa == "stop":
            msg = "🔴 [Serviço] Sistema em processo de encerramento."
            await bot.send_message(chat_id=CHAT_ID, text=msg)
            print("✅ [Sinalizador] Sinal de encerramento (Shutdown) entregue com sucesso no Telegram.")
        else:
            print(f"❌ [Sinalizador] Etapa desconhecida: {etapa}", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"❌ [Sinalizador] Falha no envio do sinal para o Telegram: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    comando = sys.argv[1] if len(sys.argv) > 1 else "start"
    asyncio.run(disparar_sinal(comando))
