import sys
import pybithumb
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem

tickers = pybithumb.get_tickers()[:5]
form = uic.loadUiType("../res/table.ui")[0]


class TablePractice(QMainWindow, form):
    def __init__(self):
        super(TablePractice, self).__init__()
        # ui 파일을 적용합니다.
        self.setupUi(self)
        # 테이블 행 사이즈를 지정합니다.
        self.tb_main.setRowCount(len(tickers))

        # 타이머를 적용합니다.
        timer = QTimer(self)
        timer.start(500)
        timer.timeout.connect(self.timeout)

    # 테이블 행에 넣을 마켓 데이터를 가져오는 함수
    def get_marget_info(self, ticker):
        # 빗썸 서버에서 가상화폐에 대한 데이터를 가져옵니다.
        df = pybithumb.get_candlestick(ticker)
        # 종가에 대해 5일 간격의 이동평균을 구합니다.
        mean_average = df['close'].rolling(5).mean()
        # 전날의 이동평균값을 가져옵니다.
        last_mean_average = mean_average[-2]
        price = pybithumb.get_current_price(ticker)

        if price > last_mean_average:
            state = "상승장"
        else:
            state = "하락장"

        return price, last_mean_average, state

    def timeout(self):
        for i, ticker in enumerate(tickers):
            price, last_average, state = self.get_marget_info(ticker)
            self.tb_main.setItem(i, 0, QTableWidgetItem(ticker))
            self.tb_main.setItem(i, 1, QTableWidgetItem(str(price)))
            self.tb_main.setItem(i, 2, QTableWidgetItem(str(last_average)))
            self.tb_main.setItem(i, 3, QTableWidgetItem(state))


app = QApplication(sys.argv)
window = TablePractice()
window.show()
app.exec_()
