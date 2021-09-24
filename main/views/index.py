from flask import Blueprint, render_template, jsonify, make_response, current_app as app, request
from flask_socketio import emit
from main import socketio, db

from main.models import User, Week_board

from .user import get_table_by_json

bp = Blueprint('index', __name__, url_prefix='/')

is_running = False

@bp.route('')
def main_page():
    #print(request.remote_addr)
    return render_template('index.html')


@bp.route('/admin')
def amdin():
	return 'Hack my site!'

####################################################

@socketio.on("refresh")
def broadcast():
    global is_running
    emit('request', broadcast=True)
    try:
        if not is_running:
            is_running = True
            emit('refresh', get_table_by_json(), broadcast=True)
            is_running = False
    except:
        is_running=False
        emit('refresh', broadcast=True)

@socketio.on("connect")
def welcome():
    broadcast()




"""
@socketio.on("connect")
def welcome():
    emit('welcome', '누군가 나타났다.', broadcast=True)

@socketio.on("message")
def chat(message):
    print(message)
    for i in range(len(message)):
        #a = bytes(message[str(i)])#.decode("UTF-8")
        a=1
        #print(base64.b64decodestring(a))
    print(message)
    #print(message['msg'])
    #message['msg'].encode('UTF-8')
    #print(message['msg'])
    #emit("message", message['msg'], broadcast=True)
"""