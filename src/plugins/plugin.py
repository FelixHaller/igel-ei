from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton

class Plugin(IPlugin):
	def __init__(self):
		super().__init__()
		self.manager = PluginManagerSingleton.get()
		self.app = self.manager.app
	
	def activate(self):
		super().activate()
		
	def deactivate(self):
		super().deactivate()

