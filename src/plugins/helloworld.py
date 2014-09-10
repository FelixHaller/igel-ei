from PyQt5 import QtCore, QtGui
from yapsy.PluginManager import PluginManagerSingleton

import plugins.plugin as plugin


class HelloWorld(plugin.Plugin):
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
		# Make sure to call `activate()` on the parent class to ensure that the
		# `is_activated` property gets set.
		super().activate()
		
		# Connect to the "delete-event" and store the handler_id so that the
		# signal handler can be disconnected when the plugin is deactivated.
		# If your plugin connects to multiple signals on multiple objects then
		# you'll want to store the object and the handler_id of each of those.
		#self._handler = self.app.window.connect("delete-event", self._on_window_delete_event)
		print("Hello World!")

	def deactivate(self):
		# Make sure to call `deactivate()` on the parent class to ensure that 
		# the `is_activated` property gets set.
            print("GoodBye World!")
            super().deactivate()
	

