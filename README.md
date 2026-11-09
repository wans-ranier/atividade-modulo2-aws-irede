# Meu Bot no Telegram 🤖

Este repositório contém a estrutura básica e os scripts iniciais para a criação de um bot no Telegram utilizando a linguagem Python e a biblioteca oficial assíncrona `python-telegram-bot`.

## 📚 O Que Aprendemos (Conceitos Fundamentais)

Este projeto foi construído com base nos seguintes princípios arquiteturais e de comunicação da API do Telegram:

### 1. Arquitetura e Comunicação HTTP
O bot não roda no aplicativo do celular, ele funciona como um servidor backend independente. A comunicação com os servidores em nuvem do Telegram ocorre de duas formas:
* **Long Polling:** Utilizado neste projeto (`run_polling()`). O script Python faz requisições contínuas aos servidores do Telegram perguntando por novas mensagens. Ideal para ambiente de desenvolvimento local.
* **Webhooks:** O padrão para produção. O Telegram envia ativamente um pacote de dados (POST request) para uma URL pública do nosso servidor sempre que um evento acontece.

### 2. Gatilhos e Árvore de Dados (Updates)
Toda interação do usuário (mensagens, cliques, envio de fotos) gera um evento chamado **Update**. 
O código utiliza **Handlers** (escutadores) para capturar esses eventos e extrair os dados da conversa (JSON), como:
* `update.message.text`: Captura o texto digitado.
* `update.effective_chat.id`: Identifica a sala de bate-papo para sabermos para onde enviar a resposta.

### 3. Segurança e Permissões
* **Proteção de Credenciais:** O token de acesso gerado pelo `@BotFather` é a chave mestra do bot. Ele está isolado em um arquivo `.env` (oculto e ignorado pelo `.gitignore`) para não ser exposto no código fonte.
* **Privacy Mode:** Por padrão, bots adicionados a grupos não leem todas as mensagens de usuários comuns por questões de privacidade. Eles só enxergam mensagens que começam com `/` (comandos), menções ao `@username` do bot, ou respostas diretas às mensagens dele.

---

## 📂 Estrutura do Projeto

Para facilitar a evolução de automações complexas, o projeto utiliza a seguinte organização de pastas:

```text
meu-bot-telegram/
├── .venv/                  # Ambiente virtual isolado
├── .env                    # Variáveis de ambiente secretas (Token)
├── .gitignore              # Arquivos que não devem subir para o GitHub
├── requirements.txt        # Lista de dependências (bibliotecas)
├── README.md               # Esta documentação
└── src/
    ├── test_bot.py         # Script principal de execução e configuração
    ├── test_bot2.py
    └── handlers/           # (Futuro) Scripts separados para cada comando
```

---

## 🚀 Como Configurar e Executar

Siga os passos abaixo para rodar o bot no seu ambiente Linux:

### 1. Preparar o Ambiente
Crie o ambiente virtual e ative-o:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências necessárias:
```bash
python -m pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente
Crie um arquivo chamado `.env` na raiz do projeto e adicione suas configurações (sem aspas):
```env
USER_NAME=seu_usuario
NAME=bot
LINK=https://link-aqui.com
TOKEN_API=SEU_TOKEN_GERADO_NO_BOTFATHER
```

### 3. Executar o Bot -> test_bot.py
Com o ambiente ativado, rode o script principal:
```bash
python src/test_bot.py
```
O terminal exibirá a mensagem de que o bot está rodando. Vá até o seu aplicativo do Telegram, busque pelo username do seu bot e envie um `/start` ou qualquer texto para testar a comunicação!

### 4. Executar o Bot -> teste_bot2.py
o comando para rodar o servidor. No seu terminal Linux, execute:

```bash
uvicorn src.test_bot2:app --reload
```
O parâmetro **teste_bot2:app** diz ao servidor Uvicorn para procurar o arquivo teste2.py e rodar o objeto app que criamos dentro dele