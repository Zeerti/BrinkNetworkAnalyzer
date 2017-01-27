import wx

APP_EXIT = 1

class Example(wx.Frame):

	def __init__(self, *args, **kwargs):
		super(Example, self).__init__(*args, **kwargs)

		self.InitUI() #Function to Start UI

	def InitUI(self):
		
		menubar = wx.MenuBar()
		fileMenu = wx.Menu() #pop up or pulldown list of items for the MenuBar
		viewMenu = wx.Menu()

		self.shst = viewMenu.Append(wx.ID_ANY, 'Show statusbar',
			'Show Statusbar', kind=wx.ITEM_CHECK)
		self.shtl = viewMenu.Append(wx.ID_ANY, 'Show toolbar',
			'Show Toolbar', kind=wx.ITEM_CHECK)

		viewMenu.Check(self.shtl.GetId(), True)
		viewMenu.Check(self.shst.GetId(), True)



		fileMenu.Append(wx.ID_NEW, '&New')
		fileMenu.Append(wx.ID_OPEN, '&Open')
		fileMenu.Append(wx.ID_SAVE, '&Save')
		fileMenu.AppendSeparator()

		imp = wx.Menu()
		imp.Append(wx.ID_ANY, 'Import newsfeed list...')
		imp.Append(wx.ID_ANY, 'Import bookmarks...')
		imp.Append(wx.ID_ANY, 'Import mail...')

		fileMenu.AppendMenu(wx.ID_ANY, 'I&mport', imp)

		qmi = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit\tAlt+F4')
		fileMenu.Append(qmi)

		
		self.Bind(wx.EVT_MENU, self.OnQuit, qmi)

		menubar.Append(fileMenu, '&File')
		menubar.Append(viewMenu, 'View')
		self.SetMenuBar(menubar)

		#Create list view
		ipList = wx.ListCtrl()




		self.SetSize((600,450))
		self.SetTitle('submenu')
		self.Centre()
		self.Show(True)

	def OnQuit(self, event):
		self.Close()

def main():
	ex = wx.App()
	Example(None)
	ex.MainLoop()


if __name__ == '__main__':
	main()