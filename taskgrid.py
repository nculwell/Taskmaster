#!/usr/bin/python

import wx, wx.grid

class TaskGrid(wx.grid.Grid):
    def __init__(self, parent, data = {}, id = wx.ID_ANY):
        wx.grid.Grid.__init__(self, parent, id=id, size=(400,300))
        try:
            self.CreateGrid(0, 3)
            self.AutoSizeRows()
            self.HideRowLabels()
            self.SetColLabelValue(0, "ID")
            self.SetColLabelValue(1, "Type")
            self.SetColLabelValue(2, "Title")
            self.AutoSizeColumns()
            self.SetColSize(2, 120)

            self.DisableCellEditControl()
            self.DisableDragColMove()
            self.DisableDragColSize()
            self.DisableDragGridSize()
            self.DisableDragRowSize()

            self.DisableRowResize(0)
            self.DisableColResize(0)

            for dataRow in data:
                self.InsertRow(dataRow)

            #self.SetCellValue(3, 3, "green on gray")
            #self.SetCellTextColour(3, 3, wx.GREEN)
            #self.SetCellBackgroundColour(3, 3, wx.LIGHT_GREY)

        except Exception as e:
            print(e)

    def UpdateRow(self, index, rowData):
        self.SetCellValue(index, 0, rowData["id"])
        self.SetCellValue(index, 1, rowData["type"])
        self.SetCellValue(index, 2, rowData["title"])

    def InsertRow(self, rowData, index = -1):
        locker = wx.grid.GridUpdateLocker(self)
        newRowIndex = self.GetNumberRows()
        if index > newRowIndex:
            raise Exception("Inserted row index is greater than row count.")
        self.AppendRows(1)
        for c in range(self.GetNumberCols()):
            self.SetReadOnly(newRowIndex, c)
        self.UpdateRow(newRowIndex, rowData)
        if index >= 0 and index < newRowIndex:
            self.MoveRow(newRowIndex, index)

    def MoveRow(self, fromIndex, toIndex):
        pass # TODO

