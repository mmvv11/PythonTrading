import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
import pybithumb

tickers = pybithumb.get_tickers()[:5]
form = uic.loadUiType("../res/table.ui")[0]


class RefreshData(QThread):
    finished = pyqtSignal(dict)
    mutex = QMutex()

    def run(self):
        while True:
            data = {}

            for ticker in tickers:
                data[ticker] = self.get_market_info(ticker)

            self.finished.emit(data)
            self.msleep(500)

    def get_market_info(self, ticker):
        try:
            self.mutex.lock()
            df = pybithumb.get_candlestick(ticker)
            mean_average = df['close'].rolling(5).mean()

            price = pybithumb.get_current_price(ticker)
            last_mean_average = mean_average[-2]

            if price > last_mean_average:
                state = "상승장"
            else:
                state = "하락장"

            self.mutex.unlock()
            return [price, last_mean_average, state]
        except:
            print("get_marget_info error")
            self.mutex.unlock()
            return [None, None, None]


class ThreadPractice(QMainWindow, form):
    def __init__(self):
        super(ThreadPractice, self).__init__()
        self.setupUi(self)

        self.tb_main.setRowCount(len(tickers))
        self.refresh_thread = RefreshData()
        self.refresh_thread.finished.connect(self.update_table_data)
        self.refresh_thread.start()

    @pyqtSlot(dict)
    def update_table_data(self, data):
        try:
            for ticker, info in data.items():
                index = tickers.index(ticker)

                self.tb_main.setItem(index, 0, QTableWidgetItem(ticker))
                self.tb_main.setItem(index, 1, QTableWidgetItem(str(info[0])))
                self.tb_main.setItem(index, 2, QTableWidgetItem(str(info[1])))
                self.tb_main.setItem(index, 3, QTableWidgetItem(str(info[2])))
        except:
            print("update_table_data error")
            pass


app = QApplication(sys.argv)
window = ThreadPractice()
window.show()
app.exec_()
