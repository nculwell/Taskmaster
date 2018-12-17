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
    urlPrefix = "%s://%s:%d/" % (session['scheme'], session['host'], session['port'])
    if session['opener'] == None:
        _Login(urlPrefix)
    with session['opener'].open(urlPrefix + path) as f:
        responseJson = f.read().decode('utf-8')
    return json.loads(responseJson)

def _Login(urlPrefix):
    session['opener'] = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(session['cj']))
    loginData = urllib.parse.urlencode({'usr': 'njc', 'pwd': 'xxx'})
    with session['opener'].open(urlPrefix + 'login', loginData.encode('utf8')) as f:
        loginResponse = f.read().decode('utf-8')

if __name__ == "__main__":
    r = CallService("user/1")
    print(r)

