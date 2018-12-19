#!/usr/bin/python3
# vim: et ts=8 sts=4 sw=4

#import http.client
import http.cookiejar, urllib.request
import json, hashlib, binascii

HTTPS=False
PASSWORD_ENCODING='utf8'

session = {
    'cj': http.cookiejar.CookieJar(),
    'scheme': 'https' if HTTPS else 'http',
    'host': 'tiamat',
    'port': 8257,
    'opener': None,
}

#def GetConnection(host):
#    if HTTPS:
#        return http.client.HTTPSConnection(host)
#    else:
#        return http.client.HTTPConnection(host)

#def Get(url):
#    conn = GetConnection("tiamat")
#    conn.request("GET", url)
#    conn.getresponse()
#    print(r1.status, r1.reason)
#    data1 = r1.read()  # This will return entire content.

def GetOpener():
    opener = session.get('opener', None)
    if opener is None:
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(session['cj']))
        session['opener'] = opener
    return opener

def CallService(path):
    with GetOpener().open(_Url(path)) as f:
        responseJson = f.read().decode('utf-8')
    # TODO: Login again (with saved username/password) if unauthorized.
    # If this login attempt also fails, raise an exception that brings
    # up the login screen.
    return json.loads(responseJson)

def Login(username, password):
    session['username'] = username
    pwdSha256 = HashPassword(password)
    pwdSha256Hex = BinToHex(pwdSha256)
    #print(pwdSha256Hex)
    session['password'] = pwdSha256Hex
    return _Login()

def HashPassword(password):
    pwdEncoded = password.encode(PASSWORD_ENCODING)
    h = hashlib.sha256(pwdEncoded)
    h.update(pwdEncoded)
    pwdSha256 = h.digest()
    return pwdSha256

def BinToHex(binary):
    by = bytes(binary)
    hex = binascii.b2a_hex(by)
    return hex.decode('ascii')

def _Login():
    usr = session['username']
    pwd = session['password']
    loginData = urllib.parse.urlencode({'usr': usr, 'pwd': pwd})
    with GetOpener().open(_Url('login'), loginData.encode('utf8')) as f:
        loginResponse = f.read().decode('utf-8')
    return json.loads(loginResponse)

def _Url(path):
    prefix = "%s://%s:%d/" % (session['scheme'], session['host'], session['port'])
    return prefix + path

if __name__ == "__main__":
    r = CallService("user/1")
    print(r)

