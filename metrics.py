import numpy as np
import pandas as pd

def calculate_max_drawdown(cumulative_returns):
    """计算最大回撤"""
    peak = cumulative_returns.cummax()
    drawdown = (cumulative_returns - peak) / peak
    max_dd = drawdown.min()
    return max_dd

def calculate_annualized_return(daily_returns, periods_per_year=252):
    """年化收益率"""
    cumulative_return = (1 + daily_returns).prod()
    annualized_return = cumulative_return ** (periods_per_year / len(daily_returns)) - 1
    return annualized_return

def calculate_annualized_volatility(daily_returns, periods_per_year=252):
    """年化波动率"""
    return np.std(daily_returns) * np.sqrt(periods_per_year)

def calculate_sharpe_ratio(daily_returns, risk_free_rate=0.0, periods_per_year=252):
    """夏普比率"""
    excess_returns = daily_returns - risk_free_rate / periods_per_year
    return np.mean(excess_returns) / (np.std(excess_returns) + 1e-8) * np.sqrt(periods_per_year)

def calculate_sortino_ratio(daily_returns, risk_free_rate=0.0, periods_per_year=252):
    """Sortino比率"""
    negative_returns = daily_returns[daily_returns < 0]
    downside_std = np.std(negative_returns)
    excess_returns = daily_returns - risk_free_rate / periods_per_year
    return np.mean(excess_returns) / (downside_std + 1e-8) * np.sqrt(periods_per_year)

def calculate_calmar_ratio(annual_return, max_drawdown):
    """Calmar比率"""
    return annual_return / abs(max_drawdown + 1e-8)

def calculate_information_ratio(strategy_returns, benchmark_returns):
    """信息比率（与基准对比）"""
    active_return = strategy_returns - benchmark_returns
    tracking_error = np.std(active_return)
    return np.mean(active_return) / (tracking_error + 1e-8)

def evaluate_performance(strategy_df, benchmark_df=None):
    """
    汇总绩效指标
    strategy_df: 包含 daily_return 和 cumulative_return 的 DataFrame
    benchmark_df: 如果有基准策略（如B&H）可提供其 daily_return
    """
    daily_returns = strategy_df['daily_return']
    cumulative_return = strategy_df['cumulative_return'].iloc[-1] - 1
    ann_return = calculate_annualized_return(daily_returns)
    ann_vol = calculate_annualized_volatility(daily_returns)
    sharpe = calculate_sharpe_ratio(daily_returns)
    sortino = calculate_sortino_ratio(daily_returns)
    max_dd = calculate_max_drawdown(strategy_df['cumulative_return'])
    calmar = calculate_calmar_ratio(ann_return, max_dd)

    info_ratio = None
    if benchmark_df is not None:
        info_ratio = calculate_information_ratio(
            strategy_df['daily_return'], benchmark_df['daily_return']
        )

    return {
        'Total Return': cumulative_return,
        'Annualized Return': ann_return,
        'Max Drawdown': max_dd,
        'Sharpe Ratio': sharpe,
        'Information Ratio': info_ratio,
        'Calmar Ratio': calmar,
        'Sortino Ratio': sortino,
        'Annual Volatility': ann_vol
    }
