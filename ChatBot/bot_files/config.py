import os
def setup_key():
    os.environ["OPENAI_API_KEY"] = "" #OpenAI Key
    return "Setup Complete"
