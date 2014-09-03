import os,glob,sys, subprocess, shlex, re
import xdg.Menu
import xdg.DesktopEntry
import xdg.IconTheme
from PyQt5 import QtCore

class Core(QtCore.QThread):
	def __init__(self):
		QtCore.QThread.__init__(self)

		self.allApps = {}
		self.results = []
		self.gui = None
		self.paths=(	"/usr/share/applications/",
						os.path.expanduser("~/.local/share/applications/"),
						os.path.expanduser("~/Desktop/")
					)
	def run(self):
		self.scan()

	def scan(self):
		print("scan started....")
		for path in self.paths:
			for entry in glob.glob(path+"/*.desktop"):
				try:
					a = self._getAppFromDesktopFile(entry)
					icon = xdg.IconTheme.getIconPath(a.getIcon())
					if icon is None:
						icon = xdg.IconTheme.getIconPath("applications-other")
					app = AppEntry(a.getName(),icon,a.getExec())
					self.allApps[self.buildIndexString(a)] = app
				except xdg.Exceptions.ParsingError:
					print("Desktop-File: " + entry + " is corrupted")
		print("scan finished.")


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
		app.command.start()
		
		
class Command(QtCore.QThread):
	def __init__(self, string):
		QtCore.QThread.__init__(self)
		self.originalString = string
	
	def _parse(self):
		command = re.sub("%.?", "", self.originalString)	# remove field codes
		return shlex.split(command)
	def run(self):
		commandWithArgs = self._parse()
		p = subprocess.Popen(commandWithArgs)
		p.wait()


class AppEntry():
	def __init__(self, name, icon, command):
		self.name = name
		self.icon = icon
		self.command = Command(command)
