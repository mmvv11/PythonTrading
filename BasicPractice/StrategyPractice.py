"""
변동성 돌파전략을 이용한 비트코인 자동매매
"""

import pybithumb
import time
import schedule

from BasicPractice.BithumbPrivateAPI.bithumb import bithumb
# from BasicPractice.logger import *

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
        print("목표가 갱신 실패")

    sell_bitcoin()  # 매도 시도, 변동성 돌파전략에 의해, 당일 구매한 코인이 있다면 자정에 매도한다.


# 매수 시도 함수 -> 지속적으로 현가를 업데이트하면서 변동성 돌파전략에 의해 구매 타이밍을 노린다.
# 변동성 돌파 전략
# 매수기준: 당일 변동폭의 0.5배 이상 상승하면 해당 가격으로 바로 매수
# 매도기준: 당일 종가 매도
def buy_bitcoin():
    if current_price > target_price: # 변동성 돌파 전략에 의해, 0.5배 이상 상승한 상태에서 바로 매수
        krw = bithumb.get_balance("BTC")[2]  # 보유중인 원화 조회
        order_book = pybithumb.get_orderbook("BTC")  # 비트코인 호가 정보 조회
        sell_price = order_book['asks'][0]['price']  # 최상단 매도 호가 조회 (가장 저렴하게 매수할 수 있는 가격)
        unit = krw / float(sell_price)  # 현재 잔액으로 매수 가능한 비트코인 갯수
        bithumb.buy_market_order("BTC", unit)  # 매수


# 매도 시도 함수
def sell_bitcoin():
    unit = bithumb.get_balance("BTC")[0]  # 보유중인 비트코인 수량
    bithumb.sell_market_order("BTC", unit)  # 매도


# 매일 자정에 목표가 갱신하기
schedule.every().day.at("00:00").do(get_target_price)
while True:
    try:
        schedule.run_pending()
        buy_bitcoin()  # 매수 시도
    except:
        pass
    time.sleep(1)
