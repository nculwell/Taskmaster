#!/usr/bin/python3
# vim: ts=4 sts=4 sw=4 et smartindent

import flask
import psycopg2, psycopg2.extras
from pg import *

TEST_SERVER_PORT=8257
TEST_LOCALHOST_ONLY=True

app = flask.Flask(__name__)

# FIXME! MOVE THE KEY OUT OF THE SOURCE CODE!
app.secret_key = b'\x9f\t\x1c$\x88\xf0\xd0.\xed\x9d\x12\\&\xda\x8f\x97'

@app.route("/")
def Home():
    return "To download the client, visit: https://github.com/nculwell/Taskmaster"

@app.route('/login', methods=['POST'])
def Login():
    username = flask.request.form.get('usr', '')
    password = flask.request.form.get('pwd', '')
    if username == '':
        raise Exception("Username not found.")
    if password == '':
        raise Exception("Password not found.")
    if DoLogin(username, password):
        flask.session['usr'] = username
    else:
        flask.abort(401)

def DoLogin(username, password):
    result = Query1("select * from usr where username = %s", username)
    return False

def CheckLogin():
    username = flask.session.get('usr', '')
    if len(username) == 0:
        flask.abort(401)

def InvokeService(function):
    CheckLogin()
    response = function()
    return ToJson(respone)

@app.route('/user/<userId>')
def GetUserRoute(userId):
    return InvokeService(lambda: GetUser(userId))

def GetUser(userId):
    CheckLogin()
    user = Query1("select * from VUser where userId = %s", userId)
    result = ResultToDict(user)
    return ToJson(result)

@app.route('/task/<taskId>')
def GetTaskRoute(taskId):
    return InvokeService(lambda: GetTask(taskId))

def GetTask(taskId):
    task = Query1("select * from VTask where taskId = %s", taskId)
    result = ResultToDict(task)
    roles = Query("select * from VTaskUser where taskId = %s", taskId)
    result['roles'] = ResultsToDicts(roles)
    return result

@app.route('/task/user/<userId>')
def GetTasksByUserRoute(userId):
    return InvokeService(lambda: GetTasksByUser(taskId))

def GetTasksByUser(userId):
    results = Query("select * from VTaskUser where userId = %s", userId)
    return ResultsToDicts(results)

if __name__ == "__main__":
    host = '127.0.0.1' if TEST_LOCALHOST_ONLY else '0.0.0.0'
    app.run(host=host, port=TEST_SERVER_PORT)

