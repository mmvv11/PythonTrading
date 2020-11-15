import pybithumb
import time
import schedule


from BasicPractice.BitumbOfficialSampleCode.bithumb import bithumb
from BasicPractice.logger import *

target_price = pybithumb.get_current_price("BTC")
current_price = pybithumb.get_current_price("BTC")


# 목표가 갱신 함수
def get_target_price():
    global target_price

    try:
        df = pybithumb.get_candlestick("BTC")
        yesterday = df.iloc[-2]

        today_open = yesterday['close']  # 오늘 시가 = 전날 종가
        yesterday_high = yesterday['high']  # 전날 고가
        yesterday_low = yesterday['low']  # 전날 저가
        target_price = today_open + (yesterday_high - yesterday_low) * 0.5  # 목표가 = 오늘 시가 + (전날 변동폭)* 0.5
        now = time.localtime()
        print("목표가 갱신 시각:",
              "%04d/%02d/%02d %02d:%02d:%02d" % (
              now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))

    except:
        # todo 에러 로그 남기는 방법
        logger.error("hi")


    sell_bitcoin()  # 매도 시도


# 매수 시도 함수
def buy_bitcoin():
    if current_price > target_price:
        krw = bithumb.get_balance("BTC")[2]  # 보유중인 원화 조회
        order_book = pybithumb.get_orderbook("BTC")  # 비트코인 호가 정보 조회
        sell_price = order_book['asks'][0]['price']  # 최상단 매도 호가 조회 (가장 저렴하게 매수할 수 있는 가격)
        unit = krw / float(sell_price)  # 현재 잔액으로 매수 가능한 비트코인 갯수
        bithumb.buy_market_order("BTC", unit)  # 매수


# 매도 시도 함수
def sell_bitcoin():
    unit = bithumb.get_balance("BTC")[0]  # 보유중인 비트코인 수량
    bithumb.sell_market_order("BTC", unit)  # 매도


# 자정에 목표가 갱신하기
schedule.every(5).seconds.do(get_target_price)
while True:
    try:
        schedule.run_pending()
        buy_bitcoin()  # 매수 시도
    except:
        pass
    time.sleep(1)
