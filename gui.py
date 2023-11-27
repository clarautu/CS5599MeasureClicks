import os.path
import pathlib
import random
import signal
import sys
import time
from ClickLabel import ClickLabel
from CountDownTimer import CountDownTimer

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
        #self.setMouseTracking(True)  # Allows the program to track where the cursor is
        self.startTime = -1  # Variable to track test start time
        self.counter = 0  # Variable to track which trial number we are on
        self.trials = 3  # Number of trials to complete, per test instance
        self.testCounter = 1  # Variable to track the current test number -- each participant will be tested 4 times
        self.testing = False  # Variable tracking whether a test is running or not
        self.rand = random  # Instance of random

        # Name of file to save to -- 'participant[currentTime].txt -- anonymous and no duplicate file names
        self.fileName = "results/participant" + str(time.time()) + ".txt"
        # Check if directory to save results in exists -- create it if it doesn't
        if not os.path.isdir("results"):
            os.mkdir("results")

        self.rows = 8  # Number of rows in the testing table
        self.columns = 15  # Number of columns in the testing table
        self.testCells = []  # List holding all labels used for testing
        self.currentMode = ""  # Variable to track what the current screen polarity is

        self.disableTime = 60000
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.enableButtons)

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
                temp = ClickLabel("")
                self.testCells.append(temp)
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

    # Method that coordinates the testing methods and handles file saving
    def testBootStrap(self, x, y, distance):
        timeToClick = time.time() - self.startTime
        file = open(self.fileName, "a")
        if self.counter == 0:
            file.write("Test " + str(self.testCounter) + "\n")
        file.write("\tMode: " + self.currentMode + " - Trial " + str(self.counter) +
                   "\n\t\tTime to click: " + str(timeToClick) + "\n\t\tMouse coords: ( %d : %d )" % (
                   x, y) + "\n\t\tDistance: " + str(distance) + "\n")
        file.close()
        self.counter += 1
        if self.counter == self.trials:
            self.counter = 0
            self.testCounter += 1
            self.endTest(True)
        else:
            self.endTest(False)
            self.start()

    # Click event that starts the test
    def start(self):
        # Allow click tracking
        self.testing = True

        # Assign the circle image as a pixmap - circle color is rgb(0,128,0)
        pixmap = QPixmap('alteredCircle.png')

        # Set target as a random integer on the range of zero to rows * columns
        target = self.rand.randint(0, (self.rows * self.columns) - 1)
        count = 0  # Track current index

        # Assign the pixmap to the target cell
        self.testCells[target].setPixmap(pixmap)
        self.testCells[target].setScaledContents(True)

        # Loop through children and hide buttons and status label
        for child in self.children():
            if type(child) == QPushButton:
                child.hide()
            elif type(child) == QLabel:
                if child.text() != "":
                    child.hide()

        # Connect the click event to testBootStrap
        self.testCells[target].clicked.connect(self.testBootStrap)

        # Update window and start the timer
        self.repaint()
        self.startTime = time.time()

    # Method that ends the test
    def endTest(self, endOfTrials):
        self.testing = False

        if endOfTrials:
            # Clear the test cells
            for item in self.testCells:
                item.clear()
            # Loop over all children and show the buttons and the mode label
            for child in self.children():
                if type(child) == QPushButton:
                    child.show()
                elif type(child) == QLabel:
                    if child.text() != "":
                        child.show()
            # Add a pause that keeps the next trial from beginning until a specified time has passed
            self.disableButtons()
        else:
            # Clear the test cells
            for item in self.testCells:
                item.clear()

        self.repaint()  # Update the window

    def disableButtons(self):
        for child in self.children():
            if type(child) == QPushButton:
                child.setEnabled(False)

        self.showCountdown()

    def enableButtons(self):
        for child in self.children():
            if type(child) == QPushButton:
                child.setEnabled(True)

    def showCountdown(self):
        dialog = CountDownTimer(self)
        dialog.countdownInterrupted.connect(self.enableButtons)
        dialog.startCountdown(self.disableTime)
        result = dialog.exec_()  # Blocking call, waits for the dialog to close
        if result == QDialog.Accepted:
            # The countdown dialog closed, re-enable buttons
            self.enableButtons()




if __name__ == '__main__':

    # This line allows CNTL-C in the terminal to kill the program
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)

    w = gui()
    sys.exit(app.exec())
