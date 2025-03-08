# PMvRLnGAN Web 介面

這是 PMvRLnGAN（基於強化學習和圖注意力網絡的投資組合管理系統）的網站介面。

## 功能

- 使用 GAT 分析股票間的關係
- 使用 Stock-Picked Agent 選擇低風險股票組合
- 使用 TCN-AE 壓縮股票技術指標
- 使用 Trading Agent 生成交易決策
- 展示投資組合績效和交易建議

## 技術棧

- **後端**：Flask
- **前端**：HTML, CSS, JavaScript, Bootstrap, Chart.js
- **數據處理**：Pandas, NumPy
- **機器學習**：PyTorch, TensorFlow

## 安裝與運行

### 環境要求

- Python 3.8.18
- Windows 11

### 安裝步驟

1. 克隆此倉庫：
   ```
   git clone <repository-url>
   ```

2. 安裝依賴：
   ```
   cd PMvRLnGAN_web
   pip install -r requirements.txt
   ```

3. 運行應用（選擇以下任一方式）：

   **方法 1：使用啟動腳本（推薦）**
   ```
   # Windows 用戶
   start.bat
   
   # 或者使用 Python 腳本
   python run.py
   ```
   
   **方法 2：直接運行 Flask 應用**
   ```
   cd backend
   python app.py
   ```

4. 在瀏覽器中訪問：
   ```
   http://localhost:5000
   ```

## 項目結構

```
PMvRLnGAN_web/
├── backend/
│   └── app.py
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── main.css
│   │   ├── js/
│   │   │   └── main.js
│   │   └── lib/
│   └── templates/
│       └── index.html
├── run.py
├── start.bat
└── requirements.txt
```

## 使用說明

1. 打開網站首頁
2. 點擊「開始分析」按鈕
3. 系統將自動執行分析流程
4. 查看分析結果，包括低風險股票列表、交易決策和績效指標

## 注意事項

- 本系統使用預訓練模型，不需要重新訓練
- 系統需要訪問 PMvRLnGAN 原始程式的預訓練模型和結果文件
- 確保 PMvRLnGAN 原始程式的路徑設置正確 