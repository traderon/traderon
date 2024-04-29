from flask_socketio import SocketIO, emit
from flask import jsonify

socketio = SocketIO(cors_allowed_origins="*")

@socketio.on("msg")
def handle_message(msg):
  emit("msg", jsonify({"msg": msg}), broadcast=True)