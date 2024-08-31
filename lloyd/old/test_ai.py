
from kate import AIInterface, get_response

ai_interface = AIInterface(config_path="/Users/aimaggie.com/projects/aimaggie.com/config.json")

response = get_response("what is the capital of France?","llama3")

print(response)