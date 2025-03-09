"""
TCN-AE 適配器模組
負責從原始程式碼中讀取 TCN-AE 模型生成的壓縮特徵，並提供給網站 API
"""

import os
import json
import numpy as np
import pandas as pd
import logging
from datetime import datetime
from ..config import (
    PMVRLNGAN_DIR,
    TCN_MODEL_PATH,
    USE_MOCK_DATA,
    TRADE_INFO_PATH
)

# 設置日誌
logger = logging.getLogger(__name__)

# 緩存壓縮特徵
_compressed_features = {}

def load_compressed_features(stock_id, date=None):
    """
    加載指定股票的壓縮特徵
    
    參數:
        stock_id (str): 股票 ID
        date (str, optional): 日期，格式為 'YYYY-MM-DD'
        
    返回:
        dict: 壓縮特徵數據
    """
    global _compressed_features
    
    # 生成緩存鍵
    cache_key = f"{stock_id}_{date}" if date else stock_id
    
    # 如果已經加載過，直接返回緩存的結果
    if cache_key in _compressed_features:
        return _compressed_features[cache_key]
    
    try:
        if not USE_MOCK_DATA:
            # 嘗試從 TCN-AE 模型結果文件中讀取壓縮特徵
            features_dir = os.path.join(PMVRLNGAN_DIR, 'TCN-AE', 'compressed_features')
            
            # 如果指定了日期，嘗試讀取該日期的特徵
            if date:
                features_path = os.path.join(features_dir, f"{stock_id}_{date}.json")
                if os.path.exists(features_path):
                    with open(features_path, 'r') as f:
                        features = json.load(f)
                    logger.info(f"成功從文件加載壓縮特徵: {features_path}")
                    _compressed_features[cache_key] = features
                    return features
            
            # 如果沒有指定日期或找不到指定日期的文件，嘗試讀取所有日期的特徵
            features_path = os.path.join(features_dir, f"{stock_id}.json")
            if os.path.exists(features_path):
                with open(features_path, 'r') as f:
                    features = json.load(f)
                logger.info(f"成功從文件加載壓縮特徵: {features_path}")
                _compressed_features[cache_key] = features
                return features
            else:
                logger.warning(f"找不到壓縮特徵文件: {features_path}")
                return generate_mock_features(stock_id, date)
        else:
            return generate_mock_features(stock_id, date)
    except Exception as e:
        logger.error(f"加載壓縮特徵時發生錯誤: {str(e)}")
        return generate_mock_features(stock_id, date)

def generate_mock_features(stock_id, date=None):
    """
    生成模擬的壓縮特徵
    
    參數:
        stock_id (str): 股票 ID
        date (str, optional): 日期，格式為 'YYYY-MM-DD'
        
    返回:
        dict: 模擬的壓縮特徵數據
    """
    # 獲取股票名稱
    from .stock_adapter import get_stock_name
    stock_name = get_stock_name(stock_id)
    
    # 生成模擬的壓縮特徵
    np.random.seed(int(stock_id))  # 使用股票 ID 作為種子以獲得一致的結果
    
    # 生成 20 維的特徵向量
    features = np.random.randn(20).tolist()
    
    # 如果指定了日期，生成該日期的特徵
    if date:
        return {
            'stock_id': stock_id,
            'stock_name': stock_name,
            'date': date,
            'features': features,
            'is_mock_data': True
        }
    else:
        # 生成最近 30 天的特徵
        from .trading_adapter import load_trading_days
        trading_days = load_trading_days()
        
        # 取最近的 30 個交易日
        recent_days = sorted(trading_days)[-30:]
        
        daily_features = {}
        for day in recent_days:
            day_str = day.strftime('%Y-%m-%d')
            # 為每天生成略有不同的特徵
            day_seed = int(day_str.replace('-', ''))
            np.random.seed(int(stock_id) + day_seed)
            daily_features[day_str] = np.random.randn(20).tolist()
        
        return {
            'stock_id': stock_id,
            'stock_name': stock_name,
            'daily_features': daily_features,
            'is_mock_data': True
        }

def get_compressed_features(stock_id, date=None):
    """
    獲取指定股票的壓縮特徵
    
    參數:
        stock_id (str): 股票 ID
        date (str, optional): 日期，格式為 'YYYY-MM-DD'
        
    返回:
        dict: 壓縮特徵數據
    """
    try:
        # 檢查股票 ID
        if not stock_id:
            return {'error': '股票 ID 不能為空'}
        
        # 檢查日期格式（如果提供）
        if date:
            try:
                datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                return {'error': '日期格式無效，請使用 YYYY-MM-DD 格式'}
        
        # 加載壓縮特徵
        features = load_compressed_features(stock_id, date)
        return features
    except Exception as e:
        logger.error(f"獲取壓縮特徵時發生錯誤: {str(e)}")
        return {'error': f'獲取壓縮特徵時發生錯誤: {str(e)}'} 