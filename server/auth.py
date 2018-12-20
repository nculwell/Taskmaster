#!/usr/bin/python3
# vim: et ts=8 sts=4 sw=4

import hashlib, binascii
from common.data import *
from .pg import *

PASSWORD_HASH = 'sha256'
PASSWORD_SALT_BYTES = 16
PASSWORD_ITERATIONS_THOUSANDS = 200

def AuthenticateUser(username, pwdSha256):
    try:
        usr = Query1("select * from v_usr where username = %s", username)
    except EntityNotFoundException:
        print("User not found: %s" % username, file=sys.stderr)
        return None
    pwdSql = """
        select p.* from pwd p where p.usr_id = %s
        order by p.create_ts desc limit 1
    """
    pwd = Query1(pwdSql, usr['id'])
    if not _VerifyPassword(pwd['method'], pwd['salt'], pwd['hash'], pwdSha256):
        print("Password not matched for user: %s" % username, file=sys.stderr)
        return None
    return usr

def _VerifyPassword(method, salt, storedPwdHash, pwdSha256):
    hashName, iterations = method.split(':')
    its = int(iterations) * 1000
    pwdHash = hashlib.pbkdf2_hmac(hashName, pwdSha256, salt, its)
    return pwdHash == bytes(storedPwdHash)

def StoreCleartextPassword(usrId, password):
    pwdSha256 = HashPassword(password)
    StoreSha256Password(usrId, pwdSha256)

def StoreSha256Password(usrId, pwdSha256):
    hashName = PASSWORD_HASH
    iterations = PASSWORD_ITERATIONS_THOUSANDS * 1000
    method = '%s:%d' % (hashName, PASSWORD_ITERATIONS_THOUSANDS)
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

