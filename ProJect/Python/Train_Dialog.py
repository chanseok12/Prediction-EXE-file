import sys
import pandas as pd
import PyQt5
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error
from math import sqrt
from pmdarima.arima import auto_arima
from pmdarima.arima import ADFTest
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import LSTM
Train_Dialog_UI = "../_uiFiles/Train_Dialog.ui"


class Train_Dialog(QDialog):
    def __init__(self, parent):
        super(Train_Dialog, self).__init__(parent)
        uic.loadUi(Train_Dialog_UI, self)

        try:
            self.data = parent.series_1
        except:
            QMessageBox.about(self, "Alert", "분석하고 싶은 파일을 먼저 불러와주세요")
            return

        self.w = parent.w
        self.h = parent.h
        self.c = parent.c
        self.setFixedSize(parent.w, parent.h)

        self.LSTMcomboboxes = [
            self.Date_combobox,
            self.Open_combobox,
            self.High_combobox,
            self.Low_combobox,
            self.Close_combobox,
            self.AdjClose_combobox,
            self.Volume_combobox
        ]
        self.Train_pushButton.clicked.connect(self.LSTM_Train)

        self.LSTM_setupUI()
        self.parent = parent
        self.p_value = 0
        self.d_value = 0
        self.q_value = 0
        self.c_nc = 'c'
        self.day = 12
        self.fig = plt.Figure()
        self.fig.set_facecolor("none")
        self.fig2 = plt.Figure()
        self.fig2.set_facecolor("none")
        self.canvas = FigureCanvas(self.fig)
        self.canvas2 = FigureCanvas(self.fig2)
        self.canvas2.hide()
        self.arima_gridLayout.addWidget(self.canvas)
        self.arima_gridLayout.addWidget(self.canvas2)
        # self.plus_pushButton.clicked.connect(self.plus_Btn_pushed)
        # self.minus_pushButton.clicked.connect(self.minus_Btn_pushed)

        for i in self.data.columns:
            self.comboBox_x.addItem(i)
            self.comboBox_y.addItem(i)

        self.show()
        self.model_save_pushButton.clicked.connect(self.model_save_pushed)
        self.progressBar.hide()
        self.Run_pushButton.clicked.connect(self.Run_Dialog)
        self.auto_arima_pushButton.clicked.connect(self.auto_arima_pushed)

        self.rmse_label.setMinimumWidth(self.w // 3 * 0.8)
        self.arima_groupBox.setMinimumWidth(self.w // 2 * 0.9)
        self.groupBox.setMinimumWidth(self.w // 2 * 0.9)

    def Run_Dialog(self):
        if self.studying_rate.text() == '':
            QMessageBox.about(self, "Alert", "학습 비율을 입력해주세요")
            return
        elif int(self.studying_rate.text()) < 0:
            QMessageBox.about(self, "Alert", "학습 비율을 양수로 입력해주세요")
            return
        elif self.verification_rate.text() == '':
            QMessageBox.about(self, "Alert", "검증 비율을 입력해주세요")
            return
        elif int(self.verification_rate.text()) < 0:
            QMessageBox.about(self, "Alert", "검증 비율을 양수로 입력해주세요")
            return
        elif self.test_rate.text() == '':
            QMessageBox.about(self, "Alert", "테스트 비율을 입력해주세요")
            return
        elif int(self.test_rate.text()) < 0:
            QMessageBox.about(self, "Alert", "테스트 비율을 양수로 입력해주세요")
            return

        # Load한 파일의 행의 길이 측정 및 학습, 검증, 테스트 비율로 csv파일 길이 나눔
        # csv로 기준
        self.total_len = int(self.studying_rate.text()) + \
            int(self.verification_rate.text()) + int(self.test_rate.text())
        self.studying_rate_length = len(self.data) * \
            int(self.studying_rate.text()) // self.total_len
        self.verification_rate_length = len(
            self.data) * int(self.verification_rate.text()) // self.total_len

        # self.series_studying = self.data.iloc[:studying_rate_length]
        # self.series_verification = self.data.iloc[studying_rate_length:
        #                                           studying_rate_length+verification_rate_length]
        # self.series_test = self.data.iloc[studying_rate_length +
        #                                   verification_rate_length:]
        ###############################################################
        # 분석 기법 선택
        if self.study_tabWidget.currentIndex() == 0:
            self.ARIMA_run(pd.Series(list(self.data[self.comboBox_y.currentText(
            )]), index=self.data[self.comboBox_x.currentText()]))
        elif self.study_tabWidget.currentIndex() == 1:
            pass

    def difference(self, dataset, interval=1):
        diff = list()
        for d in range(interval, len(dataset)):
            value = dataset[d] - dataset[d - interval]
            diff.append(value)
        return pd.Series(diff)

    def inverse_difference(self, history, yhat, interval=1):
        return yhat + history[-interval]

    def ARIMA_run(self, series):
        if self.comboBox_x.currentText() == self.comboBox_y.currentText():
            QMessageBox.about(self, "Alert", "x축 y축을 다르게 설정해주세요.")
            return
        
        self.rmse_label.clear()
        self.fig.clear()
        self.fig2.clear()
        
        try:
            series[self.comboBox_x.currentText()] = pd.to_datetime(
                series[self.comboBox_x.currentText()])
            series.set_index(self.comboBox_x.currentText(), inplace=True)
        except:
            pass
        # X = series.values
        series.astype('float32')
        print(series)
        print('hi')
        # if self.c_nc_comboBox.currentText() == '일간':
        #     self.day = 'D'
        # elif self.c_nc_comboBox.currentText() == '주간':
        #     self.day = 'W'
        # elif self.c_nc_comboBox.currentText() == '월간':
        #     self.day = 'M'
        # elif self.c_nc_comboBox.currentText() == '분기':
        #     self.day = 'Q'
        # else:
        #     self.day = 'A'
        months_in_year = 1
        series_studying = series[:self.studying_rate_length]
        series_verification = series[self.studying_rate_length:
                                self.studying_rate_length+self.verification_rate_length]
        series_test = series[self.studying_rate_length +
                                  self.verification_rate_length:]

        len_arr = len(series_verification)
        self.progressBar.setMaximum(len_arr)
        self.progressBar.show()

        # 아리마 분석
        history = [x for x in series_studying]
        predictions = list()
        diff = self.difference(history, months_in_year)
        print(self.day)
        # model = ARIMA(diff, order=(self.p_value, self.d_value, self.q_value), freq=self.day)
        model = sm.tsa.statespace.SARIMAX(diff, order=(self.p_value, self.d_value, self.q_value), seasonal_order=(self.p_value, self.d_value, self.q_value,12))
        model_fit = model.fit()
        yhat = model_fit.predict()
        yhat = self.inverse_difference(history, yhat, months_in_year)
        predictions.append(yhat[0])
        print(series_verification)
        history.append(series_verification.iloc[0])
        self.time = self.progressBar.value()
        self.time += 1
        self.progressBar.setValue(self.time)

        for i in range(1, len(series_verification)):
            diff = self.difference(history, months_in_year)
            print(diff)
            # model = ARIMA(diff, order=(
            #     self.p_value, self.d_value, self.q_value))
            model = sm.tsa.statespace.SARIMAX(diff, order=(self.p_value, self.d_value, self.q_value), seasonal_order=(self.p_value, self.d_value, self.q_value,12))
            self.model_fit = model.fit()
            yhat = self.model_fit.predict()
            print(yhat)
            yhat = self.inverse_difference(history, yhat, months_in_year)
            predictions.append(yhat[0])
            history.append(series_verification.iloc[i])
            print(series_verification.iloc[i])
            print(f'총 {len_arr} 학습 중 {i}번 째 학습 중{yhat}')
            self.rmse_label.setText(f'총 {len_arr} 학습 중 {i}번 째 학습 중')
            self.time += 1
            self.progressBar.setValue(self.time)

        # forecast = self.model_fit.predict()
        print(predictions)

        # model_fit.plot_predict()
        # fore = self.model_fit.forecast(steps=len_arr)

        # 예측값
        if len(predictions) == 1:
            print(predictions)
        else:
            x = pd.Series(predictions, index=series_verification.index)
            print(x)
            print(series_verification)
            self.rmse = sqrt(mean_squared_error(
                series_verification, x))
        self.rmse_label.setText('rmse: '+str(self.rmse))

        # print(f'예측값 : {self.predict_value}')
        print('end')
        ax = self.fig.add_subplot(1, 1, 1)
        self.fig.set_facecolor("white")
        ax.plot(series_studying)
        ax.plot(series_verification)
        ax.plot(x, color='red')
        ax.grid()
        ax2 = self.fig2.add_subplot(1, 1, 1)
        self.fig2.set_facecolor("white")
        ax2.plot(series_verification)
        ax2.plot(x, color='red')
        ax2.grid()

        self.canvas.draw()
        self.canvas2.draw()
        self.time = 0
        self.progressBar.setValue(self.time)
        self.progressBar.hide()

    def model_save_pushed(self):
        model = self.model_fit
        savefile = QFileDialog.getSaveFileName(self, '파일저장', '', '(*.pkl)')
        print(savefile[0])
        if savefile[0][-7:0] == 'pkl.pkl':
            model.save(savefile[0][:-4])
        else:
            model.save(savefile[0])
        QMessageBox.about(self, "Alert", "저장되었습니다.")

    def auto_arima_pushed(self):
        if self.comboBox_x.currentText() == self.comboBox_y.currentText():
            QMessageBox.about(self, "Alert", "x축 y축을 다르게 설정해주세요.")
            return
        self.total_len = int(self.studying_rate.text()) + \
            int(self.verification_rate.text()) + int(self.test_rate.text())
        self.studying_rate_length = len(self.data) * \
            int(self.studying_rate.text()) // self.total_len
        self.verification_rate_length = len(
            self.data) * int(self.verification_rate.text()) // self.total_len
        self.auto_arima_run(pd.Series(list(self.data[self.comboBox_y.currentText(
        )]), index=self.data[self.comboBox_x.currentText()]))

    def auto_arima_run(self, data):
        self.rmse_label.clear()
        self.fig.clear()
        self.fig2.clear()
        
        # self.adf_test_label.clear()
        try:
            data[self.comboBox_x.currentText()] = pd.to_datetime(
                data[self.comboBox_x.currentText()])
            data.set_index(self.comboBox_x.currentText(), inplace=True)
        except:
            pass
        # adf_test = ADFTest(alpha = 0.05)
        # self.adf_test_label.setText(str(adf_test.should_diff(data)))

        train = data[:self.studying_rate_length + self.verification_rate_length]
        test = data[self.studying_rate_length+self.verification_rate_length:]
        # last = data[self.studying_rate_length+self.verification_rate_length:]
        arima_model1 = auto_arima(train, start_p=0, d=1, start_q=0,
                                  max_p=3, max_d=3, max_q=3, m=12,
                                  start_P=0, D=1, start_Q=0,
                                  max_P=3, max_D=3, max_Q=3,
                                  seasonal=True, trace=True,
                                  error_action='ignore',
                                  suppress_warnings=True,
                                  stepwise=True)
        # arima_model1.summary()

        # arima_model2 = auto_arima(data, start_p=0, d=1, start_q=0,
        #                    max_p=3, max_d=3, max_q=3, m=1,
        #                    start_P=0, D=1, start_Q=0,
        #                    max_P=3, max_D=3, max_Q=3,
        #                    seasonal=True, trace=True,
        #                    error_action='ignore',
        #                    suppress_warnings=True, stepwise=True,
        #                    random_state=20)

        # arima_model2.summary()

        self.model_fit = arima_model1
        # b = arima_model2.fit(train)
        # model = ARIMA(train, order=(1,1,5))
        # model = model.fit()
        # pred = model.predict(start=len(train), end=len(train)+len(test)-1, typ='levels')
        # plt.plot(pred)
        # test.plot(legend=True)

        prediction1 = pd.DataFrame(
            self.model_fit.predict(n_periods=len(test)), index=test.index)
        prediction1.columns = [self.comboBox_y.currentText()]
        rmse1 = sqrt(mean_squared_error(
            test, prediction1[self.comboBox_y.currentText()]))
        self.rmse_label.setText('rmse: '+str(rmse1))
        # print(prediction1.iloc[0])
        # print(rmse1)
        # print(prediction1)
        # prediction2 = pd.DataFrame(b.predict(n_periods=len(test)),index=test.index)
        # prediction2.columns = ['predict']
        # rmse2 = sqrt(mean_squared_error(test, prediction2['predict']))
        # print(rmse2)

        # if rmse1 < rmse2:
        #     self.rmse = rmse1
        #     self.prediction = prediction1
        # else:
        #     self.rmse = rmse2
        #     self.prediction = prediction2
        ax = self.fig.add_subplot(1, 1, 1)
        ax.plot(train)
        ax.plot(test)
        ax.plot(prediction1)
        ax.grid()
        ax2 = self.fig2.add_subplot(1, 1, 1)
        ax2.plot(test)
        ax2.plot(prediction1)
        ax2.grid()
        self.canvas.draw()
        self.canvas2.draw()

    def LSTM_setupUI(self):
        for combo in self.LSTMcomboboxes:
            for idx in range(self.c):
                combo.addItem(self.data.columns[idx])

    def LSTM_Train(self):
        if self.studying_rate.text() == '':
            QMessageBox.about(self, "Alert", "학습 비율을 입력해주세요")
            return
        elif int(self.studying_rate.text()) < 0:
            QMessageBox.about(self, "Alert", "학습 비율을 양수로 입력해주세요")
            return
        elif self.verification_rate.text() == '':
            QMessageBox.about(self, "Alert", "검증 비율을 입력해주세요")
            return
        elif int(self.verification_rate.text()) < 0:
            QMessageBox.about(self, "Alert", "검증 비율을 양수로 입력해주세요")
            return
        elif self.test_rate.text() == '':
            QMessageBox.about(self, "Alert", "테스트 비율을 입력해주세요")
            return
        elif int(self.test_rate.text()) < 0:
            QMessageBox.about(self, "Alert", "테스트 비율을 양수로 입력해주세요")
            return
        elif self.Epochs_linetext.text() == '':
            QMessageBox.about(self, "Alert", "Epochs 값을 입력해주세요")
            return
        elif self.LearningRate_linetext.text() == '':
            QMessageBox.about(self, "Alert", "Learning Rate 값을 입력해주세요")
            return
        elif self.SequenceLength_linetext.text() == '':
            QMessageBox.about(self, "Alert", "Sequence Length 값을 입력해주세요")
            return
        elif self.ModelName_lineText.text() == '':
            QMessageBox.about(self, "Alert", "모델 이름을 지정해주세요")
            return

        stock_file = self.data.loc[:, [self.Date_combobox.currentText()]]
        for combo in self.LSTMcomboboxes:
            if combo == self.Date_combobox:
                continue
            stock_file = pd.merge(
                stock_file, self.data.loc[:, [combo.currentText()]], left_index=True, right_index=True, how='left')

        epoch_num = int(self.Epochs_linetext.text())
        learning_rate = float(self.LearningRate_linetext.text())
        seq_length = int(self.SequenceLength_linetext.text())
        train_ratio = int(self.studying_rate.text()) / (int(self.studying_rate.text()) +
                                                        int(self.verification_rate.text()) + int(self.test_rate.text()))

        Model_name = self.ModelName_lineText.text()

        Model_path = QFileDialog.getExistingDirectory(self, 'Open Folder', '')
        LSTM.Train(stock_file, epoch_num, learning_rate,
                   seq_length, train_ratio, Model_name, Model_path)

    def plus_Btn_pushed(self):
        self.canvas.hide()
        self.canvas2.show()

    def minus_Btn_pushed(self):
        self.canvas2.hide()
        self.canvas.show()