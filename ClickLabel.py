import time

from whichpyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
    from PyQt5.QtWidgets import QLabel, QMessageBox
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))


class ClickLabel(QLabel):
    clicked = pyqtSignal(int, int, float)

    def __init__(self, parent=None):
        super(ClickLabel, self).__init__(parent)
        self.cooldownTime = 500  # 500 milliseconds cooldown
        self.lastClickTime = 0
        self.setMouseTracking(True)
        self.clicked.connect(self.handle_click)

    # Mouse click event - measures time from circle displaying to user click and click position
    def mousePressEvent(self, event):
        if self.pixmap() is not None:
            center_x = self.width() / 2
            center_y = self.height() / 2
            distance = ((event.x() - center_x) ** 2 + (event.y() - center_y) ** 2) ** 0.5

            currentTime = int(round(time.time() * 1000))  # Convert to milliseconds
            # Only register the click if it has been longer than the cooldown period
            if currentTime - self.lastClickTime > self.cooldownTime:
                self.lastClickTime = currentTime
                self.clicked.emit(event.x(), event.y(), distance)


    def handle_click(self, x, y, distance):
        pass
        '''msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Time to click: " + str(0.0) + "\nMouse coords: (%d : %d)" % (x, y) +
                    "\nDistance to center: {:.2f}".format(distance))
        #msg.setText("Time to click: " + str(0.0) + "\nMouse coords: ( %d : %d )" % (self.xCoord, self.yCoord))
        msg.setWindowTitle("Click Measured - ClickLabel")
        msg.exec_()'''


