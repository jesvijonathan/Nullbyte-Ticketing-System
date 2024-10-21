import os
import json
from mimetypes import guess_type
import base64
import requests
from config import *

class OllamaChat:
    def __init__(self, http_mode=ollama_http):
        self.context = []
        self.http_mode = http_mode 

    def send_message(self, message):
        try:
            self.context.append(message)

            attachment_data = ""
            if message.get('attachments'):
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
            except json.JSONDecodeError:
                pass

            messages = []
            for key in sorted(message_history.keys()):
                msg = message_history[key]
                if msg['recipient'] == "wl_llama" or msg['recipient'] == "wl_vertex":
                    msg['recipient'] = "assistant"
                else:
                    msg['recipient'] = "user"
                messages.append({"role": msg['recipient'], "content": msg['message']})

            if self.http_mode:
                payload = {
                    "model": OLLAMA_MODEL,  
                    "messages": messages, 
                    "stream": False
                }
                print("********* : ", str(payload),"\n\n")
                response = requests.post(ollama_url, json=payload)
                print("%%%%%%%%%%%%%% : ", str(response))
                if response.status_code == 200:
                    response_data = response.json()
                    
                    if 'message' in response_data and 'content' in response_data['message']:
                        self.context.append(response_data) 
                        return response_data['message']['content']  
                    else:
                        error_message = "Response format is unexpected."
                        print(error_message)
                        return json.dumps({"error": error_message, "response_data": response_data})

                else:
                    error_message = f"HTTP error {response.status_code}: {response.text}"
                    print(error_message)
                    return json.dumps({"error": error_message})

            else:
                ollama_text = f"{last_message}\n\n{attachment_data}"
                command = f'ollama run {OLLAMA_MODEL} """{ollama_text}"""'
                print(f"Executing command: {command}")
                response = os.popen(command).read().strip()
                print("Command response:", response)

                try:
                    response_data = json.loads(response)
                    self.context.append(response_data)
                    if 'message' in response_data and 'content' in response_data['message']:
                        return response_data['message']['content'] 
                except json.JSONDecodeError:
                    print("Response is not valid JSON:", response)

        except Exception as e:
            error_message = f"Failed to execute command: {e}"
            print(error_message)
            return json.dumps({"error": error_message})
