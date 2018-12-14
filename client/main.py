#!/usr/bin/python3

#import wxversion
#wxversion.select("2.8")
import wx
import sys

from task import *
import mainframe

applicationName = "TaskMaster"

initialData = [
    { "id": "1", "type": "A", "title": "First" },
    { "id": "2", "type": "B", "title": "Second" },
]

initialTasks = [ Task(t) for t in initialData ]

app = wx.App(redirect=True)   # Error messages go to popup window
top = mainframe.MainFrame(applicationName, initialTasks)
top.Show()
app.MainLoop()

