# Telegram Message Sender

Este é um aplicativo Python para enviar mensagens em massa via Telegram usando a biblioteca [Telethon](https://github.com/LonamiWebs/Telethon). Ele permite gerenciar logins, mensagens e usuários de forma prática.

## ⚙️ Funcionalidades

- Enviar mensagens para múltiplos usuários no Telegram.
- Gerenciar uma lista de mensagens pré-salvas.
- Salvar e reutilizar dados de login.
- Excluir dados de login armazenados para segurança.
- Verificar duplicatas ao adicionar novos usuários.

---

## 🛠️ Configuração e Instalação

### Requisitos

- Python 3.8 ou superior.
- Biblioteca `Telethon`.
- Dados da API do Telegram (API_ID e API_HASH). Você pode obter esses dados criando um aplicativo no [Telegram Developers](https://my.telegram.org/apps).

### Instalando as Dependências

1. Clone o repositório ou copie o código.
2. Instale as dependências necessárias:
   ```bash
   pip install telethon

