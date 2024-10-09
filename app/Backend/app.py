from flask import Flask, request, session, render_template, make_response
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send, join_room, leave_room, close_room, rooms, disconnect, Namespace
from flask import jsonify
from flask import request
import datetime
import time
from google.api_core.exceptions import ResourceExhausted
import json
from modules.auth.auth import auth_ldap, list_users, jwt_required, cleanup_user
from ml_image_eval import vision
from ml_text_eval import text
from modules.ml.ml_handler import ChatbotHandler
from modules.ticket import ticket
from config import *
import modules.socketio_handler as socketio_handler
from modules.log import *

import modules.ml.wl_vertex as wl_vertex


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

# Socket IO event handling
@socketio.on('connect')
@jwt_required
def connect():
    sid = request.sid
    token = request.cookies.get('session')
    if token not in sockets:
        sockets[token] = {"sid": sid, "connected": True, "history": {}}
        socket_connection[token] = ChatbotHandler(token, socketio)
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
    chat_handler.handle_attachment(data['attachments'])
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


if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)




# !!!! will be done by today 
# support for attachements in ml function~
# enhance api~
# docker file for ollama~
# autofill api
