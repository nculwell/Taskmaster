#!/usr/bin/python3
# vim: et ts=8 sts=4 sw=4

import flask
import psycopg2, psycopg2.extras
import sys, os, traceback, hashlib, binascii
from .pg import *
from . import auth
from common.data import *

TEST_SERVER_PORT=8257
TEST_LOCALHOST_ONLY=False

MIN_REQUIRED_VERSION = 0

PASSWORD_HASH = 'sha256'
PASSWORD_SALT_BYTES = 16
PASSWORD_ITERATIONS_THOUSANDS = 200

app = flask.Flask(__name__)

# FIXME! CHOOSE A REAL SECRET KEY AND STORE IT PROPERLY
app.secret_key = os.urandom(16)

def Serve():
    host = '127.0.0.1' if TEST_LOCALHOST_ONLY else '0.0.0.0'
    app.run(host=host, port=TEST_SERVER_PORT)

@app.route("/")
def Home():
    return "To download the client, visit: https://github.com/nculwell/Taskmaster"

@app.route('/login', methods=['POST'])
def Login():
    username = flask.request.form.get('usr', '')
    pwdSha256Hex = flask.request.form.get('pwd', '')
    version = flask.request.form.get('v', 0)
    if version < MIN_REQUIRED_VERSION:
        flask.abort(500,
                "Requires at least version %d." % MIN_REQUIRED_VERSION)
    if username == '':
        raise Exception("Username not found.")
    if pwdSha256Hex == '':
        raise Exception("Password not found.")
    #print('PASSWORD', pwdSha256Hex)
    pwdSha256 = HexToBin(pwdSha256Hex)
    try:
        loginUsr = auth.AuthenticateUser(username, pwdSha256)
    except auth.AuthFailedError as e:
        print(e, file=sys.stderr)
        flask.abort(401)
    flask.session['usr'] = username
    return ToJson(ResultToDict(loginUsr))

def GetLoggedInUser():
    try:
        return flask.session['usr']
    except KeyError:
        app.logger.debug("User not logged in.")
        flask.abort(401)

def InvokeService(function):
    GetLoggedInUser()
    try:
        response = function()
    except EntityNotFoundException as e:
        traceback.print_exc()
        flask.abort(404, "Entity not found.")
    return ToJson(response)

@app.route('/user/<usrId>')
def GetUserRoute(usrId):
    return InvokeService(lambda: GetUser(usrId))

def GetUser(usrId):
    GetLoggedInUser()
    usr = Query1("select * from v_usr where id = %s", usrId)
    result = ResultToDict(usr)
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

@app.route('/task/user/<usrId>')
def GetTasksByUserRoute(usrId):
    return InvokeService(lambda: GetTasksByUser(usrId))

TaskKeys = 'tsk_id tsk_type_id tsk_type_name title desc_doc_id'.split()
UsrRoleKeys = 'tsk_usr_role_id tsk_usr_role_name usr_id username fullname'.split()

def GetTasksByUser(usrId):
    results = Query("select * from v_tsk_usr where usr_id = %s", usrId)
    rd = ResultsToDicts(results)
    tasks = RollUp(rd, 'tsk_id', 'usr_roles', TaskKeys, UsrRoleKeys)
    print(tasks)
    return tasks

def ExtractKeys(fromDict, keys):
    toDict = {}
    for k in keys:
        toDict[k] = fromDict[k]
    return toDict

def RollUp(dicts, primaryKey, separateKeysNode, combinedKeys, separateKeys):
    if not primaryKey in combinedKeys:
        combinedKeys = combinedKeys + [primaryKey]
    rollup = {}
    for d in dicts:
        pk = d[primaryKey]
        if pk in rollup:
            rec = rollup[pk]
        else:
            rec = ExtractKeys(d, combinedKeys)
            rec[separateKeysNode] = []
            rollup[pk] = rec
        sep = ExtractKeys(d, separateKeys)
        rec[separateKeysNode].append(sep)
    return list(rollup.values())

