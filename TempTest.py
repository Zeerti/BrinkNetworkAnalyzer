import wx

########################################################################
class GUI(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "List Control Tutorial")
 
        # Create Panels for viewports
        panel = wx.Panel(self, wx.ID_ANY, pos=(0,0), size=(200,863))
        panel2 = wx.Panel(self, wx.ID_ANY, pos=(201,0), size=(990,863))

        self.ipFont = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self.detailedFont = wx.Font(14, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self.index = 0
        self.SetSize(1200,900)
        self.Centre()

        self.lightTan = (221,216,184)
        self.deepPurple = (84,46,113)
        self.lightBlue = (132,169,192)
        self.lightPurple = (106,102,163)
 
        #Add List Control Class to IP Viewport
        self.ipListControl = wx.ListCtrl(panel, size=(200,863),
                         style=wx.LC_REPORT
                         |wx.BORDER_NONE)

        #Add List Control Class to Detailed Viewport
        self.detailedListControl = wx.ListCtrl(panel2, size=(990,863),
                         style=wx.LC_REPORT
                         |wx.BORDER_NONE)

        #Configure IP Viewport
        self.ipListControl.InsertColumn(0, 'Discovered')
        self.ipListControl.SetColumnWidth(0, 200)
        self.ipListControl.SetBackgroundColour(self.lightBlue)
        self.ipListControl.SetTextColour(self.deepPurple)
        for i in range(0,15):
            self.ipListControl.InsertItem(0, "192.168.1." + str(i))
        self.ipListControl.SetFont(self.ipFont)
        self.ipListControl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnClick)
        self.ipListControl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnClick)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnClick, self.ipListControl)


        #Configure Detailed Viewport 
        self.detailedListControl.InsertColumn(1, 'Detailed Information ')
        self.detailedListControl.SetColumnWidth(0, 990)
        self.detailedListControl.SetBackgroundColour(self.lightPurple)
        self.detailedListControl.SetTextColour(self.lightTan)
        self.detailedListControl.SetFont(self.detailedFont)
        for i in range(0,15):
            self.detailedListControl.InsertItem(0, "192.168.1." + str(i))
        

        

 
        btn = wx.Button(panel, label="Add Line")
        btn.Bind(wx.EVT_BUTTON, self.add_line)
 
    
 
    #----------------------------------------------------------------------
    def add_line(self, event):
        line = "Line %s" % self.index
        self.ipListControl.InsertStringItem(self.index, line)
        self.ipListControl.SetStringItem(self.index, 1, "01/19/2010")
        self.ipListControl.SetStringItem(self.index, 2, "USA")
        self.index += 1

    #----------------------------------------------------------------------
    def OnClick(self, event):
        print(event.GetText())
        #Insert code to change other table here.
 
#----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = GUI()
    frame.Show()
    app.MainLoop()