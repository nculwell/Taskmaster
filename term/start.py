#!/usr/bin/python3

import curses
import curses.ascii
import curses.textpad

keys = ''

def start(stdscr):
    stdscr.clear()
    displayDim = { 'h': curses.LINES-3, 'w': curses.COLS, 'y': 0, 'x': 0 }
    entryDim = { 'h': 2, 'w': curses.COLS-2, 'y': curses.LINES-2, 'x': 1 }
    displayWin = curses.newwin(displayDim['h'], displayDim['w'], displayDim['y'], displayDim['x'])
    entryWin = curses.newwin(entryDim['h'], entryDim['w'], entryDim['y'], entryDim['x'])
    stdscr.addstr(curses.LINES-3, 0, '='*curses.COLS)
    #entryWin.move(1, 1)
    entryWin.keypad(True)
    displayWin.refresh()
    #cmd = readCmd(entryWin)
    tp = curses.textpad.Textbox(entryWin)
    tp.edit()

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
    curses.wrapper(start)

if __name__ == "__main__":
    try:
        main()
    finally:
        print(keys)

