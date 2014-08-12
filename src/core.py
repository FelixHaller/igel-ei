import sys, subprocess
import xdg.Menu
import xdg.DesktopEntry
import xdg.IconTheme
from PyQt5 import QtCore

class Core(QtCore.QThread):
	def __init__(self, gui):
		QtCore.QThread.__init__(self)
		
		self.allApps = {}
		self.results = []
		self.gui = gui
		
	def run(self):
		self.buildDict(xdg.Menu.parse())
	def buildDict(self, menu):
		for entry in menu.getEntries():
			if isinstance(entry, xdg.Menu.Menu):
				self.buildDict(entry)
			elif isinstance(entry, xdg.Menu.MenuEntry):
				icon = xdg.IconTheme.getIconPath(entry.DesktopEntry.getIcon())
				if icon is None:
					icon = xdg.IconTheme.getIconPath("applications-other")
				app = App(entry.DesktopEntry.getName(),icon,entry.DesktopEntry.getExec())
				self.allApps[self.buildIndexString(entry)] = app
				
				
	
	def buildIndexString(self, entry):
		indexString = entry.DesktopEntry.getName() + " " + entry.DesktopEntry.getGenericName() + " " + entry.DesktopEntry.getComment()
		return indexString
		
	def searchApp(self, query):
		self.results = []
		for entry in self.allApps:
			if query.lower() in entry.lower():
				self.results.append(self.allApps[entry])
		return self.results
	def launchApp(self, appIndex):
		app = self.results[appIndex]
		print("starte: " + app.name)
		#subprocess.Popen(['nohup', app.command.split(" ")[0]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		subprocess.Popen(app.command.split(" ")[0], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		sys.exit(0)

class App():
	def __init__(self, name, icon, command):
		self.name = name
		self.icon = icon
		self.command = command
		
