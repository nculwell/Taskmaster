#!/usr/bin/python3

import wx, wx.dataview
from wx.dataview import *
import traceback

from . import task

class TaskGrid(wx.Panel):

    def __init__(self, parent, tasks = [], id = wx.ID_ANY):
        wx.Panel.__init__(self, parent, id=id)
        try:
            dvStyle = (DV_ROW_LINES
                    | DV_HORIZ_RULES)
            # FIXME: 'style' is invalid
            dv = DataViewListCtrl(style=dvStyle)
            self.dv = dv

            columnNames = ["ID", "Type", "Title"]
            addFlags = wx.TOP|wx.BOTTOM|wx.EXPAND|wx.ST_NO_AUTORESIZE
            for cName in columnNames:
                col = DataViewColumn(cName, renderer, model_column, align=wx.ALIGN_LEFT)
                self.fgs.Add(wx.StaticText(self, label=' '+c),
                        flag=addFlags, border=5)

            self.fields = []
            for task in tasks:
                self.InsertRow(task)

        except Exception as e:
            traceback.print_exc()

    def UpdateRow(self, index, task):
        row = self.fields[index]
        row[0].SetLabelText(task.id)
        row[1].SetLabelText(task.type)
        row[2].SetLabelText(task.title)

    def InsertRow(self, task, index=-1):
        newRowIndex = len(self.fields)
        if index > newRowIndex:
            raise Exception("Inserted row index is greater than row count.")
        def NewField():
            #f = wx.TextCtrl(self, style=wx.TE_READONLY)
            f = wx.StaticText(self, style=wx.BORDER_SIMPLE)
            return f
        row = [ NewField() for i in range(self.columnCount) ]
        self.fields.append(row)
        for field in row:
            self.fgs.Add(field, flag=wx.EXPAND|wx.ST_NO_AUTORESIZE)
        self.UpdateRow(newRowIndex, task)
        if index >= 0 and index < newRowIndex:
            self.MoveRow(newRowIndex, index)

    def MoveRow(self, fromIndex, toIndex):
        pass # TODO

