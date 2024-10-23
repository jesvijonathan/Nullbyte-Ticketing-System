from flask import Flask, request, session, render_template, make_response
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send, disconnect
from flask import jsonify
from flask import request
import datetime
import time
from google.api_core.exceptions import ResourceExhausted
import json
from modules.auth.auth import auth_ldap, jwt_required, cleanup_user
from modules.text import text
from modules.ml.ml_handler import ChatbotHandler, create_jsonl
from modules.ticket import create_ticket, modify_fields,ticket,delete_ticket as delete_ticket_sql, get_ticket as get_ticket_sql,get_all_tickets
from config import *
from modules.log import *
import base64
import shutil
import modules.db.db_models as db_models
import mimetypes
from mimetypes import guess_extension
from werkzeug.utils import secure_filename
import random
from modules.bucket import *
import pickle
import threading
import pandas as pd
import re


# Flask configurations
app = Flask(__name__)
app.secret_key = secret_key
app.config.from_prefixed_env()
CORS(app, resources={r"/*": {"origins": "*", "supports_credentials": True}})

socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Global routes
app.register_blueprint(auth_ldap, url_prefix='/sso')
app.register_blueprint(ticket, url_prefix='/ticket')
app.register_blueprint(text, url_prefix='/text')

if enable_jira:
    from modules.jira.jira_int import jiraint
    app.register_blueprint(jiraint, url_prefix='/jira')
@app.route('/')
def home():
    return render_template('index.html', token_param="")

# dummy route to test json data from ./dataset/test.json
@app.route('/test', methods=['GET'])
def test():
    with open('dataset/test.json') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/delete/<ticket_id>', methods=['DELETE'])
def handle_delete_ticket(ticket_id):
    result=None
    if dirmode:
        result = delete_ticket(ticket_id)
    if sqlmode:
        result = delete_ticket_sql(ticket_id)
    return result
    
def delete_ticket(ticket_id):
    ticket_path = os.path.join(ticket_folder, ticket_id)
    result={}
    if bucket_mode:
        try:
            delete_file_or_folder(bucket_name, f"tickets/{ticket_id}/")
            result= jsonify({"message": "Ticket deleted successfully"})
        except Exception as e:
            print(f"Error deleting ticket: {e}")
            result=jsonify({"error": "Failed to delete ticket"}), 500    
    if os.path.isdir(ticket_path):
        shutil.rmtree(ticket_path)
        result= jsonify({"message": "Ticket deleted successfully"})
    if not result:
        result= jsonify({"error": "Ticket not found"}), 404
    return result

import requests

@app.route('/get_ticket', methods=['GET'])
@app.route('/get_ticket/<ticket_id>', methods=['GET'])
def handle_get_ticket(ticket_id=None):
    result=None
    if sqlmode:
        result = get_ticket_sql(ticket_id)
    if dirmode:
        result = get_ticket(ticket_id)
    return result

def get_ticket(ticket_id=None):
    if ticket_id is None:
        ticket_id = request.args.get('ticket_id')
    print("######", ticket_id)
    if ticket_id:
        ticket_path = os.path.join(ticket_folder, ticket_id)        
        if bucket_mode:
            file_url = get_signed_url_for_file(bucket_name, f"tickets/{ticket_id}/data.json")
            print("######", file_url)
            response = requests.get(file_url)
            if response.status_code == 200:
                try:
                    data = response.json()
                    if "closed_chat" in data:
                        return jsonify(data["closed_chat"])
                    else:
                        return jsonify(data)
                except json.JSONDecodeError:
                    print("Error: Unable to decode the JSON content")
                    return None
            else:
                print(f"Error: Failed to fetch the file from {file_url}. Status code: {response.status_code}")
                return None

        if os.path.isdir(ticket_path):
            chat_file = os.path.join(ticket_path, "data.json")
            if os.path.isfile(chat_file):
                with open(chat_file, "r") as f:
                    data = json.load(f)
                    if "closed_chat" in data:
                        return jsonify(data["closed_chat"])
                    else:
                        return jsonify(data)
        return jsonify({"error": "Ticket not found"}), 404  
    return jsonify({})


@app.route('/update_ticket', methods=['POST'])
def handle_update_ticket():
    result=None
    if sqlmode:
        result = modify_fields(request)
    if dirmode:
        result = update_ticket(request)
    return result

def update_ticket(request):
    ticket_data = request.json
    ticket_id = ticket_data.get('ticket_id')
    if not ticket_id:
        return jsonify({"error": "Ticket ID is required"}), 400
    ticket_path = os.path.join(ticket_folder, ticket_id)
    if os.path.isdir(ticket_path):
        chat_file = os.path.join(ticket_path, "data.json")
        if os.path.isfile(chat_file):
            with open(chat_file, "r") as f:
                data = json.load(f)
                data.update(ticket_data)
                with open(chat_file, "w") as f:
                    json.dump(data, f)
                if bucket_mode:
                    upload_individual_files(bucket_name, [chat_file])
                return jsonify(data)
    return jsonify({"error": "Ticket not found"}), 404

@app.route('/get_incomplete_ticket', methods=['GET'])
def get_incomplete_ticket():
    with open('dataset/ticket_not.json') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/get_autofill', methods=['GET'])
def get_autofill():
    with open('dataset/ticket.json') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/get_tickets', methods=['GET'])
@app.route('/get_tickets/<int:limit>', methods=['GET'])
def handle_get_tickets(limit=20):
    result=None
    if sqlmode:
        result = get_all_tickets(limit)
    if dirmode and result is None:
        result = get_tickets(limit)
    return result
def get_tickets(limit=20):
    tickets = {}
    for ticket in os.listdir(ticket_folder):
        if tickets and len(tickets) >= limit:
            break
        ticket_path = os.path.join(ticket_folder, ticket)
        if os.path.isdir(ticket_path):
            chat_file = os.path.join(ticket_path, "data.json")
            if os.path.isfile(chat_file):
                with open(chat_file, "r") as f:
                    data = json.load(f)
                    if "closed_chat" in data:
                        tickets[data["closed_chat"]["ticket_id"]] = data
                    else:
                        tickets[data["ticket_id"]] = data

    return jsonify(tickets)

# sql, 2xapigee, 1-container, 1-ad,1- ollama 
@app.route('/get_chat_history/<user_id>', methods=['GET'])
def get_chat_history(user_id):
    if not user_id:
        user_id = request.args.get('user_id') 
    
    print("User ID:", user_id)
    return jsonify({"chat_history": old_chat.get(user_id, "No chat history found")})

# delete all tickets
@app.route('/delete_all_tickets')
def delete_all_tickets():
    for ticket in os.listdir(ticket_folder):
        ticket_path = os.path.join(ticket_folder, ticket)
        if os.path.isdir(ticket_path):
            shutil.rmtree(ticket_path)
        if bucket_mode:
            delete_file_or_folder(bucket_name, f"tickets/{ticket}/")
    return jsonify({"message": "All tickets deleted successfully"})


@app.route('/get_jsonl', methods=['GET'])
def get_jsonl():
    result_path = create_jsonl()
    load_jsonl = []
    with open(result_path, 'r') as f:
        for line in f:
            load_jsonl.append(json.loads(line))
    return jsonify(load_jsonl)

@app.route('/text_form', methods=['POST'])
def handle_ticket_creation():
    result=None
    if sqlmode:
        result = create_ticket(request)
    if dirmode:
        print("@@@\n\n\n\n")
        print(result)
        result=json.loads(result)
        if result is not  None and result['ticket_id']:
            result = text_form(request,result['ticket_id'])
        else:
            result = text_form(request)
    return result

# @app.route('/text_form', methods=['POST'])
def text_form(request,ticket_id=None):
    print("Ticket ID:", ticket_id)
    form_data = request.json 
    print(json.dumps(form_data, indent=4))
    token = request.cookies.get('session')
    attachments = []  
    attachments_list = form_data.get('attachments', [])
    # ticket_id = form_data.get('ticket_id')
    if not ticket_id:
        ticket_id = str(random.randint(10000, 99999))
        form_data['ticket_id'] = ticket_id
    else:
        form_data['ticket_id'] = ticket_id
    print("Ticket ID:", ticket_id)
    folder_this = os.path.join(ticket_folder, ticket_id)
    print("Folder:", folder_this)
    if attachments_list:
        attachment_count = 0
        for attachment in attachments_list:
            binary_file_data = attachment['data']
            b_file_data = base64.b64decode(attachment['data'])
            filename, mime = parse_attachment(b_file_data, secure_filename(attachment['name']), folder_this)
            filename = filename
            file_path = os.path.join(folder_this, filename)
            attachments_list[attachment_count]['url'] = file_path
            attachments_list[attachment_count].pop('data')
            attachment_count += 1
            # attachments.append(file_path)
    chat_file = os.path.join(folder_this, "data.json")
    os.makedirs(folder_this, exist_ok=True)
    chat_history={
            "chat_id": form_data.get('chat_id'),
            "ticket_id": ticket_id,
            "user": form_data.get('user'),
            "history": {},
            "medium": "portal",
            "comments": [],
            "attachments": attachments_list,
            "created": datetime.datetime.now().isoformat(),
            "updated": datetime.datetime.now().isoformat(),
            "logged_hrs": []
        }
    chat_history = {**chat_history, **form_data}

    with open(chat_file, "w") as f:
        json.dump(chat_history, f)
    if bucket_mode:
        files_to_upload = [chat_file] + [attachment['url'] for attachment in attachments_list]
        upload_individual_files(bucket_name, files_to_upload)

        # Upload the chat file and attachments to the cloud
        print("@@@@@@@@Chat histroy")
        print(chat_history)
    return json.dumps(chat_history, indent=4) 



def convert_to_json(csv_file,user="unknown_user"):
    df = pd.read_csv(csv_file)
    json_data = []

    df.columns = df.columns.str.strip()
    for _, row in df.iterrows():
        row = row.dropna()
        row = row.apply(lambda x: re.sub(r"\s+", " ", str(x)).strip())
        ticket_data = {
            "chat_id": "",
            "ticket_id":str(random.randint(10000, 99999)),
            "user": str(row.get("Assigned to", "")).replace(" ", "").lower() or user,
            "medium": "other",
            "connection": "closed",
            "text": str(row.get("Short description", "")).strip() or "No description provided",
            "subject": str(row.get("Short description", "")).strip() or str(row.get("Title", "")).strip()  or "No subject provided",
            "summary": None,
            "attachments": [],
            "product_type": str(row.get("Service", "")).strip() or "Unknown Product",
            "issue_type": str(row.get("Task type", "")).strip() or "Unknown Issue Type",
            "priority": str(row.get("Priority", "")).strip() or str(row.get("Urgency", "")).strip() or None,
            "story_points": None,
            "estimation": None,
            "analysis": None,
            "reply": None,
            "created": None,
            "updated": None,
            "comments": [],
            "logged_hrs": [],
            "status": str(row.get("State", "")).strip() or str(row.get("Status", "")).strip() or "Unknown",
            "assignee": str(row.get("Assigned to", "")).replace(" ", "").lower() or "unassigned"
        }

        created_str = row.get("Created", "")
        try:
            created_dt = datetime.datetime.strptime(created_str, "%d-%m-%Y %H:%M")
            ticket_data["created"] = created_dt.isoformat()
        except ValueError:
            ticket_data["created"] = datetime.datetime.now().isoformat()

        ticket_data["updated"] = ticket_data["created"]
        json_data.append(ticket_data)

    return json_data


@app.route('/import_tickets', methods=['GET', 'POST'])
def import_tickets():
    if request.method == 'GET':
        return render_template('import.html')

    total_tickets = []
    unsuccessful_tickets = []
    user = request.form.get('user', "unknown_user")

    if 'csv_files' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    files = request.files.getlist('csv_files')

    for file in files:
        try:
            filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "_" + secure_filename(file.filename)
            csv_file_path = os.path.join(imports_folder, filename)
            file.save(csv_file_path)
            if not csv_file_path.endswith(".csv"):
                unsuccessful_tickets.append({"file": filename, "error": "File is not a CSV"})
                continue
            json_data = convert_to_json(csv_file_path, user)
            for ticket in json_data:
                ticket_id = ticket.get('ticket_id')
                ticket_path = os.path.join(ticket_folder, str(ticket_id))
                os.makedirs(ticket_path, exist_ok=True)
                ticket_file = os.path.join(ticket_path, "data.json")
                with open(ticket_file, "w") as f:
                    json.dump(ticket, f)
                total_tickets.append(ticket)

        except Exception as e:
            unsuccessful_tickets.append({"file": file.filename, "error": str(e)})
            print(f"Failed to import tickets: {e}")
            return jsonify({"error": f"Failed to import tickets: {str(e)}"}), 500

    return jsonify({
        "message": "Tickets imported successfully",
        "total_tickets": total_tickets,
        "unsuccessful_tickets": unsuccessful_tickets
    })


@app.route('/changes_test', methods=['GET'])
def changes_test(user_id):
    if not user_id:
        user_id = request.args.get('oh_my_gawd') 


@app.route('/sync_bucket')
def sync_bucket():
    get_jsonl()

    list_buckets()
    list_blobs(bucket_name)

    local_directory = "./bucket" 
    uploaded_files, skipped_files = upload_files_from_directory(bucket_name, local_directory) 
    return jsonify({
        "message": "Files uploaded successfully",
        "uploaded_files": uploaded_files,
        "skipped_files": skipped_files
        })

def parse_attachment(file_data, file_name, folder_this):
    """ Save attachment to bucket/chat_id folder and return base64 encoded content. """
    chat_folder = os.path.join(folder_this)
    os.makedirs(chat_folder, exist_ok=True)
    file_path = os.path.join(folder_this, file_name)

    with open(file_path, "wb") as f:
        f.write(file_data)

    with open(file_path, "rb") as f:
        file_ext = file_path.split('.')[-1]
        mime_type = guess_extension(file_ext) or mimetypes.guess_type(file_path)[0] or "application/octet-stream"
        
    return file_name, mime_type

@app.route('/move_to_cloud')
def move_to_cloud(local_directory):
    uploaded_files, skipped_files  = upload_individual_files(bucket_name, [local_directory+ "/data.json"])
    list_all_data(bucket_name)
    # uploaded_files, skipped_files = upload_files_from_directory( bucket_name, local_directory) 
    return jsonify({
        "message": "Files uploaded successfully",
        "uploaded_files": uploaded_files,
        "skipped_files": skipped_files
        })



@app.route('/save')
def save_obj():
    with open('data_bank.pkl', 'wb') as f:
        try:
            pickle.dump([users, users_token, mailchains, old_chat], f)
        except Exception as e:
            return jsonify({"error": f"Failed to save data: {str(e)}"}), 500
    return jsonify({"message": "Data saved successfully"})

def load_obj():
    global users, users_token, mailchains, old_chat
    if os.path.exists('data_bank.pkl') and os.path.getsize('data_bank.pkl') > 0:
        with open('data_bank.pkl', 'rb') as f:
            users, users_token, mailchains, old_chat = pickle.load(f)
    print(users)
    print(users_token)
    print(mailchains)
    print(old_chat)






# Socket IO event handling
@socketio.on('connect')
@jwt_required
def connect(payload):
    sid = request.sid
    print(f"User connected: {sid}")
    token = request.cookies.get('session')
    if token not in sockets:
        sockets[token] = {"sid": sid, "connected": True, "history": {}}
        socket_connection[token] = ChatbotHandler(token, socketio,payload)
    sockets[token]["sid"] = sid 
    sockets[token]["connected"] = True

    chat_history = socket_connection[token].history if token in socket_connection else {}
    socketio.emit("live_chat" if chat_history else "message",
                  {"live_chat": chat_history} if chat_history else {"message": {**sockets[token]}},
                  room=sid)

@socketio.on('message')
@jwt_required
def message(msg):
    sid = request.sid
    print(f"Message from {sid}: {msg}")
    token = request.cookies.get('session')
    if token in socket_connection:
        socket_connection[token].response_add(msg)
    else:
        socketio.emit("message", {"message": "No active session found"}, room=sid)

@socketio.on('user_attachment')
@jwt_required
def handle_user_attachment(data):
    token = request.cookies.get('session')
    chat_handler = socket_connection[token]
    print("######", data)
    socket_connection[token].response_add(data['message'], data['attachments'])


@socketio.on('disconnect')
@jwt_required
def disconnect():
    print(f"User disconnected: {request.sid}")
    token = request.cookies.get('session')
    sockets[token]["connected"] = False
    chat= socket_connection[token]
    connec= chat.result["connection"] 
    if connec == "closed":
        chat.destroy()
        chat = None
        del socket_connection[token]
        del sockets[token]
    else:
        chat.result["connection"] = "offline"
    disconnect()

# cleanup during startup
if tmp_folders_cleanup:
    if os.path.exists(chats_folder) and os.path.isdir(chats_folder):
            for filename in os.listdir(chats_folder):
                file_path = os.path.join(chats_folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)  
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")

load_obj()

if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
