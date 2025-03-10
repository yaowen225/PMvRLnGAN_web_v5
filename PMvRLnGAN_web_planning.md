# PMvRLnGAN 網站開發規劃

## 摘要

> **核心目標**：建立一個網站介面，讓用戶能通過簡單按鈕操作執行 PMvRLnGAN 系統並查看結果。
> 
> **關鍵決策**：
> - 使用預訓練模型和結果文件，避免執行 Jupyter Notebook
> - 採用純 HTML/CSS/JavaScript 作為前端技術
> - 使用 Flask/FastAPI 作為後端框架
> - 階段性開發，確保每階段穩定後再進入下一階段
>
> **預計時間**：約 5-7 週完成全部開發
>
> **當前狀態**：規劃階段 [規劃中 -> 開發中 -> 測試中 -> 已完成]

## 快速導航

- [一、背景與需求](#一背景與需求) - 原有程式說明、專案目標
- [二、核心設計決策](#二核心設計決策) - 使用預訓練模型、前端技術選擇
- [三、開發範圍](#三開發範圍) - 需要做的事項、不需要做的事項
- [四、風險與挑戰](#四風險與挑戰) - 技術挑戰、用戶體驗挑戰
- [五、實施計劃](#五實施計劃) - 階段性開發計劃、技術選型
- [六、未來擴展](#六未來擴展) - 後續可能的功能擴展
- [七、結論](#七結論) - 總結
- [八、開發日誌](#八開發日誌) - 記錄開發進度和重要決策
- [九、參考資料](#九參考資料) - 重要文件和資源位置
- [十、測試指南（給測試者）](#十測試指南給測試者) - 階段性測試流程、常見問題排查
- [十一、協作方式](#十一協作方式) - 代碼更新流程、開發日誌規範、版本控制、溝通與反饋
- [十二、程式碼區分](#十二程式碼區分) - 明確區分原程式碼與網站程式碼

---

## 一、背景與需求

### 1.1 原有程式執行流程說明

在開始網站開發規劃前，先記錄原有 PMvRLnGAN 程式的執行流程，以便在開發過程中保持對程式的理解。

#### 1.1.1 程式執行的四個主要部分

根據論文和程式結構，這個系統分為四個主要部分：

##### 第一部分：使用 GAT (Graph Attention Network) 獲取股票間的關係
- **目的**：利用圖注意力網絡分析股票之間的關聯性
- **輸入**：財務報表數據（19個財務報表欄位）
- **輸出**：股票之間的關係權重（74x74的股票對關係矩陣）
- **執行方式**：`python train.py --epochs 10000 --lr 0.0005 --l2 5e-4 --dropout-p 0.6 --num-heads 8 --hidden-dim 1024 --val-every 1000`
- **檔案位置**：`PMvRLnGAN/GAT-main/`
- **關鍵檔案**：
  - `train.py` - 訓練 GAT 模型的主要腳本
  - `gat_model.pth` - 預訓練的 GAT 模型
  - `edge.py` - 生成股票關係的腳本

##### 第二部分：訓練 Stock-Picked Agent 獲取最小風險的股票組合
- **目的**：選擇風險最小的股票組合（投資組合）
- **輸入**：財務報表數據和GAT生成的股票關係
- **輸出**：低風險股票列表（每季度選擇的股票）
- **執行方式**：運行 `train stock-picked agent.ipynb` 或使用已訓練好的模型運行 `predict stock-picked data.ipynb`
- **檔案位置**：`PMvRLnGAN/Stock-Picked Agent/`
- **關鍵檔案**：
  - `predict stock-picked data.ipynb` - 使用預訓練模型預測低風險股票
  - `Low-risk stock list.csv` - 預選的低風險股票列表

##### 第三部分：使用 TCN-AE (Temporal Convolutional Network Autoencoder) 壓縮每日技術指標
- **目的**：壓縮股票的技術指標，提取特徵
- **輸入**：每日交易數據（117個特徵，包括20天的歷史數據）
- **輸出**：壓縮後的20維特徵向量
- **執行方式**：運行 `train TCN-AE model.ipynb` 或使用已訓練好的模型運行 `TCN-AE predict data.ipynb`
- **檔案位置**：`PMvRLnGAN/TCN-AE/`
- **關鍵檔案**：
  - `tcn_20_model.h5` - 預訓練的 TCN-AE 模型
  - `TCN-AE predict data.ipynb` - 使用預訓練模型壓縮特徵

##### 第四部分：訓練 Trading Agent 執行每日股票操作
- **目的**：基於低風險股票列表進行每日交易決策
- **輸入**：TCN-AE壓縮後的特徵和低風險股票列表
- **輸出**：每日交易決策（買入/賣出數量）
- **執行方式**：解壓 `tcn_daily_trade_info.7z` 後運行 `train trade agent.ipynb`
- **檔案位置**：`PMvRLnGAN/Trading Agent/`
- **關鍵檔案**：
  - `tcn_daily_trade_info.7z` - 壓縮的交易數據
  - `train trade agent.ipynb` - 訓練和使用交易代理的腳本

#### 1.1.2 從頭執行的準備工作

1. **環境準備**：
   - Windows 11 系統
   - Python 3.8.18
   - 安裝 requirements.txt 中的依賴包

2. **數據準備**：
   - 所有模型所需的數據已包含在各自的資料夾中
   - 如需下載新數據，需申請 FinMind token 並使用 `get Financial Statements.ipynb` 和 `get Trading Data.ipynb`

3. **執行順序**：
   - 按照上述四個步驟順序執行
   - 每個步驟都依賴於前一步驟的輸出

### 1.2 專案概述

本專案旨在為 PMvRLnGAN（基於強化學習和圖注意力網絡的投資組合管理系統）建立一個網站介面，使用戶能夠通過簡單的按鈕操作執行整個程式並獲得結果，無需直接與程式碼互動。

### 1.3 目標

1. **主要目標**：建立一個簡單的網站介面，允許用戶執行 PMvRLnGAN 的四個主要步驟
2. **模型使用**：使用預訓練模型，不考慮使用新數據或訓練新模型
3. **結果展示**：提供直觀的結果展示，包括選擇的股票組合和交易決策
4. **開發方式**：階段性開發，確保每個階段都穩定運行後再進入下一階段
5. **程式重用**：盡量使用原有程式，避免不必要的重新開發

---

## 二、核心設計決策

### 2.1 使用預訓練模型而非執行 Jupyter Notebook

> **重要決策**：直接使用預訓練模型和結果文件，而不執行 Jupyter Notebook

經過分析，我們發現可以直接使用預訓練模型和結果文件，而不需要執行 Jupyter Notebook。這種方法有以下優勢：

1. **簡化開發流程**：
   - 不需要處理 Jupyter Notebook 執行的複雜性
   - 避免依賴管理和環境配置問題
   - 減少運行時錯誤的可能性

2. **提高性能**：
   - 直接讀取結果文件比執行完整的機器學習流程快得多
   - 減少服務器資源消耗
   - 提供更快的用戶響應時間

3. **實現方式**：
   - GAT 模塊：直接使用 `gat_model.pth` 和 `edge.py` 生成的結果
   - Stock-Picked Agent：使用 `Low-risk stock list.csv` 作為預選股票列表
   - TCN-AE：使用 `tcn_20_model.h5` 和預處理好的特徵
   - Trading Agent：使用預訓練模型進行預測

4. **數據流**：
   - 網站只需要展示預先計算好的結果
   - 可以添加簡單的數據更新機制，但主要依賴現有結果

### 2.2 使用純 HTML/CSS/JavaScript 作為前端

> **重要決策**：採用純 HTML/CSS/JavaScript 作為前端技術，不使用 Node.js

選擇純 HTML/CSS/JavaScript 作為前端技術有以下注意事項：

1. **優勢**：
   - 無需複雜的前端框架和構建工具
   - 減少開發環境的複雜性
   - 更容易部署和維護
   - 不需要 Node.js 環境

2. **挑戰與解決方案**：
   - **代碼組織**：使用模塊化的 JavaScript 文件結構，按功能分離代碼
   - **狀態管理**：可以使用 localStorage 或簡單的狀態管理模式
   - **API 調用**：使用 Fetch API 或 Axios 庫進行 API 調用
   - **響應式設計**：使用 CSS Grid 和 Flexbox 實現響應式布局
   - **瀏覽器兼容性**：使用 Babel 或 polyfill 確保兼容性

3. **推薦的庫和工具**：
   - **UI 框架**：Bootstrap 或 Tailwind CSS
   - **圖表庫**：Chart.js（輕量級）或 ECharts（功能豐富）
   - **HTTP 請求**：Axios（更簡潔的 API）
   - **工具函數**：Lodash（提供實用的工具函數）

4. **文件結構建議**：
   ```
   /static
     /css
       - main.css
       - components.css
     /js
       - main.js
       - api.js
       - charts.js
       - utils.js
     /lib
       - bootstrap.min.css
       - chart.min.js
   /templates
     - index.html
     - results.html
   ```

5. **開發工作流程**：
   - 使用 Live Server 或類似工具進行本地開發
   - 使用 ESLint 確保代碼質量
   - 使用 Chrome DevTools 進行調試

---

## 三、開發範圍

### 3.1 需要做的事項

#### 3.1.1 後端設計
- 創建 Flask/FastAPI 應用作為 Web 介面
- 設計 API 端點以提供預訓練模型的結果：
  - 提供 GAT 生成的股票關係數據
  - 提供 Stock-Picked Agent 選擇的低風險股票列表
  - 提供 TCN-AE 壓縮後的特徵
  - 提供 Trading Agent 的交易決策
- 實現結果存儲和檢索機制
- 處理錯誤和異常情況

**後端 API 端點設計**：

| 端點 | 方法 | 描述 | 參數 | 返回 |
|------|------|------|------|------|
| `/api/gat/relationships` | GET | 獲取股票關係數據 | 無 | 股票關係矩陣 |
| `/api/stock-picked/list` | GET | 獲取低風險股票列表 | `quarter` (可選) | 股票列表 |
| `/api/tcn-ae/features` | GET | 獲取壓縮後的特徵 | `stock_id` | 特徵向量 |
| `/api/trading/decisions` | GET | 獲取交易決策 | `date`, `stock_ids` | 交易決策 |
| `/api/results/summary` | GET | 獲取綜合結果 | `start_date`, `end_date` | 綜合結果 |

#### 3.1.2 前端設計
- 使用純 HTML/CSS/JavaScript 設計簡潔的用戶界面，包括：
  - 主頁面介紹系統功能
  - 執行按鈕（可以是單一按鈕或分步驟按鈕）
  - 結果展示頁面（圖表、表格等）
- 實現與後端 API 的通信
- 提供適當的加載指示器和錯誤提示
- 使用 Bootstrap 或 Tailwind CSS 實現響應式設計
- 使用 Chart.js 或 ECharts 實現數據可視化

**前端頁面設計**：

| 頁面 | 功能 | 主要元素 |
|------|------|----------|
| 首頁 | 系統介紹和入口 | 系統說明、開始按鈕 |
| 結果頁 | 展示分析結果 | 股票列表表格、交易決策圖表、績效指標 |
| 詳情頁 | 展示單一股票詳情 | 股票詳細信息、歷史交易記錄、技術指標圖表 |

#### 3.1.3 部署和維護
- 選擇適當的部署方案
- 設置必要的環境和依賴
- 確保系統穩定性和安全性

### 3.2 不需要做的事項

> **範圍限制**：明確定義不在本次開發範圍內的功能

1. **重寫核心算法** - 直接使用原有程式的結果，不重新開發機器學習邏輯
2. **執行 Jupyter Notebook** - 使用預訓練模型和預計算結果，避免執行複雜的 Notebook
3. **數據獲取功能** - 使用現有數據，不實現新數據下載
4. **模型訓練功能** - 使用預訓練模型，不提供重新訓練選項
5. **複雜的用戶管理系統** - 初期可以是單用戶或簡單的用戶系統
6. **高級分析工具** - 專注於基本功能，不開發額外的分析工具

---

## 四、風險與挑戰

### 4.1 技術挑戰
1. **前端複雜度管理** - 純 JavaScript 在複雜應用中可能難以維護，需要良好的代碼組織
2. **瀏覽器兼容性** - 不同瀏覽器可能有不同的行為，需要進行兼容性測試
3. **依賴管理** - 確保所有 Python 依賴在 Web 環境中正確安裝和運行
4. **計算資源** - 即使使用預訓練模型，某些操作仍可能需要大量資源

### 4.2 用戶體驗挑戰
1. **頁面響應性** - 確保頁面在加載大量數據時保持響應
2. **結果解釋** - 確保用戶能夠理解和解釋系統生成的結果
3. **錯誤處理** - 提供友好的錯誤提示和恢復機制

### 4.3 風險評估和緩解策略

| 風險 | 可能性 | 影響 | 緩解策略 |
|------|--------|------|----------|
| 前端代碼組織混亂 | 中 | 中 | 使用模塊化的 JavaScript 文件結構；遵循良好的代碼組織實踐 |
| 瀏覽器兼容性問題 | 中 | 中 | 使用 Babel 或 polyfill；進行跨瀏覽器測試 |
| 依賴項衝突或版本問題 | 中 | 高 | 使用虛擬環境和容器化技術；詳細記錄依賴版本 |
| 服務器資源不足 | 低 | 高 | 監控資源使用情況；根據需要擴展資源；優化代碼效率 |
| 安全漏洞 | 低 | 高 | 實施基本的安全措施；定期更新依賴項；限制訪問權限 |

---

## 五、實施計劃

### 5.1 階段性開發計劃

> **開發路線圖**：清晰的階段劃分和時間安排

#### 階段一：基礎架構設計（1週）
- 設計系統架構（前端、後端、數據流）
- 選擇適當的技術棧（Python Web 框架、前端庫）
- 建立開發環境
- 創建基本的項目結構
- 測試直接讀取預訓練模型和結果文件的可行性

**驗收標準**：完成系統架構設計文檔，建立基本項目結構，成功讀取至少一個預訓練模型或結果文件

**狀態**：已完成 [未開始 -> 進行中 -> 已完成]

#### 階段二：後端開發 - 核心功能（1-2週）
- 實現 API 端點以提供預訓練模型的結果
- 實現結果存儲和檢索機制
- 處理錯誤和異常情況
- 添加基本的日誌記錄功能

**驗收標準**：所有 API 端點可正常工作，能夠返回預期的數據，並有適當的錯誤處理

**狀態**：進行中 [未開始 -> 進行中 -> 已完成]

#### 階段三：前端開發 - 基本界面（1-2週）
- 設計和實現主頁面（HTML/CSS）
- 實現執行按鈕和基本交互（JavaScript）
- 設計結果展示頁面的布局
- 實現與後端 API 的基本通信（Fetch API 或 Axios）

**驗收標準**：前端能夠成功調用後端 API 並顯示基本結果

**狀態**：未開始 [未開始 -> 進行中 -> 已完成]

#### 階段四：結果可視化和用戶體驗優化（1-2週）
- 實現股票選擇結果的可視化（表格、圖表）
- 實現交易決策的可視化（表格、圖表）
- 添加加載指示器和進度提示
- 優化錯誤提示和用戶引導
- 確保響應式設計在不同設備上正常工作

**驗收標準**：用戶能夠清晰地查看和理解系統生成的結果，有良好的用戶體驗

**狀態**：未開始 [未開始 -> 進行中 -> 已完成]

#### 階段五：集成測試和部署（1週）
- 進行端到端測試
- 修復發現的問題
- 準備部署環境
- 部署系統並進行最終測試

**驗收標準**：系統能夠在生產環境中穩定運行，所有功能正常工作

**狀態**：未開始 [未開始 -> 進行中 -> 已完成]

### 5.2 技術選型建議

#### 後端
- **框架**：Flask 或 FastAPI（Python 輕量級框架，適合 AI 應用）
- **數據處理**：Pandas, NumPy（與現有代碼兼容）
- **模型加載**：直接使用 Python 加載預訓練模型或讀取結果文件

#### 前端
- **核心技術**：純 HTML/CSS/JavaScript
- **UI 框架**：Bootstrap 或 Tailwind CSS（輕量級 CSS 框架）
- **數據可視化**：Chart.js（輕量級）或 ECharts（功能豐富）
- **HTTP 請求**：Fetch API（原生）或 Axios（更簡潔的 API）

#### 部署
- **容器化**：Docker（簡化部署和環境管理）
- **服務器**：任何支持 Python 的服務器環境
- **Web 服務器**：Gunicorn 或 Uvicorn 配合 Nginx

---

## 六、未來擴展

### 6.1 後續擴展可能性

完成基本功能後，可以考慮以下擴展：

1. 添加簡單的用戶管理系統
2. 優化結果展示和可視化
3. 添加歷史結果比較功能
4. 實現移動端適配，提供響應式設計

---

## 七、結論

通過直接使用預訓練模型和結果文件，並採用純 HTML/CSS/JavaScript 作為前端技術，我們可以快速高效地將 PMvRLnGAN 系統轉換為一個易於使用的網站介面。這種方法不僅可以節省開發時間，還可以避免執行 Jupyter Notebook 的複雜性，提供更好的用戶體驗。每個階段都有明確的目標和驗收標準，確保開發過程有序進行，並能夠及時發現和解決問題。

---

## 八、開發日誌

### 2024-05-24
- 項目開始，基礎架構設計
- 完成項目規劃文檔
- 決定使用預訓練模型，避免執行 Jupyter Notebook
- 選擇純 HTML/CSS/JavaScript 作為前端技術
- 創建基本項目結構（backend、frontend 目錄）
- 創建基本文件（app.py、index.html、main.css、main.js）
- 實現基本 API 端點設計
- 實現基本前端界面設計
- 階段一完成度：80%

### 2024-05-25
- 完成基本項目結構和文件創建
- 創建啟動腳本（run.py 和 start.bat）
- 更新 README.md 文件，添加啟動說明
- 完善項目文檔
- 添加配置模塊（config.py）
- 添加日誌模塊（logger.py）
- 更新 app.py 使用配置和日誌模塊
- 階段一完成度：100%
- 階段一已完成，開始進入階段二

### 2024-05-26
- 添加詳細的測試指南，包括環境準備、啟動應用程序、功能測試、日誌檢查和測試報告
- 添加協作方式文檔，規範代碼更新流程、開發日誌規範、版本控制和溝通反饋
- 文件變更：
  - 修改：PMvRLnGAN_web_planning.md
- 階段二完成度：10%
- 下一步：實現股票列表 API 端點的實際數據讀取功能

### 2024-05-27
- 調整測試指南和協作方式文檔的結構和語言，使其更加明確
- 明確區分用戶（測試者）和開發者的角色和職責
- 添加四階段協作流程：開發階段、測試階段、修復階段、確認階段
- 確保即使沒有前面的對話記錄，也能按照文檔中的協作方式順利進行
- 文件變更：
  - 修改：PMvRLnGAN_web_planning.md
- 階段二完成度：15%
- 下一步：實現股票列表 API 端點的實際數據讀取功能

### 2024-05-28
- 修正測試報告部分，明確開發者收到反饋後的處理流程
- 修正協作方式部分，明確區分開發者（Claude）和測試者（您）的角色
- 統一使用繁體中文術語，避免簡體字出現
- 文件變更：
  - 修改：PMvRLnGAN_web_planning.md
- 階段二完成度：15%
- 下一步：實現股票列表 API 端點的實際數據讀取功能

### 2024-05-29
- 修正文件中的角色稱呼，避免未來閱讀時的混淆
- 將「測試者（您）」改為「測試者」，並添加明確的角色定義說明
- 添加角色定義部分，明確「開發者」指 Claude，「測試者」指用戶
- 文件變更：
  - 修改：PMvRLnGAN_web_planning.md
- 階段二完成度：15%
- 下一步：實現股票列表 API 端點的實際資料讀取功能

### 2024-05-30
- 添加「十二、程式碼區分」章節，明確區分原程式碼與網站程式碼
- 定義原程式碼範圍（不可修改）和網站程式碼範圍（可開發和修改）
- 說明適配器模式的設計，用於連接原程式碼和網站界面
- 提供完整的目錄結構，明確各部分的位置和職責
- 文件變更：
  - 修改：PMvRLnGAN_web_planning.md
- 階段二完成度：20%
- 下一步：實現股票列表 API 端點的實際資料讀取功能

### 2024-05-31
- 實現日期範圍限制和有效交易日檢查功能
- 創建交易適配器（trading_adapter.py），實現日期驗證和交易決策獲取
- 創建股票適配器（stock_adapter.py），實現低風險股票列表讀取
- 添加季度選擇器功能，使用戶可以選擇不同季度的股票列表
- 更新前端 JavaScript，實現日期範圍限制和錯誤處理
- 添加新的 API 端點：
  - `/api/trading/valid-dates`：獲取有效的交易日期範圍
  - `/api/stock-picked/quarters`：獲取可用的季度列表
- 文件變更：
  - 新增：PMvRLnGAN_web/backend/adapters/__init__.py
  - 新增：PMvRLnGAN_web/backend/adapters/trading_adapter.py
  - 新增：PMvRLnGAN_web/backend/adapters/stock_adapter.py
  - 修改：PMvRLnGAN_web/backend/app.py
  - 修改：PMvRLnGAN_web/backend/config.py
  - 修改：PMvRLnGAN_web/frontend/static/js/main.js
  - 修改：PMvRLnGAN_web/frontend/templates/index.html
- 階段二完成度：40%
- 下一步：實現 GAT 適配器和 TCN-AE 適配器，完成所有 API 端點的實際數據讀取功能

### 2024-06-01
- 修復應用程序啟動錯誤：解決 logger.py 中的類型錯誤問題
- 修改 logger.py 中的日誌級別設置方式，直接使用 LOG_LEVEL 常量而非 getattr 函數
- 確保應用程序可以正常啟動和運行
- 文件變更：
  - 修改：PMvRLnGAN_web/backend/logger.py
- 階段二完成度：42%
- 下一步：實現 GAT 適配器和 TCN-AE 適配器，完成所有 API 端點的實際數據讀取功能

### 2024-06-02
- 優化交易適配器，移除不必要的 tcn_daily_trade_info.7z 解壓代碼
- 修改交易適配器，直接從 Low-risk stock list.csv 讀取交易日期和股票數據
- 實現基於低風險股票列表的交易決策生成
- 實現績效摘要 API 端點，提供模擬的績效數據
- 文件變更：
  - 修改：PMvRLnGAN_web/backend/adapters/trading_adapter.py
  - 修改：PMvRLnGAN_web/backend/app.py
- 階段二完成度：60%
- 下一步：實現 GAT 適配器，完成所有 API 端點的實際數據讀取功能

### 2024-06-03
- 訓練 Trading Agent 模型並保存結果，為網站開發準備真實數據
- 在 train trade agent.ipynb 中添加模型保存代碼，具體修改如下：
  1. 在 `trained_ppo = agent.train_model(...)` 之後添加模型保存代碼
  2. 創建 models 目錄並保存模型和配置文件
  3. 保存交易決策示例和性能指標
- 需要保存的文件包括：
  - trading_agent_model.zip：訓練好的 RL 模型
  - trading_agent_config.json：模型配置和超參數
  - trading_decisions_examples.csv：示例交易決策
  - trading_agent_performance.json：模型性能指標
- 文件變更：
  - 修改：PMvRLnGAN/Trading Agent/train trade agent.ipynb
  - 新增：PMvRLnGAN/Trading Agent/models/（包含上述保存的文件）
- 階段二完成度：65%
- 下一步：修改 trading_adapter.py 使用訓練好的模型生成交易決策

### 2024-06-04
- 修改 trading_adapter.py 使用訓練好的模型生成交易決策
- 實現 GAT 適配器，讀取股票關係數據
- 實現 TCN-AE 適配器，讀取壓縮特徵
- 更新 app.py，連接所有適配器
- 文件變更：
  - 修改：PMvRLnGAN_web/backend/adapters/trading_adapter.py
  - 新增：PMvRLnGAN_web/backend/adapters/gat_adapter.py
  - 新增：PMvRLnGAN_web/backend/adapters/tcn_adapter.py
  - 修改：PMvRLnGAN_web/backend/app.py
- 階段二完成度：85%
- 下一步：測試所有 API 端點，確保它們可以正常工作

### 2024-06-05
- 創建測試腳本 test_adapter.py，用於測試交易適配器功能和 API 端點
- 修復測試腳本中的錯誤，確保能夠正確處理 API 返回的數據結構
- 完成交易適配器和股票適配器的功能測試
- 完成相關 API 端點的測試，包括：
  - /api/trading/valid-dates：返回有效的交易日期範圍
  - /api/stock-picked/quarters：返回可用的季度列表
  - /api/stock-picked/list：返回低風險股票列表
  - /api/trading/decisions：返回指定日期的交易決策
  - /api/results/summary：返回績效摘要
- 確認 API 端點返回的數據結構正確，特別是 /api/stock-picked/list 端點
- 文件變更：
  - 新增：PMvRLnGAN_web/test_adapter.py
  - 修改：PMvRLnGAN_web/backend/adapters/trading_adapter.py（修復小錯誤）
  - 修改：PMvRLnGAN_web/backend/adapters/stock_adapter.py（修復小錯誤）
- 階段二完成度：90%
- 下一步：實現 GAT 適配器和 TCN-AE 適配器，完成所有 API 端點的實際數據讀取功能

### [待添加更多日誌條目]

---

## 九、參考資料

### 9.1 重要文件位置

| 文件 | 位置 | 用途 |
|------|------|------|
| GAT 模型 | `PMvRLnGAN/GAT-main/gat_model.pth` | 預訓練的 GAT 模型 |
| 低風險股票列表 | `PMvRLnGAN/Trading Agent/Low-risk stock list.csv` | 預選的低風險股票 |
| TCN-AE 模型 | `PMvRLnGAN/TCN-AE/tcn_20_model.h5` | 預訓練的 TCN-AE 模型 |
| 交易數據 | `PMvRLnGAN/Trading Agent/tcn_daily_trade_info.7z` | 壓縮的交易數據 |
| 論文 | `PMvRLnGAN/PMvRLnGAN_paper.md` | 系統的論文說明 |

### 9.2 外部資源

- [Flask 文檔](https://flask.palletsprojects.com/)
- [Bootstrap 文檔](https://getbootstrap.com/docs/)
- [Chart.js 文檔](https://www.chartjs.org/docs/latest/)
- [Python 3.8 文檔](https://docs.python.org/3.8/)

### 9.3 依賴版本

主要依賴包版本（詳見 requirements.txt）：
- Python: 3.8.18
- Flask/FastAPI: [待確定]

### 9.4 資料來源與網頁對應

網站使用的資料來源分為兩類：真實資料（從原始資料夾讀取的）和模擬資料（暫時生成的）。以下是各個模組的資料來源情況：

#### 資料來源概覽表

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

#### 資料來源控制機制

系統通過配置文件 `config.py` 中的 `USE_MOCK_DATA` 變數控制資料來源：

```python
# 是否使用模擬數據（當無法讀取原始數據時）
USE_MOCK_DATA = False
```

當設置為 `False` 時，系統會：
1. 優先嘗試讀取真實數據文件
2. 如果找不到真實數據，自動回退到使用模擬數據
3. 在使用模擬數據時，會在返回結果中添加 `is_mock_data: true` 標記

### 9.5 原程式執行與資料使用分析

為了確保網站能夠展示真實的分析結果，我們需要明確哪些部分需要重新執行，哪些可以直接使用訓練完的成果。以下是詳細分析：

#### 1. GAT (Graph Attention Network)

**可以直接使用的部分**：
- 預訓練的 GAT 模型 (`gat_model.pth`)
- 如果已經有生成好的股票關係矩陣，可以直接使用

**需要執行的部分**：
- 如果沒有預先生成的股票關係矩陣，需要使用 `edge.py` 腳本來生成
- 這個過程需要載入 GAT 模型並執行前向傳播，生成股票之間的關係權重

**差距與解決方案**：
- 目前的 `gat_adapter.py` 是尋找 `relationships.json` 文件，但這個文件可能不存在
- 需要執行 `edge.py` 來生成這個文件，或者修改適配器直接使用 GAT 模型
- 建議：執行一次 `edge.py` 腳本，生成 `relationships.json` 文件，然後網站可以直接讀取這個文件

#### 2. Stock-Picked Agent

**可以直接使用的部分**：
- 低風險股票列表 (`Low-risk stock list.csv`)
- 這個文件已經包含了每個季度選出的低風險股票

**需要執行的部分**：
- 如果需要更新低風險股票列表，需要執行 `predict stock-picked data.ipynb`
- 如果需要重新訓練 Stock-Picked Agent，需要執行 `train stock-picked agent.ipynb`

**差距與解決方案**：
- 目前的 `stock_adapter.py` 已經可以直接讀取 `Low-risk stock list.csv`
- 風險值是隨機生成的，實際應該從 Stock-Picked Agent 的結果中獲取
- 建議：執行一次 `predict stock-picked data.ipynb`，生成包含風險值的股票列表，然後修改 `stock_adapter.py` 讀取這個文件

#### 3. TCN-AE (Temporal Convolutional Network Autoencoder)

**可以直接使用的部分**：
- 預訓練的 TCN-AE 模型 (`tcn_20_model.h5`)
- 如果已經有生成好的壓縮特徵，可以直接使用

**需要執行的部分**：
- 如果沒有預先生成的壓縮特徵，需要使用 TCN-AE 模型來壓縮股票的技術指標
- 這個過程需要載入 TCN-AE 模型並執行前向傳播，生成壓縮後的特徵向量

**差距與解決方案**：
- 目前的 `tcn_adapter.py` 是尋找 `compressed_features` 目錄下的文件，但這些文件可能不存在
- 需要執行 `TCN-AE predict data.ipynb` 來生成這些文件，或者修改適配器直接使用 TCN-AE 模型
- 建議：執行一次 `TCN-AE predict data.ipynb`，生成壓縮特徵文件，然後網站可以直接讀取這些文件

#### 4. Trading Agent

**可以直接使用的部分**：
- 預訓練的交易模型 (`trading_agent_model.zip`)
- 模型配置 (`trading_agent_config.json`)
- 交易決策示例 (`trading_decisions_examples.csv`)
- 模型性能指標 (`trading_agent_performance.json`)

**需要執行的部分**：
- 如果需要更完整的交易決策，需要修改 `train trade agent.ipynb` 中保存交易決策的代碼
- 如果需要重新訓練 Trading Agent，需要執行 `train trade agent.ipynb`

**差距與解決方案**：
- 目前的 `trading_adapter.py` 已經可以讀取 `trading_decisions_examples.csv`
- 但這個文件只包含 2024-05-17 至 2024-06-04 的有限交易日期數據
- 建議：修改 `train trade agent.ipynb` 中的代碼，保存完整的交易決策（而不只是前 30 行），然後網站可以直接讀取這個文件

#### 只執行一次交易分析的可行性

根據以上分析，只執行一次交易分析是完全可行的，具體方法如下：

1. **預處理階段**（一次性執行）：
   - 使用 `edge.py` 生成股票關係矩陣，保存為 `relationships.json`
   - 使用 `TCN-AE predict data.ipynb` 生成壓縮特徵，保存到 `compressed_features` 目錄
   - 修改 `train trade agent.ipynb` 中的代碼，保存完整的交易決策，而不只是前 30 行

2. **網站階段**（直接使用預處理結果）：
   - `gat_adapter.py` 讀取 `relationships.json`
   - `tcn_adapter.py` 讀取 `compressed_features` 目錄下的文件
   - `trading_adapter.py` 讀取 `trading_decisions_examples.csv`
   - `stock_adapter.py` 讀取 `Low-risk stock list.csv`

這種方式的優點是：
1. 簡化開發流程
2. 減少運行時錯誤的可能性
3. 提高網站性能
4. 確保結果的一致性

## 十、測試指南（給測試者）

> **重要說明**：本測試指南專為測試者設計，目的是指導測試者如何測試每次更新後的功能。每次開發階段完成後，測試者應按照以下步驟進行測試，並將發現的問題反饋給開發者（Claude）。

### 10.1 階段性測試流程

每個開發階段完成後，測試者應進行系統測試以確保功能正常運作。以下是測試流程的詳細說明：

#### 10.1.1 環境準備

1. **確認工作目錄**：
   - 測試者應在項目根目錄 `PMvRLnGAN_web` 下執行所有命令
   - 在命令提示符或 PowerShell 中，使用 `cd` 命令導航到項目根目錄
   ```
   cd C:\path\to\PMvRLnGAN_web
   ```

2. **確認環境**：
   - 確保已安裝 Python 3.8.18
   - 確保已安裝所有依賴項
   ```
   pip install -r requirements.txt
   ```

#### 10.1.2 啟動應用程序

1. **使用啟動腳本**：
   ```
   # Windows 用戶
   start.bat
   
   # 或者使用 Python 腳本
   python run.py
   ```

2. **檢查啟動日誌**：
   - 觀察控制台輸出，確認應用程序已成功啟動
   - 確認顯示的 URL（通常是 http://localhost:5000）

#### 10.1.3 功能測試

1. **基本頁面測試**：
   - 在瀏覽器中訪問 http://localhost:5000
   - 確認首頁正確加載，包括標題、描述和按鈕

2. **API 端點測試**：
   - 使用瀏覽器或 API 測試工具（如 Postman）測試以下端點：
     - http://localhost:5000/api/gat/relationships
     - http://localhost:5000/api/stock-picked/list
     - http://localhost:5000/api/tcn-ae/features?stock_id=Stock1
     - http://localhost:5000/api/trading/decisions?date=2023-01-01
     - http://localhost:5000/api/results/summary?start_date=2023-01-01&end_date=2023-12-31

3. **前端交互測試**：
   - 點擊「開始分析」按鈕，確認加載動畫顯示
   - 確認結果頁面正確顯示（股票列表、交易決策、績效指標）
   - 測試日期選擇器功能
   - 測試標籤頁切換功能

4. **錯誤處理測試**：
   - 測試缺少必要參數的情況（例如，不提供 stock_id 或 date）
   - 測試無效參數的情況（例如，無效的日期格式）

#### 10.1.4 日誌檢查

1. **檢查應用程序日誌**：
   - 查看 `PMvRLnGAN_web/logs/app.log` 文件
   - 確認沒有錯誤或警告消息
   - 分析用戶操作的日誌記錄

#### 10.1.5 測試報告

每次測試後，測試者應記錄以下資訊並反饋給開發者（Claude）：

1. 測試日期和時間
2. 測試環境（作業系統、瀏覽器版本等）
3. 測試的功能和結果
4. 發現的問題和建議
5. 測試結論（通過/失敗）

開發者（Claude）收到測試者的反饋後，會：
1. 分析問題原因
2. 實施必要的修復
3. 記錄所採取的更動
4. 提供修復後的版本供測試者再次測試

### 10.2 常見問題排查

如果測試者在測試過程中遇到問題，可以嘗試以下排查方法：

1. **應用程序無法啟動**：
   - 檢查 Python 版本是否正確（3.8.18）
   - 檢查是否已安裝所有依賴項
   - 檢查端口 5000 是否被其他應用程序佔用

2. **API 返回錯誤**：
   - 檢查請求參數是否正確
   - 檢查日誌文件中的錯誤消息
   - 確認 PMvRLnGAN 原始程序的路徑設置是否正確

3. **前端顯示問題**：
   - 使用瀏覽器開發者工具檢查控制台錯誤
   - 檢查網絡請求是否成功
   - 確認 JavaScript 和 CSS 文件是否正確加載

## 十一、協作方式

> **重要說明**：本節描述了開發者（Claude）和測試者之間的協作流程，確保開發過程的順暢和文件的完整性。無論是否有前面的對話記錄，都應遵循此協作方式。
>
> **角色定義**：
> - **開發者**：指 Claude，負責實現功能、修復問題和更新文件
> - **測試者**：指用戶，負責測試功能、提供反饋和確認問題解決

### 11.1 協作流程

我們採用以下四階段協作流程，確保每個功能都經過充分開發和測試：

#### 11.1.1 開發階段
- 開發者（Claude）根據計劃實現功能
- 開發者（Claude）更新開發日誌，記錄完成的工作
- 開發者（Claude）提供詳細的測試指南

#### 11.1.2 測試階段
- 測試者按照測試指南測試功能
- 測試者記錄發現的問題和建議
- 測試者將問題和建議反饋給開發者（Claude）

#### 11.1.3 修復階段
- 開發者（Claude）根據測試者的反饋修復問題
- 開發者（Claude）更新程式碼和文件
- 開發者（Claude）提供修復後的測試指南

#### 11.1.4 確認階段
- 測試者再次測試，確認問題已解決
- 雙方共同決定是否進入下一個開發階段

### 11.2 程式碼更新流程

每次程式碼更新應遵循以下流程：

1. **更新前準備**：
   - 開發者（Claude）確認當前開發階段和任務
   - 開發者（Claude）檢查相關文件和依賴項

2. **程式碼更新**：
   - 開發者（Claude）實現新功能或修復問題
   - 開發者（Claude）確保程式碼符合專案風格和標準
   - 開發者（Claude）添加必要的註釋和文件

3. **測試驗證**：
   - 測試者按照「測試指南」進行測試
   - 測試者確認功能正常運作
   - 測試者記錄測試結果

4. **文件更新**：
   - 開發者（Claude）更新開發日誌，記錄所做的更改
   - 開發者（Claude）更新相關文件（如 README.md）
   - 開發者（Claude）如有必要，更新測試指南

### 11.3 開發日誌規範

每次更新後，開發者（Claude）應在開發日誌中添加新條目，包含以下資訊：

1. **日期**：更新的日期
2. **更改內容**：簡要描述所做的更改
3. **文件變更**：列出新增、修改或刪除的文件
4. **完成度**：當前階段的完成百分比
5. **下一步計劃**：簡要描述下一步的工作

範例：
```
### 2024-05-26
- 實現股票列表 API 端點
- 添加股票資料讀取功能
- 修復前端日期選擇器問題
- 文件變更：
  - 修改：backend/app.py
  - 新增：backend/models/stock.py
  - 修改：frontend/static/js/main.js
- 階段二完成度：40%
- 下一步：實現交易決策 API 端點
```

### 11.4 版本控制

1. **提交資訊**：
   - 開發者（Claude）使用清晰、描述性的提交資訊
   - 開發者（Claude）包含相關任務或問題的引用
   - 開發者（Claude）簡要說明更改的原因和影響

2. **分支管理**：
   - 主分支（main/master）保持穩定
   - 開發者（Claude）為新功能或修復創建特性分支
   - 完成並測試後合併回主分支

### 11.5 溝通與反饋

1. **定期更新**：
   - 開發者（Claude）提供開發進度的定期更新
   - 雙方討論遇到的問題和解決方案
   - 開發者（Claude）分享學習和發現

2. **反饋處理**：
   - 開發者（Claude）及時回應測試者的反饋和問題
   - 根據測試者的反饋調整開發計劃和方向
   - 開發者（Claude）記錄重要的反饋和決策

通過遵循這些協作方式，我們可以確保開發過程的透明度和效率，同時保持文件的完整性和準確性，即使沒有前面的對話記錄，也能按照此方式順利進行協作。 

## 十二、程式碼區分

> **重要說明**：為確保開發過程中不會意外修改原始程式碼，本節明確區分原程式碼與網站程式碼的範圍和職責。

### 12.1 原程式碼（不可修改）

原程式碼是指 PMvRLnGAN 系統的原始實現，這些程式碼**不應被修改**，只能被讀取和使用。

**原程式碼範圍**：
- 位於 `PMvRLnGAN/` 目錄下的所有文件
- 包括以下模組：
  - GAT 模組：`PMvRLnGAN/GAT-main/`
  - Stock-Picked Agent 模組：`PMvRLnGAN/Stock-Picked Agent/`
  - TCN-AE 模組：`PMvRLnGAN/TCN-AE/`
  - Trading Agent 模組：`PMvRLnGAN/Trading Agent/`
- 所有預訓練模型文件：
  - GAT 模型：`gat_model.pth`
  - TCN-AE 模型：`tcn_20_model.h5`
  - 其他模型檔案
- 所有結果文件：
  - 低風險股票列表：`Low-risk stock list.csv`
  - 交易數據：`tcn_daily_trade_info.7z`
  - 其他結果檔案

**原程式碼使用原則**：
1. 僅讀取原程式碼的結果和模型，不修改任何原始檔案
2. 不改變原程式碼的執行邏輯和參數設定
3. 如需使用原程式碼的功能，應通過導入模組或讀取結果文件的方式

### 12.2 網站程式碼（可開發和修改）

網站程式碼是指為本專案新開發的部分，用於提供網頁介面和連接原程式碼的功能。

**網站程式碼範圍**：
- 位於 `PMvRLnGAN_web/` 目錄下的所有文件
- 包括以下部分：
  - 後端 Flask 應用：`PMvRLnGAN_web/backend/`
  - 前端 HTML/CSS/JavaScript：`PMvRLnGAN_web/frontend/`
  - 配置文件：`PMvRLnGAN_web/config.py`
  - 啟動腳本：`PMvRLnGAN_web/run.py`、`PMvRLnGAN_web/start.bat`
  - 文檔文件：`PMvRLnGAN_web/README.md`、`PMvRLnGAN_web_planning.md`
  - 依賴項文件：`PMvRLnGAN_web/requirements.txt`

**網站程式碼開發原則**：
1. 遵循模組化設計，保持代碼清晰和可維護
2. 實現適配器模式，連接原程式碼和網站界面
3. 提供友好的用戶界面和錯誤處理
4. 確保所有功能都有適當的文檔和測試

### 12.3 適配器模式

為了連接原程式碼和網站界面，我們採用適配器模式設計：

1. **數據適配器**：
   - 位於 `PMvRLnGAN_web/backend/adapters/` 目錄
   - 負責從原程式碼的結果文件中讀取數據
   - 將數據轉換為網站 API 可用的格式

2. **模型適配器**：
   - 位於 `PMvRLnGAN_web/backend/adapters/` 目錄
   - 負責加載和使用原程式碼的預訓練模型
   - 提供模型預測結果給網站 API

3. **路徑配置**：
   - 在 `PMvRLnGAN_web/config.py` 中設置原程式碼的路徑
   - 確保適配器可以正確找到原程式碼的文件

### 12.4 目錄結構

完整的目錄結構應如下所示：

```
PMvRLnGAN/                   # 原程式碼目錄（不可修改）
  ├── GAT-main/              # GAT 模組
  ├── Stock-Picked Agent/    # Stock-Picked Agent 模組
  ├── TCN-AE/                # TCN-AE 模組
  └── Trading Agent/         # Trading Agent 模組

PMvRLnGAN_web/              # 網站程式碼目錄（可開發和修改）
  ├── backend/               # 後端程式碼
  │   ├── adapters/          # 適配器模組
  │   │   ├── gat_adapter.py
  │   │   ├── stock_adapter.py
  │   │   ├── tcn_adapter.py
  │   │   └── trading_adapter.py
  │   ├── models/            # 數據模型
  │   ├── routes/            # API 路由
  │   └── app.py             # Flask 應用主文件
  ├── frontend/              # 前端程式碼
  │   ├── static/            # 靜態資源
  │   │   ├── css/           # CSS 樣式
  │   │   ├── js/            # JavaScript 腳本
  │   │   └── lib/           # 第三方庫
  │   └── templates/         # HTML 模板
  ├── logs/                  # 日誌文件
  ├── config.py              # 配置文件
  ├── run.py                 # 啟動腳本
  ├── start.bat              # Windows 啟動批處理文件
  ├── requirements.txt       # 依賴項文件
  ├── README.md              # 說明文件
  └── PMvRLnGAN_web_planning.md  # 開發規劃文件