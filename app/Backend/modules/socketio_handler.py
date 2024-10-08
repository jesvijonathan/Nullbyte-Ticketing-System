# from flask_socketio import emit
# from flask import request
# from app import socketio 
# from .auth.auth import jwt_required
# from config import *
# from .ml.ml_handler import ChatbotHandler

# from flask_socketio import SocketIO, emit, send, join_room, leave_room, close_room, rooms, disconnect, Namespace

# # Socket.IO event handling

# def connect():
#     print("############## CONNECTED ##############")
#     sid = request.sid
#     token = request.cookies.get('session')

#     if token in sockets:
#         sockets[token]["sid"] = sid  # Update the sid to current connection
#         sockets[token]["connected"] = True
#         if token in socket_connection:
#             socketio.emit("live_chat", {"live_chat": socket_connection[token].history}, room=sid)
#         else:
#             socket_connection[token] = ChatbotHandler(token, socketio)  # Pass socketio here
#             socketio.emit("message", {"message": {**sockets[token], "connected": sockets[token]["connected"]}}, room=sid)
#     else:
#         sockets[token] = {
#             "sid": sid,
#             "connected": True,
#             "history": {}
#         }
#         socket_connection[token] = ChatbotHandler(token, socketio)  # Pass socketio here
#         socketio.emit("message", {"message": {**sockets[token], "connected": sockets[token]["connected"]}}, room=sid)


# def message(msg):
#     sid = request.sid
#     print(f"Message from {sid}: {msg}")
#     token = request.cookies.get('session')
#     if token in socket_connection:
#         socket_connection[token].response_add(msg)
#         return
#     else:
#         socketio.emit("message", {"message": "No active session found"}, room=sid)
#         return

# def disconnect():
#     sid = request.sid
#     print(f"User disconnected: {sid}")
#     emit('message', 'Disconnected from the server')