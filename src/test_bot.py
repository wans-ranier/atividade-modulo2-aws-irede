import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Carrega as variáveis do arquivo .env
load_dotenv()

TOKEN = os.getenv("TOKEN_API")
if TOKEN:
    TOKEN = TOKEN.strip("\"' ")

BOT_NAME = os.getenv("NAME", "Bot")
if BOT_NAME:
    BOT_NAME = BOT_NAME.strip("\"' ")

AUTHORIZED_CHAT_ID = os.getenv("CHAT_ID")
if AUTHORIZED_CHAT_ID:
    AUTHORIZED_CHAT_ID = AUTHORIZED_CHAT_ID.strip("\"' ")

# Configuração de logging seguro
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
# Silencia logs detalhados do httpx para não expor a URL com o token no terminal
logging.getLogger("httpx").setLevel(logging.WARNING)


def check_auth(update: Update) -> bool:
    """Verifica se quem enviou a mensagem é o proprietário autorizado do bot."""
    if not AUTHORIZED_CHAT_ID:
        logging.warning("CHAT_ID não definido no .env! Mensagem aceita sem filtro de segurança.")
        return True

    remetente_id = str(update.effective_chat.id)
    if remetente_id != str(AUTHORIZED_CHAT_ID).strip():
        usuario = update.effective_user.username or update.effective_user.first_name
        logging.warning(
            f"🚫 [Segurança] Acesso negado! Mensagem bloqueada de usuário não autorizado: "
            f"{usuario} (ID: {remetente_id})"
        )
        return False
    return True


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde ao comando /start (Apenas para o dono autorizado)"""
    if not check_auth(update):
        return  # Ignora silenciosamente qualquer estranho

    usuario = update.effective_chat.first_name
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Olá, {usuario}! Eu sou o bot {BOT_NAME}, estou ativo e exclusivo para você."
    )


async def repeat_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde a mensagens de texto (Apenas para o dono autorizado)"""
    if not check_auth(update):
        return  # Ignora silenciosamente qualquer estranho

    logging.info(f"Mensagem autorizada de {update.effective_user.first_name}: {update.message.text}")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{update.message.text}"
    )


if __name__ == "__main__":
    if not TOKEN:
        raise ValueError("ERRO: TOKEN_API não configurado no arquivo .env!")

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, repeat_text))

    print(f"Bot {BOT_NAME} rodando... (Bloqueio de segurança ativado para CHAT_ID: {AUTHORIZED_CHAT_ID})")
    application.run_polling()
