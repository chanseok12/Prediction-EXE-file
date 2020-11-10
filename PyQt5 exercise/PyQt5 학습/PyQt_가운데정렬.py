import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget


class centerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('가운데로')
        self.resize(500, 500)
        self.center()
        self.show()

    def center(self):
        frame_info = self.frameGeometry()
        # print(f'-> frame_info : {frame_info}')
        display_center = QDesktopWidget().availableGeometry().center()
        # print(f'-> display_center : { display_center }')
        frame_info.moveCenter(display_center)
        self.move(frame_info.topLeft())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ax = centerApp()
    sys.exit(app.exec_())
