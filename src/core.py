import os,glob,sys, subprocess
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
		self.paths=(	"/usr/share/applications/",
						os.path.expanduser("~/.local/share/applications/"),
						os.path.expanduser("~/Desktop/")
					)
	def run(self):
		for path in self.paths:			
			for entry in glob.glob(path+"/*.desktop"):
				try:
					a = self._getAppFromDesktopFile(entry)
					icon = xdg.IconTheme.getIconPath(a.getIcon())
					if icon is None:
						icon = xdg.IconTheme.getIconPath("applications-other")
					app = App(a.getName(),icon,a.getExec())
					self.allApps[self.buildIndexString(a)] = app
				except xdg.Exceptions.ParsingError:
					print("Desktop-File: " + entry + " is corrupted")
					pass
		
			
	def _getAppFromDesktopFile(self, desktopFile):
		return(xdg.DesktopEntry.DesktopEntry(desktopFile))
		
	def buildIndexString(self, entry):
		indexString = entry.getName() + " " + entry.getGenericName() + " " + entry.getComment()
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
		subprocess.Popen(app.command.split(" ")[0], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

class App():
	def __init__(self, name, icon, command):
		self.name = name
		self.icon = icon
		self.command = command
		
