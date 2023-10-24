import time

from whichpyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
    from PyQt5.QtWidgets import QLabel, QMessageBox
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))


class ClickLabel(QLabel):
    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
        self.setMouseTracking(True)

    # Mouse click event - measures time from circle displaying to user click and click position
    def mousePressEvent(self, event):
        # Only want click event to happen on label with image
        # When label is selected, swap with this custom class
        # Then, click event will need to send notice to gui that it has been clicked
        #       - will also want to send mouse location and relative coordinates
        #   - do this by calling gui method that is made just for this purpose
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Time to click: " + str(0.0) + "\nMouse coords: ( %d : %d )" % (event.x(), event.y()))
        msg.setWindowTitle("Click Measured - ClickLabel")
        msg.exec_()



            # # If not testing, don't measure click
            # if not self.testing:
            #     return
            #
            # timeToClick = time.time() - self.startTime
            # msg = QMessageBox()
            # msg.setIcon(QMessageBox.Critical)
            # msg.setText("Time to click: " + str(timeToClick) + "\nMouse coords: ( %d : %d )" % (event.x(), event.y()))
            # msg.setWindowTitle("Click Measured")
            # msg.exec_()
            # self.counter += 1
            # if self.counter == self.trials:
            #     self.counter = 0
            #     self.endTest()
            # else:
            #     self.endTest()
            #     self.startTest()