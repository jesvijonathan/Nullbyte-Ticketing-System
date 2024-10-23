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
from modules.bucket import *

# chatbot handler for socketio and manager
class ChatbotHandler:
    def __init__(self, token, socketio=None, payload=None, medium=None):
        self.socketio= socketio
        self.medium=medium if medium else 1 # 1 for socketio, 2 for email
        self.token= token
        self.mail = {"response": "", "processing": False, "RepliedBot": ""}
        self.customer_id= payload["upn"]
        self.result= chat_json
        self.history = {}
        if(medium==2):
            self.chat_id=token
            self.user= payload['upn']
            self.result["user"]= payload['upn']
            self.result["medium"]= "email"
        else:
            self.user= payload['username']
            self.socket= sockets[token]
            self.chat_id= self.socket["sid"]
            self.user= payload['username']
            self.result["user"]= payload['username']
            self.result["medium"]= "chat"
        self.result["chat_id"]= self.chat_id
        self.result["user"]= payload['upn']
        self.result["ticket_id"]= str(random.randint(10000, 99999))
        self.attachments = []
        
        self.bot, self.chat= self.initialize_bot(chatbot_fallback)
        self.fallback= self.initialize_fallback(chatbot_fallback)
        self.fell= False
        if bucket_mode:
            pass
        self.bucket_dir = os.path.join(chats_folder, self.user, self.chat_id)
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
        self.mail["processing"]= True
    
        attachments = []  
        if attachments_list:
            attachment_count = 0
            for attachment in attachments_list:
                print(attachment)
                binary_file_data = attachment['data']
                b_file_data = base64.b64decode(attachment['data'])
                google_string, filename, mime = self.parse_attachment(b_file_data, secure_filename(attachment['name']))
                filename = filename
                file_path = os.path.join(self.bucket_dir, filename)
    

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

                self.attachments.append(self.history[len(self.history)]["attachment"][attachment_count])
                    
                # print("00000000000:",  binary_file_data, "\n\n", b_file_data)
                attachments.append({
                    "file": file_path,
                    "data": binary_file_data
                 })
            
                attachment_count+=1

        # print("\n\n\n\n", attachments)
        if response_msg == "/close" or response_msg == "close" or response_msg == "end" or response_msg == "/end":
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
        # if db_add_closed_chat:
        tick_it = None
        if sqlmode:
            print("\n\nresult starts here:")
            res=self.result
            tid=BotAdmin().create_ticket(res)["id"]
            if[tid]:
                self.result["ticket_id"]=str(tid)
            print(res)
            print("\n\nresult ends here:")


        print("oooooooooooooo")
        if dirmode:
            print(res)
            BotAdmin().create_ticket_dirmode(res)



        ticket_folder = "./bucket/tickets"
        os.makedirs(ticket_folder, exist_ok=True)
        
        this_ticket_folder = os.path.join(ticket_folder, self.result["ticket_id"])
        os.makedirs(this_ticket_folder, exist_ok=True)
        chat_file = os.path.join(this_ticket_folder, "data.json")
        
        # have to store this details somewhere in db
        # final_file['ticket_id']=self.result["ticket_id"]
        # final_file['chat_id']=self.chat_id
        # final_file['user']=self.user
        chat_history={
            "chat_id": self.chat_id,
            "ticket_id": self.result["ticket_id"],
            "user": self.user,
            "history": self.history,
            "closed_chat": self.result
        }

        with open(chat_file, "w") as f:
            json.dump(chat_history, f)
        if bucket_mode:
            upload_individual_files(bucket_name, [chat_file])
            
        for key in self.history:
            if "attachment" in self.history[key]:
                    attachments = self.history[key]["attachment"]
                    for attachment in attachments:
                        try:
                            attachment_file = os.path.join(this_ticket_folder, attachments[attachment]["filename"])
                            os.rename(self.history[key]["attachment"][attachment]["path"], attachment_file)
                            self.history[key]["attachment"][attachment]["path"] = attachment_file
                            try:
                                print("\n\n\nattachment issue starts here:")
                                Attachment().addAttachment(self.result["ticket_id"], attachment_file)
                                print("Error adding attachment to db")
                            except:
                                pass
                            print("\n\n\nattachment issue ends here:")
                        except:
                            print("Error moving attachment file")
                            pass
        if self.user not in old_chat:
            old_chat[self.user] = {}
        
        old_chat[self.user][self.chat_id] = {
            "history": self.history,
            "closed_chat": self.result,
            "ticket_url": str(baseMyURL + "/ticket/" + self.result["ticket_id"])
        }
        print(old_chat)
        
        # print("old chat  : ", old_chat)
        # print("chat closed : ", self.result)

        if(self.socketio):
            self.socketio.emit("close_chat", {"closed_chat": self.result}, room=self.socket["sid"])
        # if self.token in sockets:
        #     del sockets[self.token]

        # if self.token in socket_connection:
        #     del socket_connection[self.token]
        
        # self.destroy()
        # move to ticket in 5 seconds
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
            self.mail["RepliedBot"]= "wl_llama"
        except Exception as e:
            print(f"An error occurred: {e}")
            self.fallback_handle()


    def vertex_generate(self, message, attachments=None):
        
        print("Sending message:", self.format_message(message))
        response = self.chat.send_message(self.format_message(message), attachments)
        
        if response.candidates:
            text_response = response.candidates[0].content.parts[0].text
            self.handle_response(text_response)
            self.mail["RepliedBot"]= "wl_vertex"
        try:
            pass
        except ResourceExhausted:
            print("Quota exceeded. Waiting before retrying...")
            self.fallback_handle()
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
            if(self.socketio):
                self.socketio.emit("message", {"message": "JSON decoding error: " + str(e)}, room=self.socket["sid"])
            self.fallback_handle()
        except Exception as e:
            print(f"An error occurred: {e}")
            if(self.socketio):
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
    
    def parse_json(self, json_msg_dict):
        tmp_json = chat_json
        for key in json_msg_dict:
            tmp_json[key] = json_msg_dict[key]
        tmp_json["chat_id"] = self.chat_id
        tmp_json["user"] = self.user
        tmp_json["ticket_id"] = self.result["ticket_id"]
        tmp_json["created"] = datetime.datetime.now().isoformat()
        tmp_json["updated"] = tmp_json["created"]
        tmp_json["attachments"] = self.attachments
        # for key in tmp_json:
        #     if key == "attachments":
        #         for attachment in tmp_json[key]:
        #             attachment["path"] = os.path.join(self.bucket_dir, self.chat_id, attachment["name"])
        #             attachment["size"] = os.path.getsize(attachment["path"])
        #             attachment["type"] = mimetypes.guess_type(attachment["path"])[0] or "application/octet-stream"
        #             attachment["url"] = f"/attachments/{self.chat_id}/{attachment['name']}"
        return tmp_json
         
    
    def handle_response(self, text_response):
        json_msg_dict, reply_msg = self.extract_json_response(text_response)
        print("@@@@@@@@@@@@@2", json_msg_dict, "\n\n", reply_msg)
    
        if json_msg_dict:
            json_msg_dict = self.parse_json(json_msg_dict)
            self.result.update(json_msg_dict)
            self.reply_send(reply_msg)
            self.mail["response"]=reply_msg
            print("Response received successfully:", self.result)
            self.close_chat()
        else:
            print("Response received successfully (No JSON found in the response; processing as plain text.):", self.result)
            self.reply_send(reply_msg if reply_msg else text_response)
            self.mail["response"]=reply_msg
        self.mail["processing"]= False
    
    def reply_send(self, reply_msg):
        # bot reply
        self.history[len(self.history) + 1] = {
            'recipient': self.bot,
            'time': datetime.datetime.now().isoformat(),
            'message': reply_msg
        }
        if(self.socketio):
            self.socketio.emit("live_chat", {"live_chat": self.history}, room=self.socket["sid"])
        return reply_msg
    
    def parse_attachment(self, file_data, file_name):
        """ Save attachment to bucket/chat_id folder and return base64 encoded content. """
        chat_folder = self.bucket_dir
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
            file_name = attachment['name'] 
            file_name = secure_filename(file_name)
            file_data = base64.b64decode(attachment['data']) 
            print ("AAAAAAAAAAAAAAAAA", attachment)
            encoded_file, file_name, mime = self.parse_attachment(file_data, file_name)
            if(self.socketio):
                self.socketio.emit("attachment_saved", {"message": f"Attachment {file_name} received and saved."}, room=self.socket["sid"])
            
    def extract_json_response(self, text_response):
        text_response = re.sub(r'//.*?(\r?\n|$)', '\n', text_response)
        text_response = re.sub(r',\s*([}\]])', r'\1', text_response)
        
        json_field_pattern = re.compile(r'{\s*["\']?(subject|chat_id|ticket_id|user|medium|text|summary|attachments|product_type|issue_type|priority|story_points|estimation|analysis|reply|assingee|status|created|updated|comments|logged_hrs)["\']?\s*:')
        json_msg=""

        if "```json" in text_response:
            start_index = text_response.index("```json") + len("```json")
            end_index = text_response.index("```", start_index)
            json_msg = text_response[start_index:end_index].strip()
        else:
            match = json_field_pattern.search(text_response)
            if match:
                start_index = match.start()
                end_index = self.find_closing_brace(text_response, start_index)
                if end_index != -1:
                    json_msg = text_response[start_index:end_index].strip()
                else:
                    return None, text_response.strip()
            # else:
            #     try:
            #         json_msg_dict = json.loads(text_response.strip())
            #         reply_msg = json_msg_dict.get("reply") or default_reply_msg
            #         return json_msg_dict, reply_msg
            #     except json.JSONDecodeError as e:
            #         print(f"JSON decoding error: {e}")
            #         print(f"Problematic JSON: {text_response}")
            #         return None, text_response.strip()  

        try:
            print(json_msg)
            json_msg_dict = json.loads(json_msg)
            reply_msg = json_msg_dict.get("reply") or default_reply_msg
            return json_msg_dict, reply_msg
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
            print(f"Problematic JSON: {text_response}")
            return None, text_response.strip()

    def find_closing_brace(self, text, start_index):
        """Finds the index of the closing brace '}' that balances the opening one."""
        open_braces = 0
        for i in range(start_index, len(text)):
            if text[i] == '{':
                open_braces += 1
            elif text[i] == '}':
                open_braces -= 1
                if open_braces == 0:
                    return i + 1  # Return the index after the closing brace
        return -1  # No matching closing brace found


import os
import json 
def create_jsonl():
    # Create a JSONL file
    # Get all JSON files from within chats_folder/* and its subdirectories
    # Create a JSONL file with all the JSON files and include the directory as a key
    # Return the JSONL file path

    # Also get all JSON from ticket_folder and its subdirectories, and add to the JSONL file
    json_files = []
    ticket_files = []

    # Get JSON files from chats folder
    for root, dirs, files in os.walk(chats_folder):
        for file in files:
            if file.endswith(".json"):
                json_files.append((os.path.join(root, file), os.path.basename(root)))

    # Get JSON files from ticket folder
    for root, dirs, files in os.walk(ticket_folder):
        for file in files:
            if file.endswith(".json"):
                ticket_files.append((os.path.join(root, file), os.path.basename(root)))

    # Combine both chat and ticket JSON files
    json_files.extend(ticket_files)

    # Define the path for the output JSONL file
    jsonl_file = os.path.join(chats_folder, "all_chats.jsonl")

    # Write the JSON objects to the JSONL file
    with open(jsonl_file, "w") as f:
        for file, dir_name in json_files:
            with open(file, "r") as jf:
                # Load each JSON file content as a Python dictionary
                data = json.load(jf)
                # Wrap the JSON data with a new key (directory name) and write it to the JSONL file
                wrapped_data = {dir_name: data}
                # Write the wrapped JSON object as a single line in the JSONL file
                f.write(json.dumps(wrapped_data) + "\n")

    return jsonl_file

    