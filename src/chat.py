import sys
from search import search_and_answer

def main():
    """
    Main CLI function that continuously prompts for questions and provides answers.
    """
    print("=== Chat de Perguntas e Respostas ===")
    print("Digite 'sair' ou 'quit' para encerrar o chat.\n")
    
    while True:
        try:
            # Prompt for user question
            print("Faça sua pergunta:")
            question = input().strip()
            
            # Check for exit commands
            if question.lower() in ['sair', 'quit', 'exit', 'q']:
                print("\nEncerrando o chat. Até logo!")
                break
            
            # Skip empty questions
            if not question:
                print("Por favor, digite uma pergunta válida.\n")
                continue
            
            print(f"\nPERGUNTA: {question}")
            
            # Get answer from search function
            print("Buscando resposta...")
            answer = search_and_answer(question)
            
            print(f"RESPOSTA: {answer}")
            print("-" * 50)
            print()
            
        except KeyboardInterrupt:
            print("\n\nChat interrompido pelo usuário. Até logo!")
            sys.exit(0)
        except Exception as e:
            print(f"\nErro ao processar a pergunta: {e}")
            print("Tente novamente com uma pergunta diferente.\n")

if __name__ == "__main__":
    main()