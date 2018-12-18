#!/usr/bin/python3
# vim: et ts=4 sts=4 sw=4 smartindent

#import http.client
import http.cookiejar, urllib.request
import json

HTTPS=False

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

def CallService(path):
    if session['opener'] == None:
        _Login()
    with session['opener'].open(_Url(path)) as f:
        responseJson = f.read().decode('utf-8')
    # TODO: Login again if unauthorized.
    return json.loads(responseJson)

def Login(username, password):
    session['username'] = username
    session['password'] = password
    return _Login()

def _Login():
    usr = session['username']
    pwd = session['password']
    session['opener'] = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(session['cj']))
    loginData = urllib.parse.urlencode({'usr': usr, 'pwd': pwd})
    with session['opener'].open(_Url('login'), loginData.encode('utf8')) as f:
        loginResponse = f.read().decode('utf-8')
    return loginResponse

def _Url(path):
    prefix = "%s://%s:%d/" % (session['scheme'], session['host'], session['port'])
    return prefix + path

if __name__ == "__main__":
    r = CallService("user/1")
    print(r)

