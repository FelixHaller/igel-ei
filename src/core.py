import os, glob, subprocess, shlex, re
import xdg.Menu
import xdg.DesktopEntry
import xdg.IconTheme
import random as r
from PyQt5 import QtCore

#from yapsy.ConfigurablePluginManager import ConfigurablePluginManager
#from yapsy.VersionedPluginManager import VersionedPluginManager
from yapsy.PluginManager import PluginManagerSingleton


class Core():
	def __init__(self):
		self.allApps = {}
		self.scanner = []
		self.results = []
		self.gui = None

					
		plugin_dir = os.path.join("plugins")
		places = [plugin_dir,]
		
		self.manager = PluginManagerSingleton.get()

		self.manager.app = self
		self.manager.setPluginInfoExtension("plugin")
		
		# Pass the manager the list of plugin directories
		self.manager.setPluginPlaces(places)
		
		# CollectPlugins is a shortcut for locatePlugins() and loadPlugins().
		self.manager.collectPlugins()
		
		# let's load all plugins we can find in the plugins directory
		for plugin in self.manager.getAllPlugins():
			self.activatePlugin(plugin.name)
		
		self.scan()
		
	def activatePlugin(self, pluginname):
		plugin = self.manager.activatePluginByName(pluginname)
		
		if plugin is None:
			print("Plugin: {0} konnte nicht gefunden werden".format(pluginname))
		else:
			print("Plugin: {0} erfolgreich geladen".format(pluginname))
	
	def scan(self):
		for scannerPlugin in self.scanner:
			scannerPlugin.scan()

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
	
	def addAppEntry(self, appEntry):
		self.allApps[appEntry.buildIndexString()] = appEntry
	
	def registerScannerPlugin(self, plugin):
		self.scanner.append(plugin)
		
		


class AppEntry():
	def __init__(self, name, command):
		self.name = name
		self.icon = None
		self.command = Command(command)
		self.genericName = None
		self.comment = None
		
	def buildIndexString(self):
		indexString = self.name + " " + self.genericName + " " + self.comment
		
		return indexString


class Command(QtCore.QThread):
	def __init__(self, string):
		QtCore.QThread.__init__(self)
		self.originalString = string

	def _parse(self):
		command = re.sub("%.?", "", self.originalString)  # remove field codes
		return shlex.split(command)

	def run(self):
		commandWithArgs = self._parse()
		p = subprocess.Popen(commandWithArgs)
		p.wait()
		self.quit()

