from time import localtime, strftime

from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO, send, emit, join_room, leave_room

import json
import uuid

from model.user import User
from errors import register_error_handlers

from security.basic_authentication import generate_password_hash, init_basic_auth
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(_name_)
auth = init_basic_auth()
register_error_handlers(app)

@app.route("/", methods=["GET"])
def main():
    return render_template("index.html")


@app.route("/chat", methods=['GET', 'POST'])
@auth.login_required
def chat():
    return render_template("chat.html", username=auth.username(), rooms = ROOMS)