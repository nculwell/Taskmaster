#!/usr/bin/python3

import curses

def start(stdscr):
    stdscr.clear()
    displayDim = { 'h': curses.LINES-2, 'w': curses.COLS, 'y': 0, 'x': 0 }
    entryDim = { 'h': 2, 'w': curses.COLS, 'y': curses.LINES-2, 'x': 0 }
    displayWin = curses.newwin(displayDim['h'], displayDim['w'], displayDim['y'], displayDim['x'])
    entryWin = curses.newwin(entryDim['h'], entryDim['w'], entryDim['y'], entryDim['x'])
    entryWin.addstr(0, 0, '='*curses.COLS)
    entryWin.move(1, 1)
    displayWin.refresh()
    entryWin.refresh()
    entryWin.getkey()

def main():
    curses.wrapper(start)

if __name__ == "__main__":
    main()

