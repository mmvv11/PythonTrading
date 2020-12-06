"""
전략 검증을 위한 백테스팅
테스트용 데이터를 얻기위해, 그동안 비트코인 일봉을 csv형태로 저장합니다.
"""

import pybithumb
import numpy as np

df = pybithumb.get_candlestick("BTC")  # 비트코인 일봉 데이터
df['range'] = (df['high'] - df['low']) * 0.5  # 변동폭, range 컬럼 추가
df['target'] = df['open'] + df['range'].shift(1)  # shift 메서드는 컬럼 값의 행을 내려준다.,, 목표가 계산
# 백테스팅을 위한 데이터 준비완료!

# 수익률(ror) 고가가 목표가보다 크면, 그날은 매수를 한 날이고, 수익률은 종가(매도가)/목표가(매수가)이다.
# 매수를 하지 않았다면 수익률은 원금 그대로 1이다.
df['ror'] = np.where(df['high'] > df['target'], df['close'] / df['target'], 1)

# cumprod는 해당 열의 값을 모두 곱하여 반환한다. 즉, 해당 기간동안의 수익률을 나타낸다.
ror = df['ror'].cumprod()[-2]
print(ror)

