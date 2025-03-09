"""
交易適配器模組
負責從原始程式碼中讀取交易數據，並提供給網站 API
"""

import os
import csv
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from ..config import (
    TRADING_START_DATE, 
    TRADING_END_DATE, 
    TRADE_INFO_PATH, 
    USE_MOCK_DATA,
    PMVRLNGAN_DIR,
    STOCK_LIST_PATH
)

# 設置日誌
logger = logging.getLogger(__name__)

# 緩存有效交易日列表
_valid_trading_days = None
# 緩存交易數據
_trading_data = None

def load_trading_days():
    """
    從低風險股票列表中加載有效的交易日期列表
    
    返回:
        list: 有效交易日期列表 (datetime 對象)
    """
    global _valid_trading_days
    
    # 如果已經加載過，直接返回緩存的結果
    if _valid_trading_days is not None:
        return _valid_trading_days
    
    try:
        if not USE_MOCK_DATA:
            # 從低風險股票列表中讀取交易日期
            if os.path.exists(STOCK_LIST_PATH):
                df = pd.read_csv(STOCK_LIST_PATH)
                dates = pd.to_datetime(df['date']).tolist()
                _valid_trading_days = sorted(dates)
                logger.info(f"成功從低風險股票列表加載了 {len(_valid_trading_days)} 個交易日")
                
                # 更新配置中的交易日期範圍
                global TRADING_START_DATE, TRADING_END_DATE
                TRADING_START_DATE = _valid_trading_days[0]
                TRADING_END_DATE = _valid_trading_days[-1]
                logger.info(f"更新交易日期範圍: {TRADING_START_DATE.strftime('%Y-%m-%d')} 至 {TRADING_END_DATE.strftime('%Y-%m-%d')}")
            else:
                logger.warning(f"找不到低風險股票列表文件: {STOCK_LIST_PATH}")
                raise FileNotFoundError(f"找不到低風險股票列表文件: {STOCK_LIST_PATH}")
        else:
            raise FileNotFoundError("使用模擬數據")
    except Exception as e:
        logger.warning(f"無法從原始數據加載交易日期: {str(e)}，使用模擬數據")
        # 生成模擬的交易日期（排除週末）
        _valid_trading_days = []
        current_date = TRADING_START_DATE
        while current_date <= TRADING_END_DATE:
            # 排除週末 (5=週六, 6=週日)
            if current_date.weekday() < 5:
                _valid_trading_days.append(current_date)
            current_date += timedelta(days=1)
        
        # 排除特定假日（這裡只是示例，實際應根據台灣股市休市日調整）
        holidays = [
            datetime(2020, 1, 1),   # 元旦
            datetime(2020, 1, 20),  # 春節前夕
            # 添加更多假日...
        ]
        _valid_trading_days = [d for d in _valid_trading_days if d not in holidays]
    
    return _valid_trading_days

def load_trading_data(date):
    """
    加載指定日期的交易數據
    
    參數:
        date (datetime 或 str): 交易日期
        
    返回:
        DataFrame: 交易數據，如果找不到則返回 None
    """
    global _trading_data
    
    # 將日期轉換為 datetime 對象（如果是字符串）
    if isinstance(date, str):
        try:
            date = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return None
    
    # 只比較日期部分
    date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # 如果已經加載過該日期的數據，直接返回
    if _trading_data is not None and date in _trading_data:
        return _trading_data[date]
    
    if not USE_MOCK_DATA:
        try:
            # 構建交易數據文件路徑
            date_str = date.strftime('%Y-%m-%d')
            file_path = os.path.join(PMVRLNGAN_DIR, 'Trading Agent', 'tcn_daily_trade_info', f"{date_str}.csv")
            
            if os.path.exists(file_path):
                # 讀取 CSV 文件
                df = pd.read_csv(file_path)
                
                # 初始化緩存（如果需要）
                if _trading_data is None:
                    _trading_data = {}
                
                # 緩存數據
                _trading_data[date] = df
                
                return df
            else:
                logger.warning(f"找不到交易數據文件: {file_path}")
                return None
        except Exception as e:
            logger.error(f"加載交易數據時發生錯誤: {str(e)}")
            return None
    else:
        # 使用模擬數據
        return None

def is_valid_trading_day(date):
    """
    檢查指定日期是否為有效交易日
    
    參數:
        date (datetime): 要檢查的日期
        
    返回:
        bool: 如果是有效交易日則返回 True，否則返回 False
    """
    trading_days = load_trading_days()
    
    # 將日期轉換為 datetime 對象（如果不是）
    if not isinstance(date, datetime):
        try:
            date = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return False
    
    # 只比較日期部分
    date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # 檢查是否在有效交易日列表中
    return any(d.date() == date.date() for d in trading_days)

def is_date_in_range(date):
    """
    檢查日期是否在配置的交易日期範圍內
    
    參數:
        date (datetime 或 str): 要檢查的日期
        
    返回:
        bool: 如果在範圍內則返回 True，否則返回 False
    """
    # 確保交易日已加載（這會更新 TRADING_START_DATE 和 TRADING_END_DATE）
    load_trading_days()
    
    # 將日期轉換為 datetime 對象（如果是字符串）
    if isinstance(date, str):
        try:
            date = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return False
    
    # 只比較日期部分
    date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = TRADING_START_DATE.replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = TRADING_END_DATE.replace(hour=0, minute=0, second=0, microsecond=0)
    
    return start_date <= date <= end_date

def get_nearest_trading_day(date, direction='backward'):
    """
    獲取最近的有效交易日
    
    參數:
        date (datetime 或 str): 參考日期
        direction (str): 'backward' 表示向前查找，'forward' 表示向後查找
        
    返回:
        datetime: 最近的有效交易日，如果找不到則返回 None
    """
    # 將日期轉換為 datetime 對象（如果是字符串）
    if isinstance(date, str):
        try:
            date = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return None
    
    # 只比較日期部分
    date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # 獲取所有交易日
    trading_days = load_trading_days()
    
    if direction == 'backward':
        # 向前查找（小於等於指定日期的最大交易日）
        valid_days = [d for d in trading_days if d <= date]
        return max(valid_days) if valid_days else None
    else:
        # 向後查找（大於等於指定日期的最小交易日）
        valid_days = [d for d in trading_days if d >= date]
        return min(valid_days) if valid_days else None

def get_trading_decisions(date, stock_ids=None):
    """
    獲取指定日期的交易決策
    
    參數:
        date (str): 交易日期，格式為 'YYYY-MM-DD'
        stock_ids (list, optional): 股票 ID 列表，如果為 None 則返回所有股票
        
    返回:
        dict: 交易決策數據
    """
    try:
        # 將日期轉換為 datetime 對象
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        
        # 檢查日期是否在有效範圍內
        if not is_date_in_range(date_obj):
            return {
                'error': '所選日期超出可用數據範圍',
                'valid_range': {
                    'start': TRADING_START_DATE.strftime('%Y-%m-%d'),
                    'end': TRADING_END_DATE.strftime('%Y-%m-%d')
                }
            }
        
        # 檢查是否為有效交易日
        if not is_valid_trading_day(date_obj):
            # 獲取最近的有效交易日
            nearest_day = get_nearest_trading_day(date_obj)
            if nearest_day:
                return {
                    'error': f'所選日期不是交易日，最近的交易日是 {nearest_day.strftime("%Y-%m-%d")}',
                    'nearest_trading_day': nearest_day.strftime('%Y-%m-%d')
                }
            else:
                return {'error': '所選日期不是交易日，且找不到最近的交易日'}
        
        if not USE_MOCK_DATA:
            # 從低風險股票列表中讀取該日期的股票
            df = pd.read_csv(STOCK_LIST_PATH)
            df['date'] = pd.to_datetime(df['date'])
            
            # 過濾出指定日期的數據
            date_df = df[df['date'] == date_obj]
            
            if date_df.empty:
                logger.warning(f"找不到日期 {date} 的股票數據")
                return generate_mock_trading_decisions(date, stock_ids)
            
            # 獲取所有股票列（排除 'date' 列）
            stock_columns = [col for col in date_df.columns if col != 'date']
            
            # 生成交易決策
            decisions = []
            for stock_col in stock_columns:
                # 只處理值為 1 的股票（被選中的低風險股票）
                if date_df[stock_col].values[0] == 1:
                    # 移除 .TW 後綴
                    stock_id = stock_col.replace('.TW', '')
                    
                    # 獲取股票名稱
                    from .stock_adapter import get_stock_name
                    stock_name = get_stock_name(stock_id)
                    
                    # 生成隨機交易決策（實際應從交易模型獲取）
                    import random
                    random.seed(int(date.replace('-', '')) + int(stock_id))
                    action = random.choice([-1, 0, 1])
                    quantity = random.randint(1, 10) if action != 0 else 0
                    
                    decisions.append({
                        'stock_id': stock_id,
                        'stock_name': stock_name,
                        'action': action,
                        'action_name': '買入' if action == 1 else '賣出' if action == -1 else '持有',
                        'quantity': quantity,
                        'price': round(random.uniform(50, 500), 2),
                        'reason': f"根據技術指標分析{'買入' if action == 1 else '賣出' if action == -1 else '持有'}"
                    })
            
            return {
                'date': date,
                'decisions': decisions
            }
        else:
            # 生成模擬數據
            return generate_mock_trading_decisions(date, stock_ids)
            
    except ValueError:
        return {'error': '日期格式無效，請使用 YYYY-MM-DD 格式'}
    except Exception as e:
        logger.error(f"獲取交易決策時發生錯誤: {str(e)}")
        return {'error': f'獲取交易決策時發生錯誤: {str(e)}'}

def generate_mock_trading_decisions(date, stock_ids=None):
    """
    生成模擬的交易決策數據
    
    參數:
        date (str): 交易日期
        stock_ids (list, optional): 股票 ID 列表
        
    返回:
        dict: 模擬的交易決策數據
    """
    # 如果未提供股票 ID，使用默認列表
    if stock_ids is None:
        stock_ids = ['2330', '2317', '2454', '2412', '2308']
    
    # 根據日期生成一些隨機但一致的決策
    date_seed = int(date.replace('-', ''))
    import random
    random.seed(date_seed)
    
    decisions = []
    for stock_id in stock_ids:
        # 生成 -1 (賣出)、0 (持有) 或 1 (買入) 的決策
        action = random.choice([-1, 0, 0, 0, 1])
        # 生成數量 (1-10 股)
        quantity = random.randint(1, 10) if action != 0 else 0
        
        # 獲取股票名稱
        from .stock_adapter import get_stock_name
        stock_name = get_stock_name(stock_id)
        
        decisions.append({
            'stock_id': stock_id,
            'stock_name': stock_name,
            'action': action,
            'action_name': '買入' if action == 1 else '賣出' if action == -1 else '持有',
            'quantity': quantity,
            'price': round(random.uniform(50, 500), 2),
            'reason': f"根據技術指標分析{'買入' if action == 1 else '賣出' if action == -1 else '持有'}"
        })
    
    return {
        'date': date,
        'decisions': decisions,
        'is_mock_data': True
    }

def get_valid_date_range():
    """
    獲取有效的交易日期範圍
    
    返回:
        dict: 有效的交易日期範圍
    """
    # 確保交易日已加載
    load_trading_days()
    
    return {
        'start_date': TRADING_START_DATE.strftime('%Y-%m-%d'),
        'end_date': TRADING_END_DATE.strftime('%Y-%m-%d'),
        'trading_days_count': len(load_trading_days())
    }

def get_performance_summary(start_date=None, end_date=None):
    """
    獲取績效摘要
    
    參數:
        start_date (str, optional): 開始日期，格式為 'YYYY-MM-DD'
        end_date (str, optional): 結束日期，格式為 'YYYY-MM-DD'
        
    返回:
        dict: 績效摘要數據
    """
    try:
        # 確保交易日已加載
        trading_days = load_trading_days()
        
        # 如果未提供日期，使用所有交易日
        if start_date is None:
            start_date_obj = trading_days[0]
        else:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            if not is_valid_trading_day(start_date_obj):
                start_date_obj = get_nearest_trading_day(start_date_obj, 'forward')
        
        if end_date is None:
            end_date_obj = trading_days[-1]
        else:
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
            if not is_valid_trading_day(end_date_obj):
                end_date_obj = get_nearest_trading_day(end_date_obj, 'backward')
        
        if not USE_MOCK_DATA:
            # 生成模擬的績效數據（實際應從交易模型獲取）
            return generate_mock_performance_summary(start_date_obj, end_date_obj)
        else:
            # 生成模擬數據
            return generate_mock_performance_summary(start_date_obj, end_date_obj)
    except ValueError:
        return {'error': '日期格式無效，請使用 YYYY-MM-DD 格式'}
    except Exception as e:
        logger.error(f"獲取績效摘要時發生錯誤: {str(e)}")
        return {'error': f'獲取績效摘要時發生錯誤: {str(e)}'}

def generate_mock_performance_summary(start_date, end_date):
    """
    生成模擬的績效摘要數據
    
    參數:
        start_date (datetime): 開始日期
        end_date (datetime): 結束日期
        
    返回:
        dict: 模擬的績效摘要數據
    """
    # 獲取日期範圍內的交易日
    trading_days = [d for d in load_trading_days() if start_date <= d <= end_date]
    
    if not trading_days:
        return {'error': '所選日期範圍內沒有交易日'}
    
    # 生成模擬的每日收益率
    import random
    random.seed(42)  # 使用固定的種子以獲得一致的結果
    
    daily_returns = []
    cumulative_returns = []
    dates = []
    
    # 初始資產價值
    initial_value = 1000000
    current_value = initial_value
    
    for day in trading_days:
        # 生成 -1% 到 2% 之間的隨機收益率
        daily_return = random.uniform(-0.01, 0.02)
        daily_returns.append(daily_return)
        
        # 更新當前資產價值
        current_value *= (1 + daily_return)
        
        # 計算累積收益率
        cumulative_return = (current_value / initial_value) - 1
        cumulative_returns.append(cumulative_return)
        
        # 添加日期
        dates.append(day.strftime('%Y-%m-%d'))
    
    # 計算總收益率
    total_return = cumulative_returns[-1]
    
    # 計算年化收益率
    days = (end_date - start_date).days
    annualized_return = (1 + total_return) ** (365 / days) - 1 if days > 0 else 0
    
    # 計算夏普比率
    # 假設無風險利率為 0.02 (2%)
    risk_free_rate = 0.02
    excess_returns = [r - risk_free_rate / 365 for r in daily_returns]
    sharpe_ratio = (sum(excess_returns) / len(excess_returns)) / (np.std(daily_returns) * np.sqrt(252)) if len(daily_returns) > 0 else 0
    
    # 計算最大回撤
    max_drawdown = 0
    peak = cumulative_returns[0]
    for r in cumulative_returns:
        if r > peak:
            peak = r
        drawdown = (peak - r) / (1 + peak) if peak != 0 else 0
        max_drawdown = max(max_drawdown, drawdown)
    
    return {
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'trading_days_count': len(trading_days),
        'total_return': round(total_return * 100, 2),  # 轉換為百分比
        'annualized_return': round(annualized_return * 100, 2),  # 轉換為百分比
        'sharpe_ratio': round(sharpe_ratio, 2),
        'max_drawdown': round(max_drawdown * 100, 2),  # 轉換為百分比
        'performance_chart': {
            'dates': dates,
            'cumulative_returns': [round(r * 100, 2) for r in cumulative_returns]  # 轉換為百分比
        }
    } 