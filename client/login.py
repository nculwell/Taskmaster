#!/usr/bin/python3
# vim: et ts=8 sts=4 sw=4

import wx, wx.lib.newevent
import sys, re, traceback, urllib, urllib.error
from . import base, net, color

LABEL_WIDTH = 200

LoginEvent, EVT_LOGIN = wx.lib.newevent.NewEvent()

class LoginActivity(base.Activity):

    def __init__(self, parent, id = wx.ID_ANY, onLogin = None):
        self.LoginSuccess = onLogin
        base.Activity.__init__(self, parent, id)

    def Construct(self):
        self.Bind(EVT_LOGIN, self.LoginSuccess)
        
        box = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(box)
        box.Add(0, 0, 1) # stretchable empty space

        headingText = wx.StaticText(self, -1, "PLEASE LOG IN",
                style=wx.ALIGN_CENTRE_HORIZONTAL|wx.ST_NO_AUTORESIZE)
        headingText.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        box.Add(headingText, 0, wx.ALL|wx.EXPAND)

        formFields = (
            { 'name': 'username', 'label': 'Username', 'value': 'njc' },
            { 'name': 'password', 'label': 'Password', 'password': True },
        )
        self.form = base.Form(self, fields=formFields)
        box.Add(self.form, 0, wx.ALL|wx.EXPAND, 10)

        submitButton = wx.Button(self, wx.ID_ANY, "Log in")
        submitButton.Bind(wx.EVT_BUTTON, self.OnLogin)
        submitButton.SetDefault()
        box.Add(submitButton, 0, wx.ALL|wx.CENTER, 10)

        self.errMsg = wx.StaticText(self, wx.ID_ANY, '')
        self.errMsg.SetForegroundColour(color.ERRMSG)
        box.Add(self.errMsg, 0, wx.ALL|wx.CENTER, 10)

        box.Add(0, 0, 1) # stretchable empty space

    def UpdateRow(self, index, task):
        self.SetCellValue(index, 0, task.id)
        self.SetCellValue(index, 1, task.type)
        self.SetCellValue(index, 2, task.title)

    def InsertRow(self, task, index = -1):
        locker = wx.grid.GridUpdateLocker(self)
        newRowIndex = self.GetNumberRows()
        if index > newRowIndex:
            raise Exception("Inserted row index is greater than row count.")
        self.AppendRows(1)
        for c in range(self.GetNumberCols()):
            self.SetReadOnly(newRowIndex, c)
        self.UpdateRow(newRowIndex, task)
        if index >= 0 and index < newRowIndex:
            self.MoveRow(newRowIndex, index)

    def MoveRow(self, fromIndex, toIndex):
        pass # TODO

    def OnLogin(self, event):
        username = self.form.fields['username'].GetText()
        password = self.form.fields['password'].GetText()
        if username == '':
            return
        try:
            loginUsr = net.Login(username, password)
            #print("LOGIN: %s, %s. RESPONSE: %s" % (username, password, loginUsr), file=sys.stderr)
            wx.PostEvent(self, LoginEvent(usr=loginUsr))
        except urllib.error.HTTPError as e:
            # urllib.error.HTTPError: HTTP Error 401: UNAUTHORIZED
            if str(e).startswith('HTTP Error 401:'):
                self.LoginFailure("Bad username/password.")
            else:
                traceback.print_exc()
                self.LoginFailure(str(e))
        except Exception as e:
            traceback.print_exc()
            self.LoginFailure(str(e))

    def LoginFailure(self, message=''):
        self.errMsg.SetLabelText("LOGIN FAILED" if message=='' else message)
        self.GetParent().Layout()

class UsernameValidator(wx.Validator):
    def __init__(self):
        # TODO: Save control or function that should be used to display error message.
        wx.Validator.__init__(self)
    def Validate(self, parent):
        value = self.GetWindow().GetLineText(0)
        valid = (None != re.fullmatch("[A-Za-z]+", value))
        # TODO: Display error message
        return valid

class PasswordValidator(wx.Validator):
    def __init__(self):
        # TODO: Save control or function that should be used to display error message.
        wx.Validator.__init__(self)
    def Validate(self, parent):
        value = self.GetWindow().GetLineText(0)
        valid = len(value) > 1
        # TODO: Display error message
        return valid

