from enum import Enum 
from flask_socketio import send
from time import localtime, strftime

class MessageType(Enum):
    TEXT = 1
    IMAGE = 2

def send_message(msg_type, content, username, room):
    current_time = strftime('%b-%d %I:%M%p', localtime())
    if msg_type == MessageType.TEXT:
        send({'type': msg_type.name, 'msg': content, 'username': username, 'time_stamp': current_time}, room=room)
    elif msg_type == MessageType.IMAGE:
        send({'type': msg_type.name, 'msg': content, 'username': username, 'time_stamp': current_time}, room=room)
    else:
        raise RuntimeError("Inalid message type {}".format(msg_type.name))