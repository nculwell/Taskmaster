#!/usr/bin/python3

#import wxversion
#wxversion.select("2.8")
import wx
import sys

from . import task, mainframe

applicationName = "TaskMaster"

initialData = [
    { "id": "1", "type": "A", "title": "First" },
    { "id": "2", "type": "B", "title": "Second" },
]

initialTasks = [ task.Task(t) for t in initialData ]

def Start():
    app = wx.App(redirect=True) # redirect: error messages go to popup window
    top = mainframe.MainFrame(initialTasks)
    top.Show()
    app.MainLoop()

if __name__ == '__main__':
    Start()

