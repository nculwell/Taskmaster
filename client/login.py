#!/usr/bin/python3
# vim: et ts=8 sts=4 sw=4

import wx
import base
import re

LABEL_WIDTH = 200

class LoginActivity(base.Activity):

    def __init__(self, parent, id = wx.ID_ANY):
        base.Activity.__init__(self, parent, id)

    def Construct(self):
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(0, 0, 1) # stretchable empty space

        headingText = wx.StaticText(self, -1, "TIME TO LOG IN",
                style=wx.ALIGN_CENTRE_HORIZONTAL|wx.ST_NO_AUTORESIZE)
        headingText.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        #headingText.SetSize(headingText.GetBestSize())
        box.Add(headingText, 0, wx.ALL|wx.EXPAND, 0)

        horz = wx.BoxSizer(wx.HORIZONTAL)
        lblUsername = wx.StaticText(self, -1, "Username:", style=wx.ST_NO_AUTORESIZE)
        lblUsername.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        #lblUsername.SetSize(lblUsername.GetBestSize())
        #lblUsername.SetSize(LABEL_WIDTH, lblUsername.GetSize().height)
        horz.Add(lblUsername, 0, wx.ALL, 0)
        txtUsername = wx.TextCtrl(self, validator=UsernameValidator())
        horz.Add(txtUsername, 1, wx.ALL, 0)
        box.Add(horz, 0, wx.ALL|wx.EXPAND, 0)

        horz = wx.BoxSizer(wx.HORIZONTAL)
        lblPassword = wx.StaticText(self, -1, "Password:", style=wx.ST_NO_AUTORESIZE|wx.TE_PASSWORD)
        lblPassword.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        #lblPassword.SetSize(lblPassword.GetBestSize())
        #lblPassword.SetSize(LABEL_WIDTH, lblPassword.GetSize().height)
        horz.Add(lblPassword, 0, wx.ALL, 0)
        txtPassword = wx.TextCtrl(self, validator=PasswordValidator())
        horz.Add(txtPassword, 1, wx.ALL, 0)
        box.Add(horz, 0, wx.ALL|wx.EXPAND, 0)

        box.Add(0, 0, 1) # stretchable empty space
        self.SetSizer(box)
    
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

