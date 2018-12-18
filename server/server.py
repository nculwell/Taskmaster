#!/usr/bin/python3
# vim: et ts=8 sts=4 sw=4

import flask
import psycopg2, psycopg2.extras
import sys, os, traceback, hashlib
from pg import *

TEST_SERVER_PORT=8257
TEST_LOCALHOST_ONLY=True

PASSWORD_HASH = 'sha256'
PASSWORD_SALT_BYTES = 16
PASSWORD_ITERATIONS_THOUSANDS = 200

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
    loginUsr = DoLogin(username, password)
    if loginUsr is None:
        flask.abort(401)
    else:
        flask.session['usr'] = username
        return loginUsr

def DoLogin(username, password):
    try:
        usr = Query1("select * from usr where username = %s", username)
    except EntityNotFoundException:
        return None
    p = Query1("""
        select p.* from pwd p where p.usr_id = %s
        order by p.create_inst desc limit 1
    """, usr.id)
    if not VerifyPassword(p['method'], p['salt'], p['hash'], password):
        return None
    return usr

def VerifyPassword(method, salt, storedHash, suppliedPassword):
    hashName, iterations = method.split(':')
    its = int(iterations) * 1000
    attempt = hashlib.pbkdf2_hmac(hashName, suppliedPassword, salt, its)
    return attempt == storedHash

def StorePassword(usrId, password):
    hashName = PASSWORD_HASH
    binaryPassword = password.encode('utf-8')
    salt = os.urandom(PASSWORD_SALT_BYTES)
    iterations = PASSWORD_ITERATIONS_THOUSANDS * 1000
    hash = hashlib.pbkdf2_hmac(hashName, binaryPassword, salt, iterations)
    Insert('pwd', (
            ('usr_id', usrId),
            ('method', hashName + ':' + str(PASSWORD_ITERATIONS_THOUSANDS)),
            ('salt', salt),
            ('hash', hash),
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

def Elt(array, index):
    try:
        return array[index]
    except IndexError:
        return None

if __name__ == "__main__":
    allPorts = False
    if '--all' in sys.argv:
        allPorts = True
        sys.argv.remove('--all')
        print(sys.argv)
    if Elt(sys.argv, 1) == 'set':
        what = sys.argv[2]
        if what == 'pwd':
            usrId = sys.argv[3]
            password = sys.argv[4]
            StorePassword(usrId, password)
        else:
            print("Don't know how to set '%s'." % what, file=sys.stderr)
    else:
        if allPorts or not TEST_LOCALHOST_ONLY:
            host = '0.0.0.0'
        else:
            host = '127.0.0.1'
        app.run(host=host, port=TEST_SERVER_PORT)

