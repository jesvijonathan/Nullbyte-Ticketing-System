import os
import json
from mimetypes import guess_type
import base64
from config import *
import requests
import json
import base64
from mimetypes import guess_type

class OllamaChat:
    def __init__(self, http_mode=ollama_http):
        self.context = []
        self.llama_http = http_mode
        self.ollama_url = ollama_url  

    def send_message(self, message):
        try:
            self.context.append(message)
            attachment_data = ""
            if message['attachments']:
                for count, attachment in enumerate(message['attachments'], start=1):
                    file_path = attachment['file']
                    binary_file_data = attachment['data']
                    with open(file_path, 'wb') as f:
                        f.write(base64.b64decode(binary_file_data))

                    mime_type = guess_type(file_path)[0]
                    if mime_type in ('text/plain', 'text/html', 'text/csv', 'text/xml', 'text/rtf', 'text/richtext', 'application/json'):
                        with open(file_path, 'r') as f:
                            file_content = f.read()
                        attachment_info = f"Attachment {count}: {file_content}"
                        attachment_data += attachment_info + "\n"

            last_message = ""
            message_history = ""
            try:
                message_history = json.loads(message["message"])
            except:
                pass

            try:
                for key in sorted(message_history.keys()):
                    msg = message_history[key]
                    if not (msg['recipient'] == "wl_vertex" or msg['recipient'] == "wl_llama"):
                        last_message = msg['message']
            except:
                last_message = message["message"]

            history = ""
            try:
                for key in sorted(message_history.keys()):
                    msg = message_history[key]
                    history += f"{msg['recipient']}: {msg['message']}\n"
            except:
                pass

            ollama_text = f"{last_message}\n\n{history}\n\n{attachment_data}"

            if self.llama_http:
                payload = {
                    "model": OLLAMA_MODEL,  
                    "input": ollama_text
                }
                
                response = requests.post(self.ollama_url, json=payload)

                if response.status_code == 200:
                    response_data = response.json()
                    self.context.append(response_data['output'])
                    return response_data['output']
                else:
                    error_message = f"HTTP error {response.status_code}: {response.text}"
                    print(error_message)
                    return json.dumps({"error": error_message})
            else:
                command = f'ollama run {OLLAMA_MODEL} """{ollama_text}"""'
                print(f"Executing command: {command}")
                response = os.popen(command).read().strip()

                self.context.append(response)
                return response

        except Exception as e:
            error_message = f"Failed to execute command: {e}"
            print(error_message)
            return json.dumps({"error": error_message})
