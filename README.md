# MBA Software Engineering with AI Challenge - Full Cycle

RAG (Retrieval-Augmented Generation) based search and answer system that allows asking questions about PDF documents and getting contextualized responses using AI.

## 📋 Prerequisites

- Python 3.8+
- Docker and Docker Compose
- OpenAI API Key

## 🚀 How to run the project

### 1. Clone the repository and navigate to the directory

```bash
git clone https://github.com/viniciuswb/mba-challenge-ingestion-search.git
cd mba-challenge-ingestion-search
```

### 2. Configure environment variables

Copy the example file and configure your credentials:

```bash
cp .env.example .env
```

Edit the `.env` file and add your OpenAI API key:

```bash
# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# OpenAI Model
OPENAI_MODEL=text-embedding-3-small

# PostgreSQL with PGVector settings
PGVECTOR_URL=postgresql+psycopg://postgres:postgres@localhost:5432/postgres
PGVECTOR_COLLECTION=gpt5_collection
```

### 3. Start the PostgreSQL database with PGVector

Run the command to start the database using Docker Compose:

```bash
docker-compose up -d
```

Wait a few seconds for the database to be fully initialized. You can check the status with:

```bash
docker-compose ps
```

### 4. Configure the Python virtual environment

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### 5. Run the data ingestion

Execute the ingestion script to process the PDF document and store the embeddings in the database:

```bash
python src/ingest.py
```

This command will:
- Load the `document.pdf` file
- Split the document into smaller chunks
- Generate embeddings using OpenAI
- Store the data in PostgreSQL with PGVector

### 6. Run the interactive chat

Start the chat system to ask questions about the document:

```bash
python src/chat.py
```

## 💬 How to use the chat

After running the command above, you will see the chat interface:

```
=== Question and Answer Chat ===
Type 'exit' or 'quit' to end the chat.

Ask your question:
```

**Usage example:**

```
Ask your question:
What is the revenue of SuperTechIABrazil Company?

QUESTION: What is the revenue of SuperTechIABrazil Company?
Searching for answer...
ANSWER: The revenue was 10 million reais.
--------------------------------------------------

Ask your question:
```

### Available chat commands:
- Type your question and press Enter
- To exit: `exit`, `quit`, `sair` or `q`
- Ctrl+C also ends the chat

## 🗂️ Project structure

```
├── docker-compose.yml        # PostgreSQL + PGVector configuration
├── document.pdf              # Document to be analyzed
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables example
├── README.md                 # This file
└── src/
    ├── ingest.py             # Data ingestion script
    ├── search.py             # Search and answer generation functions
    └── chat.py               # CLI chat interface
```

## 🔧 Useful commands

### Stop the database:
```bash
docker-compose down
```

### View database logs:
```bash
docker-compose logs postgres
```

### Reset the database (delete all data):
```bash
docker-compose down -v
docker-compose up -d
```

### Test only the search function:
```bash
python src/search.py
```

## 🛠️ Technologies used

- **LangChain**: Framework for LLM applications
- **OpenAI GPT**: Language model for answer generation
- **OpenAI Embeddings**: For text vectorization
- **PostgreSQL + PGVector**: Vector database for semantic search
- **PyPDF**: For PDF document processing
- **Docker**: Database containerization

## ❗ Troubleshooting

### Database connection error:
- Check if Docker is running: `docker ps`
- Restart the containers: `docker-compose restart`

### OpenAI API error:
- Check if the key is correct in the `.env` file
- Confirm if there are available credits in the OpenAI account

### Dependencies error:
- Make sure the virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Document not found:
- Check if the `document.pdf` file is in the project root
- Run the ingestion script again: `python src/ingest.py`