import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp
from PyQt5.QtGui import QIcon

dir = os.path.dirname(os.getcwd())
print(dir)
print()
class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        exit = QAction(QIcon(dir + 'images/ex_01.png'), '&Exit', self)
        exit.setShortcut('Ctrl+e')
        exit.setStatusTip(('Exit application'))
        exit.triggered.connect(QApplication.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMunu = menubar.addMenu('&File')
        fileMunu.addAction('exit')

        self.show()

if __name__ == '__main':

    app = QApplication(sys.argv)
    ex = Example()
    screen = app.primaryScreen()
    size = screen.size()
    w, h = 300, 300
    ex.setGeometry(size.width()/2-w, size.height()/2-h, w, h)
    sys.exit(app.exec_())