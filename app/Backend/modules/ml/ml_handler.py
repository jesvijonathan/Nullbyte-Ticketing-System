from flask import jsonify
import datetime
import time
from google.api_core.exceptions import ResourceExhausted
from flask_socketio import SocketIO, emit, send, join_room, leave_room, close_room, rooms, disconnect, Namespace

import json
import modules.ml.wl_vertex as wl_vertex
import modules.ml.wl_llama as wl_llama
from config import *
import random

import base64
from werkzeug.utils import secure_filename


from vertexai.generative_models import  Part
from mimetypes import guess_extension
import mimetypes

# chatbot handler for socketio and manager
class ChatbotHandler:
    def __init__(self, token, socketio):
        self.socketio= socketio
        self.token= token
        self.user= users[token]
        self.socket= sockets[token]
        self.chat_id= self.socket["sid"]
        self.history = {}
        self.result= chat_json
        self.result["chat_id"]= self.chat_id
        self.result["user"]= self.user["username"]
        self.result["ticket_id"]= "SVC-" + str(random.randint(10000, 99999))

        self.bot, self.chat= self.initialize_bot(chatbot_fallback)
        self.fallback= self.initialize_fallback(chatbot_fallback)
        self.fell= False

        self.bucket_dir = "./bucket"
        os.makedirs(self.bucket_dir, exist_ok=True)

        self.init_chat()

    def initialize_bot(self, fallback_option):
        if fallback_option in [0, 2]:
            return "wl_vertex", wl_vertex.google_vertex_chat()
        else:
            return "wl_llama", wl_llama.OllamaChat()

    def initialize_fallback(self, fallback_option):
        return "wl_vertex" if fallback_option == 3 else "wl_llama" if fallback_option == 2 else None

    def init_chat(self):
        self.reply_send(default_greet_msg)

        
    def response_add(self, response_msg, attachments_list=None):
        # User response
        self.history[len(self.history) + 1] = {
            'recipient': self.user["username"],
            'time': datetime.datetime.now().isoformat(),
            'message': response_msg
        }
    
        attachments = []  
    
        if attachments_list:
            for attachment in attachments_list:
                binary_file_data = attachment['file_data']
                b_file_data = base64.b64decode(attachment['file_data'])
                google_string, filename, mime = self.parse_attachment(b_file_data, attachment['file_name'])
                file_path = os.path.join(self.bucket_dir, self.chat_id, filename)
    
                if google_string:
                    attachment_count = len(os.listdir(os.path.join(self.bucket_dir, self.chat_id)))
                    self.history[len(self.history)]["attachment"] = {
                        "file_id": attachment_count,
                        "filename": filename,
                        "path": file_path,
                        'extension': filename.split('.')[-1] if '.' in filename else '',
                        'mime_type': mime,
                        'size': len(b_file_data),
                    }
                    
                print("00000000000:",  binary_file_data, "\n\n", b_file_data)
                attachments.append({
                    "file": file_path,
                    "data": binary_file_data
                 })

        print("\n\n\n\n", attachments)
        if response_msg == "/close" or response_msg == "close":
            self.close_chat()
        elif response_msg == "/change" or response_msg == "change":
            if self.bot == "wl_vertex":
                self.bot = "wl_llama"
                self.chat = wl_llama.OllamaChat()
                self.fallback = "wl_vertex"
                print("changing to llama")
                self.bot_response(self.history)
            else:
                self.bot = "wl_vertex"
                self.chat = wl_vertex.google_vertex_chat()
                self.fallback = "wl_llama"
                print("changing to vertex")
                self.bot_response(self.history)
        else:
            self.bot_response(response_msg, attachments)


    def format_message(self, message):
        if isinstance(message, dict):
            message = json.dumps(message)
        message = message.strip()
        filter_list = ["`", "``", "```", "```json", "```json\n", "```json\n\n", "```json\n\n\n"]
        
        for filter in filter_list:
            if filter in message:
                message = message.replace(filter, "") 

        return str(message)

    def close_chat(self):
        self.result["connection"]= "closed"
        # logic to add details to db here, for later
        self.socketio.emit("close_chat", {"close_chat": self.result}, room=self.socket["sid"])
        # if self.token in sockets:
        #     del sockets[self.token]

        # if self.token in socket_connection:
        #     del socket_connection[self.token]
        
        # self.destroy()
        return

    
    def destroy(self):
        for attr in list(self.__dict__.keys()):
            try:
                delattr(self, attr)
            except:
                pass
        self = None
        return

    def fallback_handle(self):
        print("falling back to :", self.fallback, "user", self.user)
        self.fell = True
        self.bot = self.fallback
        if self.fallback == "wl_vertex":
            self.chat = wl_vertex.google_vertex_chat()
            self.vertex_generate(str(self.history))
        else:
            self.chat = wl_llama.OllamaChat()
            self.llama_generate(str(self.history))
        return

    def llama_generate(self, message, attachments=None):
        formatted_message = self.format_message(message)

        message_payload = {
            'attachments': attachments,
            'message': formatted_message
        }

        try:
            print("Sending message:", message_payload)
            response = self.chat.send_message(message_payload)
            self.handle_response(response)
            print("Response received successfully:", response)
        except Exception as e:
            print(f"An error occurred: {e}")
            self.fallback_handle()


    def vertex_generate(self, message, attachments=None):
        try:
            response = self.chat.send_message(self.format_message(message), attachments)

            if response.candidates:
                text_response = response.candidates[0].content.parts[0].text
                self.handle_response(text_response)
        except ResourceExhausted:
            print("Quota exceeded. Waiting before retrying...")
            self.fallback_handle()
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
            self.socketio.emit("message", {"message": "JSON decoding error: " + str(e)}, room=self.socket["sid"])
            self.fallback_handle()
        except Exception as e:
            print(f"An error occurred: {e}")
            self.socketio.emit("message", {"message": str(e)}, room=self.socket["sid"])
            self.fallback_handle()

    
    def bot_response(self, response_msg, attachment=None):
        # bot response
        if self.bot == "wl_vertex":
            self.vertex_generate(response_msg, attachment)
        else:
            self.llama_generate(self.history, attachment)

        return
    
    def handle_response(self, text_response):
        json_msg_dict, reply_msg = self.extract_json_response(text_response)
    
        if json_msg_dict:
            self.result.update(json_msg_dict)
            self.reply_send(reply_msg)
            print(self.result)
            # Process json_msg to ticket
            self.close_chat()
        else:
            print("No JSON found in the response; processing as plain text.")
            self.reply_send(reply_msg if reply_msg else text_response)
    
    def reply_send(self, reply_msg):
        # bot reply
        self.history[len(self.history) + 1] = {
            'recipient': self.bot,
            'time': datetime.datetime.now().isoformat(),
            'message': reply_msg
        }
        self.socketio.emit("live_chat", {"live_chat": self.history}, room=self.socket["sid"])
        return reply_msg
    
    def parse_attachment(self, file_data, file_name):
        """ Save attachment to bucket/chat_id folder and return base64 encoded content. """
        chat_folder = os.path.join(self.bucket_dir, self.chat_id)
        os.makedirs(chat_folder, exist_ok=True)
        file_path = os.path.join(chat_folder, file_name)

        # Write the file to disk
        with open(file_path, "wb") as f:
            f.write(file_data)

        # Convert file to base64
        with open(file_path, "rb") as f:
            # get mime type, from file extension
            file_ext = file_path.split('.')[-1]
            mime_type = guess_extension(file_ext) or mimetypes.guess_type(file_path)[0] or "application/octet-stream"
            encoded_file = Part.from_data(
                mime_type=mime_type,
                data=base64.b64encode(f.read()).decode("utf-8")
            )

        return encoded_file, file_name, mime_type
    
#     document1_1 = Part.from_data(
#     mime_type="text/plain",
#     data=base64.b64decode("""="""),
# )
    
    def convert_to_base64(self, file_path):
        """Convert a file to a base64 encoded string."""
        try:
            with open(file_path, "rb") as file:
                encoded_string = base64.b64encode(file.read()).decode('utf-8')
            return encoded_string
        except Exception as e:
            print(f"Error converting file to base64: {e}")
            return None
        
    def handle_attachment(self, attachment_list):
        # save the attachment to the bucket
        for attachment in attachment_list:
            """ Receives attachment data from frontend and processes it. """
            file_name = attachment['file_name']
            file_data = base64.b64decode(attachment['file_data']) 
            print ("AAAAAAAAAAAAAAAAA", attachment)
            encoded_file, file_name, mime = self.parse_attachment(file_data, file_name)
            self.socketio.emit("attachment_saved", {"message": f"Attachment {file_name} received and saved."}, room=self.socket["sid"])
            
    def extract_json_response(self, text_response):
        if "```json" in text_response:
            start_index = text_response.index("```json") + len("```json")
            end_index = text_response.index("```", start_index)
            json_msg = text_response[start_index:end_index].strip()
        elif '{ "subject":' in text_response:
            start_index = text_response.index('{ "subject":')
            end_index = text_response.index('}', start_index) + 1
            json_msg = text_response[start_index:end_index].strip()
        else:
            # No JSON found, returning the plain text response
            return None, text_response.strip()

        try:
            json_msg_dict = json.loads(json_msg)
            reply_msg = json_msg_dict.get("reply") or default_reply_msg
            return json_msg_dict, reply_msg
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
            print(f"Problematic JSON: {json_msg}")
            return None, text_response.strip()