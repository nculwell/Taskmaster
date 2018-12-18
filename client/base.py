#!/usr/bin/python3
# vim: et ts=8 sts=4 sw=4

import wx, wx.html, wx.grid
import sys, os, traceback
import color

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

class Activity(wx.Panel):

    def __init__(self, parent, id=wx.ID_ANY):
        style = wx.BORDER_SIMPLE
        wx.Panel.__init__(self, parent, id, style=style)
        try:
            self.Construct()
        except Exception as e:
            traceback.print_exc()

    # Wrap event handlers so we can control exception logging.
    def Bind(self, event, handler, source=None, id=wx.ID_ANY, id2=wx.ID_ANY, logEvents=False):
        wx.Frame.Bind(self, event, EventHandlerWrapper(handler, logEvents), source, id, id2)

class Form(wx.Panel):

    def __init__(self, parent, id=wx.ID_ANY, fields=()):
        wx.Panel.__init__(self, parent, id=id, style=wx.BORDER_NONE)
        try:
            self.Construct(fields)
        except Exception as e:
            traceback.print_exc()

    def Construct(self, fields):
        fgs = wx.FlexGridSizer(cols=3, hgap=5, vgap=5)
        fgs.AddGrowableCol(idx=1, proportion=6)
        fgs.AddGrowableCol(idx=2, proportion=1)
        errMsgFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
        i=0
        self.fields = {}
        for field in fields:
            i = i + 1
            fieldName = field['name']
            labelValue = field['label']
            entryValue = field.get('value', '')
            validator = field.get('validator')
            label = wx.StaticText(self, -1, labelValue + ':')
            teStyle = 0
            if field.get('password', False):
                teStyle = wx.TE_PASSWORD
            if validator == None:
                entry = wx.TextCtrl(self, value=entryValue, style=teStyle)
            else:
                entry = wx.TextCtrl(self, value=entryValue, style=teStyle, validator=validator)
            errMsg = wx.StaticText(self, -1, '')
            errMsg.SetForegroundColour(color.ERRMSG)
            addFlag = wx.ALL|wx.ALIGN_CENTER_VERTICAL
            fgs.Add(label, flag=addFlag)
            fgs.Add(entry, flag=addFlag|wx.EXPAND)
            fgs.Add(errMsg, flag=addFlag)
            self.fields[fieldName] = FormField(fieldName, entry, errMsg)
        self.SetSizer(fgs)

    # Wrap event handlers so we can control exception logging.
    def Bind(self, event, handler, source=None, id=wx.ID_ANY, id2=wx.ID_ANY, logEvents=False):
        wx.Frame.Bind(self, event, EventHandlerWrapper(handler, logEvents), source, id, id2)

class FormField:

    def __init__(self, name, textCtrl, errMsgText):
        assert isinstance(name, str)
        assert isinstance(textCtrl, wx.TextCtrl)
        assert isinstance(errMsgText, wx.StaticText)
        self.name = name
        self.textCtrl = textCtrl
        self.errMsgText = errMsgText

    def GetText(self):
        return '\n'.join(self.GetTextLines())

    def GetTextLines(self):
        tc = self.textCtrl
        lines = [ tc.GetLineText(ln) for ln in range(tc.GetNumberOfLines()) ]
        return lines

    def ClearErrorMessage(self):
        self.errMsgText.SetLabelText('')

    def SetErrorMessage(self, message):
        assert isinstance(message, str)
        self.errMsgText.SetLabelText(message)

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

