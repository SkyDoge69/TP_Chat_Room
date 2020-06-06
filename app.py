import os
from time import localtime, strftime
 
from flask import Flask, request, render_template, jsonify, redirect, url_for, flash, send_from_directory
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_socketio import SocketIO, send, emit, join_room, leave_room, close_room
import requests
from PIL import Image
from message import MessageType, send_message
 
import json
import uuid
 
from model.user import User
from model.rooms import Room
from model.invites import Invite
from errors import register_error_handlers
from errors import ApplicationError
 
from security.basic_authentication import generate_password_hash, init_basic_auth
from werkzeug.security import generate_password_hash, check_password_hash 
from wtform_fields import *

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
auth = init_basic_auth()
app.secret_key = 'takamekefinenemekefibratnqkude33trqqima'
login_manager = LoginManager()
login_manager.init_app(app)
register_error_handlers(app) 
socketio = SocketIO(app)


@login_manager.user_loader
def load_user(user_id):
    return User.find(user_id)

@app.route("/", methods=["GET", "POST"])
def main():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user_object = User.find_by_name(login_form.username.data)
        login_user(user_object)
        return redirect(url_for('chat'))
    return render_template("index.html", form=login_form)

@app.route("/chat", methods=['GET', 'POST'])
def chat():
    return render_template("chat.html", username=current_user.name, rooms = Room.all_neznam(), private_rooms = Room.all_private())

@app.route("/profiles/<username>", methods=['GET', 'POST'])
def profile(username):
    user = User.find_by_name(username)
    return render_template("profile.html", user = user)

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('You have successfully logged yourself out.')
    return redirect(url_for('main'))

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

@app.route("/api/invites", methods=["POST"])
def create_invite():
    invite_data = request.get_json(force=True, silent=True)
    if invite_data == None:
        return "Bad request", 401
    invite = Invite(invite_data["room_id"], invite_data["username"])
    invite.save()
    return jsonify(invite.to_dict()), 201

@app.route("/api/invites", methods=["GET"])
def list_invites():
    result = {"result": []}
    for invite in Invite.all():
        result["result"].append(invite.to_dict())
    return jsonify(result), 201

@app.route("/api/users", methods=["POST"])
def create_user():
    user_data = request.get_json(force=True, silent=True)
    if user_data == None:
        return "Bad request", 401
    #hashed_password = generate_password_hash(user_data["password"])
    user = User(user_data['name'], user_data['password'], user_data['room'], user_data['description'], user_data['picture_location'])
    user.save()
    return jsonify(user.to_dict()), 201

@app.route("/api/users/<user_id>", methods=["GET"])
def get_user(user_id):
    return jsonify(User.find(user_id).to_viewable())

@app.route("/api/users", methods=["GET"])
def list_users():
    result = {"result": []}
    for user in User.all():
        result["result"].append(user.to_viewable())
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
def send_text(data):
    send_message(MessageType.TEXT, data['msg'], data['username'], data['room'])

@socketio.on('send_gif')
def send_gif(data):
    uri = data['gif_url']
    send_message(MessageType.IMAGE, uri, data['username'], data['room'])


def notify_join_room(username, room_name, invite_check):
    if invite_check:
        join_room(room_name)
        send({'msg': username + " has joined the " + room_name + " room."}, room=room_name)
        User.update_room(room_name, User.find_by_name(username).name)
    else:
        join_room("Lounge")
        send({'msg': "You are not invited, choose another room."})
        User.update_room("Lounge", User.find_by_name(username).name)

@socketio.on('join')
def join(data):
    if Room.private_check(data['room']):
        if Invite.check_for_invite(data['room'], data['username']):
            notify_join_room(data['username'], data['room'], True)
        else:
            notify_join_room(data['username'], data['room'], False)
    else:
        notify_join_room(data['username'], data['room'], True)

@socketio.on('leave')
def leave(data):
    leave_room(data['room'])
    send({'msg': data['username'] + " has left the " + data['room'] + " room."}, room=data['room'])


def notify_room_creation(username, room_name, is_private):
    if is_private == True:
        for current_room in Room.all_rooms():  
            send({'msg': username + " has created 'private' " +  room_name + " room. Refresh page."}, room=current_room)
        Room.add_room(1, room_name)
    elif is_private == False:
        for current_room in Room.all_rooms():  
            send({'msg': username + " has created " +  room_name + " room. Refresh page."}, room=current_room)
        Room.add_room(0, room_name)
    Invite.add_invite(room_name, username)

@socketio.on('create_room')
def create_room(data):
    notify_room_creation(data['username'], data['name'], False)

@socketio.on('create_private_room')
def create_private_room(data): 
    notify_room_creation(data['username'], data['name'], True)


def static_check(room_name):
    if room_name == "Lounge" or room_name == "Narga" or room_name == "Clashka" or room_name == "Techno boom boom":
        return True
    return False

def neznamkvopravi(room_name, username):
    if room_name in Room.all_rooms() and Invite.check_for_invite(room_name, username):
        for current_room in Room.all_rooms():  
            send({'msg': username + " has deleted " +  room_name + " room. Refresh page."}, room=current_room)
        Room.delete_room(room_name)
        Invite.delete_invite(room_name)
    else:
        send({'msg': "Cannot delete this room"})

@socketio.on('close_room')
def close_room(data):
    if static_check(data['name']):
        send({'msg': "Cannot delete static rooms!"}, room=data['room'])
    else:
        neznamkvopravi(data['name'], data['username'])


def search_and_invite(username, invited_user, room_name):
    for user in User.all():
        if user.name == invited_user:
            Invite.add_invite(room_name, invited_user)
            send({'msg': "Invite sent!"})
            send({'msg': username + " has invited you in the " + room_name + " room."}, room=user.room)
            return True
    return False

@socketio.on('invite_user')
def invite_user(data):
    if data['invited_user'] == data['username']:
        send({'msg': "Cannot invite yourself!"})
        raise ApplicationError("Can't invite yourself", 404)
    else:
        check = False
        if not search_and_invite(data['username'], data['invited_user'], data['room']):
            send({'msg': "User does not exist!"})
            raise ApplicationError("User doesn't exist", 404)
    
if __name__ == "__main__":
    socketio.run(app, debug=True)
