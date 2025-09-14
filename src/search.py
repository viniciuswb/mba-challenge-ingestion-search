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
        context += f"DOCUMENT (Score: {score:.2f}):\n{doc.page_content}\n\n"
    
    # Create prompt template
    PROMPT_TEMPLATE = """
    CONTEXT:
    {context}

    RULES:
    - Answer only based on the CONTEXT.
    - If the information is not explicitly in the CONTEXT, respond:
      "I don't have the necessary information to answer your question."
    - Never invent or use external knowledge.
    - Never produce opinions or interpretations beyond what is written.
    - Always answer in the same language as the question. 
      If the question is in Portuguese, answer in Portuguese. If the question is in English, answer in English.

    Examples of words to be translated:
    - "faturamento" -> "revenue"
    - "ano de fundação" -> "foundation year"

    EXAMPLES OF QUESTIONS OUTSIDE THE CONTEXT:
    Question: "What is the capital of France?"
    Answer: "I don't have the necessary information to answer your question."

    Question: "How many clients do we have in 2024?"
    Answer: "I don't have the necessary information to answer your question."

    Question: "Do you think this is good or bad?"
    Answer: "I don't have the necessary information to answer your question."

    USER QUESTION:
    {question}

    ANSWER THE "USER QUESTION"
    """
    
    prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
    
    # Format the prompt with context and question
    formatted_prompt = prompt.format(context=context, question=question)
    
    # Call the LLM and get the response
    response = llm.invoke(formatted_prompt)
    
    # Return the answer content
    return response.content


# Main execution for testing
if __name__ == "__main__":
    query = "What is the revenue of Alfa Energia Holding company?"
    
    try:
        answer = search_and_answer(query)
        print(f"Question: {query}")
        print(f"Answer: {answer}")
    except Exception as e:
        print(f"Error searching for answer: {e}")