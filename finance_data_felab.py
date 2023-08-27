# -*- coding: utf-8 -*-
"""Finance Data_FELab.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1d2ymuPWH5LKCHPfdAE2nJuQ-kdzRAUQR

# 금융 데이터 라이브러리

## 1. Finance datareader

## 2. pykrx

## 3. yfinance

## 4. pandas datareader

## 1. Finance DataReader

참고1: [FinanceDataReader 사용자 안내서](https://financedata.github.io/posts/finance-data-reader-users-guide.html)

참고2: [FinanceDataReader 깃허브](https://github.com/financedata-org/FinanceDataReader)
"""

!pip install finance-datareader

import FinanceDataReader as fdr
import pandas as pd
import numpy as np

"""### Finance Data Reader의 2가지 함수

* fdr.DataReader(symbol, start, end, exchange=, data_source=) <br>
&nbsp;&nbsp; data_source를 통해 start~end 기간 동안, exchange의 거래소의 symbol의 데이터를 가져오는 함수

<br>

* fdr.StockListing(market=) <br>
&nbsp;&nbsp; market의 상장종목 리스트를 출력하는 함수

* ### DataReader
"""

# DataReader
samsung = fdr.DataReader('005930') # 삼성전자(005930) 주식 전체 기간
samsung # 출력결과: 시가, 고가, 저가, 종가, 거래량, 수익률이 나타남

toyota = fdr.DataReader('7203', '2020-01-01', '2021-01-01', exchange='TSE') # 토요타 자동차(7203)의 2020년 데이터
toyota # 해외 주식은 Adj Close(수정 종가)도 나옴

df = fdr.DataReader('036360', exchange='KRX-DELISTING') # KRX-DELISTING: 상장폐지 종목 데이터
df

# 지수, 환율, 선물, 비트코인, 채권 등의 데이터도 수집 가능

# Indexes, 2015 ~ Now
sp500 = fdr.DataReader('US500', '2015-01-01') # S&P 500 지수 (NYSE)

# FX 환율, 1995 ~ 현재
usdkrw = fdr.DataReader('USD/KRW', '1995-01-01') # 달러 원화

# 상품 선물 가격 데이터
gold = fdr.DataReader('ZG') # 금 선물 (ICE)

# Bitcoin KRW price (Bithumbs), 2016 ~ Now
btc = fdr.DataReader('BTC/KRW', '2020-01-01')

# 채권 수익률
bond = fdr.DataReader('US10YT') # 10년만기 미국국채 수익률
bond

# 여러 주식을 하나의 df로 저장하는 함수

def get_data(start, end):
  ticker = ['005930','003670','000660','207940','006400','051910','005380','000270','005490','035420'] # 시가총액 상위 10개 (LG에너지솔루션 제외)
  asset = pd.DataFrame()
  for t in ticker:
    asset[t] = fdr.DataReader(t, start, end)['Close'] # asset은 종가 가격
  asset_pct = asset.pct_change()
  asset_pct = asset_pct.dropna() # asset_pct는 종가의 수익률 값을 저장함
  return asset, asset_pct

asset, asset_pct = get_data('2021-01-01', '2021-02-01')
asset

# FRED 데이터
nas = fdr.DataReader('FRED:NASDAQCOM') # NASDAQCOM 나스닥종합지수
nas

"""* ### StockListing"""

# 한국 etf 종목 리스트 불러오기
etf_kr = fdr.StockListing('ETF/KR')
etf_kr

krx = fdr.StockListing('KRX') # 코스피, 코스닥, 코넥스 전체
stocks = fdr.StockListing('NYSE')   # 뉴욕거래소
sp500 = fdr.StockListing('S&P500')

krx_delisting = fdr.StockListing('KRX-DELISTING') # 상장폐지 종목 전체 리스트
krx_delisting

!pip install --upgrade bokeh

# 차트 그리기
df = fdr.DataReader('005930', '2021-01-01', '2022-01-01')
df['Close'].plot()

# 여러 종목 차트 그리기

asset, asset_pct = get_data(start='2021-01-01', end='2022-01-01')
asset.plot()

"""## 2. pykrx

참고2: [pykrx 깃허브](https://github.com/sharebook-kr/pykrx)

"""

!pip install pykrx

from pykrx import stock

# 종목 출력
ticker = stock.get_market_ticker_list(date='2023-08-01', market='KOSPI')
len(ticker)

"""* <b> pykrx는 krx의 라이브러리라 OHLCV 데이터가 시가, 고가 등 한글로 표시됨. </b>"""

ohlcv = stock.get_market_ohlcv_by_date(fromdate='20230801', todate='20230810', ticker='005930')
ohlcv

ohlcv_m = stock.get_market_ohlcv(fromdate='20230101', todate='20230810', ticker='005930', freq='m', adjusted=True)
ohlcv_m

ohlcv_ticker = stock.get_market_ohlcv_by_ticker(date='20230101', market='KOSPI', alternative=True)
ohlcv_ticker

"""#### 함수의 adjusted를 통해 수정종가를 가져올 수 있음"""

ohlcv_date = stock.get_market_ohlcv_by_date(fromdate='20230101', todate='20230801', ticker='005930', freq='m', adjusted=True, name_display=True)
ohlcv_date

# 여러 종목 한번에 가져오기
ticker = ['005930', '373220', '000660']
pykrx_close = pd.DataFrame()
for i in ticker:
  pykrx_close[i] = stock.get_market_ohlcv(fromdate='20230101', todate='20230810', ticker=i, freq='m', adjusted=True)['종가']
pykrx_close

len(dir(stock))

"""### pykrx에는 다양한 함수가 존재, 카테고리별로 분류를 보고 필요한 함수를 사용하면 됨"""

# ELW, ETF
'get_elw_ticker_list',
'get_elw_ticker_name',
'get_etf_isin',
'get_etf_ohlcv_by_date',
'get_etf_ohlcv_by_ticker',
'get_etf_portfolio_deposit_file',
'get_etf_price_change_by_ticker',
'get_etf_price_deviation',
'get_etf_ticker_list',
'get_etf_ticker_name',
'get_etf_tracking_error',
'get_etf_trading_volume_and_value',
'get_etn_ticker_list',
'get_etn_ticker_name',
'get_etx_ticker_list',

# 외국인
'get_exhaustion_rates_of_foreign_investment',
'get_exhaustion_rates_of_foreign_investment_by_date',
'get_exhaustion_rates_of_foreign_investment_by_ticker',

# 선물
'get_future_ohlcv',
'get_future_ohlcv_by_ticker',
'get_future_ticker_list',
'get_future_ticker_name',

# 지수
'get_index_fundamental',
'get_index_fundamental_by_date',
'get_index_fundamental_by_ticker',
'get_index_listing_date',
'get_index_ohlcv',
'get_index_ohlcv_by_date',
'get_index_ohlcv_by_ticker',
'get_index_portfolio_deposit_file',
'get_index_price_change',
'get_index_price_change_by_name',
'get_index_price_change_by_ticker',
'get_index_ticker_list',
'get_index_ticker_name',

# 재무지표
'get_market_cap',
'get_market_cap_by_date',
'get_market_cap_by_ticker',
'get_market_fundamental',
'get_market_fundamental_by_date',
'get_market_fundamental_by_ticker',
'get_market_net_purchases_of_equities',
'get_market_net_purchases_of_equities_by_ticker',
'get_stock_major_changes',

# 주식
'get_market_ohlcv',
'get_market_ohlcv_by_date',
'get_market_ohlcv_by_ticker',
'get_market_price_change',
'get_market_price_change_by_ticker',
'get_market_sector_classifications',
'get_market_ticker_list',
'get_market_ticker_name',
'get_market_trading_value_and_volume_by_ticker',
'get_market_trading_value_by_date',
'get_market_trading_value_by_investor',
'get_market_trading_volume_by_date',
'get_market_trading_volume_by_investor',

# 날짜
'get_business_days',
'get_nearest_business_day_in_a_week',
'get_previous_business_days',

# 공매도
'get_shorting_balance',
'get_shorting_balance_by_date',
'get_shorting_balance_by_ticker',
'get_shorting_balance_top50',
'get_shorting_investor_value_by_date',
'get_shorting_investor_volume_by_date',
'get_shorting_status_by_date',
'get_shorting_value_by_date',
'get_shorting_value_by_ticker',
'get_shorting_volume_by_date',
'get_shorting_volume_by_ticker',
'get_shorting_volume_top50',

"""## 3. yfinance

참고: [yfinance, pandas-datareader 정리 tistory](https://psystat.tistory.com/145?category=1206707)


"""

import yfinance as yf
yf.pdr_override() # 야후에서 데이터를 획득하는 방식이 크롤링으로 변경

"""### yfinance는 yahoo finance의 데이터를 받아오는 라이브러리임.
#### 따라서 한국 종목은 .KS를 붙여야함
"""

yf.Ticker('005930.KS').info

"""### <u> yfinance.history 와 download 함수의 파라미터들

#### tickers : 종목코드(str)
#### period : 기간(str)
- Valid periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
- 기본값: 'max'

#### interval : 간격(str)
- Valid intervals: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
- 최근 60일 기간 동안 조회 가능(이게 1m 기준인듯)
- 하지만 1h은 5m보다, 5m도 1m에 비해 날짜가 더 긴 것 같으므로 자세한 사항은 원하는 간격을 직접 돌려봐야함.
- 기본값: '1d'

#### start: 시작 날짜(str)
- 기본값: '1900-01-01'

#### end: 끝 날짜(str)
- 기본값: now

#### group_by : 정렬(str)
- ticker나 column 지정 가능

#### prepost : bool
- Include Pre and Post market data in results?
- 일별 가격은 상관없으나 시간, 분별로 가져올 때 시장 전이나 후의 가격도 불러오는 옵션. 보통 지정하지 않아 False로 고려.
- 기본값: False

#### auto_adjust: bool
- 모든 OHLC 데이터를 수정(adjust)으로 자동 조정할 것인지
- 기본값은 False이나 True로 해도 좋다고 생각.
- 기본값: False

#### back_adjust: bool
- 실제 과거 가격을 모방하기 위해 데이터를 뒤로 조정
- 기본값: False
#### actions: bool
- 배당(dividend)과 주식 분할(stock splits) 데이터 유무
- 기본값: False

#### threads: bool / int
- 대용량 다운에 사용할 threads의 수
- 기본값: True

#### proxy: str
- 선택 옵션. Proxy server URL scheme.
- 기본값: None

#### rounding: bool
- 선택 옵션. 반올림 소수 2째자리까지 할지
- 기본값: False

#### show_errors: bool
- 선택 옵션. True이면 에러를 표시하지 않음

#### tz: str
- 선탭 옵션. timezone locale for dates.
- 기본값: non-localized dates

#### timeout: None or float
- 특정 시간(초) 이후로 응답 대기를 중지함
- Can also be a fraction of a second e.g. 0.01
- 기본값: None.
"""

ticker = yf.Ticker('AAPL')
df_sam = ticker.history(interval='1h',
                        start='2023-07-19',
                        end='2023-07-20',
                        prepost=True,
                        actions=True,
                        auto_adjust=True)
df_sam

ticker = yf.Ticker('AAPL')

df_sam = ticker.history(interval='5m',
                        start='2023-07-19',
                        end='2023-07-20',
                        actions=True,
                        auto_adjust=True)
df_sam

"""### yf.download
- history 험수는 a = yf.Ticker('ticker')로 a를 Ticker로 생성 후 a.history를 진행했음
- download 함수는 yf.download('ticker')와 같이 파라미터로 ticker를 바로 직접 넣는 차이점이 있음
"""

AAPL_1m = yf.download('AAPL', period='1mo')
AAPL_1m

AAPL = yf.download('AAPL', start='2022-01-01', end='2022-08-01')
AAPL

"""#### yfinance는 한국, 해외 주식 모두 close, adj close 가져올 수 있음.

- history, download 둘 다 가능
"""

tick = yf.Ticker('005930.KS')
tick.history(start='2022-01-01', end='2022-08-01')['Close']

# 여러 종목 한번에 가져오기
ticker = ['AAPL', '005930.KS', '373220.KS', '000660.KS']
yf_close = pd.DataFrame()
hist_close = pd.DataFrame()
for i in ticker:
  tick = yf.Ticker(i)
  hist_close[i] = tick.history(start='2022-01-01', end='2022-08-01')['Close'] # history 방법
  yf_close[i] = yf.download(i, start='2022-01-01', end='2022-08-01')['Adj Close'] # download 방법
yf_close

# 하지만 history 방법은 시간대가 달라 해외, 국내 주식은 따로 불러오는 것이 현명한 방법
# download 방법 역시 국내와 해외의 날짜(공휴일)가 달라 NaN 값이 나오는 것으로 추정
hist_close

"""## 4. pandas datareader

참고: [yfinance, pandas-datareader 정리 tistory](https://psystat.tistory.com/145?category=1206707)
"""

import pandas_datareader as pdr

!pip install --upgrade pandas_datareader

# naver를 통해 국내 주식들을 가져올 수 있음
Samsung = pdr.DataReader('005930', 'naver', start='2023-08-01', end='2023-08-05')
Samsung

"""#### pandas datareader 제공 데이터 종류

* Yahoo Finance: 주식, 환율, 암호화폐, 지수 등
* FRED: 미국 정부에서 발표한 경제 통계자료
* Fama-French Factor: 주식 투자 전략에 대한 자료
* World Bank: 세계 경제, 인구 통계자료
* OECD: OECD 회원국들의 경제 통계자료

출처: [파이썬 기반 금융 데이터 수집 라이브러리: 가장 인기 있는 5가지 라이브러리 소개](https://backtesting.tistory.com/entry/Python-based-financial-data-collection-libraries)
"""

# Samsung = pdr.DataReader('005930.KS', 'yahoo', start='2023-08-01', end='2023-08-05')
# Samsung = pdr.get_data_yahoo('005930.KS', start='2023-08-01', end='2023-08-05')

# 위 코드처럼 pandas_datareader는 source로 야후를 지정하면 오류가 남, 다른 라이브러리 사용 권장

"""#### FamaFrench Data

* Fama-French Factor: 주식 투자 전략에 대한 자료
"""

# FamaFrench의 데이터 불러오는 방법1: DataReader
FamaFrench = pdr.DataReader('5_Industry_Portfolios', 'famafrench', start='2020-01-01', end='2023-01-01')
FamaFrench

# FamaFrench의 데이터 불러오는 방법2: get_data_famafrench 함수
fama_get = pdr.get_data_famafrench('5_Industry_Portfolios', start='2020-01-01', end='2023-01-01')
fama_get

import pandas_datareader.famafrench as ff

# famafrench에서 사용 가능한 데이터셋
datasets = ff.get_available_datasets()
datasets

"""### FRED
* FRED: 미국 정부에서 발표한 경제 통계자료

* fred의 다양한 데이터는 Ticker를 통해 불러올 수 있음.

* fred 사이트: [FRED](https://fred.stlouisfed.org/)
"""

# Fred의 데이터 불러오는 방법1: DataReader
fred = pdr.DataReader('GDP', 'fred', start='2020-01-01', end='2023-01-01')
fred

# Fred의 데이터 불러오는 방법2: get_data_fred 함수
fred_get = pdr.get_data_fred('GDP', start='2020-01-01', end='2023-01-01')
fred_get

# 여러 종목 한번에 가져오기
ticker = ['005930', '373220', '000660']
pd_close = pd.DataFrame()

for i in ticker:
  pd_close[i] = pdr.DataReader(i, 'naver', start='2022-08-01', end='2022-08-10')['Close']
pd_close

