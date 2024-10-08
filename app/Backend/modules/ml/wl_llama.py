import os
from config import *

class OllamaChat:
    def __init__(self):
        self.context = []
    def send_message(self, message):
        self.context.append(message)  
        input_text = ' '.join(self.context)  
        command = f"ollama run {OLLAMA_MODEL} \"{input_text}\""
        response = os.popen(command).read()
        self.context.append(response.strip())  
        return response.strip()