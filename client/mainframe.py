#!/usr/bin/python3
# vim: et ts=4 sts=4 sw=4 smartindent

import wx, wx.html, wx.grid
import sys, datetime
from taskgrid import TaskGrid
from login import LoginActivity
import defs, base

aboutText = """
<div>
<p>Sorry, there is no information about this program.</p>
<p>It is running on version %(wxpy)s of <b>wxPython</b> and %(python)s of <b>Python</b>.</p>
</div>
"""

class MainFrame(base.Frame):

    def __init__(self, initialTasks):
        try:
            self.initialTasks = initialTasks
            base.Frame.__init__(self, None, title=defs.AppName,
                    pos=(50,50), size=(700,500))
        except Exception as e:
            traceback.print_exc()

    def Construct(self):
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        menuBar = self.BuildMenuBar()
        self.SetMenuBar(menuBar)
        self.statusbar = self.CreateStatusBar()

        self.panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)

        header = self.BuildHeader()
        box.Add(header, 0, wx.ALL|wx.EXPAND, 10)

        #closeButton = wx.Button(self.panel, wx.ID_CLOSE, "Close")
        #closeButton.Bind(wx.EVT_BUTTON, self.OnClose)
        #box.Add(closeButton, 0, wx.ALL, 10)

        self.activity = None
        self.activitySizer = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.activitySizer, 1, wx.ALL|wx.EXPAND, 10)

        self.panel.SetSizer(box)
        self.LoadActivity(LoginActivity(self.panel))
        #self.LoadActivity(TaskGrid(self.panel, tasks=self.initialTasks))
        del self.initialTasks

    def LoadActivity(self, activity):
        if self.activity != None:
            self.activitySizer.Detach(self.activity)
        self.activity = activity
        self.activitySizer.Add(self.activity, 1, wx.ALL|wx.EXPAND, 0)
        self.panel.Layout()

    def BuildMenuBar(self):
        menuBar = wx.MenuBar()

        menu = wx.Menu()
        m_exit = menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Close window and exit program.")
        self.Bind(wx.EVT_MENU, self.OnClose, m_exit)
        menuBar.Append(menu, "&File")

        menu = wx.Menu()
        m_about = menu.Append(wx.ID_ABOUT, "&About", "Information about this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, m_about)
        menuBar.Append(menu, "&Help")

        return menuBar

    def BuildHeader(self):
        box = wx.BoxSizer(wx.HORIZONTAL)
        usernameText = wx.StaticText(self.panel, -1, defs.UserFullName)
        usernameText.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        usernameText.SetSize(usernameText.GetBestSize())
        box.Add(usernameText, 0, wx.ALL, 0)
        box.Add(0, 0, 1) # stretchable empty space
        todaysDate = datetime.datetime.today().strftime('%Y-%m-%d')
        dateText = wx.StaticText(self.panel, -1, todaysDate)
        dateText.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        dateText.SetSize(dateText.GetBestSize())
        box.Add(dateText, 0, wx.ALL, 0)
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
        dlg = AboutBox()
        dlg.ShowModal()
        dlg.Destroy()  

class HtmlWindow(wx.html.HtmlWindow):
    import urllib, urllib.parse

    def __init__(self, parent, size=(600,400)):
        wx.html.HtmlWindow.__init__(self, parent, size=size)
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()

    def OnLinkClicked(self, link):
        href = link.GetHref()
        url = urllib.parse.urlparse(href)
        if url.scheme == 'self':
            pass # TODO
        elif url.scheme in ['http', 'https', 'ftp']:
            wx.LaunchDefaultBrowser(href)
        else:
            parent.DispatchUrl(url)

class AboutBox(base.Dialog):

    def __init__(self):
        base.Dialog.__init__(self, None, "About " + defs.AppName)

    def Construct(self):
        hwin = HtmlWindow(self, size=(400,200))
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

