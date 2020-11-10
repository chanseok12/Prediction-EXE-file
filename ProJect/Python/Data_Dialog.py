import sys

import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import numpy as np
import Train_Dialog
import matplotlib.pyplot as plt
import missingno as msno
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlibwidgetFile import matplotlibwidget


Data_Dialog_ui = '../_uiFiles/Data_Dialog_test.ui'


class new_Dialog(QDialog):
    def __init__(self, parent):
        super(new_Dialog, self).__init__(parent)
        uic.loadUi(Data_Dialog_ui, self)
        self.w = parent.w
        self.h = parent.h
        self.setFixedSize(self.w, self.h)
        self.data = parent.series_1
        self.r = parent.r
        self.c = parent.c
        self.setupUI(self.data, self.r, self.c)

        self.show()

    def setupUI(self, data, r, c):
        # 컬럼명 변경
        self.formLayout = QFormLayout(self.scrollAreaWidgetContents_2)
        self.formLayout.setObjectName("formLayout")
        for idx in range(c):
            self.label = QLabel(self.scrollAreaWidgetContents_2)
            self.label.setMinimumSize(QSize(0, 30))
            self.label.setObjectName(f"label_{idx}")
            self.formLayout.setWidget(idx, QFormLayout.LabelRole, self.label)
            self.label.setText(data.columns[idx])

            self.lineEdit = QLineEdit(self.scrollAreaWidgetContents_2)
            self.lineEdit.setMinimumSize(QSize(0, 30))
            # self.lineEdit.setMaximumSize(QSize(200, 100))
            self.lineEdit.setObjectName(f"lineEdit_{idx}")
            self.formLayout.setWidget(
                idx, QFormLayout.FieldRole, self.lineEdit)
        self.pushButton = QPushButton('변경', self.groupBox_2)
        self.pushButton.setObjectName("changeButton")
        self.pushButton.clicked.connect(
            lambda state, c=c: self.changeTextFunction(state, r, c, data))
        self.pushButton.setMaximumWidth(100)
        self.gridLayout_4.addWidget(self.pushButton, 2, 0, 1, 1, Qt.AlignRight)

        self.Save_Button.clicked.connect(self.saveFunction)
        self.Training_Button.clicked.connect(self.training_btn)

        # self.vbox = QVBoxLayout()
        # for i in range(c):
        #     self.checkbox = QCheckBox()
        #     self.checkbox.setMinimumSize(QSize(0, 30))
        #     self.checkbox.setObjectName(f"checkbox_{idx}")
        #     self.checkbox.setText(data.columns[i])
        #     self.vbox.addWidget(self.checkbox)
        #     self.groupBox_3.setLayout(self.vbox)


        self.fig = plt.Figure()
        ax = self.fig.add_subplot(111, )
        ax.grid()

        missing = data.isnull().sum()
        x_val = []
        y_val = []
        # print(data.columns)
        for i in range(data.shape[1]):
            cnt = data[data.columns[i]].isnull().sum()
            if cnt:
                x_val.append(data.columns[i])
                y_val.append(cnt)
            else:
                x_val.append(data.columns[i])
                y_val.append(0)

        try:
            missing = missing[missing > 0]
            missing.sort_values(inplace=True)
            ax.barh(x_val, y_val)
            ax.set_xlabel('개수')
            ax.set_xlim([0, data.shape[0]])
            for i, v in enumerate(x_val):
                ax.text(y_val[i], v, str(y_val[i]))
        except:
            ax.bar(x_val, y_val)
            ax.set_xlabel('Column')
            ax.set_ylabel('개수')
            for i, v in enumerate(x_val):
                ax.text(y_val[i], v, str(y_val[i]))

        self.canvas = FigureCanvas(self.fig)
        self.graph_view.addWidget(self.canvas)
        self.graph_frame.addLayout(self.graph_view)
        self.setLayout(self.graph_frame)


        # 결측치 처리
        origin_data = self.data
        self.text = self.data.isnull().sum()
        self.formLayout_2 = QFormLayout(self.scrollAreaWidgetContents_3)
        self.formLayout_2.setObjectName("formLayout_2")
        for i in range(c):
            self.label = QLabel(self.scrollAreaWidgetContents_3)
            self.label.setMinimumSize(QSize(0, 30))
            self.label.setObjectName(f'label_{i}')
            self.formLayout_2.setWidget(i, QFormLayout.LabelRole, self.label)
            self.label.setText(data.columns[i])

            self.combo = QComboBox(self.scrollAreaWidgetContents_3)
            self.combo.setMinimumHeight(30)
            self.combo.setObjectName(f'comboBox_{i}')
            self.combo.addItem('제거')
            self.combo.addItem('0으로 대체')
            self.combo.addItem('평균값으로 대체')
            self.combo.addItem('중앙값으로 대체')
            self.formLayout_2.setWidget(i, QFormLayout.FieldRole, self.combo)
        self.radioButton.setChecked(True)
        self.process_Button.clicked.connect(self.process_btn)
        self.reset_Button.clicked.connect(
            lambda state, origin_data=origin_data: self.reset_btn(state, origin_data))

        column_headers = data.columns

        self.tableWidget.resize(500, 300)
        if r >= 200:
            r = 200
        self.tableWidget.setRowCount(r)
        self.tableWidget.setColumnCount(c)
        self.tableWidget.setHorizontalHeaderLabels(column_headers)

        for i in range(r):
            for j in range(c):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(data.iloc[i, j])))
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

    # 컬럼 header 변경
    def changeTextFunction(self, state, r, c, data):
        for i in range(c):
            text = self.findChild(QLineEdit, f"lineEdit_{i}").text()
            if text != '':
                data.columns.values[i] = text
        self.tableWidget.setHorizontalHeaderLabels(data.columns)

    # Tabel cell 내용 변경
    def changeTableCells(self):
        for i in range(self.r):
            for j in range(self.c):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(self.data.iloc[i, j])))
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

    # 전처리
    def process_btn(self):
        if self.radioButton.isChecked():
            if self.all_comboBox.currentText() == '제거':
                self.data = self.data.dropna()
                self.r = self.data.shape[0]
                self.c = self.data.shape[1]
            elif self.all_comboBox.currentText() == '0으로 대체':
                self.data = self.data.fillna(0)
            elif self.all_comboBox.currentText() == '평균값으로 대체':
                self.data = round(self.data.fillna(self.data.mean()))
            elif self.all_comboBox.currentText() == '중앙값으로 대체':
                self.data = round(self.data.fillna(self.data.median()))

        else:
            for i in range(c):
                combo = self.findChild(
                    QComboBox, f"comboBox_{i}").currentText()
                if combo == '제거':
                    data = data.dropna(subset=[data.columns[i]])
                elif combo == '0으로 대체':
                    data[data.columns[i]] = data[data.columns[i]].fillna(0)
                elif combo == '평균값으로 대체':
                    data[data.columns[i]] = data[data.columns[i]].fillna(
                        data[data.columns[i]].mean())
                elif combo == '중앙값으로 대체':
                    data[data.columns[i]] = round(
                        data[data.columns[i]].fillna(data[data.columns[i]].median()))
        return self.changeTableCells()

    # 데이터 초기화
    def reset_btn(self, state, origin_data):
        self.data = origin_data
        return self.changeTableCells()

    # 데이터 저장
    def saveFunction(self):
        csv = self.data
        savefile = QFileDialog.getSaveFileName(self, '파일저장', '', '(*.csv)')
        csv.to_csv(savefile[0], index=False)

    # training과 연동
    def training_btn(self):
        self.series_1 = self.data
        Train_Dialog.Train_Dialog(self)
        self.close()
