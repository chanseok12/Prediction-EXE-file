import sys
import os
from Data_Dialog_1 import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from ARIMA import *

Data = '../_uiFiles/DataAnalysis.ui'


class MyWindow(QMainWindow):
    def __init__(self):
        global p_value, d_value, q_value, c_nc
        c, series_1 = 0, 0
        QMainWindow.__init__(self, None)
        uic.loadUi(Data, self)
        self.setWindowTitle("S-Prediction")
        self.setWindowIcon(QIcon("../images/icon.ico"))

        p_value = 0
        d_value = 1
        q_value = 0
        c_nc = 'c'

        # File Button
        self.OpenBtn.triggered.connect(self.Open_File)
        self.CloseBtn.triggered.connect(self.Close_exe)
        self.p_spinBox.valueChanged.connect(self.p_spinBoxChanged)
        self.d_spinBox.valueChanged.connect(self.d_spinBoxChanged)
        self.q_spinBox.valueChanged.connect(self.q_spinBoxChanged)
        self.c_nc_comboBox.currentIndexChanged.connect(
            self.c_nc_comboBoxChanged)
        self.ARIMA_.clicked.connect(self.ARIMA_pushed)
        # uic.loadUi(Dialog, self)

        # ARIMA

    def p_spinBoxChanged(self):
        global p_value
        p_value = self.p_spinBox.value()

    def d_spinBoxChanged(self):
        global d_value
        d_value = self.d_spinBox.value()

    def q_spinBoxChanged(self):
        global q_value
        q_value = self.q_spinBox.value()

    def c_nc_comboBoxChanged(self):
        global c_nc
        c_nc = self.c_nc_comboBox.currentText()
        # self.lbl_display.setText(self.c_nc_comboBox.currentText())

    def ARIMA_pushed(self):
        ARIMA_run(series_1.iloc[:, 1:3], p_value, d_value, q_value, c_nc)
        # print(p_value)
        # print(d_value)
        # print(q_value)
        # print(c_nc)

    def Close_exe(self):
        close = QMessageBox()
        close.setText("종료하시겠습니까??")
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        close = close.exec()

        if close == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def Open_File(self):
        global series_1
        self.showFile()
        # di = new_Dialog(self, series_1, c)
        # di.setupUI(self, n)

    def showFile(self):
        global c, series_1
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename = QFileDialog.getOpenFileName(
            self,
            "파일열기", "", "(*.csv);;(*.json)")
        if filename[0][-1] == 'v':
            series_1 = pd.read_csv(
                filename[0], squeeze=True)
        else:
            series_1 = pd.read_json(
                filename[0], squeeze=True)
        # print(series_1)
        c = len(series_1.columns)
        return


app = QApplication(sys.argv)
window = MyWindow()

window.show()

sys.exit(app.exec_())
