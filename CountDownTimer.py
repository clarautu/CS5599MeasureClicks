import sys

from whichpyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
    from PyQt5.QtGui import QFont
    from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QDialog, QLabel, QProgressBar, QHBoxLayout, QSizePolicy, QDesktopWidget
    from PyQt5.QtCore import QTimer, Qt, QSize, QDateTime, pyqtSignal
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

class CountDownTimer(QDialog):
    countdownInterrupted = pyqtSignal()

    def __init__(self, parent=None):
        super(CountDownTimer, self).__init__(parent)
        self.setWindowTitle("CountDown Timer Until Next Trail")

        self.timerLabel = QLabel("Time remaining until next trial can begin:")
        self.timerLabel.setFont(QFont("Arial", 16))  # Set the font size here
        self.progressBar = QProgressBar()
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)

        layout = QVBoxLayout(self)
        layout.addWidget(self.timerLabel, alignment=Qt.AlignCenter)
        layout.addWidget(self.progressBar)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTimer)

    def startCountdown(self, duration):
        self.duration = duration
        self.timerInterval = 1000  # 1 second
        self.progressBar.setMaximum(self.duration)
        self.timer.setInterval(self.timerInterval)
        self.timer.start()

    def updateTimer(self):
        self.duration -= self.timerInterval
        if self.duration <= 0:
            self.timer.stop()
            self.accept()
        else:
            remainingSeconds = self.duration // 1000  # Convert milliseconds to seconds
            self.timerLabel.setText(f"<div align='center'>Time remaining until next trial can begin:<br/>{remainingSeconds} seconds</div>")
            self.progressBar.setValue(self.progressBar.maximum() - self.duration)


    def resizeEvent(self, event):
        # Override resizeEvent to enforce the desired size
        screenSize = QDesktopWidget().availableGeometry().size()
        dialogWidth = int(screenSize.width() * 0.4)
        dialogHeight = int(screenSize.height() * 0.4)

        newSize = QSize(dialogWidth, dialogHeight)
        self.setFixedSize(newSize)

    def closeEvent(self, event):
        # You can choose either option below:

        # Option 1: Prevent the dialog from being closed
        # event.ignore()

        # Option 2: Emit a signal to indicate countdown interruption
        self.countdownInterrupted.emit()
        event.accept()
