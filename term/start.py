#!/usr/bin/python3

import curses, urllib
import curses.ascii
import curses.textpad
from client import net

keys = ''

def start(stdscr, usr):
    stdscr.clear()
    ENTRY_WINDOW_HEIGHT = 2
    displayWin = curses.newwin(curses.LINES - ENTRY_WINDOW_HEIGHT - 1, curses.COLS-1, 0, 0)
    dividerWin = curses.newwin(1, curses.COLS, curses.LINES - ENTRY_WINDOW_HEIGHT - 1, 0)
    entryWin = curses.newwin(ENTRY_WINDOW_HEIGHT, curses.COLS-3, curses.LINES - ENTRY_WINDOW_HEIGHT, 1)
    dividerWin.addstr(0, 0, '='*(curses.COLS-1))
    dividerWin.refresh()
    #entryWin.move(1, 1)
    entryWin.keypad(True)
    displayWin.refresh()
    #cmd = readCmd(entryWin)
    kk = entryWin.getkey()
    if kk == ':':
        cmd = readCommand(entryWin)

def login():
    import getpass 
    username = input("Username: ")
    if username == "":
        return False
    password = getpass.getpass("Password: ")
    if password == "":
        return False
    try:
        usr = net.Login(username, password)
        return usr
    except urllib.error.HTTPError as e:
        # urllib.error.HTTPError: HTTP Error 401: UNAUTHORIZED
        if str(e).startswith('HTTP Error 401:'):
            print("Bad username/password.")
        else:
            traceback.print_exc()
        return False
    except urllib.error.URLError as e:
        print("Unable to connect to server:", e)
        return False

def readCommand(entryWin):
    tp = curses.textpad.Textbox(entryWin)
    return tp.edit(handleEntryKey)

def handleEntryKey(k):
    if k == 7:
        return -1
    if k == 10:
        return 7
    return k

def readCmd(ew):
    global keys
    c = 0
    cmd = ''
    ew.move(1,1)
    while True:
        #ew.move(1, 1 + c)
        ew.refresh()
        k = ew.getkey()
        keys += str(k)+','
        cmd += str(k)+','
        #cmd += k
        if k == "\x0A":
            return cmd
        else:
            ew.addstr(k)
        c = c + 1

def main():
    try:
        usr = login()
        if usr:
            curses.wrapper(start, usr)
    finally:
        print(keys)

if __name__ == "__main__":
    main()

