import os
import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel
from telegram import Bot

# Carrega variáveis do arquivo .env
load_dotenv()

TOKEN = os.getenv("TOKEN_API")
CHAT_ID = os.getenv("CHAT_ID") or os.getenv("MEU_CHAT_ID")
SENHA_API = os.getenv("SENHA_API")

logging.basicConfig(level=logging.INFO)
# Silencia logs do httpx para não vazar a URL contendo o Token da API do Telegram
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Inicializa o cliente do Telegram Bot
bot = Bot(token=TOKEN) if TOKEN else None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerenciador de ciclo de vida do FastAPI:
    Apenas sinaliza as etapas de inicialização e encerramento.
    """
    # 🟢 Notificação simples de inicialização
    if bot and CHAT_ID:
        try:
            msg_inicio = "🟢 [Serviço] Sistema iniciado e operacional."
            await bot.send_message(chat_id=CHAT_ID, text=msg_inicio)
            logger.info("Notificação de inicialização enviada ao Telegram.")
        except Exception as e:
            logger.error(f"Erro ao enviar notificação de inicialização: {e}")

    yield  # Aplicação segue rodando

    # 🔴 Notificação simples de encerramento
    if bot and CHAT_ID:
        try:
            msg_fim = "🔴 [Serviço] Sistema em processo de encerramento."
            await bot.send_message(chat_id=CHAT_ID, text=msg_fim)
            logger.info("Notificação de encerramento enviada ao Telegram.")
        except Exception as e:
            logger.error(f"Erro ao enviar notificação de encerramento: {e}")

app = FastAPI(
    title="Notificador Telegram",
    description="Servidor FastAPI para disparo de notificações no Telegram",
    lifespan=lifespan
)

class MensagemInput(BaseModel):
    texto: str

@app.get("/")
def health_check():
    """Rota simples para checagem de saúde da aplicação."""
    return {"status": "online"}

@app.post("/enviar")
async def enviar_notificacao(dados: MensagemInput, authorization: str = Header(None)):
    """
    Endpoint para envio de notificações genéricas.
    Exige autenticação via Header 'Authorization'.
    """
    if not SENHA_API or authorization != SENHA_API:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autorizado."
        )

    if not bot or not CHAT_ID:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Configurações ausentes no servidor."
        )

    try:
        await bot.send_message(chat_id=CHAT_ID, text=dados.texto)
        return {"status": "sucesso"}
    except Exception as e:
        logger.error(f"Falha ao enviar mensagem: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Falha ao enviar mensagem."
        )
