import wx
import scan

########################################################################
class GUI(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Network Analyzer")

        self.scan = scan.ScanNetwork(10)                                                        #Init scanNetwork class, 10 threads

        self.SetSize(1200,900)                                                                  #Set window size
        self.Centre()     
        self.version = '0.0.2'    

        self.ipFont = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)      
        self.detailedFont = wx.Font(14, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self.index = 0
        


        self.lightTan = (221,216,184)
        self.deepPurple = (84,46,113)
        self.lightBlue = (132,169,192)
        self.lightPurple = (106,102,163)                                                                  #Center window on display

        #Create Menu Bar
        menubar = wx.MenuBar()                                                                  #Parent Menu Viewport

        fileMenu = wx.Menu()                                                                    #Actual Visible Menu Object Displayed as File
        quitMenuItem = fileMenu.Append(wx.ID_EXIT, 'Quit\tCtrl+Q', 'Quit application')          #The actual clickable menu object in GUI
        menubar.Append(fileMenu, '&File')                                                       #Add fileMenu to visible menu Parent, menubar

        scanMenu = wx.Menu()
        scanMenuItem = scanMenu.Append(wx.ID_ANY, 'Scan All\tCtrl+S',
                                                  'Scan The Network!')

        scanIPOnlyMenuItem = scanMenu.Append(wx.ID_ANY, 'Scan IP\tCtrl+I',
                                                        'Scan Only for IP Addresses')
        menubar.Append(scanMenu, '&Scan')


        helpMenu = wx.Menu()
        helpMenuItem = helpMenu.Append(wx.ID_ANY, 'Help', 'Having Problems?')
        menubar.Append(helpMenu, '&Help')

        versionMenu = wx.Menu()
        versionMenu.Append(wx.ID_ANY, self.version)
        helpMenu.Append(wx.ID_ANY, '&Version', versionMenu)



        self.SetMenuBar(menubar)                                                                #Add parent menu object to parent frame

        self.Bind(wx.EVT_MENU, self.OnQuit, quitMenuItem)                                       #Bind quit function to menu click event
        self.Bind(wx.EVT_MENU, self.ScanNetwork, scanMenuItem)                                  #Bind scan function to menu click event
        self.Bind(wx.EVT_MENU, self.DisplayHelp, helpMenuItem)                                  #Bind help display function to menu click event
        #self.Bind(wx.EVT_MENU, self.DisplayVersion, versionMenu)                            #Bind version display function to menu click event
 
        # Create Panels for viewports
        panel = wx.Panel(self, wx.ID_ANY, pos=(0,0), size=(200,863))                            #Panel to contain listctrl ipListControl
        panel2 = wx.Panel(self, wx.ID_ANY, pos=(201,0), size=(990,863))                         #Panel to contain listctrl detailedListControl
        
 
        #Add List Control Class to IP Viewport#
        self.ipListControl = wx.ListCtrl(panel, size=(200,863),
                         style=wx.LC_REPORT
                         |wx.BORDER_NONE)

        #Add List Control Class to Detailed Viewport#
        self.detailedListControl = wx.ListCtrl(panel2, size=(990,863),
                         style=wx.LC_REPORT
                         |wx.BORDER_NONE)

        #Configure IP Viewport#
        self.ipListControl.InsertColumn(0, 'Discovered')
        self.ipListControl.SetColumnWidth(0, 200)
        self.ipListControl.SetBackgroundColour(self.lightBlue)
        self.ipListControl.SetTextColour(self.deepPurple)
        #for i in range(0,15):
        #    self.AddToListCtrl(self.ipListControl, 0, "192.168.1." + str(i))
        self.ipListControl.SetFont(self.ipFont)
        self.ipListControl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnIPListClick)


        #Configure Detailed Viewport# 
        self.detailedListControl.InsertColumn(1, 'Detailed Information ')
        self.detailedListControl.SetColumnWidth(0, 990)
        self.detailedListControl.SetBackgroundColour(self.lightPurple)
        self.detailedListControl.SetTextColour(self.lightTan)
        self.detailedListControl.SetFont(self.detailedFont)
        #for i in range(0,15):
        #    self.AddToListCtrl(self.detailedListControl, 0, "192.168.1." + str(i))


 
    ##BEGIN FUNCTIONS##

    #----------------------------------------------------------------------
    def add_line(self, event):
        line = "Line %s" % self.index
        self.ipListControl.InsertStringItem(self.index, line)
        self.ipListControl.SetStringItem(self.index, 1, "01/19/2010")
        self.ipListControl.SetStringItem(self.index, 2, "USA")
        self.index += 1

    #----------------------------------------------------------------------
    def OnIPListClick(self, event):
        print(event.GetText())
        #Insert code to display 

    #----------------------------------------------------------------------
    #
    def AddToListCtrl(self, listctrl, column, item):
        TempListCtrl = listctrl
        TempColumn = column
        TempItem = item

        TempListCtrl.InsertItem(TempColumn, TempItem)

     #----------------------------------------------------------------------
    def OnQuit(self, event):
        self.Close()

    #----------------------------------------------------------------------
    def ScanNetwork(self, event):
        self.scan._get_IP_From_ARP_Table()
        for currentIP in range(self.scan._get_ipList_Size()): #Add Ping Function To queue
            self.scan.primaryQueue.put(lambda currentIP = currentIP: self.scan._get_Active_IP_Addresses(currentIP)) 

        self.scan._startScan() #Run Queue
        self.scan.primaryQueue.join() #Wait for queue to finish

        for activeIP in range(self.scan._get_active_ipList_Size()):
            self.AddToListCtrl(self.ipListControl, 0, self.scan.activeIPList[activeIP])


        

    #----------------------------------------------------------------------
    def DisplayHelp(self, event):
        self.Close()

    #----------------------------------------------------------------------
    def DisplayVersion(self, event):
        self.Close()
 
#----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = GUI()
    frame.Show()
    app.MainLoop()