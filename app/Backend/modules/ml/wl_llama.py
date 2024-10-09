import os
import json
from mimetypes import guess_type
import base64
from config import *

class OllamaChat:
    def __init__(self):
        self.context = []

    def send_message(self, message):
        try:
            self.context.append(message)
            
            attachment_data = ""
            if message['attachments']:
                for count, attachment in enumerate(message['attachments'], start=1):
                    file_path = attachment['file']
                    binary_file_data = attachment['data']

                    # Write the binary data to the file (if needed for reading)
                    with open(file_path, 'wb') as f:
                        f.write(base64.b64decode(binary_file_data))

                    # Read the file content if it is a supported text type
                    mime_type = guess_type(file_path)[0]
                    if mime_type in ('text/plain', 'text/html', 'text/csv', 'text/xml', 'text/rtf', 'text/richtext', 'application/json'):
                        with open(file_path, 'r') as f:
                            file_content = f.read()
                        attachment_info = f"Attachment {count}: {file_content}"
                        attachment_data += attachment_info + "\n"
            
            # Extracting the last message from admin (user)
            last_message = ""
            message_history = json.loads(message["message"])

            for key in sorted(message_history.keys()):
                msg = message_history[key]
                if msg['recipient'] == 'admin':  # Assuming 'admin' is the user
                    last_message = msg['message']

            # Creating a chronological history
            history = ""
            for key in sorted(message_history.keys()):
                msg = message_history[key]
                history += f"{msg['recipient']}: {msg['message']}\n"

            # Construct text for ollama
            ollama_text = f"{last_message}\n\n{history}\n\n{attachment_data}"

            # Construct command with triple quotes for multiline support
            command = f'ollama run {OLLAMA_MODEL} """{ollama_text}"""'
            print(f"Executing command: {command}")
            response = os.popen(command).read().strip()
            
            self.context.append(response)
            return response

        except Exception as e:
            error_message = f"Failed to execute command: {e}"
            print(error_message)
            return json.dumps({"error": error_message})

