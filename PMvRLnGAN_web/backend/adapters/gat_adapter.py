"""
GAT 適配器模組
負責從原始程式碼中讀取 GAT 模型生成的股票關係數據，並提供給網站 API
"""

import os
import json
import numpy as np
import pandas as pd
import logging
from ..config import (
    PMVRLNGAN_DIR,
    GAT_MODEL_PATH,
    USE_MOCK_DATA
)

# 設置日誌
logger = logging.getLogger(__name__)

# 緩存股票關係數據
_stock_relationships = None

def load_stock_relationships():
    """
    加載股票關係數據
    
    返回:
        dict: 股票關係數據
    """
    global _stock_relationships
    
    # 如果已經加載過，直接返回緩存的結果
    if _stock_relationships is not None:
        return _stock_relationships
    
    try:
        if not USE_MOCK_DATA:
            # 嘗試從 GAT 模型結果文件中讀取股票關係數據
            relationships_path = os.path.join(PMVRLNGAN_DIR, 'GAT-main', 'relationships.json')
            
            if os.path.exists(relationships_path):
                with open(relationships_path, 'r') as f:
                    _stock_relationships = json.load(f)
                logger.info(f"成功從文件加載股票關係數據: {relationships_path}")
                return _stock_relationships
            else:
                logger.warning(f"找不到股票關係數據文件: {relationships_path}")
                # 嘗試從低風險股票列表中獲取股票列表
                from .stock_adapter import get_stock_list
                stock_list = get_stock_list()
                if 'stocks' in stock_list:
                    stocks = stock_list['stocks']
                    # 生成模擬的股票關係數據
                    return generate_mock_relationships(stocks)
                else:
                    return generate_mock_relationships()
        else:
            return generate_mock_relationships()
    except Exception as e:
        logger.error(f"加載股票關係數據時發生錯誤: {str(e)}")
        return generate_mock_relationships()

def generate_mock_relationships(stocks=None):
    """
    生成模擬的股票關係數據
    
    參數:
        stocks (list, optional): 股票列表
        
    返回:
        dict: 模擬的股票關係數據
    """
    # 如果未提供股票列表，使用默認列表
    if stocks is None:
        stocks = [
            {'stock_id': '2330', 'stock_name': '台積電'},
            {'stock_id': '2317', 'stock_name': '鴻海'},
            {'stock_id': '2454', 'stock_name': '聯發科'},
            {'stock_id': '2412', 'stock_name': '中華電'},
            {'stock_id': '2308', 'stock_name': '台達電'}
        ]
    
    # 生成模擬的關係矩陣
    n = len(stocks)
    np.random.seed(42)  # 使用固定的種子以獲得一致的結果
    
    # 生成隨機的關係權重（0.0-1.0）
    relationships_matrix = np.random.rand(n, n)
    
    # 確保對角線為 1.0（自己與自己的關係最強）
    np.fill_diagonal(relationships_matrix, 1.0)
    
    # 確保矩陣對稱（關係是雙向的）
    relationships_matrix = (relationships_matrix + relationships_matrix.T) / 2
    
    # 將矩陣轉換為列表格式
    relationships = []
    for i in range(n):
        for j in range(i+1, n):  # 只保存上三角矩陣（避免重複）
            if relationships_matrix[i, j] > 0.5:  # 只保存關係強度大於 0.5 的
                relationships.append({
                    'source': stocks[i]['stock_id'],
                    'source_name': stocks[i]['stock_name'],
                    'target': stocks[j]['stock_id'],
                    'target_name': stocks[j]['stock_name'],
                    'weight': float(relationships_matrix[i, j])
                })
    
    # 按關係強度排序
    relationships.sort(key=lambda x: x['weight'], reverse=True)
    
    return {
        'stocks': stocks,
        'relationships': relationships,
        'is_mock_data': True
    }

def get_stock_relationships():
    """
    獲取股票關係數據
    
    返回:
        dict: 股票關係數據
    """
    try:
        # 加載股票關係數據
        relationships = load_stock_relationships()
        return relationships
    except Exception as e:
        logger.error(f"獲取股票關係數據時發生錯誤: {str(e)}")
        return {'error': f'獲取股票關係數據時發生錯誤: {str(e)}'} 