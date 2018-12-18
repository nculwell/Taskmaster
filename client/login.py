#!/usr/bin/python3
# vim: et ts=8 sts=4 sw=4

import wx
import sys, re
import base, net, color

LABEL_WIDTH = 200

class LoginActivity(base.Activity):

    def __init__(self, parent, id = wx.ID_ANY):
        base.Activity.__init__(self, parent, id)

    def Construct(self):
        box = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(box)
        box.Add(0, 0, 1) # stretchable empty space

        headingText = wx.StaticText(self, -1, "TIME TO LOG IN",
                style=wx.ALIGN_CENTRE_HORIZONTAL|wx.ST_NO_AUTORESIZE)
        headingText.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        box.Add(headingText, 0, wx.ALL|wx.EXPAND)

        formFields = (
            { 'name': 'username', 'label': 'Username' },
            { 'name': 'password', 'label': 'Password', 'password': True },
        )
        self.form = base.Form(self, fields=formFields)
        box.Add(self.form, 0, wx.ALL|wx.EXPAND, 10)

        submitButton = wx.Button(self, wx.ID_ANY, "Log in")
        submitButton.Bind(wx.EVT_BUTTON, self.OnLogin)
        submitButton.SetDefault()
        box.Add(submitButton, 0, wx.ALL|wx.CENTER, 10)

        self.errMsg = wx.StaticText(self, wx.ID_ANY, "(ERROR)")
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
        response = net.Login(username, password)
        print("LOGIN: %s, %s. RESPONSE: %s" % (username, password, response), file=sys.stderr)
        if response.startswith("Welcome,"):
            self.LoginSuccess()
        else:
            self.LoginFailure()

    def LoginSuccess(self, username, password):
        parent.Login(username)

    def LoginFailure(self):
        self.errMsg.SetLabelText("LOGIN FAILED")

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

