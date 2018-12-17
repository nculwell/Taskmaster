#!/usr/bin/python3
# vim: et ts=8 sts=4 sw=4

import wx, wx.html, wx.grid
import sys, os, traceback

class Dialog(wx.Dialog):

    def __init__(self, parent, title,
            pos=wx.DefaultPosition, size=wx.DefaultSize):
        style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.TAB_TRAVERSAL
        wx.Dialog.__init__(self, parent,
                title=title, style=style, pos=pos, size=size)
        try:
            self.Construct()
        except Exception as e:
            traceback.print_exc()

    def DispatchUrl(self, url):
        if parent != None:
            parent.DispatchUrl(url)
        else:
            print("ERROR: URL dispatched from orphan dialog.", file=sys.stderr)

    # Wrap event handlers so we can control exception logging.
    def Bind(self, event, handler, source=None, id=wx.ID_ANY, id2=wx.ID_ANY, logEvents=False):
        wx.Frame.Bind(self, event, EventHandlerWrapper(handler, logEvents), source, id, id2)

class Frame(wx.Frame):

    def __init__(self, parent, title,
            pos=wx.DefaultPosition, size=wx.DefaultSize):
        wx.Frame.__init__(self, parent, title=title, pos=pos, size=size)
        try:
            self.Construct()
        except Exception as e:
            traceback.print_exc()

    def DispatchUrl(self, url):
        if parent != None:
            parent.DispatchUrl(url)
        else:
            # MainFrame should override this to do the work.
            print("ERROR: DispatchUrl not implemented.", file=sys.stderr)

    # Wrap event handlers so we can control exception logging.
    def Bind(self, event, handler, source=None, id=wx.ID_ANY, id2=wx.ID_ANY, logEvents=False):
        wx.Frame.Bind(self, event, EventHandlerWrapper(handler, logEvents), source, id, id2)

class Activity(wx.Control):

    def __init__(self, parent, id=wx.ID_ANY):
        style = wx.BORDER_SIMPLE
        wx.Control.__init__(self, parent, id, style=style)
        try:
            self.Construct()
        except Exception as e:
            traceback.print_exc()

    # Wrap event handlers so we can control exception logging.
    def Bind(self, event, handler, source=None, id=wx.ID_ANY, id2=wx.ID_ANY, logEvents=False):
        wx.Frame.Bind(self, event, EventHandlerWrapper(handler, logEvents), source, id, id2)

class Form(wx.Control):

    def __init__(self, parent, fields):
        wx.Control.__init__(self, parent, id, style=wx.BORDER_NONE)
        try:
            self.Construct(fields)
        except Exception as e:
            traceback.print_exc()

    def Construct(self, fields):
        gs = wx.GridSizer(rows=len(fields), cols=3, hgap=5, vgap=5)
        self.SetSizer(gs)
        labelFont = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)
        errMsgFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
        for field in fields:
            label = wx.StaticText(self, -1, field['label'])
            #label.SetFont(labelFont)
            textCtrl = wx.TextCtrl(self,
                    value=field.get('value', ''),
                    validator=field.get('validator'))
            errMsg = wx.StaticText(self, -1, '')
            #errMsg.SetFont(errMsgFont)
            gs.Add(label, 0, wx.ALL|wx.EXPAND, 0)
            gs.Add(textCtrl, 4, wx.ALL|wx.EXPAND, 0)
            gs.Add(errMsg, 1, wx.ALL|wx.EXPAND, 0)

    # Wrap event handlers so we can control exception logging.
    def Bind(self, event, handler, source=None, id=wx.ID_ANY, id2=wx.ID_ANY, logEvents=False):
        wx.Frame.Bind(self, event, EventHandlerWrapper(handler, logEvents), source, id, id2)

class EventHandlerWrapper:

    def __init__(self, handlerFunction, logEvents):
        self.handlerFunction = handlerFunction
        self.logEvents = logEvents

    def __call__(self, evt):
        try:
            if self.logEvents:
                pass # TODO: log event
            self.handlerFunction(evt)
        except Exception as e:
            traceback.print_exc()
            #print(e, file=sys.stderr)

