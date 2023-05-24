'''This file is used to setup the OpenAI API Key.'''

import os
def setup_key():
    '''This function sets up the OpenAI API Key.'''
    # Dont need the below line if you have the key in your environment variables
    if "OPENAI_API_KEY" not in os.environ:
        os.environ["OPENAI_API_KEY"] = ""   # OpenAI Key
    return "Setup Complete"