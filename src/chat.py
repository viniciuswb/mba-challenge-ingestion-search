import sys
from search import search_and_answer

def main():
    """
    Main CLI function that continuously prompts for questions and provides answers.
    """
    print("=== Question and Answer Chat ===")
    print("Type 'exit' or 'quit' to end the chat.\n")
    
    while True:
        try:
            # Prompt for user question
            print("Ask your question:")
            question = input().strip()
            
            # Check for exit commands
            if question.lower() in ['exit', 'quit', 'sair', 'q']:
                print("\nEnding the chat. Goodbye!")
                break
            
            # Skip empty questions
            if not question:
                print("Please enter a valid question.\n")
                continue
            
            print(f"\nQUESTION: {question}")
            
            # Get answer from search function
            print("Searching for answer...")
            answer = search_and_answer(question)
            
            print(f"ANSWER: {answer}")
            print("-" * 50)
            print()
            
        except KeyboardInterrupt:
            print("\n\nChat interrupted by user. Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\nError processing the question: {e}")
            print("Try again with a different question.\n")

if __name__ == "__main__":
    main()