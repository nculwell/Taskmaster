#!/usr/bin/python3
# vim: et ts=4 sts=4 sw=4 smartindent

import wx, wx.html, wx.grid
import sys, os, traceback

class Dialog(wx.Dialog):

    def __init__(self, parent, title,
            pos=wx.DefaultPosition, size=wx.DefaultSize):
        style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.TAB_TRAVERSAL
        wx.Dialog.__init__(self, parent,
                title=title, style=style, pos=pos, size=size)

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

    def DispatchUrl(self, url):
        if parent != None:
            parent.DispatchUrl(url)
        else:
            # MainFrame should override this to do the work.
            print("ERROR: DispatchUrl not implemented.", file=sys.stderr)

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

