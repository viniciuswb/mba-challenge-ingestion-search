# Desafio MBA Engenharia de Software com IA - Full Cycle

Sistema de busca e resposta baseado em RAG (Retrieval-Augmented Generation) que permite fazer perguntas sobre documentos PDF e obter respostas contextualizadas usando IA.

## 📋 Pré-requisitos

- Python 3.8+
- Docker e Docker Compose
- Chave da API OpenAI

## 🚀 Como executar o projeto

### 1. Clone o repositório e navegue até o diretório

```bash
git clone https://github.com/viniciuswb/mba-challenge-ingestion-search.git
cd mba-challenge-ingestion-search
```

### 2. Configure as variáveis de ambiente

Copie o arquivo de exemplo e configure suas credenciais:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione sua chave da API OpenAI:

```bash
# OpenAI API Key
OPENAI_API_KEY=sua_chave_api_openai_aqui

# OpenAI Model
OPENAI_MODEL=text-embedding-3-small

# PostgreSQL with PGVector settings
PGVECTOR_URL=postgresql+psycopg://postgres:postgres@localhost:5432/postgres
PGVECTOR_COLLECTION=gpt5_collection
```

### 3. Inicie o banco de dados PostgreSQL com PGVector

Execute o comando para subir o banco de dados usando Docker Compose:

```bash
docker-compose up -d
```

Aguarde alguns segundos para que o banco seja inicializado completamente. Você pode verificar o status com:

```bash
docker-compose ps
```

### 4. Configure o ambiente virtual Python

Crie e ative um ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate  # No macOS/Linux
# ou
venv\Scripts\activate     # No Windows
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

### 5. Execute a ingestão dos dados

Execute o script de ingestão para processar o documento PDF e armazenar os embeddings no banco:

```bash
python src/ingest.py
```

Este comando irá:
- Carregar o arquivo `document.pdf`
- Dividir o documento em chunks menores
- Gerar embeddings usando OpenAI
- Armazenar os dados no banco PostgreSQL com PGVector

### 6. Execute o chat interativo

Inicie o sistema de chat para fazer perguntas sobre o documento:

```bash
python src/chat.py
```

## 💬 Como usar o chat

Após executar o comando acima, você verá a interface do chat:

```
=== Chat de Perguntas e Respostas ===
Digite 'sair' ou 'quit' para encerrar o chat.

Faça sua pergunta:
```

**Exemplo de uso:**

```
Faça sua pergunta:
Qual o faturamento da Empresa SuperTechIABrazil?

PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?
Buscando resposta...
RESPOSTA: O faturamento foi de 10 milhões de reais.
--------------------------------------------------

Faça sua pergunta:
```

### Comandos disponíveis no chat:
- Digite sua pergunta e pressione Enter
- Para sair: `sair`, `quit`, `exit` ou `q`
- Ctrl+C também encerra o chat

## 🗂️ Estrutura do projeto

```
├── docker-compose.yml        # Configuração do PostgreSQL + PGVector
├── document.pdf              # Documento a ser analisado
├── requirements.txt          # Dependências Python
├── .env.example              # Exemplo de variáveis de ambiente
├── README.md                 # Este arquivo
└── src/
    ├── ingest.py             # Script de ingestão de dados
    ├── search.py             # Funções de busca e geração de respostas
    └── chat.py               # Interface CLI do chat
```

## 🔧 Comandos úteis

### Parar o banco de dados:
```bash
docker-compose down
```

### Ver logs do banco:
```bash
docker-compose logs postgres
```

### Resetar o banco (apagar todos os dados):
```bash
docker-compose down -v
docker-compose up -d
```

### Testar apenas a função de busca:
```bash
python src/search.py
```

## 🛠️ Tecnologias utilizadas

- **LangChain**: Framework para aplicações com LLM
- **OpenAI GPT**: Modelo de linguagem para geração de respostas
- **OpenAI Embeddings**: Para vetorização de texto
- **PostgreSQL + PGVector**: Banco vetorial para busca semântica
- **PyPDF**: Para processamento de documentos PDF
- **Docker**: Containerização do banco de dados

## ❗ Solução de problemas

### Erro de conexão com o banco:
- Verifique se o Docker está rodando: `docker ps`
- Reinicie os containers: `docker-compose restart`

### Erro de API OpenAI:
- Verifique se a chave está correta no arquivo `.env`
- Confirme se há créditos disponíveis na conta OpenAI

### Erro de dependências:
- Certifique-se de que o ambiente virtual está ativado
- Reinstale as dependências: `pip install -r requirements.txt`

### Documento não encontrado:
- Verifique se o arquivo `document.pdf` está na raiz do projeto
- Execute novamente o script de ingestão: `python src/ingest.py`