#!/usr/bin/python3
# vim: et ts=8 sts=4 sw=4

import sys
from collections import deque
from . import server

def Start():
    flags = [ x for x in sys.argv[1:] if x.startswith('-') ]
    args = [ x for x in sys.argv[1:] if not x.startswith('-') ]

    if Elt(args, 0) == 'set':
        try:
            what = args[1]
            if what == 'pwd':
                usrId = args[2]
                password = args[3]
                server.StorePassword(usrId, password)
            else:
                print("Don't know how to set '%s'." % what, file=sys.stderr)
        except IndexError:
            print("Invalid arguments.", file=sys.stderr)
    else:
        server.Serve()

def Elt(array, index):
    try:
        return array[index]
    except IndexError:
        return None

