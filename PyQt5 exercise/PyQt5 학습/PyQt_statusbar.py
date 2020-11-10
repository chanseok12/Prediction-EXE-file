# 스테이터스 바 만들기

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QToolTip
from PyQt5.QtGui import QFont
import sys

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # status bar
        self.statusBar().showMessage("Nothing is happening")

        # PushButton
        # QToolTip.setFont(QFont('SansSerif', 50))
        btn = QPushButton('Button 01', self)
        btn.setToolTip('This is a <b> Button 01 </b>\n It has no event handler')
        btn.setStatusTip('This is a Button 01')
        btn.setGeometry(0, 0, 100, 100)
        # self.resize(200, 200)
        btn.move(200, 200)
        # frame_info.m

        # Window Title
        self.setWindowTitle('Status Bar Example')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    screen = app.primaryScreen()
    size = screen.size()
    w, h = 500, 500
    ex.setGeometry(size.width()/2-w/2, size.height()/2-h/2, w, h)
    sys.exit(app.exec_())