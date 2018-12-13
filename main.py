#!/usr/bin/python
# -*- coding: <<encoding>> -*-
#-------------------------------------------------------------------------------
#   <<project>>
# 
#-------------------------------------------------------------------------------

#import wxversion
#wxversion.select("2.8")
import wx, wx.html, wx.grid
import sys

applicationName = "TaskMaster"

aboutText = """<p>Sorry, there is no information about this program.

It is running on version %(wxpy)s of <b>wxPython</b> and %(python)s of <b>Python</b>.

See <a href="http://wiki.wxpython.org">wxPython Wiki</a></p>""" 

initialData = [
    { "id": "1", "type": "A", "title": "First" },
    { "id": "2", "type": "B", "title": "Second" },
]

class HtmlWindow(wx.html.HtmlWindow):
    def __init__(self, parent, id, size=(600,400)):
        wx.html.HtmlWindow.__init__(self,parent, id, size=size)
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()

    def OnLinkClicked(self, link):
        wx.LaunchDefaultBrowser(link.GetHref())
        
class AboutBox(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, "About " + applicationName,
            style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.TAB_TRAVERSAL)
        hwin = HtmlWindow(self, -1, size=(400,200))
        vers = {}
        vers["python"] = sys.version.split()[0]
        vers["wxpy"] = wx.VERSION_STRING
        hwin.SetPage(aboutText % vers)
        btn = hwin.FindWindowById(wx.ID_OK)
        irep = hwin.GetInternalRepresentation()
        hwin.SetSize((irep.GetWidth()+25, irep.GetHeight()+10))
        self.SetClientSize(hwin.GetSize())
        self.CentreOnParent(wx.BOTH)
        self.SetFocus()

class TaskGrid(wx.grid.Grid):
    def __init__(self, parent, id=wx.ID_ANY):
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

            for d in initialData:
                self.InsertRow(d)

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

class Frame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title) # , pos=(150,150), size=(350,200))
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        menuBar = wx.MenuBar()
        menu = wx.Menu()
        m_exit = menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Close window and exit program.")
        self.Bind(wx.EVT_MENU, self.OnClose, m_exit)
        menuBar.Append(menu, "&File")
        menu = wx.Menu()
        m_about = menu.Append(wx.ID_ABOUT, "&About", "Information about this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, m_about)
        menuBar.Append(menu, "&Help")
        self.SetMenuBar(menuBar)
        
        self.statusbar = self.CreateStatusBar()

        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)
        
        m_text = wx.StaticText(panel, -1, "Hello World!")
        m_text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        m_text.SetSize(m_text.GetBestSize())
        box.Add(m_text, 0, wx.ALL, 10)
        
        m_close = wx.Button(panel, wx.ID_CLOSE, "Close")
        m_close.Bind(wx.EVT_BUTTON, self.OnClose)
        box.Add(m_close, 0, wx.ALL, 10)

        grid = TaskGrid(panel)
        box.Add(grid, 0, wx.ALL, 10)
        
        panel.SetSizer(box)
        panel.Layout()

    def OnClose(self, event):
        dlg = wx.MessageDialog(self, 
            "Do you really want to close this application?",
            "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()

    def OnAbout(self, event):
        dlg = AboutBox()
        dlg.ShowModal()
        dlg.Destroy()  

app = wx.App(redirect=True)   # Error messages go to popup window
top = Frame(applicationName)
top.Show()
app.MainLoop()
