import sys
import os
import pandas as pd
import numpy
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA, ARIMAResults
from keras.models import load_model
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from sklearn.metrics import mean_squared_error
from math import sqrt

import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

from keras.models import load_model

Data_Predict_ui = '../_uiFiles/Data_Predict1.ui'


class Data_Predict(QDialog):
    def __init__(self, parent):
        super(Data_Predict, self).__init__(parent)
        uic.loadUi(Data_Predict_ui, self)
        self.show()

        # 다이어로그 크기
        self.w = parent.w
        self.h = parent.h
        self.setFixedSize(self.w, self.h)
        self.center()

        # 그래프

        # plt.style.use(color='#19232D')
        self.fig = plt.Figure()
        self.fig.set_facecolor("None")
        self.canvas = FigureCanvas(self.fig)
        self.result_gridLayout.addWidget(self.canvas)

        # 모델 불러오기
        self.data = 'x'
        self.model_fit = 'x'
        self.show()

        self.Import_Data.setStyleSheet(
            'image:url(../images/dataset2.webp); background-color:rgb(25,35,45); border-width:5px; ')
        self.Import_Model.setStyleSheet(
            'image:url(../images/model1.webp); background-color:rgb(25,35,45); border-width:5px;')

        self.predict_pushbutton.setStyleSheet(
            'image:url(../images/prediction7.png); background-color:rgb(25,35,45); border-width:5px;'
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

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


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
                # print('1')
                # print(self.filename)
                self.data_name1 = self.filename[0][::-1]
                self.res1_name = ''
                for i in self.data_name1:
                    if i == '/':
                        break
                    else:
                        self.res1_name = i + self.res1_name
                self.data_name.setText(self.res1_name)
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

        for i in self.data.columns:
            self.comboBox_x.addItem(i)
            self.comboBox_y.addItem(i)
        # print(type(self.data[self.comboBox_x.currentText()][0]))
        if type(self.data[self.comboBox_x.currentText()][0]) == str:
            print('hello')
            try:
                self.data[self.comboBox_x.currentText()] = pd.to_datetime(self.data[self.comboBox_x.currentText()], format='%Y-%m-%d')
            except:
                print('잘못왔어요')
                pass
        print(type(self.data[self.comboBox_x.currentText()][0]))
        self.c = len(self.data.columns)
        self.r = len(self.data.index)
        self.data_file = self.data.columns
        self.data_load = self.data
        # print(type(self.data_load))
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
        self.load_file = QFileDialog.getOpenFileName(
            self, '파일열기', '', '(*.pkl);; (*.h5)')
        # print('1')
        # print(self.load_file)
        try:
            if self.load_file[0][-3:] == 'pkl':
                # print(load_file[0][-3:])

                self.model = ARIMAResults.load(self.load_file[0])
                # print('2')
                # print(self.load_file)
                self.name = self.load_file[0][::-1]
                self.res_name = ''
                for i in self.name:
                    if i == '/':
                        break
                    else:
                        self.res_name = i + self.res_name
                # print(self.res_name)


            else:
                self.model = load_model(load_file[0])
        except:
            return
        QMessageBox.about(self, "Alert", "성공적으로 불러왔습니다.")
        self.model_name.setText(self.res_name)
        print('3')
        print(self.model_name)

    def showTable(self):
        self.tableWidget.setRowCount(self.r)
        self.tableWidget.setColumnCount(self.c)
        self.tableWidget.setHorizontalHeaderLabels(self.data.columns)
        
        for i in range(self.r):
            for j in range(self.c):
                if type(self.data.iloc[i, j]) == pd._libs.tslibs.timestamps.Timestamp:
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(self.data.iloc[i, j].to_pydatetime().strftime('%Y-%m-%d')))
                else:
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(str(self.data.iloc[i, j])))
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)


    def predict(self):
        try:
            if self.data == 'x':
                QMessageBox.about(self, "Alert", "데이터를 불러와 주세요.")
                return
        except:
            pass
        try:
            if self.model == 'x':
                QMessageBox.about(self, "Alert", "모델을 불러와 주세요.")
                return
        except:
            pass
        print(self.res_name[-3:])
        if self.comboBox_x.currentText() == self.comboBox_y.currentText():
            QMessageBox.about(self, "Alert", "x축 y축을 다르게 설정해주세요.")
            return
        if self.predict_periods.text() == '':
            QMessageBox.about(self, "Alert", "기간을 설정해주세요.")
            return
        if self.res_name[-3:] == 'pkl':
            self.fig.clear()
            ax = self.fig.add_subplot(1, 1, 1)
            series_data = pd.Series(list(self.data[self.comboBox_y.currentText()]), index=self.data[self.comboBox_x.currentText()])
            self.model = self.model.apply(series_data, refit=True )
            self.model_fit = self.model.model.fit()
            self.model.summary()
            print(self.model.summary())

            # 예측기간

        self.fig.clear()
        ax = self.fig.add_subplot(1, 1, 1)
        self.fig.set_facecolor("white")
        series_data = pd.Series(list(self.data[self.comboBox_y.currentText()]), index=self.data[self.comboBox_x.currentText()])
        self.model = self.model.apply(series_data, refit=True )
        self.model_fit = self.model.model.fit()
        self.model.summary()
        print(self.model.summary())

        # 예측기간

        # self.s = self.start_prediction.text()
        # self.l = self.last_prediction.text()

        self.p = self.predict_periods.text()

        self.fore = self.model_fit.forecast(steps=int(self.p))
        ax.plot(series_data)
        ax.plot(self.fore)
        ax.grid()
        self.canvas.draw()
        print(self.fore)
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

            self.p = self.predict_periods.text()

            self.fore = self.model_fit.forecast(steps=int(self.p))
            print(series_data)
            print(self.fore)
            ax.plot(series_data)
            ax.plot(self.fore)
            ax.grid()
            self.canvas.draw()
            print(self.fore)
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
                    self.tableWidget.setHorizontalHeaderLabels(self.data_file)
                    for i in range(int(self.data_load.iloc[self.r - 1, 0]) + 1, int(self.data_load.iloc[self.r - 1, 0]) + int(self.p)+1):
                        self.tableWidget.setItem(
                            r, 0, QTableWidgetItem(str(i)))
                        # print(i)
                        self.tmp_df.iloc[r, 0] = str(i)
                        self.tmp_df.iloc[r, 1] = self.fore[r]
                        r += 1
                    c = 0
                    print(self.tmp_df)
                    print(type(self.tmp_df))
                    self.tableWidget.setEditTriggers(
                        QAbstractItemView.NoEditTriggers)
                    # self.tmp_df = self.tableWidget.currentItem()
                    # print(self.data_load)
                    # print(type(self.data_load))

                # else:
                #     print(self.data_load.iloc[self.r - 1, 1])

            except:

                if pd.to_datetime(self.data_load.iloc[self.r - 1, 0], format='%YYYY%MM%DD'):
                    self.date_time = pd.date_range(self.data_load.iloc[self.r - 1, 0], periods=int(self.p) + 1, freq='D')
                print(pd.date_range(self.data_load.iloc[self.r - 1, 0], periods=int(self.p) + 1, freq='D'))
            
                self.tableWidget.clear()

                self.p = self.predict_periods.text()

                col = self.data_file

                self.tmp_df = pd.DataFrame(
                    columns=col, index=range(int(self.p)))    

                self.tableWidget.setRowCount(int(self.p))
                r = 0
                self.tableWidget.setHorizontalHeaderLabels(self.data_file)

                for i in self.date_time[1:]:
                    self.tableWidget.setItem(
                        r, 0, QTableWidgetItem(str(i)))
                    self.tableWidget.setItem(
                        r, 1,  QTableWidgetItem(str(self.fore[r])))
                    self.tmp_df.iloc[r, 0] = str(i)
                    self.tmp_df.iloc[r, 1] = self.fore[r]
                    r += 1
                c = 0
                print(self.tmp_df)
                print(type(self.tmp_df))
                self.tableWidget.setEditTriggers(
                    QAbstractItemView.NoEditTriggers)
            print(self.data)
            
            # forecast = self.model.predict()
            # print(forecast)
            print('hi')
    #     X = self.data.iloc[:,1].values
    #     test = X.astype('float32')
    #     months_in_year = 1
    #     # series_studying = X[:self.studying_rate_length]
    #     # series_verification = X[self.studying_rate_length:
    #     #                                           self.studying_rate_length+self.verification_rate_length]
    #     # print(self.data_load.index)
    #     len_arr = int(self.l) - int(self.data_load.index[-1])
        
    #     # 아리마 분석
    #     # history = [x for x in test]
    #     # predictions = list()
    #     # yhat = float(self.model_fit.forecast()[0])
    #     # yhat = self.inverse_difference(history, yhat, months_in_year)
    #     # # print(yhat)
    #     # predictions.append(yhat)
    #     # history.append(yhat)
    #     # for i in range(1,len_arr):
    #     #     diff = self.difference(history, months_in_year)
    #     #     # print(diff)
    #     #     model = ARIMA(diff, order=(1,1,0))
    #     #     self.model_fit = model.fit(trend='nc', disp=0)
    #     #     yhat = self.model_fit.forecast()[0]
    #     #     yhat = self.inverse_difference(history, yhat, months_in_year)
    #     #     print(yhat)
    #     #     predictions.append(yhat[0])
    #     #     history.append(yhat[0])
    #     #     print(f'총 {len_arr} 학습 중 {i}번 째 학습 중{yhat}')
        
    #     # xhat = x

    #     print(self.data_load['data'])
    #     forecast = self.model_fit.predict(self.data_load['data'], n_periods=len_arr)
    #     print(forecast)
    #     plt.plot(forecast)
    #     plt.show()

    #     # model_fit.plot_predict()
    #     # fore = self.model_fit.forecast(steps=len_arr)

    #     # 예측값
    #     # if len(predictions) == 1:
    #     #     print(predictions)
    #     # else:
    #     #     # x = pd.Series(predictions, index=series_verification.index)
    #     #     self.rmse = sqrt(mean_squared_error(
    #     #         series_verification, predictions))
    #     # print(self.rmse)

    #     # print(f'예측값 : {self.predict_value}')
    #     print('end')
    #     plt.plot(predictions, color='red')
    #     plt.show()

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
        csv = self.tmp_df
        savefile = QFileDialog.getSaveFileName(self, '파일저장', '', '(*.csv)')
        csv.to_csv(savefile[0], index=False)

    def graph_save(self):
        print('graph_save')