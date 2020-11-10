import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.setGeometry(500, 500, 500, 200)
        self.setWindowTitle("Example 02")
        self.setWindowIcon(QIcon("images/ex_01.png"))

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())