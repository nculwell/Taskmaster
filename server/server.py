#!/usr/bin/python3
# vim: et ts=8 sts=4 sw=4

import flask
import psycopg2, psycopg2.extras
import sys, os, traceback, hashlib, binascii
from .pg import *
from common.data import *

TEST_SERVER_PORT=8257
TEST_LOCALHOST_ONLY=False

MIN_REQUIRED_VERSION = 0

PASSWORD_HASH = 'sha256'
PASSWORD_SALT_BYTES = 16
PASSWORD_ITERATIONS_THOUSANDS = 200
PASSWORD_ENCODING = 'utf8'

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
    print('PASSWORD', pwdSha256Hex)
    pwdSha256 = HexToBin(pwdSha256Hex)
    loginUsr = DoLogin(username, pwdSha256)
    if loginUsr is None:
        flask.abort(401)
    else:
        flask.session['usr'] = username
        return ToJson(ResultToDict(loginUsr))

def DoLogin(username, pwdSha256):
    try:
        usr = Query1("select * from usr where username = %s", username)
    except EntityNotFoundException:
        print("User not found: %s" % username, file=sys.stderr)
        return None
    p = Query1("""
        select p.* from pwd p where p.usr_id = %s
        order by p.create_ts desc limit 1
    """, usr['id'])
    if not VerifyPassword(p['method'], p['salt'], p['hash'], pwdSha256):
        print("Password not matched for user: %s" % username, file=sys.stderr)
        return None
    return usr

def VerifyPassword(method, salt, storedPwdHash, pwdSha256):
    hashName, iterations = method.split(':')
    its = int(iterations) * 1000
    pwdHash = hashlib.pbkdf2_hmac(hashName, pwdSha256, salt, its)
    return pwdHash == bytes(storedPwdHash)

def StorePassword(usrId, password):
    hashName = PASSWORD_HASH
    iterations = PASSWORD_ITERATIONS_THOUSANDS * 1000
    method = '%s:%d' % (hashName, PASSWORD_ITERATIONS_THOUSANDS)
    pwdSha256 = HashPassword(password)
    print(BinToHex(pwdSha256))
    salt = os.urandom(PASSWORD_SALT_BYTES)
    newPwdHash = hashlib.pbkdf2_hmac(hashName, pwdSha256, salt, iterations)
    print("SALT: " + BinToHex(salt))
    print("HASH: " + BinToHex(newPwdHash))
    Insert('pwd', (
            ('usr_id', usrId),
            ('method', method),
            ('salt', salt),
            ('hash', newPwdHash),
        ))

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
    usr = Query1("select * from usr where id = %s", usrId)
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

@app.route('/task/user/<userId>')
def GetTasksByUserRoute(usrId):
    return InvokeService(lambda: GetTasksByUser(usrId))

def GetTasksByUser(usrId):
    results = Query("select * from v_tsk_usr where usr_id = %s", usrId)
    return ResultsToDicts(results)

