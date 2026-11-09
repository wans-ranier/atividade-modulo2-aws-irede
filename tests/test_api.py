import unittest
from unittest.mock import AsyncMock, patch
from starlette.testclient import TestClient
import src.test_bot2 as mod

class TestNotificadorBot(unittest.TestCase):
    def setUp(self):
        # Mock para simular o bot do Telegram sem precisar de conexão externa nos testes
        self.mock_bot = AsyncMock()
        self.patcher = patch.object(mod, 'bot', self.mock_bot)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_health_check(self):
        """Testa se a rota / está respondendo online."""
        with TestClient(mod.app) as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {'status': 'online'})

    def test_enviar_sucesso(self):
        """Testa envio de notificação com a senha correta."""
        with TestClient(mod.app) as client:
            headers = {'Authorization': mod.SENHA_API}
            response = client.post('/enviar', json={'texto': 'Mensagem teste'}, headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {'status': 'sucesso'})
            self.mock_bot.send_message.assert_called()

    def test_enviar_senha_incorreta(self):
        """Testa rejeição 401 caso a senha esteja incorreta."""
        with TestClient(mod.app) as client:
            headers = {'Authorization': 'senha_invalida'}
            response = client.post('/enviar', json={'texto': 'Mensagem teste'}, headers=headers)
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json(), {'detail': 'Não autorizado.'})

    def test_ciclo_de_vida_startup_shutdown(self):
        """Testa se as mensagens de início e fim são disparadas no ciclo de vida."""
        with TestClient(mod.app) as client:
            # Ao iniciar a aplicação (startup)
            self.mock_bot.send_message.assert_any_call(
                chat_id=mod.CHAT_ID,
                text='🟢 [Serviço] Sistema iniciado e operacional.'
            )
        # Ao encerrar a aplicação (shutdown)
        self.mock_bot.send_message.assert_any_call(
            chat_id=mod.CHAT_ID,
            text='🔴 [Serviço] Sistema em processo de encerramento.'
        )

if __name__ == '__main__':
    unittest.main()
