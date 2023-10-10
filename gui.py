import os.path
import pathlib
import signal
import sys

from whichpyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtWidgets import *
	from PyQt5.QtGui import *
	from PyQt5.QtCore import *
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

class gui:
    def __init__(self):
        self.currentMode = ""
        self.window = QWidget()
        self.SetUp()
        self.switchMode()
        self.Show()

    # Method that performs initial setup for the window
    def SetUp(self):
        self.window = QWidget()
        self.window.setWindowTitle("Measure Click Accuracy and Speed")

        # Create label that shows what mode is currently selected
        lbCurrentMode = QLabel("Current Mode: " + self.currentMode)

        # Create mode switching and start buttons
        btnSwitchMode = QPushButton("Switch Between Modes")
        btnSwitchMode.clicked.connect(self.switchMode)
        btnStart = QPushButton("Start Test")
        btnStart.clicked.connect(self.start)

        # Create the layout and add the widgets
        layout = QVBoxLayout()
        layout.addWidget(lbCurrentMode)
        layout.addWidget(btnSwitchMode)
        layout.addWidget(btnStart)

        self.window.setLayout(layout)

    # Method that shows the window
    def Show(self):
        self.window.showMaximized()

    # Click event that switches between light and dark modes
    def switchMode(self):
        if self.currentMode == "Light Mode":
            self.currentMode = "Dark Mode"
            self.updateLabel()
            self.window.setStyleSheet("background-color: rgb(62,62,66); color: white")
            for child in self.window.children():
                if type(child) == QPushButton:
                    child.setStyleSheet("background-color: rgb(37,37,38)")
        else:
            self.currentMode = "Light Mode"
            self.updateLabel()
            self.window.setStyleSheet("background-color: white; color: black")
            for child in self.window.children():
                if type(child) == QPushButton:
                    child.setStyleSheet("background-color: lightGrey")

    # Method that updates the current mode label
    def updateLabel(self):
        for child in self.window.children():
            if type(child) == QLabel:
                child.setText("Current Mode: " + self.currentMode)
                return
        # Shouldn't get here
        raise Exception("Current mode label not found")

    # Click event that starts the test
    def start(self):
        pass


if __name__ == '__main__':

    # This line allows CNTL-C in the terminal to kill the program
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)

    w = gui()
    sys.exit(app.exec())
