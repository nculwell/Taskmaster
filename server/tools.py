#!/usr/bin/python3
# vim: et ts=8 sts=4 sw=4

import sys
from collections import deque
from . import server, auth

USAGE = """
USAGE: dbtools.py set pwd <usr_id> <password>
""".strip()

def Run():
    flags = [ x for x in sys.argv[1:] if x.startswith('-') ]
    args = [ x for x in sys.argv[1:] if not x.startswith('-') ]
    try:
        if Elt(args, 0) == 'set':
            try:
                what = args[1]
                if what == 'pwd':
                    usrId = args[2]
                    password = args[3]
                    auth.StoreCleartextPassword(usrId, password)
                else:
                    print("Don't know how to set '%s'." % what, file=sys.stderr)
            except IndexError:
                print("Invalid arguments.", file=sys.stderr)
        else:
            raise Exception("Unknown command.")
    except (IndexError, Exception) as e:
        print(e)
        print(USAGE, file=sys.stderr)

def Elt(array, index):
    try:
        return array[index]
    except IndexError:
        return None

