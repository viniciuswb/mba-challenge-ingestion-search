import os
from dotenv import load_dotenv

from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()
for k in ("OPENAI_API_KEY", "PGVECTOR_URL", "PGVECTOR_COLLECTION"):
    if k not in os.environ:
        raise ValueError(f"Environment variable {k} not set")
    
def search_and_answer(question: str) -> str:
    """
    Search for relevant documents and generate an answer based on the context.
    
    Args:
        question (str): The question to search for and answer
        
    Returns:
        str: The generated answer based on the retrieved context
    """
    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-5-nano",
        temperature=0
    )
    
    # Initialize embeddings
    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL", "text-embedding-3-small"))
    
    # Initialize vector store
    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PGVECTOR_COLLECTION"),
        connection=os.getenv("PGVECTOR_URL"),
        use_jsonb=True,
    )
    
    # Search for relevant documents (k=10 as requested)
    results = store.similarity_search_with_score(query=question, k=10)
    
    # Create context from retrieved documents
    context = ""
    for doc, score in results:
        context += f"DOCUMENTO (Score: {score:.2f}):\n{doc.page_content}\n\n"
    
    # Create prompt template
    PROMPT_TEMPLATE = """
    CONTEXTO:
    {contexto}

    REGRAS:
    - Responda somente com base no CONTEXTO.
    - Se a informação não estiver explicitamente no CONTEXTO, responda:
      "Não tenho informações necessárias para responder sua pergunta."
    - Nunca invente ou use conhecimento externo.
    - Nunca produza opiniões ou interpretações além do que está escrito.

    EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
    Pergunta: "Qual é a capital da França?"
    Resposta: "Não tenho informações necessárias para responder sua pergunta."

    Pergunta: "Quantos clientes temos em 2024?"
    Resposta: "Não tenho informações necessárias para responder sua pergunta."

    Pergunta: "Você acha isso bom ou ruim?"
    Resposta: "Não tenho informações necessárias para responder sua pergunta."

    PERGUNTA DO USUÁRIO:
    {pergunta}

    RESPONDA A "PERGUNTA DO USUÁRIO"
    """
    
    prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
    
    # Format the prompt with context and question
    formatted_prompt = prompt.format(contexto=context, pergunta=question)
    
    # Call the LLM and get the response
    response = llm.invoke(formatted_prompt)
    
    # Return the answer content
    return response.content


# Main execution for testing
if __name__ == "__main__":
    query = "Qual o faturamento da empresa alfa energia holding?"
    
    try:
        answer = search_and_answer(query)
        print(f"Pergunta: {query}")
        print(f"Resposta: {answer}")
    except Exception as e:
        print(f"Erro ao buscar resposta: {e}")