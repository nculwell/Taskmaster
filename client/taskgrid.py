#!/usr/bin/python3

import wx, wx.grid
import traceback
from task import *

class TaskGrid(wx.Panel):

    def __init__(self, parent, tasks = [], id = wx.ID_ANY):
        wx.Panel.__init__(self, parent, id=id)
        try:
            self.columnCount = 3
            self.fgs = wx.FlexGridSizer(cols=self.columnCount)
            self.SetSizer(self.fgs)
            self.fgs.SetFlexibleDirection(wx.HORIZONTAL)
            self.fgs.AddGrowableCol(2, 1)

            columnNames = ["ID", "Type", "Title"]
            addFlags = wx.TOP|wx.BOTTOM|wx.EXPAND
            for c in columnNames:
                self.fgs.Add(wx.StaticText(self, label=' '+c),
                        flag=addFlags, border=5)

            self.fields = []
            for task in tasks:
                self.InsertRow(task)

        except Exception as e:
            traceback.print_exc()

    def UpdateRow(self, index, task):
        row = self.fields[index]
        row[0].SetValue(task.id)
        row[1].SetValue(task.type)
        row[2].SetValue(task.title)

    def InsertRow(self, task, index=-1):
        newRowIndex = len(self.fields)
        if index > newRowIndex:
            raise Exception("Inserted row index is greater than row count.")
        def NewField():
            f = wx.TextCtrl(self, style=wx.TE_READONLY)
            #f = wx.StaticText(self, style=wx.BORDER_SIMPLE)
            return f
        row = [ NewField() for i in range(self.columnCount) ]
        self.fields.append(row)
        for field in row:
            self.fgs.Add(field)
        self.UpdateRow(newRowIndex, task)
        if index >= 0 and index < newRowIndex:
            self.MoveRow(newRowIndex, index)

    def MoveRow(self, fromIndex, toIndex):
        pass # TODO

