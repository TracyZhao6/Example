import numpy as np
import pandas as pd

def strategy_bh(price_series):
    """Buy and Hold 策略，永远持有多头仓位"""
    signal = pd.Series(1, index=price_series.index)
    return signal

def strategy_double_ma(price_series, short_window=5, long_window=10):
    """双均线策略"""
    short_ma = price_series.rolling(window=short_window).mean()
    long_ma = price_series.rolling(window=long_window).mean()
    signal = pd.Series(0, index=price_series.index)
    signal[short_ma > long_ma] = 1
    signal[short_ma < long_ma] = -1
    return signal

def strategy_macd(price_series, fast=12, slow=26, signal_window=9):
    """MACD 策略"""
    ema_fast = price_series.ewm(span=fast).mean()
    ema_slow = price_series.ewm(span=slow).mean()
    macd = ema_fast - ema_slow
    macd_signal = macd.ewm(span=signal_window).mean()

    signal = pd.Series(0, index=price_series.index)
    signal[(macd.shift(1) < macd_signal.shift(1)) & (macd > macd_signal)] = 1
    signal[(macd.shift(1) > macd_signal.shift(1)) & (macd < macd_signal)] = -1
    return signal

def strategy_rsi(price_series, period=14):
    """RSI 策略"""
    delta = price_series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / (avg_loss + 1e-8)
    rsi = 100 - (100 / (1 + rs))

    signal = pd.Series(0, index=price_series.index)
    signal[rsi < 20] = 1
    signal[rsi > 60] = -1
    return signal
'''
def strategy_forecast(predicted_returns):
    """
    预测模型输出策略：将预测的收益率直接转换为交易信号（基于符号）
    输入为预测值序列
    """
    signal = np.sign(predicted_returns)
    return pd.Series(signal, index=predicted_returns.index)
'''