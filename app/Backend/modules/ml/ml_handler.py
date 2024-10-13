from flask import jsonify
import datetime
import time
from google.api_core.exceptions import ResourceExhausted
from flask_socketio import SocketIO, emit, send, join_room, leave_room, close_room, rooms, disconnect, Namespace
from modules.ticket import BotAdmin
import json
import modules.ml.wl_vertex as wl_vertex
import modules.ml.wl_llama as wl_llama
from config import *
import random
from modules.log import logger
import base64
from werkzeug.utils import secure_filename
from vertexai.generative_models import  Part
from mimetypes import guess_extension
import mimetypes
from modules.db.db_models import Attachment
import re

# chatbot handler for socketio and manager
class ChatbotHandler:
    def __init__(self, token, socketio,payload):
        self.socketio= socketio
        self.token= token
        self.user= payload['upn']
        self.customer_id= payload["upn"]
        self.socket= sockets[token]
        self.chat_id= self.socket["sid"]
        self.history = {}
        self.result= chat_json
        self.result["chat_id"]= self.chat_id
        self.result["user"]= payload['upn']
        self.result["ticket_id"]= "SVC-" + str(random.randint(10000, 99999))

        self.bot, self.chat= self.initialize_bot(chatbot_fallback)
        self.fallback= self.initialize_fallback(chatbot_fallback)
        self.fell= False

        self.bucket_dir = chats_folder
        os.makedirs(self.bucket_dir, exist_ok=True)

        self.init_chat()

    def initialize_bot(self, fallback_option):
        print("Starting Bot")
        if fallback_option in [0, 2]:
            print("Starting Vertex")
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
            'recipient': self.user,
            'time': datetime.datetime.now().isoformat(),
            'message': response_msg
        }
    
        attachments = []  
        if attachments_list:
            attachment_count = 0
            for attachment in attachments_list:
                binary_file_data = attachment['file_data']
                b_file_data = base64.b64decode(attachment['file_data'])
                google_string, filename, mime = self.parse_attachment(b_file_data, secure_filename(attachment['file_name']))
                filename = filename
                file_path = os.path.join(self.bucket_dir, self.chat_id, filename)
    

                try:
                    self.history[len(self.history)]["attachment"]
                except:
                    self.history[len(self.history)]["attachment"] = {}
                self.history[len(self.history)]["attachment"][attachment_count] = {
                "filename": filename,
                "path": file_path,
                'extension': filename.split('.')[-1] if '.' in filename else '',
                'mime_type': mime,
                'size': len(b_file_data),
                }
                    
                # print("00000000000:",  binary_file_data, "\n\n", b_file_data)
                attachments.append({
                    "file": file_path,
                    "data": binary_file_data
                 })
            
                attachment_count+=1

        # print("\n\n\n\n", attachments)
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
        print("\n\nresult starts here:")
        res=self.result
        tid=BotAdmin().create_ticket(res)['id']
        if[tid]:
            self.result["ticket_id"]=str(tid)
        print(res)
        print("\n\nresult ends here:")
        
        ticket_folder = "./bucket/tickets"
        os.makedirs(ticket_folder, exist_ok=True)
        
        this_ticket_folder = os.path.join(ticket_folder, "SVC-" + self.result["ticket_id"])
        os.makedirs(this_ticket_folder, exist_ok=True)
        chat_file = os.path.join(this_ticket_folder, "chat.json")
        
        with open(chat_file, "w") as f:
            json.dump(self.history, f)
        
        for key in self.history:
            if "attachment" in self.history[key]:
                    attachments = self.history[key]["attachment"]
                    for attachment in attachments:
                        try:
                            attachment_file = os.path.join(this_ticket_folder, attachments[attachment]["filename"])
                            os.rename(self.history[key]["attachment"][attachment]["path"], attachment_file)
                            self.history[key]["attachment"][attachment]["path"] = attachment_file
                            print("\n\n\nattachment issue starts here:")
                            Attachment().addAttachment(self.result["ticket_id"], attachment_file)
                            print("\n\n\nattachment issue ends here:")
                        except:
                            print("Error moving attachment file")
                            pass


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
        # send a msg to user saying that the bot is down, do not store in history, if user says yes then change the bot, else close the chat
        # user_rep=self.reply_send("The bot is currently down, would you like to switch to {self.fallback} bot?")
        # if user_rep.lower() != "yes" or user_rep.lower() != "y" or user_rep.lower() != "s":
        #     self.close_chat()

        if self.fallback == "wl_vertex":
            self.chat = wl_vertex.google_vertex_chat()
            self.vertex_generate(str(self.history))
        elif self.fallback == "wl_llama":
            self.chat = wl_llama.OllamaChat()
            self.llama_generate(str(self.history))
        else:
            user_rep=self.reply_send("There was an error !")
            self.close_chat()
        return

    def llama_generate(self, message, attachments=None):
        formatted_message = self.format_message(message)

        message_payload = {
            'message': formatted_message,
            'attachments': attachments,
        }

        try:
            print("Sending message:", message_payload)
            response = self.chat.send_message(message_payload)
            self.handle_response(response)
        except Exception as e:
            print(f"An error occurred: {e}")
            self.fallback_handle()


    def vertex_generate(self, message, attachments=None):
        try:
            print("Sending message:", self.format_message(message))
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
            if not ollama_amnesia:
                self.llama_generate(self.history, attachment)
            else:
                self.llama_generate(response_msg, attachment)
        return
    
    def handle_response(self, text_response):
        json_msg_dict, reply_msg = self.extract_json_response(text_response)
    
        if json_msg_dict:
            self.result.update(json_msg_dict)
            self.reply_send(reply_msg)
            print("Response received successfully:", self.result)
            self.close_chat()
        else:
            print("Response received successfully (No JSON found in the response; processing as plain text.):", self.result)
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
            file_ext = file_path.split('.')[-1]
            mime_type = guess_extension(file_ext) or mimetypes.guess_type(file_path)[0] or "application/octet-stream"
            encoded_file = Part.from_data(
                mime_type=mime_type,
                data=base64.b64encode(f.read()).decode("utf-8")
            )

        return encoded_file, file_name, mime_type
    
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
            file_name = secure_filename(file_name)
            file_data = base64.b64decode(attachment['file_data']) 
            print ("AAAAAAAAAAAAAAAAA", attachment)
            encoded_file, file_name, mime = self.parse_attachment(file_data, file_name)
            self.socketio.emit("attachment_saved", {"message": f"Attachment {file_name} received and saved."}, room=self.socket["sid"])
            
    def extract_json_response(self, text_response):
        text_response = re.sub(r'//.*?(\r?\n|$)', '\n', text_response)
    
        text_response = re.sub(r',\s*([}\]])', r'\1', text_response)
        if "```json" in text_response:
            start_index = text_response.index("```json") + len("```json")
            end_index = text_response.index("```", start_index)
            json_msg = text_response[start_index:end_index].strip()
        elif "{ \"subject\":" in text_response or '``` { "subject":' in text_response:
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
