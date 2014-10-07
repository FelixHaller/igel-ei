import os, glob
import xdg.Exceptions
import xdg.DesktopEntry
import xdg.IconTheme
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
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
		

	def activate(self):
		super().activate()
		print("Desktop Files!")
		self.app.registerScannerPlugin(self)
		
		self.scanner = Scanner()
		self.scanner.appfound.connect(self.app.addAppEntry)
		

	def deactivate(self):
		print("GoodBye Desktop Files!")
		super().deactivate()
	
	def scan(self):
		self.scanner.start()
		

class Scanner(QThread):
	appfound = pyqtSignal([AppEntry])
	
	def __init__(self):
		QThread.__init__(self)
		self.paths = []
		self.setScanTargets()
		
	
	def setScanTargets(self):
		pathsRec = ("/usr/share/applications/","~/.local/share/applications/") # recursive scanning paths
		paths = ("~/Desktop/",)
		
		for path in pathsRec:
			for p,d,f in os.walk(os.path.expanduser(path)):
				self.paths.append(p)
		for path in paths:
			self.paths.append(os.path.expanduser(path))
		
	def run(self):
		
		print("scan started....")
		for path in self.paths:
			self._scanFolderForFiles(path)
		print("scan finished.")

	def _scanFolderForFiles(self, path):
		iconManager = IconManager()
		for entry in glob.glob(path+"/*.desktop"):
			try:
				desktopEntry = self._getAppFromDesktopFile(entry)
			except xdg.Exceptions.ParsingError:
				print("Desktop-File: " + entry + " is corrupted")
			else:
				appEntry = AppEntry(desktopEntry.getName(), desktopEntry.getExec())

				icon = iconManager.getIconPath(desktopEntry.getIcon())
					
				appEntry.icon = icon
				appEntry.genericName = desktopEntry.getGenericName()
				appEntry.comment = desktopEntry.getComment()
				
				
				self.appfound.emit(appEntry)
	
	def _getAppFromDesktopFile(self, desktopFile):
		return(xdg.DesktopEntry.DesktopEntry(desktopFile))
		
class IconManager():
	
	GNOME_SESSIONS=["mate", "unity", "gnome", "cinnamon"]
	'''
	This class is to deliver an icon for an app because there are some hacks 
	needed to always deliver an Icon for every app.
	
	I'm not sure about that class. If someone knows a better way, please tell me.
	
	http://stackoverflow.com/questions/997904/system-theme-icons-and-pyqt4
	
	
	'''
		
	def isThemeAvailable(self):
		'''Is there a theme available to use with PyQt'''
		return (QIcon.themeName() != "")
		
	
	def isDesktopGnomish(self):
		'''Returns if the desktop is gnome or similar to it.'''
		try:
			from gi.repository.Gtk import IconTheme
		except ImportError:
			return False
		return os.environ.get("DESKTOP_SESSION") in self.GNOME_SESSIONS
		
	def getIconPath(self, iconName :str):
		if self.isThemeAvailable():
			if (QIcon.hasThemeIcon()):
				return QIcon.fromTheme(iconName)
		if self.isDesktopGnomish():
			from gi.repository.Gtk import IconTheme
			icon_theme = IconTheme.get_default()
			icon_info = icon_theme.lookup_icon(iconName, 48, 0)
			if icon_info is not None:
				return icon_info.get_filename()
		icon = xdg.IconTheme.getIconPath(iconName)
		if icon is not None:
			return icon
		else:
			return xdg.IconTheme.getIconPath("applications-other")
