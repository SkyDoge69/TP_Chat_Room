from time import localtime, strftime

from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO, send, emit, join_room, leave_room, close_room

import json
import uuid

from model.user import User
from errors import register_error_handlers

from security.basic_authentication import generate_password_hash, init_basic_auth
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
auth = init_basic_auth()
register_error_handlers(app)

socketio = SocketIO(app)

ROOMS = ["lounge", "shisha", "games", "coding"]


@app.route("/", methods=["GET"])
def main():
    return render_template("index.html")


@app.route("/chat", methods=['GET', 'POST'])
@auth.login_required
def chat():
    return render_template("chat.html", username=auth.username(), rooms = ROOMS)


@app.route("/api/users", methods=["POST"])
def create_user():
    user_data = request.get_json(force=True, silent=True)
    if user_data == None:
        return "Bad request", 401
    hashed_password = generate_password_hash(user_data["password"])
    user = User(user_data["name"], hashed_password)
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

@socketio.on('leave')
def leave(data):
    leave_room(data['room']) 
    send({'msg': data['username'] + " has left the " + data['room'] + " room."}, room=data['room'])

@socketio.on('create_room')
def create_room(data):
    print("dasads")
    ROOMS.append(data['name'])
    
if __name__ == "__main__":
    socketio.run(app, debug=True)  
