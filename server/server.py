#!/usr/bin/python3
# vim: ts=4 sts=4 sw=4 et smartindent

import flask
import psycopg2, psycopg2.extras
import sys, os, traceback
from pg import *

TEST_SERVER_PORT=8257
TEST_LOCALHOST_ONLY=True

app = flask.Flask(__name__)

# FIXME! CHOOSE A REAL SECRET KEY AND STORE IT PROPERLY
app.secret_key = os.urandom(16)

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
        return 'Welcome, %s.' % username
    else:
        flask.abort(401)

def DoLogin(username, password):
    result = Query1("select * from usr where username = %s", username)
    return True 

def CheckLogin():
    if not 'usr' in flask.session:
        app.logger.debug("No username.")
        flask.abort(401)

def InvokeService(function):
    CheckLogin()
    try:
        response = function()
    except EntityNotFoundException as e:
        traceback.print_exc()
        flask.abort(404, "Entity not found.")
    return ToJson(response)

@app.route('/user/<userId>')
def GetUserRoute(userId):
    return InvokeService(lambda: GetUser(userId))

def GetUser(userId):
    CheckLogin()
    user = Query1("select * from usr where id = %s", userId)
    result = ResultToDict(user)
    return ToJson(result)

@app.route('/task/<taskId>')
def GetTaskRoute(taskId):
    return InvokeService(lambda: GetTask(taskId))

def GetTask(taskId):
    task = Query1("select * from v_tsk where tsk_id = %s", taskId)
    result = ResultToDict(task)
    roles = Query("select * from v_tsk_usr where tsk_id = %s", taskId)
    result['roles'] = ResultsToDicts(roles)
    return result

@app.route('/task/user/<userId>')
def GetTasksByUserRoute(userId):
    return InvokeService(lambda: GetTasksByUser(userId))

def GetTasksByUser(userId):
    results = Query("select * from v_tsk_usr where usr_id = %s", userId)
    return ResultsToDicts(results)

if __name__ == "__main__":
    host = '127.0.0.1' if TEST_LOCALHOST_ONLY else '0.0.0.0'
    app.run(host=host, port=TEST_SERVER_PORT)

