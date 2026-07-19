import sys
import os

# Add the project directory to python path for modular relative imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_agent_memory_variations.config.settings import initialize_llm
from langchain_agent_memory_variations.core.rag import build_vectorstore
from langchain_agent_memory_variations.core.agent import get_agent
from langchain_agent_memory_variations.core.memory import (
    FullHistoryAgent,
    SlidingWindowAgent,
    SummaryWindowAgent
)

def print_banner():
    """Prints a beautiful CLI banner."""
    print("=" * 70)
    print("   🌐  LANGCHAIN AGENT & RAG MEMORY VARIATIONS PLATFORM  🌐   ".center(70))
    print("=" * 70)
    print("  Build: v1.0.0 | Tools: Weather API, SerpAPI Google Search, PDF RAG")
    print("=" * 70)

def main():
    print_banner()

    # 1. Initialize LLM
    try:
        llm = initialize_llm()
    except Exception as e:
        print(f"❌ Error initializing LLM: {e}")
        return

    # 2. Configure Vector Store (PDF)
    print("\n--- 📚 RAG Setup ---")
    while True:
        pdf_path = input("Enter path to a PDF document for RAG search (or press Enter to skip): ").strip()
        if not pdf_path:
            print("⚠️ Skipping PDF RAG configuration. The RAG tool will not be active.")
            break
        # Normalize and strip double quotes
        pdf_path = pdf_path.replace('"', '').strip()
        if os.path.exists(pdf_path):
            try:
                build_vectorstore(pdf_path)
                break
            except Exception as e:
                print(f"❌ Failed to load and build vector store: {e}. Please try again.")
        else:
            print(f"❌ File not found at: {pdf_path}. Please try again.")

    # 3. Create Agent
    try:
        agent_executor = get_agent(llm)
    except Exception as e:
        print(f"❌ Error creating agent: {e}")
        return

    # 4. Choose Memory Variation
    print("\n" + "=" * 50)
    print("   Select Chat Memory Variation   ".center(50))
    print("=" * 50)
    print("1. [Complete History] Retain entire dialogue history.")
    print("2. [Last-10 Messages] Sliding window of the 10 most recent messages.")
    print("3. [Summary + Last-10] Summarize older messages, keep last 10 intact.")
    print("=" * 50)
    
    while True:
        choice = input("Enter your choice (1-3): ").strip()
        if choice in ["1", "2", "3"]:
            break
        print("❌ Invalid input. Please enter 1, 2, or 3.")

    if choice == "1":
        chat_agent = FullHistoryAgent(agent_executor, llm)
        mode_name = "Complete History"
    elif choice == "2":
        chat_agent = SlidingWindowAgent(agent_executor, llm, max_messages=10)
        mode_name = "Sliding Window (Last-10 Messages)"
    else:
        chat_agent = SummaryWindowAgent(agent_executor, llm, window_size=10)
        mode_name = "Summary Memory + Sliding Window"

    print(f"\n⚡ Mode activated: {mode_name}")
    print("Type your questions below. Commands available:")
    print("  /clear  - Clear current conversation memory")
    print("  /exit   - Terminate program")
    print("-" * 50)

    # 5. Interactive Loop
    while True:
        try:
            question = input("\n👤 You: ").strip()
            if not question:
                continue

            if question.lower() == "/exit":
                print("👋 Exiting agent terminal. Goodbye!")
                break
            elif question.lower() == "/clear":
                chat_agent.clear()
                continue

            print("🤖 Assistant: Thinking...")
            response = chat_agent.ask(question)
            print(f"🤖 Assistant: {response}")
            
        except KeyboardInterrupt:
            print("\n👋 Exiting agent terminal. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error processing question: {e}")

if __name__ == "__main__":
    main()
