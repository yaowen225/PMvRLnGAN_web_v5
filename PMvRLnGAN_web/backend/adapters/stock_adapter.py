"""
股票適配器模組
負責從原始程式碼中讀取低風險股票列表，並提供給網站 API
"""

import os
import csv
import pandas as pd
import numpy as np
import logging
from datetime import datetime
from ..config import STOCK_LIST_PATH, USE_MOCK_DATA

# 設置日誌
logger = logging.getLogger(__name__)

def get_stock_list(quarter=None):
    """
    獲取低風險股票列表
    
    參數:
        quarter (str, optional): 季度，格式為 'YYYY-Q1'、'YYYY-Q2'、'YYYY-Q3' 或 'YYYY-Q4'
                                如果為 None，則返回所有季度的股票列表
    
    返回:
        dict: 股票列表數據
    """
    try:
        if not USE_MOCK_DATA:
            # 嘗試從原始數據中讀取低風險股票列表
            if os.path.exists(STOCK_LIST_PATH):
                # 讀取 CSV 文件
                df = pd.read_csv(STOCK_LIST_PATH)
                
                # 將日期列轉換為季度格式
                df['quarter'] = pd.to_datetime(df['date']).apply(date_to_quarter)
                
                # 獲取所有股票代碼（列名，排除 'date' 列）
                stock_columns = [col for col in df.columns if col not in ['date', 'quarter']]
                
                # 處理每個季度的數據
                result = {}
                for quarter_val, group in df.groupby('quarter'):
                    # 獲取該季度選中的股票（值為1的列）
                    selected_stocks = []
                    for _, row in group.iterrows():
                        for stock_id in stock_columns:
                            if row[stock_id] == 1:
                                # 移除 .TW 後綴
                                clean_stock_id = stock_id.replace('.TW', '')
                                # 獲取股票名稱（這裡使用模擬數據，實際應從另一個來源獲取）
                                stock_name = get_stock_name(clean_stock_id)
                                selected_stocks.append({
                                    'stock_id': clean_stock_id,
                                    'stock_name': stock_name,
                                    'risk': round(np.random.uniform(0.1, 0.5), 2),  # 模擬風險值
                                    'weight': 1.0 / len(selected_stocks) if selected_stocks else 0  # 平均權重
                                })
                    
                    # 調整權重使總和為 1
                    if selected_stocks:
                        total_weight = sum(stock['weight'] for stock in selected_stocks)
                        for stock in selected_stocks:
                            stock['weight'] = round(stock['weight'] / total_weight, 2)
                        
                        # 再次調整以確保總和為 1（處理四捨五入的誤差）
                        total_weight = sum(stock['weight'] for stock in selected_stocks)
                        if total_weight != 1:
                            selected_stocks[0]['weight'] += round(1 - total_weight, 2)
                    
                    result[quarter_val] = selected_stocks
                
                # 如果指定了季度，過濾數據
                if quarter and quarter in result:
                    return {
                        'quarter': quarter,
                        'stocks': result[quarter]
                    }
                elif quarter:
                    return {
                        'error': f'找不到季度 {quarter} 的股票列表',
                        'available_quarters': list(result.keys())
                    }
                else:
                    return {
                        'quarters': list(result.keys()),
                        'stocks': result
                    }
            else:
                logger.warning(f"找不到低風險股票列表文件: {STOCK_LIST_PATH}")
                raise FileNotFoundError(f"找不到低風險股票列表文件: {STOCK_LIST_PATH}")
        else:
            # 使用模擬數據
            return generate_mock_stock_list(quarter)
    except Exception as e:
        logger.error(f"獲取低風險股票列表時發生錯誤: {str(e)}")
        return {
            'error': f'獲取低風險股票列表時發生錯誤: {str(e)}'
        }

def date_to_quarter(date):
    """
    將日期轉換為季度格式 (YYYY-QN)
    
    參數:
        date (datetime): 日期
        
    返回:
        str: 季度格式，如 '2021-Q4'
    """
    month = date.month
    if month <= 3:
        quarter = 'Q1'
    elif month <= 6:
        quarter = 'Q2'
    elif month <= 9:
        quarter = 'Q3'
    else:
        quarter = 'Q4'
    
    return f"{date.year}-{quarter}"

def get_stock_name(stock_id):
    """
    獲取股票名稱
    
    參數:
        stock_id (str): 股票代碼
        
    返回:
        str: 股票名稱
    """
    # 常見台股對應表
    stock_names = {
        '1101': '台泥',
        '1102': '亞泥',
        '1216': '統一',
        '1229': '聯華',
        '1301': '台塑',
        '1303': '南亞',
        '1326': '台化',
        '1402': '遠東新',
        '1476': '儒鴻',
        '1504': '東元',
        '1590': '亞德客-KY',
        '1605': '華新',
        '2002': '中鋼',
        '2027': '大成鋼',
        '2049': '上銀',
        '2105': '正新',
        '2201': '裕隆',
        '2207': '和泰車',
        '2301': '光寶科',
        '2303': '聯電',
        '2308': '台達電',
        '2317': '鴻海',
        '2324': '仁寶',
        '2327': '國巨',
        '2330': '台積電',
        '2344': '華邦電',
        '2345': '智邦',
        '2347': '聯強',
        '2352': '佳世達',
        '2353': '宏碁',
        '2356': '英業達',
        '2357': '華碩',
        '2360': '致茂',
        '2371': '大同',
        '2376': '技嘉',
        '2377': '微星',
        '2379': '瑞昱',
        '2382': '廣達',
        '2383': '台光電',
        '2395': '研華',
        '2408': '南亞科',
        '2409': '友達',
        '2412': '中華電',
        '2454': '聯發科',
        '2474': '可成',
        '2603': '長榮',
        '2609': '陽明',
        '2610': '華航',
        '2615': '萬海',
        '2618': '長榮航',
        '2912': '統一超',
        '3008': '大立光',
        '3017': '奇鋐',
        '3023': '信邦',
        '3034': '聯詠',
        '3037': '欣興',
        '3045': '台灣大',
        '3231': '緯創',
        '3443': '創意',
        '3481': '群創',
        '3533': '嘉澤',
        '3653': '健策',
        '3702': '大聯大',
        '4904': '遠傳',
        '4938': '和碩',
        '4958': '臻鼎-KY',
        '5871': '中租-KY',
        '6505': '台塑化',
        '8046': '南電',
        '9904': '寶成',
        '9910': '豐泰',
        '9921': '巨大',
        '9941': '裕融',
        '9945': '潤泰新'
    }
    
    return stock_names.get(stock_id, f'未知股票 {stock_id}')

def get_available_quarters():
    """
    獲取可用的季度列表
    
    返回:
        list: 可用的季度列表
    """
    try:
        if not USE_MOCK_DATA:
            # 從原始數據中讀取可用的季度
            if os.path.exists(STOCK_LIST_PATH):
                df = pd.read_csv(STOCK_LIST_PATH)
                quarters = pd.to_datetime(df['date']).apply(date_to_quarter).unique().tolist()
                return {'quarters': sorted(quarters)}
            else:
                logger.warning(f"找不到低風險股票列表文件: {STOCK_LIST_PATH}")
                raise FileNotFoundError(f"找不到低風險股票列表文件: {STOCK_LIST_PATH}")
        else:
            # 使用模擬數據
            mock_data = generate_mock_stock_list()
            return {'quarters': mock_data['quarters']}
    except Exception as e:
        logger.error(f"獲取可用季度列表時發生錯誤: {str(e)}")
        return {'error': f'獲取可用季度列表時發生錯誤: {str(e)}'}

def generate_mock_stock_list(quarter=None):
    """
    生成模擬的低風險股票列表
    
    參數:
        quarter (str, optional): 季度
    
    返回:
        dict: 模擬的股票列表數據
    """
    # 定義模擬的季度和股票
    mock_quarters = ['2020-Q1', '2020-Q2', '2020-Q3', '2020-Q4', 
                     '2021-Q1', '2021-Q2', '2021-Q3', '2021-Q4',
                     '2022-Q1', '2022-Q2', '2022-Q3', '2022-Q4',
                     '2023-Q1', '2023-Q2', '2023-Q3', '2023-Q4']
    
    mock_stocks = {
        '2330': '台積電',
        '2317': '鴻海',
        '2454': '聯發科',
        '2412': '中華電',
        '2308': '台達電',
        '2881': '富邦金',
        '2882': '國泰金',
        '1301': '台塑',
        '1303': '南亞',
        '2303': '聯電'
    }
    
    # 如果指定了季度，檢查是否有效
    if quarter and quarter not in mock_quarters:
        return {
            'error': f'找不到季度 {quarter} 的股票列表',
            'available_quarters': mock_quarters
        }
    
    # 為每個季度生成不同的股票組合
    import random
    random.seed(42)  # 使用固定的種子以獲得一致的結果
    
    result = {}
    for q in mock_quarters:
        # 為每個季度隨機選擇 5-7 支股票
        num_stocks = random.randint(5, 7)
        selected_stocks = random.sample(list(mock_stocks.keys()), num_stocks)
        
        # 生成股票列表
        stocks = []
        for stock_id in selected_stocks:
            stocks.append({
                'stock_id': stock_id,
                'stock_name': mock_stocks[stock_id],
                'risk': round(random.uniform(0.1, 0.5), 2),
                'weight': round(random.uniform(0.05, 0.3), 2)
            })
        
        # 調整權重使總和為 1
        total_weight = sum(stock['weight'] for stock in stocks)
        for stock in stocks:
            stock['weight'] = round(stock['weight'] / total_weight, 2)
        
        # 再次調整以確保總和為 1（處理四捨五入的誤差）
        total_weight = sum(stock['weight'] for stock in stocks)
        if total_weight != 1:
            stocks[0]['weight'] += round(1 - total_weight, 2)
        
        result[q] = stocks
    
    if quarter:
        return {
            'quarter': quarter,
            'stocks': result[quarter],
            'is_mock_data': True
        }
    else:
        return {
            'quarters': mock_quarters,
            'stocks': result,
            'is_mock_data': True
        } 