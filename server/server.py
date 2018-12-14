#!/usr/bin/python3
# vim: ts=4 sts=4 sw=4 et smartindent

import flask
app = flask.Flask(__name__)

# FIXME! MOVE THE KEY OUT OF THE SOURCE CODE!
app.secret_key = b'\x9f\t\x1c$\x88\xf0\xd0.\xed\x9d\x12\\&\xda\x8f\x97'

@app.route("/")
def Home():
    return "To download the client, visit: https://github.com/nculwell/Taskmaster"

@app.route('/login', methods=['POST'])
def Login():
    username = flask.request.form["username"]
    password = flask.request.form["password"]
    if DoLogin(username, password):
        flask.session['username'] = username
    else:
        flask.abort(401)

def DoLogin(username, password):
    if username == 'njc' and password == 'njc':
        return True
    return False

def CheckLogin():
    username = flask.session.get('username', '')
    if len(username) == 0:
        flask.abort(401)

@app.route('/user/<userId>')
def GetUser(userId):
    CheckLogin()
    return 'User %s' % userId

@app.route('/task/<taskId>')
def GetTask(taskId):
    CheckLogin()
    return 'Task %d' % taskId

