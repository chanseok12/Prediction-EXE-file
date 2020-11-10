from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QPushButton
import sys
from PyQt5.QtCore import QTime, Qt
from PyQt5.QtCore import QTime
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtCore import QDate

# now = QDate.currentDate()
# print(now.toString())


# now = QDate.currentDate()
# print(now.toString('d.M.yy'))
# print(now.toString('dd.MM.yyyy'))
# print(now.toString('ddd.MMMM.yyyy'))
# print(now.toString(Qt.ISODate))
# print(now.toString(Qt.DefaultLocaleLongDate))


# time = QTime.currentTime()
# print(time.toString())

# time = QTime.currentTime()
# print(time.toString('h.m.s'))
# print(time.toString('hh.mm.ss'))
# print(time.toString('hh.mm.ss.zzz'))
# print(time.toString(Qt.DefaultLocaleLongDate))
# print(time.toString(Qt.DefaultLocaleShortDate))


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.date = QDate.currentDate()
        self.initUI()

    def initUI(self):
        btn = QPushButton('Button 01', self)
        btn.setGeometry(0, 0, 100, 100)
        self.statusBar().showMessage(self.date.toString(Qt.DefaultLocaleLongDate))

        self.setWindowTitle('Date')
        self.setGeometry(300, 300, 400, 200)
        self.center()
        self.show()

    def center(self):
        frame_info = self.frameGeometry()
        # print(f'-> frame_info : {frame_info}')
        display_center = QDesktopWidget().availableGeometry().center()
        # print(f'-> display_center : { display_center }')
        frame_info.moveCenter(display_center)
        self.move(frame_info.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
