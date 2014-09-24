import os, subprocess, shlex, re
import dbus.service
from PyQt5 import QtCore
from yapsy.PluginManager import PluginManagerSingleton

from launcher import Launcher



class DBusObject(dbus.service.Object):

	def __init__(self, core):
		busName = dbus.service.BusName('org.pygmy.launcher', bus = dbus.SessionBus())
		dbus.service.Object.__init__(self, busName, '/org/pygmy/MainWindow')
		self.core = core
		
	@dbus.service.method(dbus_interface='org.pygmy.launcher')
	def wakeup(self):
		print("waking up...")
		self.window = Launcher(self.core)
		self.core.gui = self.window
		self.window.show()
		self.window.activateWindow()

class Core():
	def __init__(self):
		self.allApps = {}
		self.scanner = []
		self.results = []
		self.gui = None

		currentDir = os.path.dirname(os.path.realpath(__file__))

		plugin_dir = currentDir + "/" + "plugins"
		places = [plugin_dir, ]

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

