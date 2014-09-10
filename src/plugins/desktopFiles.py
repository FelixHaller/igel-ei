import time,os, glob, xdg
from PyQt5.QtCore import QThread, pyqtSignal
from yapsy.PluginManager import PluginManagerSingleton

import plugins.plugin as plugin
from core import AppEntry


class DesktopFiles(plugin.Plugin):
	"""

	"""
	def __init__(self):
		# Make sure to call the parent class (`IPlugin`) methods when 
		# overriding them.
		super().__init__()

		# The `app` property was added to the manager singleton instance when
		# the manager was setup. See ExampleApp.__init__() in the 
		# yapsy-gtk-example.py file. 
		manager = PluginManagerSingleton.get()
		self.app = manager.app
		
		self.app.registerScannerPlugin(self)
		
		self.scanner = Scanner()
		self.scanner.appfound.connect(self.app.addAppEntry)
		

	def activate(self):
		super().activate()
		print("Desktop Files!")
		

	def deactivate(self):
		print("GoodBye Desktop Files!")
		super().deactivate()
	
	def scan(self):
		
		self.scanner.start()	
		

class Scanner(QThread):
	appfound = pyqtSignal([AppEntry])
	
	def __init__(self):
		QThread.__init__(self)
		self.paths=("/usr/share/applications/",
		     os.path.expanduser("~/.local/share/applications/"),
		     os.path.expanduser("~/Desktop/")
					)
		
		
	def run(self):
		print("scan started....")
		for path in self.paths:
			for entry in glob.glob(path+"/*.desktop"):
				try:
					desktopEntry = self._getAppFromDesktopFile(entry)
				except xdg.Exceptions.ParsingError:
					print("Desktop-File: " + entry + " is corrupted")
				else:
					appEntry = AppEntry(desktopEntry.getName(), desktopEntry.getExec())
					
					icon = xdg.IconTheme.getIconPath(desktopEntry.getIcon())
					if icon is None:
						icon = xdg.IconTheme.getIconPath("applications-other")
					appEntry.icon = icon
					appEntry.genericName = desktopEntry.getGenericName()
					appEntry.comment = desktopEntry.getComment()
					
					
					self.appfound.emit(appEntry)
		print("scan finished.")
	
	def _getAppFromDesktopFile(self, desktopFile):
		return(xdg.DesktopEntry.DesktopEntry(desktopFile))
