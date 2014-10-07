from PyQt5 import QtGui, QtWidgets, QtCore

MIN_INPUT_LENGTH = 3


class MainWindow(QtWidgets.QMainWindow):
	def __init__(self, core, parent=None):
		super().__init__(parent)

		self.core = core
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

		self.inputLine.setGeometry(0, 0, self.width(), 25)
		self.resultWidget = QtWidgets.QListWidget()
		self.resultWidget.setStyleSheet("selection-background-color: #d64937;")
		layout.addWidget(self.inputLine)
		layout.addWidget(self.resultWidget)
		centralWidget.setLayout(layout)


	def inputHandler(self):
		self.resultWidget.clear()
		if len(self.inputLine.text()) >= MIN_INPUT_LENGTH:
			for entry in self.core.searchApp(self.inputLine.text()):
				icon = QtGui.QIcon(entry.icon)
				item = QtWidgets.QListWidgetItem(icon, entry.name)
				self.resultWidget.addItem(item)

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

	def _centerOnScreen(self):
		'''Centers the window on the screen.'''
		resolution = QtWidgets.QDesktopWidget().screenGeometry()
		self.setGeometry(0, 0, resolution.width() / 2, resolution.height() / 3)
		self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
				(resolution.height() / 2) - (self.frameSize().height() / 2))


