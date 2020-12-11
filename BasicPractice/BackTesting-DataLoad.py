"""
    전략 검증을 위한 백테스팅
테스트용 데이터를 얻기위해, 그동안 비트코인 일봉을 csv형태로 저장

    수수료 및 슬리피지
실제로 매매하면 거래소의 수수료가 부과된다.
슬리피지란, 실제 재고 부족이나 과공급으로 매수호가보다 더 비싸거나 싸게 매수되는 비용을 의미한다.
20.12 기준 빗썸 매매수수료는 0.25% ==> 0.0025, 매수, 매도 체결시, 0.005배의 수수료가 발생할 것.
여기서는 실습의 편의를 위해 수수료와 슬리피지는 고려하지 않는다.
"""

import pybithumb
import numpy as np
import operator


def get_ror(k):
    """
    :param k: 변동폭
    :return: 수익률
    """
    df = pybithumb.get_candlestick("BTC")  # 비트코인 일봉 데이터
    df = df['2020']
    df["ma5"] = df['close'].rolling(5).mean().shift(1)  # 5일간 이동평균 컬럼 추가
    df['range'] = (df['high'] - df['low']) * k  # 변동폭, range 컬럼 추가
    df['target'] = df['open'] + df['range'].shift(1)  # shift 메서드는 컬럼 값의 행을 내려준다.,, 목표가 계산
    df['isBull'] = df['open'] > df['ma5']  # 상승장여부 컬럼
    # 백테스팅을 위한 데이터 준비완료!

    # 변동성 돌파와 상승장 전략과 일치하면, 그날은 매수를 한 날이고, 수익률은 종가(매도가)/목표가(매수가)이다.
    # 매수를 하지 않았다면 수익률은 원금 그대로 1이다.
    df['ror'] = np.where((df['high'] > df['target']) & (df['isBull']), (df['close'] / df['target']), 1)

    # cumprod는 해당 열의 값을 모두 곱하여 반환한다. 즉, 해당 기간동안의 수익률을 나타낸다.
    ror = df['ror'].cumprod()[-2]
    return ror


def get_optimized_k():
    """
    :return: 0.1~1 사이에 값들 중 최적의 k값과 그때 수익률을 반환
    """
    result = {}
    for k in np.arange(0.1, 1, 0.1):
        result[k] = get_ror(k)
    return max(result.items(), key=operator.itemgetter(1))


print(get_optimized_k())
