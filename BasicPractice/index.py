# 실습에 필요한 모듈을 가져옵니다.

import sys
from PyQt5.QtWidgets import *
from BasicPractice.KorbitPractice import KorbitPractice

app = QApplication(sys.argv)
window = KorbitPractice()
window.show()
app.exec_()