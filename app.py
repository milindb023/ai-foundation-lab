user_database=[ 
{"id": 101, "name": "Alice", "role": "admin", "is_active": True},
{"id": 102, "name": "Bob", "role": "user", "is_active": False},
{"id": 103, "name": "Charlie", "role": "user", "is_active": True}
]

i=0
active_users = []
for user in user_database:
    if user["is_active"]:
        print(f"Active user: {user['name']} (ID: {user['id']})")
        active_users.append(user)   
        i += 1
print(f"Total active users: {i}")

context_block = ""
for index, user in enumerate(active_users, start=1):                             
    context_block += f"{index}. {user['name']} \n"
print("Context Block for Active Users:")
print(context_block)

system_prompt = f"""System Instruction: you are corporate communication assistant, your task is to generate a message for the active users in the database.
Context: The following users are active in the system:
{context_block}
keep tone professional and concise, and address the users by their names in the message.
"""
print("System Prompt:")
print(system_prompt)

def execute_llm_call(prompt_text,model_engine="gpt-4",**kwargs):
    print(f"Routing request to target LLM model engine: {model_engine}")
    print(f"Prompt text: {prompt_text}")
    print(f"Additional parameters: {kwargs}")
    print("Executing LLM call...")
    return f"Mock API Output: Welcome aboard, {', '.join([user['name'] for user in active_users])}! We are excited to have you as part of our active user community. Please stay engaged and reach out if you need any assistance.  Thank you for being an active member of our platform.   "

if __name__ == "__main__":
    api_response = execute_llm_call(system_prompt, model_engine="gpt-4", temperature=0.7, max_tokens=150)
    print("API Response:")
    print(api_response)
    