import sys
import UI

import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
# from PyQt5 import uic

# CalUI = 'cir_1.ui'


class MainDialog(QDialog, UI.Ui_Dialog):
    def __init__(self):
        QDialog.__init__(self, None, Qt.WindowStaysOnTopHint)
        # uic.loadUi(CalUI, self)
        self.setupUi(self)

        # 숫자 클릭
        self.num_pushButton_1.clicked.connect(
            lambda state, button=self.num_pushButton_1: self.NumClicked(state, button))
        self.num_pushButton_2.clicked.connect(
            lambda state, button=self.num_pushButton_2: self.NumClicked(state, button))
        self.num_pushButton_3.clicked.connect(
            lambda state, button=self.num_pushButton_3: self.NumClicked(state, button))
        self.num_pushButton_4.clicked.connect(
            lambda state, button=self.num_pushButton_4: self.NumClicked(state, button))
        self.num_pushButton_5.clicked.connect(
            lambda state, button=self.num_pushButton_5: self.NumClicked(state, button))
        self.num_pushButton_6.clicked.connect(
            lambda state, button=self.num_pushButton_6: self.NumClicked(state, button))
        self.num_pushButton_7.clicked.connect(
            lambda state, button=self.num_pushButton_7: self.NumClicked(state, button))
        self.num_pushButton_8.clicked.connect(
            lambda state, button=self.num_pushButton_8: self.NumClicked(state, button))
        self.num_pushButton_9.clicked.connect(
            lambda state, button=self.num_pushButton_9: self.NumClicked(state, button))
        self.num_pushButton_0.clicked.connect(
            lambda state, button=self.num_pushButton_0: self.NumClicked(state, button))

        # 사칙연산
        self.minus_pushButton.clicked.connect(
            lambda state, button=self.minus_pushButton: self.NumClicked(state, button))
        self.plus_pushButton.clicked.connect(
            lambda state, button=self.plus_pushButton: self.NumClicked(state, button))
        self.cross_pushButton.clicked.connect(
            lambda state, button=self.cross_pushButton: self.NumClicked(state, button))
        self.division_pushButton.clicked.connect(
            lambda state, button=self.division_pushButton: self.NumClicked(state, button))

        # 나머지

        self.result_pushButton.clicked.connect(self.MakeResult)
        self.reset_pushButton.clicked.connect(self.Reset)
        self.del_pushButton.clicked.connect(self.Delete)
        # self.del_pushButton.setStyleSheet(
        #     'image:url(image/delete.png); border:0px;')
        self.del_pushButton.setStyleSheet(
            '''
            QPushButton{image:url(image/delete.png); border:0px;}
            QPushButton:hover{image:url(image/delete_red.png); border:0px;}
            ''')

        self.p_open_pushButton.clicked.connect(
            lambda state, button=self.p_open_pushButton: self.NumClicked(state, button))
        self.q_open_pushButton.clicked.connect(
            lambda state, button=self.q_open_pushButton: self.NumClicked(state, button))
        self.per_pushButton.clicked.connect(
            lambda state, button=self.per_pushButton: self.NumClicked(state, button))
        self.dot_pushButton.clicked.connect(
            lambda state, button=self.dot_pushButton: self.NumClicked(state, button))

    def NumClicked(self, state, button):
        # print('hello')
        # print(self.num_pushButton_1.text())
        if button == self.per_pushButton:
            now_num_text = '*0.01'
        else:
            now_num_text = button.text()
        exist_line_text = self.q_lineEdit.text()

        self.q_lineEdit.setText(exist_line_text + now_num_text)

        # print(self.q_lineEdit.setText('hi'))

    def MakeResult(self):
        try:
            result = eval(self.q_lineEdit.text())
            # print(type(result))
            self.answer_lineEdit.setText(str(result))
        except Exception as e:
            print(e)
            pass

    def Reset(self):
        # print('reset')
        self.q_lineEdit.clear()
        self.answer_lineEdit.setText(str(0))

    def Delete(self):
        exist_line_text = self.q_lineEdit.text()
        exist_line_text = exist_line_text[:-1]
        self.q_lineEdit.setText(exist_line_text)


app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()
app.exec_()
