import sys
import os
import Data_Dialog
import Train_Dialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

import Data_Predict
Main_ui = '../_uiFiles/Main.ui'


class MyWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None)
        uic.loadUi(Main_ui, self)
        self.setWindowTitle("S-Prediction")
        self.setWindowIcon(QIcon("../images/icon.ico"))
        self.showMaximized()

        self.setWindowIcon(QIcon("../images/web_icon.png"))

        self.Dataset_pushButton.setStyleSheet(
            "image:url(../images/dataset.webp); background-color:white; border:0px;")
        self.Training_pushButton.setStyleSheet(
            "image:url(../images/Training.png); background-color:white; border:0px;")
        # self.Test_pushButton.setStyleSheet(
        #     "image:url(../images/dataset.webp); background-color:white; border:0px;")
        self.Test_pushButton.setStyleSheet(
            "image:url(../images/test.png); background-color:white; border:0px;")
        self.Dataset_pushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Training_pushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.Test_pushButton.setCursor(QCursor(Qt.PointingHandCursor))
        # File Button
        self.Dataset_pushButton.clicked.connect(self.Open_File)
        self.Training_pushButton.clicked.connect(self.TrainBtn_pushed)
        self.Test_pushButton.clicked.connect(self.Import_modelBtn_pushed)

        self.main_width = QApplication.desktop().screenGeometry().width()
        self.main_height = QApplication.desktop().screenGeometry().height()
        self.w = self.main_width // 5 * 4
        self.h = self.main_height // 5 * 4
    def Open_File(self):
        self.showFile()
        if self.filename[0] == '':
            return
        Data_Dialog.new_Dialog(self)
        

    def showFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        self.filename = QFileDialog.getOpenFileName(
            self, "파일열기", "", "(*.csv);;(*.json)")

        if self.filename[0] == '':
            return
        if self.filename[0][-1] == 'v':
            try:
                self.series_1 = pd.read_csv(
                    self.filename[0], squeeze=True)
                try:
                    if int(self.series_1.columns[0]) or float(self.series_1.columns[0]):
                        c = self.series_1.shape[1]
                        head = [str(i)+'열' for i in range(1, c + 1)]
                        self.series_1 = pd.read_csv(
                            self.filename[0], squeeze=True, names=head, encoding='cp949'
                        )
                except:
                    pass
            except:
                self.series_1 = pd.read_csv(
                    self.filename[0], squeeze=True, encoding='cp949')
                c = self.series_1.shape[1]
                head = [str(i)+'열' for i in range(1, c + 1)]
                self.series_1 = pd.read_csv(
                    self.filename[0], squeeze=True, names=head, encoding='cp949'
                )

        else:
            self.series_1 = pd.read_json(
                self.filename[0], squeeze=True)
        self.c = len(self.series_1.columns)
        self.r = len(self.series_1.index)
        print(self.series_1.isnull().sum())
        # for i in range(self.c):
        #     print(self.series_1.iloc[:, i:i+1].isnull().sum())

    def TrainBtn_pushed(self):
        Train_Dialog.Train_Dialog(self)

    def Import_modelBtn_pushed(self):

        # ARIMA_Analysis_Dialog_1.ARIMA_Analysis_Dialog(self)
        Data_Predict.Data_Predict(self)


app = QApplication(sys.argv)
window = MyWindow()

window.show()

sys.exit(app.exec_())
