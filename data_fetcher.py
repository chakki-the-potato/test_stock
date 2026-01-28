import yfinance as yf
import pandas as pd
from datetime import datetime

# 종목 정보
STOCKS = {
    "삼성전자": "005930.KS",
    "SK하이닉스": "000660.KS",
    "LG에너지솔루션": "373220.KS",
}

# 데이터 기간
START_DATE = "2025-10-01"
END_DATE = "2025-12-31"


def fetch_stock_data(ticker: str, start: str = START_DATE, end: str = END_DATE) -> pd.DataFrame:
    """yfinance로 일봉 데이터 가져오기"""
    stock = yf.Ticker(ticker)
    df = stock.history(start=start, end=end)
    return df


def add_moving_averages(df: pd.DataFrame) -> pd.DataFrame:
    """이동평균선 추가 (5일, 20일, 60일)"""
    df = df.copy()
    df["MA5"] = df["Close"].rolling(window=5).mean()
    df["MA20"] = df["Close"].rolling(window=20).mean()
    df["MA60"] = df["Close"].rolling(window=60).mean()
    return df


def convert_to_weekly(df: pd.DataFrame) -> pd.DataFrame:
    """일봉 → 주봉 변환"""
    weekly = df.resample("W").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum",
    }).dropna()

    # 이동평균선 다시 계산
    weekly["MA5"] = weekly["Close"].rolling(window=5).mean()
    weekly["MA20"] = weekly["Close"].rolling(window=20).mean()
    weekly["MA60"] = weekly["Close"].rolling(window=60).mean()
    return weekly


def convert_to_monthly(df: pd.DataFrame) -> pd.DataFrame:
    """일봉 → 월봉 변환"""
    monthly = df.resample("ME").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum",
    }).dropna()

    # 이동평균선 다시 계산
    monthly["MA5"] = monthly["Close"].rolling(window=5).mean()
    monthly["MA20"] = monthly["Close"].rolling(window=20).mean()
    monthly["MA60"] = monthly["Close"].rolling(window=60).mean()
    return monthly


def get_stock_info(ticker: str) -> dict:
    """현재가 정보 조회 (현재가, 등락률, 52주 최고/최저)"""
    stock = yf.Ticker(ticker)
    info = stock.info

    # 최근 데이터에서 현재가 정보 가져오기
    hist = stock.history(period="5d")

    if len(hist) >= 2:
        current_price = hist["Close"].iloc[-1]
        prev_price = hist["Close"].iloc[-2]
        change = current_price - prev_price
        change_percent = (change / prev_price) * 100
    else:
        current_price = info.get("currentPrice", 0)
        change = 0
        change_percent = 0

    return {
        "current_price": current_price,
        "change": change,
        "change_percent": change_percent,
        "high_52week": info.get("fiftyTwoWeekHigh", 0),
        "low_52week": info.get("fiftyTwoWeekLow", 0),
        "volume": hist["Volume"].iloc[-1] if len(hist) > 0 else 0,
    }


def get_all_data(stock_name: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    """종목의 모든 데이터 가져오기 (일봉, 주봉, 월봉, 현재가 정보)"""
    ticker = STOCKS.get(stock_name)
    if not ticker:
        raise ValueError(f"Unknown stock: {stock_name}")

    # 일봉 데이터 가져오기
    daily = fetch_stock_data(ticker)
    daily = add_moving_averages(daily)

    # 주봉, 월봉 변환
    weekly = convert_to_weekly(daily)
    monthly = convert_to_monthly(daily)

    # 현재가 정보
    info = get_stock_info(ticker)

    return daily, weekly, monthly, info
