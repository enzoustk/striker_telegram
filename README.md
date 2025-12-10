
# Striker Telegram

**Striker Telegram** é uma biblioteca Python leve projetada para facilitar a integração com a API de Bots do Telegram. Ela permite enviar e editar mensagens, além de lidar com a formatação de texto para MarkdownV2.

## 📋 Funcionalidades

* **Enviar Mensagens:** Envio simples de mensagens de texto para chats ou canais.
* **Editar Mensagens:** Capacidade de atualizar o texto de mensagens já enviadas.
* **Utilitários de Formatação:** Função auxiliar para escapar caracteres especiais reservados do MarkdownV2.
* **Gerenciamento de Rate Limit:** Tratamento automático básico para o erro 429 (Too Many Requests).

## 🚀 Instalação

Como o projeto possui um arquivo `pyproject.toml`, você pode instalar a biblioteca diretamente na raiz do projeto usando o pip:

```bash
pip install .
````

Ou instalar as dependências manualmente listadas no `requirements.txt`:

```bash
pip install -r requirements.txt
```

*Dependências:* Esta biblioteca requer o pacote `requests`.

## 💻 Como Usar

### 1\. Enviar uma Mensagem

Use o módulo `message` para enviar mensagens. A função `send` retorna o ID da mensagem e o ID do chat em caso de sucesso.

```python
from striker_telegram.message import send

# Substitua pelo seu Token e Chat ID
TOKEN = "SEU_BOT_TOKEN"
CHAT_ID = "SEU_CHAT_ID"

msg_id, chat_id = send(
    message="Olá, mundo! Esta é uma mensagem de teste.",
    chat_id=CHAT_ID,
    token=TOKEN,
    verbose=True  # Imprime log de sucesso no console
)

if msg_id:
    print(f"Mensagem enviada com sucesso: {msg_id}")
```

**Parâmetros de `send`**:

  * `message`: O texto a ser enviado.
  * `chat_id`: O identificador único do chat alvo.
  * `token`: O token do seu bot Telegram.
  * `parse_mode`: O modo de formatação (padrão: `"MarkdownV2"`).
  * `hide_web_page_preview`: Se `True`, esconde pré-visualizações de links (padrão: `True`).
  * `verbose`: Se `True`, imprime mensagens de status no console (padrão: `True`).

### 2\. Editar uma Mensagem

Para alterar uma mensagem existente, use a função `edit`. É necessário saber o `message_id` da mensagem original.

```python
from striker_telegram.message import edit

# Supondo que você tem o msg_id de um envio anterior
novo_texto = "Este texto foi editado via script!"

sucesso = edit(
    message_id=msg_id,
    message=novo_texto,
    chat_id=CHAT_ID,
    token=TOKEN
)

if sucesso:
    print("A mensagem foi atualizada.")
```

### 3\. Escapar Caracteres para MarkdownV2

O Telegram MarkdownV2 exige que muitos caracteres especiais sejam "escapados" (precedidos por `\`). O módulo `escape` facilita essa tarefa.

```python
from striker_telegram.escape import markdown_v2
from striker_telegram.message import send

texto_cru = "Olá! Tenho pontos final., parênteses () e underscores _."
texto_seguro = markdown_v2(texto_cru)

send(
    message=f"*Mensagem Segura:*\n{texto_seguro}",
    chat_id=CHAT_ID,
    token=TOKEN,
    parse_mode="MarkdownV2"
)
```

## 🛠️ Estrutura do Projeto

  * **`striker_telegram/message.py`**: Contém a lógica principal para interagir com a API do Telegram (`send`, `edit`).
  * **`striker_telegram/escape.py`**: Utilitário para sanitizar strings para MarkdownV2.

## 📝 Autores

  * **enzoustk**
