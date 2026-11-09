# Teste 2: Bot como Servidor de Notificações (FastAPI) 🚀

Este documento explica o funcionamento do script `teste2.py`, que introduz uma arquitetura diferente para o bot do Telegram.

## 🏗️ Objetivo e Arquitetura

Enquanto um script tradicional de bot (Polling) fica "escutando" as conversas no aplicativo, este teste transforma o bot em um **Microserviço de Notificações de mão única**.

Nesta arquitetura, o bot **não lê** mensagens do usuário. Em vez disso, ele levanta um servidor web (usando o framework **FastAPI**) que aguarda requisições HTTP de sistemas externos. Quando recebe um chamado válido, ele usa a API do Telegram apenas para *disparar* um alerta para um chat específico.

**Casos de uso reais para esta arquitetura:**

* Avisar no Telegram que o backup de um banco de dados foi concluído.
* Receber um alerta quando alguém finaliza uma compra no seu site.
* Integrar com ferramentas de automação como n8n ou Zapier.

## ⚙️ Configuração do Ambiente

Além das configurações básicas de token, este script exige duas novas variáveis no arquivo `.env`:

```env
# Seu ID numérico único do Telegram (onde a notificação será entregue)
MEU_CHAT_ID=123456789

# Uma senha inventada por você para proteger sua API contra invasores
SENHA_API=SuaSenhaSecretaAqui
```

Além das configurações básicas de token, este script exige duas novas variáveis no arquivo `.env`:

```env
# Seu ID numérico único do Telegram (onde a notificação será entregue)
MEU_CHAT_ID=123456789

# Uma senha inventada por você para proteger sua API contra invasores
SENHA_API=SuaSenhaSecretaAqui
```


## 🚀 Como Executar o Servidor (src/test_bot2.py)

Para iniciar o servidor FastAPI localmente (para testes), abra seu terminal e execute:

```bash
uvicorn src.test_bot2:app --reload
```

O servidor ficará ativo na sua própria máquina no endereço local: `http://localhost:8000`.

## 🧪 Como Testar (Simulando um Sistema Externo)

Abra outro terminal para testar. Usaremos o comando `curl` para simular um sistema externo fazendo uma requisição HTTP POST para o nosso bot. 

*Nota: No ambiente de testes (sua máquina), usamos `localhost`. Quando você colocar este bot em um servidor real na internet, você trocará `localhost:8000` pelo domínio ou IP público do seu servidor (ex: `api.seudominio.com`).*

### Teste de Sucesso (Com a senha correta)

```bash
curl -X POST "http://localhost:8000/enviar" \
     -H "Content-Type: application/json" \
     -H "Authorization: SuaSenhaSecretaAqui" \
     -d '{"texto": "Teste de sistema: Servidor FastAPI operando perfeitamente!"}'
```

**Resultado esperado:** Você receberá a mensagem instantaneamente no seu aplicativo do Telegram.

### Teste de Falha de Segurança (Senha incorreta)

```bash
curl -X POST "http://localhost:8000/enviar" \
     -H "Content-Type: application/json" \
     -H "Authorization: SenhaIncorreta" \
     -d '{"texto": "Esta mensagem não deve chegar."}'
```

**Resultado esperado:** A API bloqueará o disparo e retornará um erro `401 Unauthorized`, protegendo o seu bot contra disparos não autorizados.