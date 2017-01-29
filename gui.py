"""
#Determine how to Identify The following: -- HIGHEST PRIORITY
#Register 
    Scan Lab Registers for open ports, find similarities
#Network Printer
#Tablet
    Scan Lab Tablet for open ports. Research Standard android ports open
#Verifone
    Scan Lab Verifone for open ports.

#unmanaged Switch(s) -- May not be possible.

One way is to list the mac address table on the managed switches
and look for ports with multiple mac addresses with are not links
to other known switches. Then, using arp lookup and ping -a, you
can find the ip address/dns names of the hosts connected to the
unmanaged switches.


#Create Custom Header Renderer to change appearance. -- LOW

"""

import wx
import wx.lib.agw.ultimatelistctrl as ULC
import scan

########################################################################
class GUI(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Network Analyzer")
        self.window = wx.GetActiveWindow()
        self.scan = scan.ScanNetwork(20)                                                        #Init scanNetwork class, 10 threads

        self.SetSize(1200,900)                                                                  #Set window size
        self.Centre()     
        self.version = '0.0.2'    

        self.ipFont = wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL)      
        self.detailedFont = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.InsertCount = 0
        self.currentSelection = None
        

        #Theme Pastel
        self.lightTan = (221,216,184)
        self.deepPurple = (84,46,113)
        self.lightBlue = (132,169,192)
        self.lightPurple = (106,102,163) 

        #Theme Brink
        self.lightOrange = (226,130,113) 
        self.darkGrey = (61,62,67)
        self.darkBlack = (41,42,47)
        self.brinkBlue = (36,118,185)
        self.lightGrey = (238,238,238)                                                                  
        self.white = (255,255,255)

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
        scanPortsMenuItem = scanMenu.Append(wx.ID_ANY, 'Scan Open Ports')
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
        self.Bind(wx.EVT_MENU, self.ScanOpenPortsOnTargetIP, scanPortsMenuItem)
        #self.Bind(wx.EVT_MENU, self.DisplayVersion, versionMenu)                            #Bind version display function to menu click event
 
        # Create Panels for viewports
        panel = wx.Panel(self, wx.ID_ANY, pos=(0,0), size=(200,863))                            #Panel to contain listctrl ipULC
        panel2 = wx.Panel(self, wx.ID_ANY, pos=(200,0), size=(990,863))                         #Panel to contain listctrl detailedListControl
        
 
        #Add List Control Class to IP Viewport#
        self.ipULC = ULC.UltimateListCtrl(panel, wx.ID_ANY, size=(200,863),
                                        agwStyle=wx.LC_REPORT|
                                                wx.LC_VRULES|
                                                wx.LC_SINGLE_SEL|
                                                wx.BORDER_NONE)

        #Add List Control Class to Detailed Viewport#
        self.detailedULC = ULC.UltimateListCtrl(panel2, wx.ID_ANY, size=(990,863),
                                                agwStyle=wx.LC_REPORT|
                                                        wx.LC_VRULES|
                                                        wx.LC_SINGLE_SEL|
                                                        ULC.ULC_NO_HIGHLIGHT|
                                                        wx.BORDER_NONE)

        #Configure IP Viewport#
        self.ipULC.InsertColumn(0, 'Discovered')
        self.ipULC.SetColumnWidth(0, 200)
        self.ipULC.SetBackgroundColour(self.darkBlack)
        self.ipULC.SetTextColour(self.brinkBlue)
        self.ipULC.SetScrollbar(0,0,0,0, refresh=False)
        self.ipULC.SetFont(self.ipFont)
        self.ipULC.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnIPListClick)



        #Configure Detailed Viewport# 
        self.detailedULC.InsertColumn(0, 'Detailed Information ')
        self.detailedULC.SetColumnWidth(0, 990)
        self.detailedULC.SetBackgroundColour(self.darkGrey)
        self.detailedULC.SetTextColour(self.lightOrange)
        self.detailedULC.SetFont(self.detailedFont)
        
        #for i in range(0,15):
        #    self.AddToListCtrl(self.detailedULC, 0, "192.168.1." + str(i))

        #Ultimate List Control Test

       
        #self.list.SetPalette(7)


 
    ##BEGIN FUNCTIONS##
    

    #----------------------------------------------------------------------
    def add_line(self, event):
        line = "Line %s" % self.index
        self.ipULC.InsertStringItem(self.index, line)
        self.ipULC.SetStringItem(self.index, 1, "01/19/2010")
        self.ipULC.SetStringItem(self.index, 2, "USA")
        self.index += 1

    #----------------------------------------------------------------------
    def OnIPListClick(self, event):
        self.currentSelection = event.GetIndex()
        for i in range(0, self.InsertCount):
            if(self.InsertCount > 0):
                #print("Deleting Item Index {}".f`ormat(i))
                self.detailedULC.DeleteItem(i)
                self.InsertCount -= 1

        self.AddToListCtrl(self.detailedULC, self.InsertCount, self.scan._Get_Ping_Statistics(event.GetIndex()))
        self.InsertCount += 1
        self.currentSelection = event.GetText()
        #self.detailedULC.InsertStringItem(self.detailedIndex, self.scan._Get_Ping_Statistics(event.GetIndex()))

    #----------------------------------------------------------------------
    #
    def AddToListCtrl(self, listctrl, position, item):
        TempListCtrl = listctrl
        TempItem = item
        TempPosition = position

        TempListCtrl.InsertStringItem(TempPosition, TempItem)

        TempListCtrl = None
        TempItem = None
        TempPosition = None

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
            self.AddToListCtrl(self.ipULC, activeIP, self.scan.activeIPList[activeIP])
            

    #----------------------------------------------------------------------
    def ScanOpenPortsOnTargetIP(self, event):

        for currentPort in range(0, 1024):
            #print("{} CURRENT PORT".format(currentPort))
            self.scan.primaryQueue.put(lambda ipaddress = self.currentSelection, currentPort = currentPort: self.scan._Scan_IP_Port(ipaddress, currentPort))

        self.AddToListCtrl(self.detailedULC, self.InsertCount, "Current Open Ports")
        self.InsertCount += 1

        self.scan._startScan()
        self.scan.primaryQueue.join() #wait until all IPs have been scanned on port, port.

        #Add all entries into detailed view list
        for ports in range(0, self.scan._get_Open_Ports_Size()):
            self.AddToListCtrl(self.detailedULC, self.InsertCount, self.scan._get_Open_Ports(ports))
            self.InsertCount += 1

        

    #----------------------------------------------------------------------
    #Function may not be needed
    def DisplayHelp(self, event):
        self.Close()

    #----------------------------------------------------------------------
    #Function may not be needed
    def DisplayVersion(self, event):
        self.Close() 
 
#----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = GUI()
    frame.Show()
    app.MainLoop()