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
from modules.ml.ml_handler import ChatbotHandler
from modules.ticket import ticket
from config import *
from modules.log import *
import base64
import shutil
import modules.db.db_models as db_models


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

@app.route('/get_ticket', methods=['GET'])
def get_ticket():
    with open('dataset/ticket.json') as f:
        data = json.load(f)
    return jsonify(data)

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
