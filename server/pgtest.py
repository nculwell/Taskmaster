#!/usr/bin/python3
# vim: ts=4 sts=4 sw=4 et smartindent

import flask
import psycopg2, psycopg2.extras
import json

PORT=8257

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
    result = Query1("select * from usr where id = %s", username)
    return False

def CheckLogin():
    username = flask.session.get('usr', '')
    if len(username) == 0:
        flask.abort(401)

def Connect():
    conn = psycopg2.connect(
            host="localhost", database="taskmaster",
            cursor_factory=psycopg2.extras.DictCursor)
    return conn

def Query(sql, params=()):
    params = FixParams(params)
    conn = Connect()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        rows = cur.fetchall()
        rowCount = cur.rowcount
        cur.close()
        return rows
    finally:
        conn.close()

def Query1(sql, params=()):
    params = FixParams(params)
    conn = Connect()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        row = cur.fetchone()
        cur.close()
        return row
    finally:
        conn.close()

def ResultToDict(result):
    return { k: v for k, v in result.items() }

def ResultsToDicts(results):
    return ( ResultToDict(r) for r in results )

def FixParams(params):
    if isinstance(params, list) or isinstance(params, tuple):
        return params
    return (params,)

def InvokeService(function):
    CheckLogin()
    response = function()
    return json.dumps(respone)

@app.route('/user/<userId>')
def GetUserRoute(userId):
    return InvokeService(lambda: GetUser(userId))

def GetUser(userId):
    CheckLogin()
    user = Query1("select * from VUser where userId = %s", userId)
    result = ResultToDict(user)
    return json.dumps(result)

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
    app.run(host='127.0.0.1', port=PORT)

