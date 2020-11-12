# 디자인툴로 만든 ui 객채를 생성합니다.
import pykorbit
from PyQt5 import uic
from PyQt5.QtCore import QTime, QTimer
from PyQt5.QtWidgets import QMainWindow

design = uic.loadUiType("../res/test.ui")[0]


# PyQt
class KorbitPractice(QMainWindow, design):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.timer = QTimer(self)
        self.timer.start(5000)  # 5초마다 스케쥴링을 합니다.
        self.timer.timeout.connect(self.get_btc_price)  # 5초마다 실행할 함수를 conncet 합니다.

    def get_btc_price(self):
        current_time = QTime.currentTime().toString("hh:mm:ss")
        self.statusBar().showMessage(current_time)
        price = pykorbit.get_current_price("BTC")
        self.text_show_btc_price.setText(str(price))
