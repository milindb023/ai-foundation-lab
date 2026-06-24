from pydantic import BaseModel, ValidationError
import requests
import json

# Define the validation Model
class Validationmodel(BaseModel):
    user_name: str
    sentiment_score: int
    is_flagged_for_review: bool

print("Model defined successfully")
# Using model_json_schema() and json.dumps() to avoid Pydantic v2 deprecation warning
print("pydantic schema: \n\n" + json.dumps(Validationmodel.model_json_schema(), indent=2)) 

def analyze_user_data_via_api():
    api_url = "https://jsonplaceholder.typicode.com/posts"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer sk-mock-api-key-12345"  
    }

    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, how are you?"}
        ]
    }
    
    try:
        print("Sending request to API...")
        response = requests.post(api_url, json=payload, headers=headers)
        print("API Response:", response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    raw_api_data=analyze_user_data_via_api()
    if raw_api_data:
        try:
            validate_insight=Validationmodel(**raw_api_data)
            print("\nData validated successfully:")
            print(f"User Name: {validate_insight.user_name}")
            print(f"Sentiment Score: {validate_insight.sentiment_score + 10}")
            print(f"Is Flagged for Review: {validate_insight.is_flagged_for_review}")
        except ValidationError as e:
            print("\nData Validation Error:")
            print(e)
        except Exception as e:
            print("\nUnexpected Error:")
            print(e)
    else:
        print("No data received from API")

