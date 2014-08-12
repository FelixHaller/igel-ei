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
import sys, time, threading, os
from PyQt5 import QtGui, QtWidgets, QtCore
from core import Core

MIN_INPUT_LENGTH = 0

class Launcher(QtWidgets.QMainWindow):
	def __init__(self, parent=None):
		super(Launcher, self).__init__(parent)
		
		self.core = Core(self)
		self.core.start()
		self.liste = []
		centralWidget = QtWidgets.QWidget(parent=self)
		self.setCentralWidget(centralWidget)
		layout = QtWidgets.QVBoxLayout()
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.inputLine = QtWidgets.QLineEdit()
		self.inputLine.textChanged.connect(self.inputHandler)
		self.centerOnScreen()
		self.inputLine.setGeometry(0,0,self.width(),25)
		self.resultWidget = QtWidgets.QListWidget()
		layout.addWidget(self.inputLine)
		layout.addWidget(self.resultWidget)
		centralWidget.setLayout(layout)
	def inputHandler(self):
		self.resultWidget.clear()
		if len(self.inputLine.text()) > MIN_INPUT_LENGTH:
			for entry in self.core.searchApp(self.inputLine.text()):
				icon = QtGui.QIcon(entry.icon)
				item = QtWidgets.QListWidgetItem(icon,entry.name)
				self.resultWidget.addItem(item)
	def centerOnScreen (self):
		'''Centers the window on the screen.'''
		resolution = QtWidgets.QDesktopWidget().screenGeometry()
		self.setGeometry(0,0,resolution.width() / 2,resolution.height()/3)
		self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
				  (resolution.height() / 2) - (self.frameSize().height() / 2))
		
	def keyPressEvent(self, e):
		if e.key() == QtCore.Qt.Key_Escape:
			if self.inputLine.text() == "":
				self.close()
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
			#self.inputLine.setText("")
			self.inputLine.setFocus(True)
			self.inputLine.setCursorPosition(len(self.inputLine.text()))
			self.resultWidget.item(0).setSelected(False)
		elif e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
			if self.inputLine.hasFocus() and self.resultWidget.count() > 0:
				self.core.launchApp(0)
			elif not self.inputLine.hasFocus() and self.resultWidget.count() > 0:
				self.core.launchApp(self.resultWidget.currentRow())
if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	myapp = Launcher()
	myapp.show()
	sys.exit(app.exec_())

