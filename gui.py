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
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))


class gui(QWidget):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.startTime = -1
        self.counter = 0
        self.trials = 10
        self.testCounter = 1
        self.testing = False
        self.rand = random
        self.fileName = "results/participant" + str(time.time()) + ".txt"
        if not os.path.isdir("results"):
            os.mkdir("results")
        self.rows = 8
        self.columns = 15
        self.currentMode = ""
        self.SetUp()
        self.switchMode()
        self.Show()

    # Method that performs initial setup for the window
    def SetUp(self):
        self.setWindowTitle("Measure Click Accuracy and Speed")

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

        self.setLayout(mainLayout)

    # Method that shows the window
    def Show(self):
        self.showMaximized()

    # Click event that switches between light and dark modes
    def switchMode(self):
        if self.currentMode == "Light Mode":
            self.currentMode = "Dark Mode"
            self.updateLabel()
            self.setStyleSheet("background-color: rgb(62,62,66); color: white")
            for child in self.children():
                if type(child) == QPushButton:
                    child.setStyleSheet("background-color: rgb(37,37,38)")
        else:
            self.currentMode = "Light Mode"
            self.updateLabel()
            self.setStyleSheet("background-color: white; color: black")
            for child in self.children():
                if type(child) == QPushButton:
                    child.setStyleSheet("background-color: lightGrey")

    # Method that updates the current mode label
    def updateLabel(self):
        for child in self.children():
            if type(child) == QLabel:
                if child.text() != "":
                    child.setText("Current Mode: " + self.currentMode)
                    return
        # Shouldn't get here
        raise Exception("Current mode label not found")

    # Click event that starts the test
    def start(self):
        # Allow click tracking
        self.testing = True

        # Assign the circle image as a pixmap - circle color is rgb(0,128,0)
        pixmap = QPixmap('alteredCircle.png')

        # Set target as a random integer on the range of zero to rows * columns
        target = self.rand.randint(0, (self.rows * self.columns))
        count = 0  # Track current index

        # Loop through children and hide buttons and status label
        for child in self.children():
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
        self.repaint()  # Update window
        self.startTime = time.time()

    # Method that ends the test
    def endTest(self):
        self.testing = False
        for child in self.children():
            if type(child) == QPushButton:
                child.show()
            elif type(child) == QLabel:
                if child.text() == "":
                    child.clear()
                else:
                    child.show()
        self.repaint()

    # Mouse click event - measures time from circle displaying to user click and click position
    def mousePressEvent(self, event):
        # If not testing, don't measure click
        if not self.testing:
            return

        timeToClick = time.time() - self.startTime
        file = open(self.fileName, "a")
        if self.counter == 0:
            file.write("Test " + str(self.testCounter) + "\n")
        file.write("\tMode: " + self.currentMode + " - Trial " + str(self.counter) +
                   "\n\t\tTime to click: " + str(timeToClick) +"\n\t\tMouse coords: ( %d : %d )\n" % (event.x(), event.y()))
        file.close()
        '''msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Time to click: " + str(timeToClick) +"\nMouse coords: ( %d : %d )" % (event.x(), event.y()))
        msg.setWindowTitle("Click Measured")
        msg.exec_()'''
        self.counter += 1
        if self.counter == self.trials:
            self.counter = 0
            self.testCounter += 1
            self.endTest()
        else:
            self.endTest()
            self.start()


if __name__ == '__main__':

    # This line allows CNTL-C in the terminal to kill the program
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)

    w = gui()
    sys.exit(app.exec())
