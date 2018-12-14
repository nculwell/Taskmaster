#!/usr/bin/python3
# vim: et ts=4 sts=4 sw=4 smartindent

import wx, wx.html, wx.grid
import sys
from taskgrid import TaskGrid

aboutText = """
<p>Sorry, there is no information about this program.</p>
<p>It is running on version %(wxpy)s of <b>wxPython</b> and %(python)s of <b>Python</b>.</p>
"""

userFullName = "Nathan Culwell-Kanarek [12345]"

class HtmlWindow(wx.html.HtmlWindow):
    def __init__(self, parent, id, size=(600,400)):
        wx.html.HtmlWindow.__init__(self,parent, id, size=size)
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()

    def OnLinkClicked(self, link):
        wx.LaunchDefaultBrowser(link.GetHref())

class AboutBox(wx.Dialog):
    def __init__(self, applicationName):
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

class MainFrame(wx.Frame):
    def __init__(self, applicationName, initialTasks):
        try:
            wx.Frame.__init__(self, None, title=applicationName) # , pos=(150,150), size=(350,200))
            self.Bind(wx.EVT_CLOSE, self.OnClose)
            self.applicationName = applicationName

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

            header = self.BuildHeader(panel)
            box.Add(header, 0, wx.ALL, 10)

            m_close = wx.Button(panel, wx.ID_CLOSE, "Close")
            m_close.Bind(wx.EVT_BUTTON, self.OnClose)
            box.Add(m_close, 0, wx.ALL, 10)

            self.grid = TaskGrid(panel, tasks=initialTasks)
            box.Add(self.grid, 1, wx.ALL|wx.EXPAND, 10)

            panel.SetSizer(box)
            panel.Layout()

        except Exception as e:
            print(e)

    def BuildHeader(self, panel):
        box = wx.BoxSizer(wx.HORIZONTAL)
        usernameText = wx.StaticText(panel, -1, userFullName)
        usernameText.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        usernameText.SetSize(usernameText.GetBestSize())
        box.Add(usernameText, 0, wx.ALL, 10)
        return box

    def OnClose(self, event):
        dlg = wx.MessageDialog(self, 
            "Do you really want to close this application?",
            "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()

    def OnAbout(self, event):
        dlg = AboutBox(self.applicationName)
        dlg.ShowModal()
        dlg.Destroy()  

