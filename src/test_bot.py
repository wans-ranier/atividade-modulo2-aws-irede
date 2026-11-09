import os
import logging
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler

# Carrega as variáveis do arquivo .env para o sistema
load_dotenv()

# Busca as variáveis pelo nome exato que está no .env
TOKEN = os.getenv("TOKEN_API")
BOT_NAME = os.getenv("NAME")

logging.basicConfig(level=logging.INFO)
# Silencia logs detalhados do httpx para não expor a URL com o token no terminal
logging.getLogger("httpx").setLevel(logging.WARNING)

#Objeto	Para que serve
# Update: Contém toda info da mensagem recebida (update.message.text, update.effective_chat.id, update.effective_user, etc.)
# ContextTypes.DEFAULT_TYPE: Acesso ao bot (context.bot), dados do usuário (context.user_data), chat (context.chat_data), job queue, etc.
#  Dentro do metodo do bot, "send_message()", o parametro "text" esta recebendo o texto da mensagem do usuario
async def Repeat_Text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde a QUALQUER mensagem de texto"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{update.message.text}"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=f"Olá, {update.effective_chat.first_name}! Eu sou o bot {BOT_NAME}, vou repetir todo texto que em enviar"
    )
    

if __name__ == '__main__':
    # Usa a variável TOKEN de forma segura
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, Repeat_Text))

    
    print(f"Bot {BOT_NAME} rodando...")
    application.run_polling()   