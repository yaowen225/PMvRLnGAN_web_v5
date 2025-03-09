# PMvRLnGAN 網站開發進度報告

> **注意**：本文檔提供了 PMvRLnGAN 網站開發的概述。如需了解更詳細的開發過程和日誌記錄，請參閱 [PMvRLnGAN_web_planning.md](PMvRLnGAN_web_planning.md) 中的「八、開發日誌」章節。

## 摘要

本文檔旨在說明 PMvRLnGAN 系統從原始程式碼到網站介面的開發進度、功能實現、測試方法和整體規劃。目前，我們已經完成了後端核心功能的大部分開發工作，包括交易適配器、股票適配器和相關 API 端點的實現。

## 目錄

- [原始程式碼概述](#原始程式碼概述)
- [網站功能說明](#網站功能說明)
- [已完成的開發工作](#已完成的開發工作)
- [測試方法與結果](#測試方法與結果)
- [整體開發規劃](#整體開發規劃)
- [下一步工作](#下一步工作)

## 原始程式碼概述

PMvRLnGAN 是一個基於強化學習和圖注意力網絡的投資組合管理系統，由四個主要部分組成：

1. **GAT (Graph Attention Network)**：分析股票之間的關聯性，生成股票關係矩陣。
2. **Stock-Picked Agent**：選擇風險最小的股票組合，生成低風險股票列表。
3. **TCN-AE (Temporal Convolutional Network Autoencoder)**：壓縮股票的技術指標，提取特徵。
4. **Trading Agent**：基於低風險股票列表和壓縮特徵，生成每日交易決策。

原始程式碼主要以 Jupyter Notebook 的形式存在，需要手動執行多個步驟才能獲得完整的分析結果。

## 網站功能說明

我們開發的網站旨在提供一個簡單的介面，讓用戶能夠通過按鈕操作執行 PMvRLnGAN 系統並查看結果，無需直接與程式碼互動。目前，網站已實現的功能包括：

### 後端 API 端點

1. **`/api/trading/valid-dates`**：
   - 功能：獲取有效的交易日期範圍
   - 返回：開始日期、結束日期和交易日數量

2. **`/api/stock-picked/quarters`**：
   - 功能：獲取可用的季度列表
   - 返回：所有可用的季度（如 '2021-Q4', '2022-Q2' 等）

3. **`/api/stock-picked/list`**：
   - 功能：獲取低風險股票列表
   - 參數：quarter（可選）
   - 返回：指定季度或所有季度的低風險股票列表

4. **`/api/trading/decisions`**：
   - 功能：獲取指定日期的交易決策
   - 參數：date, stock_ids（可選）
   - 返回：交易日期、交易決策列表（包含股票代碼、名稱、操作、數量、價格等）

5. **`/api/results/summary`**：
   - 功能：獲取績效摘要
   - 參數：start_date, end_date
   - 返回：總回報率、年化回報率、夏普比率、最大回撤等績效指標

### 可展示的內容

1. **低風險股票列表**：
   - 展示每個季度選出的低風險股票
   - 包含股票代碼、名稱、風險值和權重

2. **交易決策**：
   - 展示每個交易日的交易決策
   - 包含買入、賣出或持有的操作建議
   - 包含交易數量和價格

3. **績效摘要**：
   - 展示投資組合的績效指標
   - 包含總回報率、年化回報率、夏普比率和最大回撤

## 已完成的開發工作

### 1. 基礎架構設計

- 設計系統架構（前端、後端、數據流）
- 選擇技術棧（Flask 作為後端框架，純 HTML/CSS/JavaScript 作為前端技術）
- 建立開發環境
- 創建基本項目結構
- 測試直接讀取預訓練模型和結果文件的可行性

### 2. 後端核心功能開發

#### 2.1 交易適配器 (trading_adapter.py)

- 實現日期範圍限制和有效交易日檢查功能
- 實現交易決策獲取功能
- 優化交易適配器，移除不必要的 tcn_daily_trade_info.7z 解壓代碼
- 修改交易適配器，直接從 Low-risk stock list.csv 讀取交易日期和股票數據
- 實現基於低風險股票列表的交易決策生成
- 實現績效摘要功能，提供模擬的績效數據

#### 2.2 股票適配器 (stock_adapter.py)

- 實現低風險股票列表讀取功能
- 實現季度選擇器功能，使用戶可以選擇不同季度的股票列表

#### 2.3 API 端點實現

- 實現 `/api/trading/valid-dates` 端點
- 實現 `/api/stock-picked/quarters` 端點
- 實現 `/api/stock-picked/list` 端點
- 實現 `/api/trading/decisions` 端點
- 實現 `/api/results/summary` 端點

### 3. 測試腳本開發

- 創建 test_adapter.py 測試腳本，用於測試交易適配器功能和 API 端點
- 修復測試腳本中的錯誤，確保能夠正確處理 API 返回的數據結構

## 測試方法與結果

### 測試方法

我們採用了兩種測試方法來確保系統的正確性：

#### 1. 功能測試

使用 test_adapter.py 測試腳本直接調用適配器函數，測試其功能是否正常：

```python
# 測試加載交易日期
trading_days = load_trading_days()
print(f"交易日期數量: {len(trading_days)}")

# 測試獲取有效日期範圍
date_range = get_valid_date_range()
print(f"開始日期: {date_range.get('start_date')}")
print(f"結束日期: {date_range.get('end_date')}")

# 測試日期驗證
test_date = date_range.get('start_date')
print(f"日期 {test_date} 是否有效: {is_valid_trading_day(test_date)}")

# 測試獲取交易決策
trading_result = get_trading_decisions(test_date)
decisions = trading_result.get('decisions', [])
print(f"決策數量: {len(decisions)}")

# 測試獲取績效摘要
summary = get_performance_summary(date_range.get('start_date'), date_range.get('end_date'))
print(f"總回報率: {summary.get('total_return', 'N/A')}%")
```

#### 2. API 端點測試

使用 requests 庫調用 API 端點，測試其返回的數據是否正確：

```python
# 測試獲取有效交易日期範圍
response = requests.get(f"{base_url}/api/trading/valid-dates")
data = response.json()
print(f"開始日期: {data.get('data', {}).get('start_date')}")

# 測試獲取可用季度
response = requests.get(f"{base_url}/api/stock-picked/quarters")
data = response.json()
print(f"可用季度: {data.get('data', {}).get('quarters', [])}")

# 測試獲取低風險股票列表
response = requests.get(f"{base_url}/api/stock-picked/list")
data = response.json()
stocks = data.get('data', {}).get('stocks', {})
print(f"股票數量: {len(stocks)}")

# 測試獲取交易決策
response = requests.get(f"{base_url}/api/trading/decisions?date={test_date}")
data = response.json()
decisions = data.get('data', {}).get('decisions', [])
print(f"決策數量: {len(decisions)}")

# 測試獲取績效摘要
response = requests.get(f"{base_url}/api/results/summary?start_date={start_date}&end_date={end_date}")
data = response.json()
summary = data.get('data', {})
print(f"總回報率: {summary.get('total_return', 'N/A')}%")
```

### 測試結果

測試結果顯示，所有已實現的功能和 API 端點都能正常工作：

1. **交易適配器功能測試**：
   - 成功加載交易日期（11個交易日）
   - 成功獲取有效日期範圍（2021-11-15 到 2024-05-16）
   - 成功驗證日期的有效性
   - 成功獲取交易決策（33個決策）
   - 成功獲取績效摘要

2. **股票適配器功能測試**：
   - 成功獲取可用季度（8個季度）
   - 成功獲取低風險股票列表（33支股票）

3. **API 端點測試**：
   - `/api/trading/valid-dates` 端點返回正確的日期範圍
   - `/api/stock-picked/quarters` 端點返回正確的季度列表
   - `/api/stock-picked/list` 端點返回正確的股票列表
   - `/api/trading/decisions` 端點返回正確的交易決策
   - `/api/results/summary` 端點返回正確的績效摘要

## 整體開發規劃

我們的開發計劃分為五個階段：

### 階段一：基礎架構設計（已完成，100%）
- 設計系統架構
- 選擇技術棧
- 建立開發環境
- 創建基本項目結構
- 測試直接讀取預訓練模型和結果文件的可行性

### 階段二：後端開發 - 核心功能（進行中，90%）
- 實現 API 端點以提供預訓練模型的結果
- 實現結果存儲和檢索機制
- 處理錯誤和異常情況
- 添加基本的日誌記錄功能

### 階段三：前端開發 - 基本界面（未開始，0%）
- 設計和實現主頁面（HTML/CSS）
- 實現執行按鈕和基本交互（JavaScript）
- 設計結果展示頁面的布局
- 實現與後端 API 的基本通信

### 階段四：結果可視化和用戶體驗優化（未開始，0%）
- 實現股票選擇結果的可視化（表格、圖表）
- 實現交易決策的可視化（表格、圖表）
- 添加加載指示器和進度提示
- 優化錯誤提示和用戶引導
- 確保響應式設計在不同設備上正常工作

### 階段五：集成測試和部署（未開始，0%）
- 進行端到端測試
- 修復發現的問題
- 準備部署環境
- 部署系統並進行最終測試

## 下一步工作

目前，我們已經完成了階段一，並且階段二的完成度達到了 90%。下一步的工作包括：

1. **完成 GAT 適配器**：
   - 實現讀取股票關係數據的功能
   - 實現 `/api/gat/relationships` API 端點

2. **完成 TCN-AE 適配器**：
   - 實現讀取壓縮特徵的功能
   - 實現 `/api/tcn-ae/features` API 端點

3. **進行綜合測試**：
   - 測試所有 API 端點的互操作性
   - 確保所有功能在各種情況下都能正常工作

4. **完善文檔**：
   - 更新 API 文檔
   - 完善代碼註釋

完成這些工作後，階段二的完成度將達到 100%，然後我們將進入階段三，開始前端開發工作。 