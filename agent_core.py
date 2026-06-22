"""13/06/2026 second session start"""
from dataclasses import dataclass, field, asdict 
import json
import time

@dataclass
class AgentProfile:
    agent_name: str
    model_engine: str
    temperature: float

    #default values for additional parameters
    max_retries: int = 3
    is_active: bool = True

print("Initializing AgentProfile dataclass...")

primary_agent = AgentProfile(agent_name="Corporate Communication Assistant", 
                            model_engine="gpt-4", 
                            temperature=0.7)
print(f"Primary Agent Profile: {primary_agent}")

print("Serializing AgentProfile to JSON...")
config_filename = "agent_profile_config.json"
with open(config_filename, 'w') as config_file:
    json.dump(asdict(primary_agent), config_file, indent=4)

print(f"Configuration sucessflly saved to {config_filename}")

def mock_api_call(payload:dict,
                    simulate_timeout:bool=False,
                    simulate_missing_key:bool=False):
                
    print("Simulating API call with payload:")
    print(json.dumps(payload, indent=4))
    try:
        if simulate_missing_key:
            print("Simulating missing key error...")
            malformed_response = {"status": "error", "message": "Missing required key in payload."}
            tokens=malformed_response["missing_key"]
            print(f"Token Used: {tokens}")
        if simulate_timeout:
            print("Simulating timeout error...")
            time.sleep(10)
            raise TimeoutError("Simulated API timeout occurred.")  
          
        print("API call simulation successful. Processing response...")
        return True
    
    except KeyError as e:
        print(f"KeyError encountered: {e}. Missing key in payload.")
    except TimeoutError as e:
        print(f"TimeoutError encountered: {e}. API call took too long to respond.")    
    finally:
        print("API call simulation completed.")

if __name__ == "__main__":
    mock_api_call(payload={'data':'test'}, simulate_timeout=True)
    mock_api_call(payload={'data':'test'}, simulate_missing_key=True)

