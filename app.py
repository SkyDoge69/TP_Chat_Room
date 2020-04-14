from time import localtime, strftime
 
from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO, send, emit, join_room, leave_room, close_room
 
import json
import uuid
 
from model.user import User
from model.rooms import Room
from errors import register_error_handlers
from errors import ApplicationError
 
from security.basic_authentication import generate_password_hash, init_basic_auth
from werkzeug.security import generate_password_hash, check_password_hash
 
 
app = Flask(__name__)
auth = init_basic_auth()
register_error_handlers(app)
 
socketio = SocketIO(app)

ROOMS = [Room.find_by_name("lounge").name, Room.find_by_name("shisha").name, Room.find_by_name("games").name, Room.find_by_name("coding").name]

PRIVATE_ROOMS = []

 
@app.route("/", methods=["GET"])
def main():
    return render_template("index.html")
 
 
@app.route("/chat", methods=['GET', 'POST'])
@auth.login_required
def chat():
    return render_template("chat.html", username=auth.username(), rooms = ROOMS, private_rooms = PRIVATE_ROOMS)
 

@app.route("/api/rooms", methods=["POST"])
def create_room():
    room_data = request.get_json(force=True, silent=True)
    if room_data == None:
        return "Bad request", 401
    room = Room(room_data["is_private"], room_data['name'])
    room.save()
    return jsonify(room.to_dict()), 201

@app.route("/api/rooms", methods=["GET"])
def list_rooms():
    result = {"result": []}
    for room in Room.all():
        result["result"].append(room.to_dict())
    return jsonify(result), 201
 

@app.route("/api/users", methods=["POST"])
def create_user():
    user_data = request.get_json(force=True, silent=True)
    if user_data == None:
        return "Bad request", 401
    hashed_password = generate_password_hash(user_data["password"])
    user = User(user_data["name"], hashed_password, user_data['room'])
    user.save()
    return jsonify(user.to_dict()), 201
 
 
@app.route("/api/users/<user_id>", methods=["GET"])
def get_user(user_id):
    return jsonify(User.find(user_id).to_dict())
 
 
@app.route("/api/users", methods=["GET"])
def list_users():
    result = {"result": []}
    for user in User.all():
        result["result"].append(user.to_dict())
    return jsonify(result), 201
 
 
@app.route("/api/users/<user_id>", methods=["PATCH"])
def update_user(user_id):
    user_data = request.get_json(force=True, silent=True)
    if user_data == None:
        return "Bad request", 401
 
    user = User.find(user_id)
    return jsonify(user.save().to_dict()), 201
 
 
@app.route("/api/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.find(user_id)
    user.delete(user_id)
    return ""
 
 
@socketio.on('message')
def message(data):
    print(f"\n\n{data}\n\n")
    send({'msg': data['msg'], 'username': data['username'], 'time_stamp': strftime('%b-%d %I:%M%p', localtime())}, room=data['room'])
 
@socketio.on('join')
def join(data):
    join_room(data['room'])
    send({'msg': data['username'] + " has joined the " + data['room'] + " room."}, room=data['room'])
    for user in User.all():
        if user.name == data['username']:
            user.update_room(data['room'], data['username'])
 
@socketio.on('leave')
def leave(data):
    leave_room(data['room'])
    send({'msg': data['username'] + " has left the " + data['room'] + " room."}, room=data['room'])
 
@socketio.on('create_room')
def create_room(data):
    send({'msg': data['username'] + " has created the " +  data['name'] + " room. Refresh page."})
    ROOMS.append(data['name'])
    Room.add_room(0, data['name'])

@socketio.on('create_private_room')
def create_private_room(data):    
    send({'msg': data['username'] + " has created 'private' " +  data['name'] + " room. Refresh page."})
    PRIVATE_ROOMS.append(data['name'])
    Room.add_room(1, data['name'])

@socketio.on('close_room')
def close_room(data):
    if data['name'] == 'lounge' or data['name'] == 'shisha' or data['name'] == 'games' or data['name'] == 'coding':
        send({'msg': "Cannot delete static rooms!"}, room=data['room'])
    else:
        if data['name'] in ROOMS:
            ROOMS.remove(data['name'])
            Room.delete_room(data['name'])
        elif data['name'] in PRIVATE_ROOMS:
            PRIVATE_ROOMS.remove(data['name'])
            Room.delete_room(data['name'])
          
        send({'msg': data['username'] + " has deleted the " + data['name'] + " room. Refresh page."})
    
@socketio.on('invite_user')
def invite_user(data):
    if data['invited_user'] == data['username']:
        send({'msg': "Cannot invite yourself!"})
        raise ApplicationError("Can't invite yourself", 404)
    else:
        check = False
        for user in User.all():
            if user.name == data['invited_user']:
                send({'msg': "Invite sent!"})
                genaka = user.room
                send({'msg': data['username'] + " has invited you in the " + data['room'] + " room."}, room=genaka)
                check = True
        if not check:
            send({'msg': "User does not exist!"})
            raise ApplicationError("User doesn't exist", 404)

if __name__ == "__main__":
    socketio.run(app, debug=True)