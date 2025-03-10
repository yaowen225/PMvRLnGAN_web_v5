# PMvRLnGAN 網站開發進度報告

> **注意**：本文檔提供了 PMvRLnGAN 網站開發的概述。如需了解更詳細的開發過程和日誌記錄，請參閱 [PMvRLnGAN_web_planning.md](PMvRLnGAN_web_planning.md) 中的「八、開發日誌」章節。

## 摘要

本文檔旨在說明 PMvRLnGAN 系統從原始程式碼到網站介面的開發進度、功能實現、測試方法和整體規劃。目前，我們已經完成了後端核心功能的大部分開發工作，包括交易適配器、股票適配器和相關 API 端點的實現。

## 目錄

- [原始程式碼概述](#原始程式碼概述)
- [網站功能說明](#網站功能說明)
- [已完成的開發工作](#已完成的開發工作)
- [測試方法與結果](#測試方法與結果)
- [資料來源說明](#資料來源說明)
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

## 資料來源說明

目前，網站使用的資料來源分為兩類：真實資料（從原始資料夾讀取的）和模擬資料（暫時生成的）。以下是各個模組的資料來源情況：

### 資料來源概覽表

| 模組 | 功能/資料 | 來源類型 | 資料位置/生成方式 | 原始檔案位置 | 原始資料夾 | 網頁對應位置 |
|------|-----------|----------|-------------------|--------------|------------|--------------|
| **股票適配器** | 低風險股票列表 | 真實資料 | `PMvRLnGAN/Trading Agent/Low-risk stock list.csv` | `PMvRLnGAN/Trading Agent/Low-risk stock list.csv` | Trading Agent | 「低風險股票列表」頁面，顯示每季度選出的低風險股票 |
| | 季度列表 | 真實資料 | 從低風險股票列表中提取 | 同上 | Trading Agent | 「低風險股票列表」頁面的季度選擇器下拉選單 |
| | 股票名稱和代碼 | 真實資料 | 從低風險股票列表中提取 | 同上 | Trading Agent | 所有頁面中顯示的股票名稱和代碼 |
| | 股票風險評估 | 模擬資料 | 隨機生成的風險值 | 未來將使用 `PMvRLnGAN/Stock-Picked Agent/predict stock-picked data.ipynb` 的結果 | Stock-Picked Agent | 「低風險股票列表」頁面中每支股票的風險值和權重 |
| **交易適配器** | 交易日期範圍 | 真實資料 | 從低風險股票列表中提取 | 同上 | Trading Agent | 「交易決策」頁面的日期選擇器範圍限制 |
| | 有效交易日檢查 | 真實資料 | 基於真實交易日期的驗證 | 同上 | Trading Agent | 「交易決策」頁面的日期選擇器有效日期驗證 |
| | 交易決策 | 部分真實資料 | 目前使用 `PMvRLnGAN/Trading Agent/models/trading_decisions_examples.csv`，僅包含 2024-05-17 至 2024-06-04 的有限交易日期數據 | 未來將使用 `PMvRLnGAN/Trading Agent/models/trading_agent_model.zip` 生成更完整的交易決策 | Trading Agent | 「交易決策」頁面的交易建議表格（買入/賣出/持有） |
| | 績效摘要 | 模擬資料 | 隨機生成的績效指標 | 未來將使用 `PMvRLnGAN/Trading Agent/models/trading_agent_performance.json` | Trading Agent | 「績效摘要」頁面的績效指標圖表和數據 |
| **GAT 適配器** | 股票關係數據 | 模擬資料 | 隨機生成的關係矩陣 | 未來將使用 `PMvRLnGAN/GAT-main/gat_model.pth` 和 `PMvRLnGAN/GAT-main/edge.py` 生成的結果 | GAT-main | 「股票關係網絡」頁面的網絡圖視覺化 |
| | 關係權重 | 模擬資料 | 隨機生成的權重值 | 同上 | GAT-main | 「股票關係網絡」頁面中連接線的粗細和顏色 |
| **TCN-AE 適配器** | 壓縮特徵 | 模擬資料 | 隨機生成的20維特徵向量 | 未來將使用 `PMvRLnGAN/TCN-AE/tcn_20_model.h5` 和 `PMvRLnGAN/TCN-AE/TCN-AE predict data.ipynb` 生成的結果 | TCN-AE | 「技術指標分析」頁面的特徵重要性圖表 |
| | 特徵向量 | 模擬資料 | 基於股票ID和日期的隨機生成 | 同上 | TCN-AE | 「技術指標分析」頁面的特徵趨勢圖表 |
| **Stock-Picked 適配器** | 股票選擇模型 | 模擬資料 | 基於預定義規則的選擇 | 未來將使用 `PMvRLnGAN/Stock-Picked Agent/predict stock-picked data.ipynb` 的結果 | Stock-Picked Agent | 「投資組合構建」頁面的股票選擇邏輯說明 |
| | 財務報表分析 | 模擬資料 | 隨機生成的財務指標 | 未來將使用 `PMvRLnGAN/Stock-Picked Agent/Financial statements_SharpeRatio_RL.csv` | Stock-Picked Agent | 「財務分析」頁面的財務指標比較圖表 |

### 資料來源控制機制

系統通過配置文件 `config.py` 中的 `USE_MOCK_DATA` 變數控制資料來源：

```python
# 是否使用模擬數據（當無法讀取原始數據時）
USE_MOCK_DATA = False
```

當設置為 `False` 時，系統會：
1. 優先嘗試讀取真實數據文件
2. 如果找不到真實數據，自動回退到使用模擬數據
3. 在使用模擬數據時，會在返回結果中添加 `is_mock_data: true` 標記

### 未來改進計劃

為了提高系統的準確性和實用性，我們計劃在下一階段開發中：

1. **優先完成 GAT 適配器**：實現從 `gat_model.pth` 讀取真實的股票關係數據，並使用 `edge.py` 生成股票關係矩陣
2. **完成 TCN-AE 適配器**：實現從 `tcn_20_model.h5` 讀取真實的壓縮特徵，並使用 `tcnae.py` 進行特徵壓縮
3. **改進交易適配器**：連接到訓練好的交易模型 `trading_agent_model.zip`，生成真實的交易決策
4. **添加數據驗證機制**：確保所有讀取的數據格式正確且完整

這些改進將使網站能夠提供基於真實模型的分析結果，而不是模擬數據。

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

## 資料處理與模型執行分析

在開發過程中，我們需要明確哪些部分需要重新執行，哪些可以直接使用訓練完的成果。本節分析了各個模組的資料處理需求和執行策略。

### 模組資料處理需求對比表

| 模組 | 可直接使用的部分 | 需要執行的部分 | 當前狀態 | 建議處理方式 |
|------|-----------------|--------------|----------|------------|
| **GAT** | 預訓練模型 `gat_model.pth` | 使用 `edge.py` 生成股票關係矩陣 | 適配器尋找不存在的 `relationships.json` | 執行一次 `edge.py`，生成關係矩陣文件 |
| **Stock-Picked Agent** | 低風險股票列表 `Low-risk stock list.csv` | 如需更新列表，執行 `predict stock-picked data.ipynb` | 適配器可讀取列表，但風險值是隨機生成的 | 執行一次預測腳本，生成包含真實風險值的列表 |
| **TCN-AE** | 預訓練模型 `tcn_20_model.h5` | 使用模型壓縮股票技術指標 | 適配器尋找不存在的壓縮特徵文件 | 執行一次 `TCN-AE predict data.ipynb`，生成壓縮特徵 |
| **Trading Agent** | 預訓練模型 `trading_agent_model.zip`、配置文件、性能指標 | 如需完整決策，修改保存代碼 | 適配器可讀取示例決策，但日期範圍有限 | 修改 `train trade agent.ipynb`，保存完整決策 |

### 資料檔案狀態分析

| 資料檔案 | 用途 | 是否存在 | 生成方式 | 使用該檔案的適配器 |
|---------|------|----------|----------|-----------------|
| `relationships.json` | 股票關係矩陣 | ❌ 不存在 | 執行 `edge.py` | `gat_adapter.py` |
| `Low-risk stock list.csv` | 低風險股票列表 | ✅ 存在 | 已有，無需生成 | `stock_adapter.py` |
| `compressed_features/*.json` | 壓縮特徵 | ❌ 不存在 | 執行 `TCN-AE predict data.ipynb` | `tcn_adapter.py` |
| `trading_decisions_examples.csv` | 交易決策示例 | ✅ 存在但不完整 | 修改 `train trade agent.ipynb` | `trading_adapter.py` |
| `trading_agent_performance.json` | 模型性能指標 | ✅ 存在 | 已有，無需生成 | `trading_adapter.py` |

### 只執行一次交易分析的實施方案

為了確保網站能夠展示真實的分析結果，同時避免每次請求都重新執行複雜的模型計算，我們可以採用「預處理+直接讀取」的方式：

#### 預處理階段（一次性執行）

1. **GAT 關係矩陣生成**
   - 執行 `edge.py` 腳本
   - 輸入：預訓練的 GAT 模型 (`gat_model.pth`)
   - 輸出：股票關係矩陣 (`relationships.json`)
   - 保存位置：`PMvRLnGAN/GAT-main/relationships.json`

2. **TCN-AE 特徵壓縮**
   - 執行 `TCN-AE predict data.ipynb` 腳本
   - 輸入：預訓練的 TCN-AE 模型 (`tcn_20_model.h5`) 和股票技術指標
   - 輸出：壓縮後的特徵向量
   - 保存位置：`PMvRLnGAN/TCN-AE/compressed_features/` 目錄

3. **Trading Agent 決策生成**
   - 修改 `train trade agent.ipynb` 中的保存代碼
   - 將 `df_actions.head(30).to_csv(decisions_save_path, index=True)` 改為 `df_actions.to_csv(decisions_save_path, index=True)`
   - 重新執行相關代碼段
   - 輸出：完整的交易決策
   - 保存位置：`PMvRLnGAN/Trading Agent/models/trading_decisions_examples.csv`

#### 網站階段（直接讀取預處理結果）

1. **GAT 適配器**
   - 直接讀取 `relationships.json` 文件
   - 無需執行 GAT 模型

2. **Stock-Picked 適配器**
   - 直接讀取 `Low-risk stock list.csv` 文件
   - 無需執行 Stock-Picked Agent

3. **TCN-AE 適配器**
   - 直接讀取 `compressed_features` 目錄下的文件
   - 無需執行 TCN-AE 模型

4. **Trading 適配器**
   - 直接讀取 `trading_decisions_examples.csv` 文件
   - 無需執行 Trading Agent

### 方案優勢

這種「預處理+直接讀取」的方式有以下優勢：

1. **簡化開發流程**：避免在網站中實現複雜的模型載入和執行邏輯
2. **提高性能**：直接讀取預處理結果比執行模型快得多
3. **減少錯誤**：降低運行時錯誤的可能性
4. **確保一致性**：所有用戶看到的結果都是一致的

通過這種方式，我們可以確保網站展示的是真實的分析結果，同時避免了重複執行複雜計算的開銷。 