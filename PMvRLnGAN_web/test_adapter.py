#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
測試交易適配器功能和API端點
"""

import sys
import os
import json
import traceback
from datetime import datetime

# 添加項目根目錄到Python路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# 導入交易適配器函數
from backend.adapters.trading_adapter import (
    load_trading_days, 
    get_trading_decisions, 
    get_valid_date_range,
    get_performance_summary,
    is_valid_trading_day
)

# 導入股票適配器函數
from backend.adapters.stock_adapter import (
    get_stock_list,
    get_available_quarters
)

def test_trading_adapter():
    """測試交易適配器的主要功能"""
    print("=== 測試交易適配器功能 ===")
    
    # 測試加載交易日期
    print("\n1. 測試加載交易日期:")
    trading_days = load_trading_days()
    print(f"  - 交易日期數量: {len(trading_days)}")
    if len(trading_days) > 0:
        print(f"  - 第一個交易日: {trading_days[0]}")
        print(f"  - 最後一個交易日: {trading_days[-1]}")
    
    # 測試獲取有效日期範圍
    print("\n2. 測試獲取有效日期範圍:")
    date_range = get_valid_date_range()
    print(f"  - 開始日期: {date_range.get('start_date')}")
    print(f"  - 結束日期: {date_range.get('end_date')}")
    print(f"  - 交易日數量: {date_range.get('trading_days_count')}")
    
    # 測試日期驗證
    print("\n3. 測試日期驗證:")
    test_date = date_range.get('start_date')
    print(f"  - 日期 {test_date} 是否有效: {is_valid_trading_day(test_date)}")
    
    # 測試獲取交易決策
    print("\n4. 測試獲取交易決策:")
    trading_result = get_trading_decisions(test_date)
    if 'error' in trading_result:
        print(f"  - 錯誤: {trading_result.get('error')}")
    else:
        decisions = trading_result.get('decisions', [])
        print(f"  - 日期: {trading_result.get('date')}")
        print(f"  - 決策數量: {len(decisions)}")
        if decisions and len(decisions) > 0:
            print(f"  - 第一個決策: {decisions[0]}")
    
    # 測試獲取績效摘要
    print("\n5. 測試獲取績效摘要:")
    summary = get_performance_summary(date_range.get('start_date'), date_range.get('end_date'))
    print(f"  - 總回報率: {summary.get('total_return', 'N/A')}%")
    print(f"  - 年化回報率: {summary.get('annualized_return', 'N/A')}%")
    print(f"  - 夏普比率: {summary.get('sharpe_ratio', 'N/A')}")
    print(f"  - 最大回撤: {summary.get('max_drawdown', 'N/A')}%")
    
    # 測試獲取低風險股票列表
    print("\n6. 測試獲取低風險股票列表:")
    quarters = get_available_quarters()
    print(f"  - 可用季度: {quarters.get('quarters', [])}")
    if quarters.get('quarters'):
        stock_data = get_stock_list(quarters.get('quarters')[0])
        print(f"  - {quarters.get('quarters')[0]} 季度的股票數據類型: {type(stock_data)}")
        if 'stocks' in stock_data and stock_data['stocks']:
            print(f"  - 股票數量: {len(stock_data['stocks'])}")
            if len(stock_data['stocks']) > 0:
                print(f"  - 第一支股票: {stock_data['stocks'][0]}")

def test_api_endpoints():
    """測試API端點"""
    print("\n=== 測試API端點 ===")
    print("注意: 此測試需要應用程序正在運行")
    
    try:
        import requests
        base_url = "http://localhost:5000"
        
        # 測試獲取有效交易日期範圍
        print("\n1. 測試 /api/trading/valid-dates 端點:")
        try:
            response = requests.get(f"{base_url}/api/trading/valid-dates")
            if response.status_code == 200:
                data = response.json()
                print(f"  - 狀態碼: {response.status_code}")
                print(f"  - 狀態: {data.get('status')}")
                if data.get('status') == 'success' and 'data' in data:
                    date_range = data.get('data', {})
                    print(f"  - 開始日期: {date_range.get('start_date')}")
                    print(f"  - 結束日期: {date_range.get('end_date')}")
                    print(f"  - 交易日數量: {date_range.get('trading_days_count')}")
                else:
                    print(f"  - 錯誤信息: {data.get('message', '未知錯誤')}")
            else:
                print(f"  - 錯誤: 狀態碼 {response.status_code}")
        except Exception as e:
            print(f"  - 測試 /api/trading/valid-dates 端點時發生錯誤: {str(e)}")
            traceback.print_exc()
        
        # 測試獲取可用季度
        print("\n2. 測試 /api/stock-picked/quarters 端點:")
        try:
            response = requests.get(f"{base_url}/api/stock-picked/quarters")
            if response.status_code == 200:
                data = response.json()
                print(f"  - 狀態碼: {response.status_code}")
                print(f"  - 狀態: {data.get('status')}")
                if data.get('status') == 'success' and 'data' in data:
                    quarters_data = data.get('data', {})
                    print(f"  - 可用季度: {quarters_data.get('quarters', [])}")
                else:
                    print(f"  - 錯誤信息: {data.get('message', '未知錯誤')}")
            else:
                print(f"  - 錯誤: 狀態碼 {response.status_code}")
        except Exception as e:
            print(f"  - 測試 /api/stock-picked/quarters 端點時發生錯誤: {str(e)}")
            traceback.print_exc()
        
        # 測試獲取低風險股票列表
        print("\n3. 測試 /api/stock-picked/list 端點:")
        try:
            response = requests.get(f"{base_url}/api/stock-picked/list")
            if response.status_code == 200:
                data = response.json()
                print(f"  - 狀態碼: {response.status_code}")
                print(f"  - 狀態: {data.get('status')}")
                if data.get('status') == 'success' and 'data' in data:
                    stock_data = data.get('data', {})
                    print(f"  - 股票數據類型: {type(stock_data)}")
                    print(f"  - 股票數據鍵: {list(stock_data.keys())}")
                    
                    # 檢查 'stocks' 鍵是否存在
                    if 'stocks' in stock_data:
                        stocks = stock_data.get('stocks', [])
                        print(f"  - 股票數量: {len(stocks)}")
                        print(f"  - 股票類型: {type(stocks)}")
                        
                        # 檢查 stocks 是否為列表或字典
                        if isinstance(stocks, list) and len(stocks) > 0:
                            print(f"  - 第一支股票: {stocks[0]}")
                        elif isinstance(stocks, dict) and len(stocks) > 0:
                            # 如果是字典，顯示第一個鍵值對
                            first_key = list(stocks.keys())[0]
                            print(f"  - 第一支股票 (鍵: {first_key}): {stocks[first_key]}")
                        else:
                            print(f"  - 股票數據為空或格式不支持")
                    else:
                        # 如果沒有 'stocks' 鍵，嘗試直接顯示 stock_data
                        print(f"  - 沒有 'stocks' 鍵，直接顯示數據: {stock_data}")
                        
                        # 如果 stock_data 是字典，嘗試顯示第一個鍵值對
                        if isinstance(stock_data, dict) and len(stock_data) > 0:
                            first_key = list(stock_data.keys())[0]
                            print(f"  - 第一個季度 (鍵: {first_key}): {stock_data[first_key][:1] if isinstance(stock_data[first_key], list) and len(stock_data[first_key]) > 0 else '無數據'}")
                else:
                    print(f"  - 錯誤信息: {data.get('message', '未知錯誤')}")
            else:
                print(f"  - 錯誤: 狀態碼 {response.status_code}")
        except Exception as e:
            print(f"  - 測試 /api/stock-picked/list 端點時發生錯誤: {str(e)}")
            traceback.print_exc()
        
        # 獲取有效日期用於測試
        try:
            response = requests.get(f"{base_url}/api/trading/valid-dates")
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success' and 'data' in data:
                    date_range = data.get('data', {})
                    test_date = date_range.get('start_date')
                    
                    # 測試獲取交易決策
                    print("\n4. 測試 /api/trading/decisions 端點:")
                    try:
                        response = requests.get(f"{base_url}/api/trading/decisions?date={test_date}")
                        if response.status_code == 200:
                            data = response.json()
                            print(f"  - 狀態碼: {response.status_code}")
                            print(f"  - 狀態: {data.get('status')}")
                            if data.get('status') == 'success' and 'data' in data:
                                trading_data = data.get('data', {})
                                decisions = trading_data.get('decisions', [])
                                print(f"  - 日期: {trading_data.get('date')}")
                                print(f"  - 決策數量: {len(decisions)}")
                                if decisions and len(decisions) > 0:
                                    print(f"  - 第一個決策: {decisions[0]}")
                            else:
                                print(f"  - 錯誤信息: {data.get('message', '未知錯誤')}")
                        else:
                            print(f"  - 錯誤: 狀態碼 {response.status_code}")
                            print(f"  - 響應內容: {response.text}")
                    except Exception as e:
                        print(f"  - 測試 /api/trading/decisions 端點時發生錯誤: {str(e)}")
                        traceback.print_exc()
                    
                    # 測試獲取績效摘要
                    print("\n5. 測試 /api/results/summary 端點:")
                    try:
                        start_date = date_range.get('start_date')
                        end_date = date_range.get('end_date')
                        response = requests.get(f"{base_url}/api/results/summary?start_date={start_date}&end_date={end_date}")
                        if response.status_code == 200:
                            data = response.json()
                            print(f"  - 狀態碼: {response.status_code}")
                            print(f"  - 狀態: {data.get('status')}")
                            if data.get('status') == 'success' and 'data' in data:
                                summary = data.get('data', {})
                                print(f"  - 總回報率: {summary.get('total_return', 'N/A')}%")
                                print(f"  - 年化回報率: {summary.get('annualized_return', 'N/A')}%")
                                print(f"  - 夏普比率: {summary.get('sharpe_ratio', 'N/A')}")
                                print(f"  - 最大回撤: {summary.get('max_drawdown', 'N/A')}%")
                            else:
                                print(f"  - 錯誤信息: {data.get('message', '未知錯誤')}")
                        else:
                            print(f"  - 錯誤: 狀態碼 {response.status_code}")
                            print(f"  - 響應內容: {response.text}")
                    except Exception as e:
                        print(f"  - 測試 /api/results/summary 端點時發生錯誤: {str(e)}")
                        traceback.print_exc()
                else:
                    print("無法獲取有效日期範圍，跳過後續測試")
            else:
                print(f"獲取有效日期範圍失敗，狀態碼: {response.status_code}")
        except Exception as e:
            print(f"獲取有效日期範圍時發生錯誤: {str(e)}")
            traceback.print_exc()
    
    except Exception as e:
        print(f"測試API端點時發生錯誤: {str(e)}")
        traceback.print_exc()
        print("請確保應用程序正在運行，並且可以通過 http://localhost:5000 訪問")

if __name__ == "__main__":
    print("開始測試交易適配器和API端點...\n")
    
    # 測試交易適配器功能
    test_trading_adapter()
    
    # 詢問用戶是否要測試API端點
    response = input("\n是否要測試API端點？(需要應用程序正在運行) [y/N]: ")
    if response.lower() == 'y':
        test_api_endpoints()
    
    print("\n測試完成！") 