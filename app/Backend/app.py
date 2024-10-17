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
from ml_image_eval import vision
from modules.text import text
from modules.ml.ml_handler import ChatbotHandler, create_jsonl
from modules.ticket import ticket
from config import *
from modules.log import *
import base64
import shutil
import modules.db.db_models as db_models
import mimetypes
from mimetypes import guess_extension
from werkzeug.utils import secure_filename
import random

# Flask configurations
app = Flask(__name__)
app.secret_key = secret_key
app.config.from_prefixed_env()
CORS(app, resources={r"/*": {"origins": "*", "supports_credentials": True}})

socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Global routes
app.register_blueprint(auth_ldap, url_prefix='/sso')
app.register_blueprint(ticket, url_prefix='/ticket')
app.register_blueprint(vision, url_prefix='/vision')
app.register_blueprint(text, url_prefix='/text')

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
def delete_ticket(ticket_id):
    ticket_path = os.path.join(ticket_folder, ticket_id)
    if os.path.isdir(ticket_path):
        shutil.rmtree(ticket_path)
        return jsonify({"message": "Ticket deleted successfully"})
    return jsonify({"message": "Ticket not found"}), 404


@app.route('/get_ticket', methods=['GET'])
@app.route('/get_ticket/<ticket_id>', methods=['GET'])
def get_ticket(ticket_id=None):
    # Check if ticket_id is None, meaning it might be passed as a query parameter
    if ticket_id is None:
        # Fetch it from the query parameters
        ticket_id = request.args.get('ticket_id')

    # Log to check if ticket_id is being passed
    print("######", ticket_id)

    # Ensure ticket_id is not None before proceeding
    if ticket_id:
        ticket_path = os.path.join(ticket_folder, ticket_id)
        if os.path.isdir(ticket_path):
            chat_file = os.path.join(ticket_path, "data.json")
            if os.path.isfile(chat_file):
                with open(chat_file, "r") as f:
                    data = json.load(f)
                    if "closed_chat" in data:
                        return jsonify(data["closed_chat"])
                    else:
                        return jsonify(data)
    
    # Return an empty response if ticket_id is None or not found
    return jsonify({})


@app.route('/update_ticket', methods=['POST'])
def update_ticket():
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

@app.route('/get_chat_history', methods=['GET'])
def get_chat_history():
    return jsonify(socket_connection)


@app.route('/get_jsonl', methods=['GET'])
def get_jsonl():
    result_path = create_jsonl()
    load_jsonl = []
    with open(result_path, 'r') as f:
        for line in f:
            load_jsonl.append(json.loads(line))
    return jsonify(load_jsonl)


@app.route('/text_form', methods=['POST'])
def text_form():
    form_data = request.json 
    print(json.dumps(form_data, indent=4))
    token = request.cookies.get('session')
    attachments = []  
    attachments_list = form_data.get('attachments', [])
    ticket_id = form_data.get('ticket_id')
    if not ticket_id:
        ticket_id = "SVC-" + str(random.randint(10000, 99999))

    folder_this = os.path.join(ticket_folder, ticket_id)
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
    return json.dumps(chat_history, indent=4) 



def parse_attachment(file_data, file_name, folder_this):
    """ Save attachment to bucket/chat_id folder and return base64 encoded content. """
    chat_folder = os.path.join(folder_this)
    os.makedirs(chat_folder, exist_ok=True)
    file_path = os.path.join(folder_this, file_name)

    # Write the file to disk
    with open(file_path, "wb") as f:
        f.write(file_data)

    # Convert file to base64
    with open(file_path, "rb") as f:
        file_ext = file_path.split('.')[-1]
        mime_type = guess_extension(file_ext) or mimetypes.guess_type(file_path)[0] or "application/octet-stream"
        
    return file_name, mime_type



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



if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
