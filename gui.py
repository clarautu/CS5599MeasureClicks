import os.path
import pathlib
import random
import signal
import sys
import time

from whichpyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtTest import QTest
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))


class gui:
    def __init__(self):
        self.rand = random
        self.rows = 8
        self.columns = 15
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

        # Create testing area
        testArea = QGridLayout()
        testArea.setContentsMargins(100, 100, 100, 100)
        for i in range(self.rows):
            for j in range(self.columns):
                temp = QLabel("")
                #temp.setScaledContents(True)
                # Green seems to be the best color that has the same visibility in both polarities
                #       fuchsia was the second best I tested
                #temp.setStyleSheet("border: 3px solid green; border-radius: 20px")
                testArea.addWidget(temp, i, j)

        # Create mode switching and start buttons
        btnSwitchMode = QPushButton("Switch Between Modes")
        btnSwitchMode.clicked.connect(self.switchMode)
        btnStart = QPushButton("Start Test")
        btnStart.clicked.connect(self.start)

        # Create layout for buttons and mode label, then add them
        btnBar = QHBoxLayout()
        btnBar.addSpacing(500)
        btnBar.addWidget(btnSwitchMode)
        btnBar.addSpacing(100)
        btnBar.addWidget(lbCurrentMode)
        btnBar.addSpacing(300)
        btnBar.addSpacing(500)
        btnBar.addWidget(btnStart)
        btnBar.addSpacing(500)

        # Create the layout and add the widgets
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(btnBar)
        mainLayout.addLayout(testArea)

        self.window.setLayout(mainLayout)

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
                if child.text() != "":
                    child.setText("Current Mode: " + self.currentMode)
                    return
        # Shouldn't get here
        raise Exception("Current mode label not found")

    # Click event that starts the test
    def start(self):
        # Assign the circle image as a pixmap - circle color is rgb(0,128,0)
        pixmap = QPixmap('alteredCircle.png')

        # Run 5 trials
        trialCount = 0
        while trialCount < 5:
            trialCount += 1  # Increment trial count
            # Set target as a random integer on the range of zero to rows * columns
            target = self.rand.randint(0, (self.rows * self.columns))
            count = 0  # Track current index

            # Loop through children and hide buttons and status label
            for child in self.window.children():
                if type(child) == QPushButton:
                    child.hide()
                elif type(child) == QLabel:
                    if child.text() == "":
                        if count == target:  # Set pixmap to target label
                            child.setPixmap(pixmap)
                            child.setScaledContents(True)
                            break
                        else:
                            count += 1
                    else:
                        child.hide()
            self.window.repaint()  # Update window
            # Set up timer and send timeout signal to endTest for now
            QTest.qWait(3000)
            self.endTest()
            #timer = QTimer()
            #timer.singleShot(3000, self.endTest)

    # Method that ends the test
    def endTest(self):
        for child in self.window.children():
            if type(child) == QPushButton:
                child.show()
            elif type(child) == QLabel:
                if child.text() == "":
                    child.clear()
                else:
                    child.show()
        self.window.repaint()


if __name__ == '__main__':

    # This line allows CNTL-C in the terminal to kill the program
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)

    w = gui()
    sys.exit(app.exec())
