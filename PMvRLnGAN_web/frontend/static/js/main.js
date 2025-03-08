// 等待 DOM 加載完成
document.addEventListener('DOMContentLoaded', function() {
    // 獲取元素
    const startAnalysisBtn = document.getElementById('startAnalysisBtn');
    const introductionSection = document.getElementById('introduction');
    const analysisSection = document.getElementById('analysis');
    const loadingSection = document.getElementById('loading');
    const tradingDateInput = document.getElementById('tradingDate');
    
    // 設置今天的日期為交易日期輸入框的默認值
    const today = new Date();
    const formattedDate = today.toISOString().split('T')[0];
    tradingDateInput.value = formattedDate;
    
    // 初始化績效圖表
    const performanceChartCtx = document.getElementById('performanceChart').getContext('2d');
    const performanceChart = new Chart(performanceChartCtx, {
        type: 'line',
        data: {
            labels: [], // 將由 API 數據填充
            datasets: [{
                label: '投資組合價值',
                data: [], // 將由 API 數據填充
                borderColor: '#0d6efd',
                backgroundColor: 'rgba(13, 110, 253, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.1
            }, {
                label: '基準指數',
                data: [], // 將由 API 數據填充
                borderColor: '#6c757d',
                borderWidth: 2,
                fill: false,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: '日期'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: '價值'
                    },
                    beginAtZero: false
                }
            }
        }
    });
    
    // 開始分析按鈕點擊事件
    startAnalysisBtn.addEventListener('click', function() {
        // 顯示加載動畫
        introductionSection.classList.add('d-none');
        loadingSection.classList.remove('d-none');
        
        // 模擬 API 請求延遲
        setTimeout(function() {
            // 隱藏加載動畫，顯示分析結果
            loadingSection.classList.add('d-none');
            analysisSection.classList.remove('d-none');
            
            // 獲取數據
            fetchStockList();
            fetchTradingDecisions(tradingDateInput.value);
            fetchPerformanceSummary();
        }, 2000);
    });
    
    // 交易日期變更事件
    tradingDateInput.addEventListener('change', function() {
        fetchTradingDecisions(this.value);
    });
    
    // 獲取股票列表
    function fetchStockList() {
        fetch('/api/stock-picked/list')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    populateStockListTable(data.data.stocks);
                } else {
                    showError('獲取股票列表失敗：' + data.message);
                }
            })
            .catch(error => {
                showError('獲取股票列表時發生錯誤：' + error.message);
            });
    }
    
    // 獲取交易決策
    function fetchTradingDecisions(date) {
        fetch(`/api/trading/decisions?date=${date}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    populateTradingDecisionsTable(data.data.decisions);
                } else {
                    showError('獲取交易決策失敗：' + data.message);
                }
            })
            .catch(error => {
                showError('獲取交易決策時發生錯誤：' + error.message);
            });
    }
    
    // 獲取績效摘要
    function fetchPerformanceSummary() {
        // 計算過去一年的日期範圍
        const endDate = new Date();
        const startDate = new Date();
        startDate.setFullYear(startDate.getFullYear() - 1);
        
        const formattedStartDate = startDate.toISOString().split('T')[0];
        const formattedEndDate = endDate.toISOString().split('T')[0];
        
        fetch(`/api/results/summary?start_date=${formattedStartDate}&end_date=${formattedEndDate}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    updatePerformanceMetrics(data.data);
                    updatePerformanceChart(data.data);
                } else {
                    showError('獲取績效摘要失敗：' + data.message);
                }
            })
            .catch(error => {
                showError('獲取績效摘要時發生錯誤：' + error.message);
            });
    }
    
    // 填充股票列表表格
    function populateStockListTable(stocks) {
        const tableBody = document.querySelector('#stockListTable tbody');
        tableBody.innerHTML = '';
        
        // 模擬數據
        const mockStocks = [
            { code: 'Stock1', name: '股票一', risk: 0.2, weight: 0.3 },
            { code: 'Stock2', name: '股票二', risk: 0.3, weight: 0.2 },
            { code: 'Stock3', name: '股票三', risk: 0.1, weight: 0.5 }
        ];
        
        mockStocks.forEach(stock => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${stock.code}</td>
                <td>${stock.name}</td>
                <td>${stock.risk.toFixed(2)}</td>
                <td>${(stock.weight * 100).toFixed(2)}%</td>
            `;
            tableBody.appendChild(row);
        });
    }
    
    // 填充交易決策表格
    function populateTradingDecisionsTable(decisions) {
        const tableBody = document.querySelector('#tradingDecisionsTable tbody');
        tableBody.innerHTML = '';
        
        // 使用模擬數據
        const mockDecisions = {
            'Stock1': { name: '股票一', action: 'buy', quantity: 100 },
            'Stock2': { name: '股票二', action: 'sell', quantity: 50 },
            'Stock3': { name: '股票三', action: 'hold', quantity: 0 }
        };
        
        Object.entries(mockDecisions).forEach(([code, decision]) => {
            const row = document.createElement('tr');
            
            // 根據操作類型設置不同的顏色
            let actionClass = '';
            let actionText = '';
            
            switch (decision.action) {
                case 'buy':
                    actionClass = 'text-success';
                    actionText = '買入';
                    break;
                case 'sell':
                    actionClass = 'text-danger';
                    actionText = '賣出';
                    break;
                case 'hold':
                    actionClass = 'text-warning';
                    actionText = '持有';
                    break;
            }
            
            row.innerHTML = `
                <td>${code}</td>
                <td>${decision.name}</td>
                <td class="${actionClass}">${actionText}</td>
                <td>${decision.quantity}</td>
            `;
            tableBody.appendChild(row);
        });
    }
    
    // 更新績效指標
    function updatePerformanceMetrics(data) {
        document.getElementById('totalReturn').textContent = (data.total_return * 100).toFixed(2) + '%';
        document.getElementById('sharpeRatio').textContent = data.sharpe_ratio.toFixed(2);
        document.getElementById('maxDrawdown').textContent = (data.max_drawdown * 100).toFixed(2) + '%';
    }
    
    // 更新績效圖表
    function updatePerformanceChart(data) {
        // 模擬數據
        const dates = [];
        const portfolioValues = [];
        const benchmarkValues = [];
        
        // 生成過去一年的日期和模擬數據
        const endDate = new Date();
        const startDate = new Date();
        startDate.setFullYear(startDate.getFullYear() - 1);
        
        let currentDate = new Date(startDate);
        let portfolioValue = 1000000; // 初始投資金額
        let benchmarkValue = 1000000; // 初始基準金額
        
        while (currentDate <= endDate) {
            const formattedDate = currentDate.toISOString().split('T')[0];
            dates.push(formattedDate);
            
            // 模擬投資組合價值變化（加入一些隨機波動）
            const dailyReturn = 0.0005 + (Math.random() - 0.5) * 0.002; // 平均每日回報率 0.05% 加上隨機波動
            portfolioValue *= (1 + dailyReturn);
            portfolioValues.push(portfolioValue);
            
            // 模擬基準指數價值變化（加入一些隨機波動，但平均回報率較低）
            const benchmarkDailyReturn = 0.0003 + (Math.random() - 0.5) * 0.002; // 平均每日回報率 0.03% 加上隨機波動
            benchmarkValue *= (1 + benchmarkDailyReturn);
            benchmarkValues.push(benchmarkValue);
            
            // 增加一天
            currentDate.setDate(currentDate.getDate() + 1);
        }
        
        // 更新圖表數據
        performanceChart.data.labels = dates;
        performanceChart.data.datasets[0].data = portfolioValues;
        performanceChart.data.datasets[1].data = benchmarkValues;
        performanceChart.update();
    }
    
    // 顯示錯誤信息
    function showError(message) {
        console.error(message);
        // 這裡可以添加顯示錯誤信息的 UI 邏輯
        alert(message);
    }
}); 