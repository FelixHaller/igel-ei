#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  launcher.py
#  
#  Copyright 2014 Felix Haller <ich@ein-freier-mensch.de>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import sys, time, threading, os, dbus
import dbus.service
from dbus.mainloop.qt import DBusQtMainLoop
from dbus.mainloop.glib import DBusGMainLoop
from PyQt5 import QtGui, QtWidgets, QtCore
from core import Core

MIN_INPUT_LENGTH = 3


class Launcher(QtWidgets.QMainWindow):
	def __init__(self, parent=None):
		super(Launcher, self).__init__(parent)
		
		self.core = Core(self)
		self.core.start()
		self.liste = []
		centralWidget = QtWidgets.QWidget(self)
		
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
		
		
		self.setStyleSheet("background-color: rgba(45, 45, 45, 75%); color: #dedede;")
		
		self.setCentralWidget(centralWidget)
		layout = QtWidgets.QVBoxLayout()
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
		self.inputLine = QtWidgets.QLineEdit(centralWidget)
		self.inputLine.textChanged.connect(self.inputHandler)
		self._centerOnScreen()
		
		self.setFocusProxy(centralWidget)
		centralWidget.setFocusProxy(self.inputLine)
		
		self.inputLine.setGeometry(0,0,self.width(),25)
		self.resultWidget = QtWidgets.QListWidget()
		self.resultWidget.setStyleSheet("selection-background-color: #d64937;")
		layout.addWidget(self.inputLine)
		layout.addWidget(self.resultWidget)
		centralWidget.setLayout(layout)
		
	def showEvent(self, event):
		print("show")
		self.inputLine.setText("")
		self.inputLine.setFocus(True)
		self.inputLine.raise_()
		
	def inputHandler(self):
		self.resultWidget.clear()
		if len(self.inputLine.text()) >= MIN_INPUT_LENGTH:
			for entry in self.core.searchApp(self.inputLine.text()):
				icon = QtGui.QIcon(entry.icon)
				item = QtWidgets.QListWidgetItem(icon,entry.name)
				self.resultWidget.addItem(item)
			
	def _centerOnScreen (self):
		'''Centers the window on the screen.'''
		resolution = QtWidgets.QDesktopWidget().screenGeometry()
		self.setGeometry(0,0,resolution.width() / 2,resolution.height()/3)
		self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
				  (resolution.height() / 2) - (self.frameSize().height() / 2))
		
	def keyPressEvent(self, e):
		if e.key() == QtCore.Qt.Key_Escape:
			if self.inputLine.text() == "":
				self.hide()
			else:
				self.inputLine.setText("")
				self.inputLine.setFocus(True)
		elif e.key() == QtCore.Qt.Key_Down:
			if self.inputLine.hasFocus() and self.resultWidget.count() > 0:
				self.resultWidget.setFocus(True)
				self.resultWidget.item(0).setSelected(True)
		elif e.key() == QtCore.Qt.Key_Up:
			if self.resultWidget.hasFocus() and self.resultWidget.item(0).isSelected():
				self.inputLine.setFocus(True)
				self.inputLine.setCursorPosition(len(self.inputLine.text()))
				self.resultWidget.item(0).setSelected(False)
		elif e.key() == QtCore.Qt.Key_Backspace:
			self.inputLine.setFocus(True)
			self.inputLine.setCursorPosition(len(self.inputLine.text()))
			self.resultWidget.item(0).setSelected(False)
		elif e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
			if self.inputLine.hasFocus() and self.resultWidget.count() > 0:
				self.hide()
				self.core.launchApp(0)
			elif not self.inputLine.hasFocus() and self.resultWidget.count() > 0:
				self.hide()
				self.core.launchApp(self.resultWidget.currentRow())

	
class DBusTrayMainWindowObject(dbus.service.Object):
	"""DBus wrapper object for the mainwindow."""

	def __init__(self, mainwindow, bus):
		"""Creates a new service object. `mainwindow` specifies the window,
		which is to be exposed through this service object. `bus` is the
		DBus bus, at which this object is registered."""
		# register this object on the given bus
		dbus.service.Object.__init__(self, bus,
									 # the dbus object path
									 '/org/pygmy/MainWindow')
		self.mainwindow = mainwindow

	
	@dbus.service.method(dbus_interface='org.pygmy.launcher')
	def show(self):
		self.mainwindow.show()
		self.mainwindow.activateWindow()
		
if __name__ == "__main__":
	bus = dbus.SessionBus(mainloop=DBusGMainLoop())
	
	try:
		launcher = bus.get_object("org.pygmy.launcher","/org/pygmy/MainWindow")
		
	except dbus.DBusException:
		
		# the application is not running, so the service is registered and
		# the window created
		name = dbus.service.BusName("org.pygmy.launcher", bus)
		app = QtWidgets.QApplication(sys.argv)
		launcher = Launcher()
		# register the service object for the main window
		mainwindowobject = DBusTrayMainWindowObject(launcher, bus)
		# show the window and get the message loop running
		launcher.show()
		app.exec_()
	else:
		# the try clause completed, the application must therefore be
		# running.  Now the mainwindow is shown and activated.
		launcher.show()
		
		
		
		
	
