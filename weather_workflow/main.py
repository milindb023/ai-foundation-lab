import sys
import os
import json
from pydantic import ValidationError

# Add project root directory to the python search path to support relative imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from weather_workflow.core.workflows import (
    run_basic_call,
    run_json_mode,
    run_structured_output,
    run_weather_workflow
)

def print_banner(title: str):
    print("\n" + "=" * 60)
    print(title.center(60))
    print("=" * 60)

def main():
    print_banner("OpenRouter & Weather Tool-Calling CLI Client")
    
    while True:
        print("\nAvailable Workflows:")
        print("1. Run Basic OpenRouter Chat Completion")
        print("2. Run JSON Mode Completion")
        print("3. Run Structured Output (Pydantic validation)")
        print("4. Run Live Weather Tool-Calling Workflow")
        print("5. Run All Demo Workflows Sequentially")
        print("6. Exit")
        
        choice = input("\nSelect workflow to execute (1-6): ").strip()
        
        if choice == "1":
            print_banner("Workflow 1: Basic Completion")
            prompt = input("Prompt (default: 'Explain what an API is in two sentences.'): ").strip()
            if not prompt:
                prompt = "Explain what an API is in two sentences."
            try:
                print("\nExecuting basic API call...")
                result = run_basic_call(prompt)
                print("\n--- Response ---")
                print(result)
            except Exception as e:
                print(f"\nError: {e}")
                
        elif choice == "2":
            print_banner("Workflow 2: JSON Mode")
            prompt = input("Prompt (default: 'Explain cosine similarity with two simple examples.'): ").strip()
            if not prompt:
                prompt = "Explain cosine similarity with two simple examples."
            try:
                print("\nExecuting JSON-mode call...")
                result = run_json_mode(prompt)
                print("\n--- Parsed JSON Dictionary ---")
                print(json.dumps(result, indent=2))
            except Exception as e:
                print(f"\nError: {e}")
                
        elif choice == "3":
            print_banner("Workflow 3: Structured Output (Pydantic Schema)")
            prompt = input("Prompt (default: 'Explain LoRA scaling in simple language.'): ").strip()
            if not prompt:
                prompt = "Explain LoRA scaling in simple language."
            try:
                print("\nExecuting Structured Output call...")
                result = run_structured_output(prompt)
                print("\n--- Validated Pydantic Schema Output ---")
                print(result.model_dump_json(indent=2))
            except ValidationError as ve:
                print(f"\nPydantic validation failed: {ve}")
            except Exception as e:
                print(f"\nError: {e}")
                
        elif choice == "4":
            print_banner("Workflow 4: Weather Agent Tool Calling")
            question = input("Weather question (default: 'What is the current weather in Kolkata?'): ").strip()
            if not question:
                question = "What is the current weather in Kolkata?"
            try:
                print("\nRunning weather tool workflow...")
                result = run_weather_workflow(question)
                print("\n--- Final Natural-Language Answer ---")
                print(result)
            except Exception as e:
                print(f"\nError: {e}")
                
        elif choice == "5":
            print_banner("Running All Workflows Sequentially")
            try:
                print("\n===============================")
                print("1. BASIC CALL")
                print("===============================")
                print(run_basic_call("Explain what an API is in two sentences."))
                
                print("\n===============================")
                print("2. JSON MODE")
                print("===============================")
                print(json.dumps(run_json_mode("Explain cosine similarity with two simple examples."), indent=2))
                
                print("\n===============================")
                print("3. STRUCTURED OUTPUT")
                print("===============================")
                concept = run_structured_output("Explain LoRA scaling in simple language.")
                print(concept.model_dump_json(indent=2))
                
                print("\n===============================")
                print("4. WEATHER TOOL WORKFLOW")
                print("===============================")
                print(run_weather_workflow("What is the current weather in Kolkata?"))
            except Exception as e:
                print(f"\nError during sequential run: {e}")
                
        elif choice == "6":
            print("\nExiting. Goodbye!")
            break
        else:
            print("Invalid selection. Please choose a option between 1 and 6.")

if __name__ == "__main__":
    main()
