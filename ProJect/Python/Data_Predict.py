import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima_model import ARIMA, ARIMAResults
from keras.models import load_model

from sklearn.metrics import mean_squared_error
from math import sqrt

import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

# from statsmodels.tsa.arima_model import ARIMAResults
from keras.models import load_model

Data_Predict_ui = '../_uiFiles/Data_Predict.ui'


class Data_Predict(QDialog):
    def __init__(self, parent):
        super(Data_Predict, self).__init__(parent)
        uic.loadUi(Data_Predict_ui, self)
        try:
            self.data = parent.series_1
        except:
            self.show()

        # 다이어로그 크기
        self.W = int(parent.main_width) // 5 * 4
        self.H = int(parent.main_height) // 5 * 4
        self.setFixedSize(self.W, self.H)

        # 모델 불러오기
        self.show()

        self.Import_Data.setStyleSheet(
            'image:url(../images/dataset.webp); background-color:white; border:0px;')
        self.Import_Model.setStyleSheet(
            'image:url(../images/model.png); background-color:white; border:0px;')

        self.predict_pushbutton.setStyleSheet(
            'image:url(../images/predict.JPEG); background-color:white; border:0px;'
        )

        # pushbutton
        self.Import_Data.setCursor(QCursor(Qt.PointingHandCursor))
        self.Import_Data.clicked.connect(self.Open_File)
        self.Import_Model.setCursor(QCursor(Qt.PointingHandCursor))
        self.Import_Model.clicked.connect(self.showModel)
        self.predict_pushbutton.setCursor(QCursor(Qt.PointingHandCursor))
        self.predict_pushbutton.clicked.connect(self.predict)

        # 데이터 불러오기 및 그래프 레이아웃
        # self.start_prediction.setPlaceholderText("값을 입력해 주세요.")
        # self.setFocus()

        # 불러온 모델 학습
        # self.prediction.clicked.connect(self.predict)

        # 파일 저장
        self.save_csv.clicked.connect(self.csv_save)
        self.save_graph.clicked.connect(self.graph_save)

    def Open_File(self):
        self.showFile()
        if self.filename[0] == '':
            return
        # self.start_prediction.setPlaceholderText(
        #     'ex) ' + str(self.data.iloc[self.r - 1, 0]))

    def showFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        self.filename = QFileDialog.getOpenFileName(
            self, "파일열기", "", "(*.csv);;(*.json)")

        if self.filename[0] == '':
            return
        if self.filename[0][-1] == 'v':
            try:
                self.data = pd.read_csv(
                    self.filename[0], squeeze=True)
                try:
                    if int(self.data.columns[0]) or float(self.data.columns[0]):
                        c = self.data.shape[1]
                        head = [str(i)+'열' for i in range(1, c + 1)]
                        self.data = pd.read_csv(
                            self.filename[0], squeeze=True, names=head, encoding='cp949'
                        )
                except:
                    pass
            except:
                self.data = pd.read_csv(
                    self.filename[0], squeeze=True, encoding='cp949')
                c = self.data.shape[1]
                head = [str(i)+'열' for i in range(1, c + 1)]
                self.data = pd.read_csv(
                    self.filename[0], squeeze=True, names=head, encoding='cp949'
                )

        else:
            self.data = pd.read_json(
                self.filename[0], squeeze=True)
        self.c = len(self.data.columns)
        self.r = len(self.data.index)
        self.data_file = self.data.columns
        self.data_load = self.data
        print(type(self.data_load))
        # print(self.data_file)

        return self.showTable()

    def showModel(self):
        # self.loaded_model = QFileDialog.getOpenFileName(
        #     self, 'Open Folder', "../save", "(*.h5);;")
        # if self.loaded_model[0] == '':
        #     return
        # # self.model = parent.loaded_model
        # self.model_name = ''
        # start_save = 0
        # for i in range(len(self.loaded_model[0])-1, -1, -1):

        #     if self.loaded_model[0][i] == '.':
        #         start_save = 1
        #         continue
        #     if self.loaded_model[0][i] == '/':
        #         start_save = 0

        #     if start_save == 0:
        #         continue
        #     self.model_name += self.loaded_model[0][i]
        # print(self.model_name)
        # test = ARIMAResults.load(
        #     f'../save/{self.model_name[::-1]}.h5')  # ARIMA 불러오는 방식

        # model = self.model_fit
        load_file = QFileDialog.getOpenFileName(
            self, '파일열기', '', '(*.pkl);; (*.h5)')
        if load_file[0][-3:] == 'pkl':
            # print(load_file[0][-3:])

            self.model_fit = ARIMAResults.load(load_file[0])

        else:
            self.model_fit = load_model(load_file[0])
        QMessageBox.about(self, "Alert", "성공적으로 불러왔습니다.")

    def showTable(self):
        self.tableWidget.setRowCount(self.r)
        self.tableWidget.setColumnCount(self.c)
        self.tableWidget.setHorizontalHeaderLabels(self.data.columns)

        for i in range(self.r):
            for j in range(self.c):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(self.data.iloc[i, j])))
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def predict(self):

        # 예측기간

        # self.s = self.start_prediction.text()
        # self.l = self.last_prediction.text()

        self.p = self.predict_periods.text()

        num_rows = self.tableWidget.rowCount()
        print(self.tableWidget.rowCount())
        num_cols = self.tableWidget.columnCount()
        print(self.tableWidget.columnCount())

        col = self.data_file

        self.tmp_df = pd.DataFrame(
            columns=col, index=range(num_rows))

        # print(tmp_df)
        # for i in range(num_rows):
        #     for j in range(num_cols):
        #         print(self.tableWidget.item(i, j))
        #         # print(self.tableWidget.item(i, j))
        #         tmp_df.iloc[i, j] = self.tableWidget.item(i, j)
        # tmp_df.iloc[i, j] = QtWidgets.QTableWidgetItem(
        #     self.tableWidget.item(i, j).text())
        print(type(self.tmp_df))
        print("pass")

        try:
            if int(self.data_load.iloc[self.r - 1, 0]):
                self.tableWidget.clear()
                # print(type(self.data_load))
                # print(self.data_file)

                self.tableWidget.setRowCount(int(self.p))
                r = 0
                p = 0
                self.tableWidget.setHorizontalHeaderLabels(self.data_file)
                for i in range(int(self.data_load.iloc[self.r - 1, 0]) + 1, int(self.data_load.iloc[self.r - 1, 0]) + int(self.p)+1):
                    self.tableWidget.setItem(
                        r, 0, QTableWidgetItem(str(i)))
                    # print(i)
                    self.tmp_df.iloc[p, 0] = str(i)
                    p += 1
                    r += 1
                c = 0
                print(self.tmp_df)
                print(type(self.tmp_df))
                self.tableWidget.setEditTriggers(
                    QAbstractItemView.NoEditTriggers)
                # self.tmp_df = self.tableWidget.currentItem()
                # print(self.data_load)
                # print(type(self.data_load))

        except:
            pass

        # X = self.data.iloc[:, 1].values()
        # test = X.astype('float32')
        # months_in_year = 1
        # series_studying = X[:self.studying_rate_length]
        # series_verification = X[self.studying_rate_length:
        #                                           self.studying_rate_length+self.verification_rate_length]
        # print(self.data_load.index)
        # len_arr = int(self.l) - int(self.data_load.index[-1])

        # 아리마 분석
        # history = [x for x in test]
        # predictions = list()
        # yhat = float(self.model_fit.forecast()[0])
        # yhat = self.inverse_difference(history, yhat, months_in_year)
        # # print(yhat)
        # predictions.append(yhat)
        # history.append(yhat)
        # for i in range(1,len_arr):
        #     diff = self.difference(history, months_in_year)
        #     # print(diff)
        #     model = ARIMA(diff, order=(1,1,0))
        #     self.model_fit = model.fit(trend='nc', disp=0)
        #     yhat = self.model_fit.forecast()[0]
        #     yhat = self.inverse_difference(history, yhat, months_in_year)
        #     print(yhat)
        #     predictions.append(yhat[0])
        #     history.append(yhat[0])
        #     print(f'총 {len_arr} 학습 중 {i}번 째 학습 중{yhat}')

        # xhat = x

        # print(self.data_load['data'])
        # forecast = self.model_fit.predict(
        #     self.data_load['data'], n_periods=len_arr)
        # print(forecast)
        # plt.plot(forecast)
        # plt.show()

        # model_fit.plot_predict()
        # fore = self.model_fit.forecast(steps=len_arr)

        # 예측값
        # if len(predictions) == 1:
        #     print(predictions)
        # else:
        #     # x = pd.Series(predictions, index=series_verification.index)
        #     self.rmse = sqrt(mean_squared_error(
        #         series_verification, predictions))
        # print(self.rmse)

        # print(f'예측값 : {self.predict_value}')
        # print('end')
        # plt.plot(predictions, color='red')
        # plt.show()

    # def difference(self, dataset, interval=1):
    #     diff = list()
    #     for d in range(interval, len(dataset)):
    #         value = dataset[d] - dataset[d - interval]
    #         diff.append(value)
    #     return pd.Series(diff)

    # def inverse_difference(self, history, yhat, interval=1):
    #     return yhat + history[-interval]

    def csv_save(self):

        # # dataframe로 변환
        # num_rows = self.tableWidget.rowCount()
        # print(self.tableWidget.rowCount())
        # num_cols = self.tableWidget.columnCount()
        # print(self.tableWidget.columnCount())

        # col = self.data_file

        # tmp_df = pd.DataFrame(
        #     columns=col, index=range(num_rows))

        # # print(tmp_df)
        # for i in range(num_rows):
        #     for j in range(num_cols):
        #         print(self.tableWidget.item(i, j))
        #         # print(self.tableWidget.item(i, j))
        #         tmp_df.iloc[i, j] = self.tableWidget.item(i, j)
        #         # tmp_df.iloc[i, j] = QtWidgets.QTableWidgetItem(
        #         #     self.tableWidget.item(i, j).text())
        # print(type(tmp_df))
        # print("pass")
        # print('csv_save')
        # print(self.tmp_df)
        csv = self.tmp_df
        savefile = QFileDialog.getSaveFileName(self, '파일저장', '', '(*.csv)')
        csv.to_csv(savefile[0], index=False)

    def graph_save(self):
        print('graph_save')
