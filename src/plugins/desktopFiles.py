import time,os, glob, xdg
import xdg.DesktopEntry
import xdg.IconTheme
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtGui
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
		Icons()
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
		
class Icons():
	
	GNOME_SESSIONS=["mate", "unity", "gnome"]
	'''
	This class is to deliver an icon for an app because there are some hacks 
	needed to always deliver an Icon for every app.
	
	I'm not sure about that class. If someone knows a better way, please tell me.
	'''
	def __init__(self):
		#self.desktop = self.selectDesktop()
		
		if self.isThemeAvailable():
			print("Juhu")
		if self.isDesktopGnomish():
			print("yeah")
		
		
	def isThemeAvailable(self):
		'''Is there a theme available to use with PyQt'''
		return (QtGui.QIcon.themeName() != "")
		
	
	def isDesktopGnomish(self):
		'''
		Returns if the desktop is gnome or similar to it.
		'''
	
		return True
		
		#~ try:
			#~ from gi.repository import Gtk
		#~ except ImportError:
			#~ return False
		
		#~ return os.environ.get("DESKTOP_SESSION") in self.GNOME_SESSIONS
		
		
		
		
		
		
		
		
		
		
		
		
		
	
