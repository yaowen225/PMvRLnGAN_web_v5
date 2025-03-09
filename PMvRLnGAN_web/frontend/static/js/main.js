// 等待 DOM 加載完成
document.addEventListener('DOMContentLoaded', function() {
    // 獲取元素
    const startAnalysisBtn = document.getElementById('startAnalysisBtn');
    const introductionSection = document.getElementById('introduction');
    const analysisSection = document.getElementById('analysis');
    const loadingSection = document.getElementById('loading');
    const tradingDateInput = document.getElementById('tradingDate');
    const quarterSelect = document.getElementById('quarterSelect');
    
    // 獲取有效的交易日期範圍
    fetchValidDateRange();
    
    // 獲取可用的季度列表
    fetchAvailableQuarters();
    
    // 季度選擇器變更事件
    if (quarterSelect) {
        quarterSelect.addEventListener('change', function() {
            fetchStockListByQuarter(this.value);
        });
    }
    
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
    
    // 獲取有效的交易日期範圍
    function fetchValidDateRange() {
        fetch('/api/trading/valid-dates')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const { start_date, end_date } = data.data;
                    
                    // 設置日期選擇器的最小和最大值
                    tradingDateInput.min = start_date;
                    tradingDateInput.max = end_date;
                    
                    // 添加日期範圍提示
                    const dateRangeInfo = document.createElement('small');
                    dateRangeInfo.classList.add('form-text', 'text-muted');
                    dateRangeInfo.textContent = `有效日期範圍: ${start_date} 到 ${end_date}`;
                    tradingDateInput.parentNode.appendChild(dateRangeInfo);
                    
                    // 設置默認日期為範圍內的日期
                    const today = new Date();
                    const formattedToday = today.toISOString().split('T')[0];
                    
                    // 如果今天在有效範圍內，使用今天；否則使用範圍的結束日期
                    if (formattedToday >= start_date && formattedToday <= end_date) {
                        tradingDateInput.value = formattedToday;
                    } else {
                        tradingDateInput.value = end_date;
                    }
                } else {
                    showError('獲取有效日期範圍失敗：' + data.message);
                    
                    // 設置今天的日期為交易日期輸入框的默認值
                    const today = new Date();
                    const formattedDate = today.toISOString().split('T')[0];
                    tradingDateInput.value = formattedDate;
                }
            })
            .catch(error => {
                showError('獲取有效日期範圍時發生錯誤：' + error.message);
                
                // 設置今天的日期為交易日期輸入框的默認值
                const today = new Date();
                const formattedDate = today.toISOString().split('T')[0];
                tradingDateInput.value = formattedDate;
            });
    }
    
    // 獲取可用的季度列表
    function fetchAvailableQuarters() {
        fetch('/api/stock-picked/quarters')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success' && data.data.quarters) {
                    populateQuarterSelect(data.data.quarters);
                } else {
                    showError('獲取季度列表失敗：' + (data.message || '未知錯誤'));
                }
            })
            .catch(error => {
                showError('獲取季度列表時發生錯誤：' + error.message);
            });
    }
    
    // 填充季度選擇器
    function populateQuarterSelect(quarters) {
        if (!quarterSelect) return;
        
        // 清空現有選項
        quarterSelect.innerHTML = '';
        
        // 添加季度選項
        quarters.forEach(quarter => {
            const option = document.createElement('option');
            option.value = quarter;
            option.textContent = quarter;
            quarterSelect.appendChild(option);
        });
        
        // 設置默認選中的季度（最新的季度）
        if (quarters.length > 0) {
            const latestQuarter = quarters[quarters.length - 1];
            quarterSelect.value = latestQuarter;
            
            // 獲取該季度的股票列表
            fetchStockListByQuarter(latestQuarter);
        }
    }
    
    // 根據季度獲取股票列表
    function fetchStockListByQuarter(quarter) {
        // 顯示加載提示
        const tableBody = document.querySelector('#stockListTable tbody');
        tableBody.innerHTML = '<tr><td colspan="4" class="text-center">正在加載股票列表...</td></tr>';
        
        fetch(`/api/stock-picked/list?quarter=${quarter}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success' && data.data.stocks) {
                    populateStockListTable(data.data.stocks);
                    
                    // 更新季度標題
                    const quarterTitle = document.getElementById('stockListTitle');
                    if (quarterTitle) {
                        quarterTitle.textContent = `低風險股票列表 (${quarter})`;
                    }
                } else {
                    showError('獲取股票列表失敗：' + (data.message || '未知錯誤'));
                    tableBody.innerHTML = '<tr><td colspan="4" class="text-center text-danger">獲取股票列表失敗</td></tr>';
                }
            })
            .catch(error => {
                showError('獲取股票列表時發生錯誤：' + error.message);
                tableBody.innerHTML = '<tr><td colspan="4" class="text-center text-danger">獲取股票列表時發生錯誤</td></tr>';
            });
    }
    
    // 獲取股票列表（修改為使用當前選擇的季度）
    function fetchStockList() {
        // 如果季度選擇器已經初始化，使用選中的季度
        if (quarterSelect && quarterSelect.value) {
            fetchStockListByQuarter(quarterSelect.value);
        } else {
            // 否則使用當前季度
            const currentQuarter = getCurrentQuarter();
            fetchStockListByQuarter(currentQuarter);
        }
    }
    
    // 獲取當前季度
    function getCurrentQuarter() {
        const today = new Date();
        const year = today.getFullYear();
        const month = today.getMonth() + 1;
        let quarter;
        
        if (month <= 3) {
            quarter = 'Q1';
        } else if (month <= 6) {
            quarter = 'Q2';
        } else if (month <= 9) {
            quarter = 'Q3';
        } else {
            quarter = 'Q4';
        }
        
        return `${year}-${quarter}`;
    }
    
    // 獲取交易決策
    function fetchTradingDecisions(date) {
        // 顯示加載提示
        const tableBody = document.querySelector('#tradingDecisionsTable tbody');
        tableBody.innerHTML = '<tr><td colspan="4" class="text-center">正在加載交易決策...</td></tr>';
        
        fetch(`/api/trading/decisions?date=${date}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    populateTradingDecisionsTable(data.data.decisions);
                } else {
                    // 檢查是否有最近的交易日建議
                    if (data.details && data.details.nearest_trading_day) {
                        const nearestDate = data.details.nearest_trading_day;
                        showWarning(`所選日期不是交易日。是否要查看 ${nearestDate} 的交易決策？`, function() {
                            tradingDateInput.value = nearestDate;
                            fetchTradingDecisions(nearestDate);
                        });
                        tableBody.innerHTML = '<tr><td colspan="4" class="text-center text-warning">所選日期不是交易日</td></tr>';
                    } else {
                        showError('獲取交易決策失敗：' + data.message);
                        tableBody.innerHTML = '<tr><td colspan="4" class="text-center text-danger">獲取交易決策失敗</td></tr>';
                    }
                }
            })
            .catch(error => {
                showError('獲取交易決策時發生錯誤：' + error.message);
                tableBody.innerHTML = '<tr><td colspan="4" class="text-center text-danger">獲取交易決策時發生錯誤</td></tr>';
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
                    // 檢查是否有有效日期範圍建議
                    if (data.valid_range) {
                        const { start_date, end_date } = data.valid_range;
                        showWarning(`所選日期範圍無效。使用有效範圍 ${start_date} 到 ${end_date} 代替？`, function() {
                            fetchPerformanceSummaryWithDates(start_date, end_date);
                        });
                    } else {
                        showError('獲取績效摘要失敗：' + data.message);
                    }
                }
            })
            .catch(error => {
                showError('獲取績效摘要時發生錯誤：' + error.message);
            });
    }
    
    // 使用指定日期範圍獲取績效摘要
    function fetchPerformanceSummaryWithDates(startDate, endDate) {
        fetch(`/api/results/summary?start_date=${startDate}&end_date=${endDate}`)
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
        
        if (!stocks || stocks.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="4" class="text-center">沒有股票數據</td></tr>';
            return;
        }
        
        stocks.forEach(stock => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${stock.stock_id}</td>
                <td>${stock.stock_name}</td>
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
        
        if (!decisions || decisions.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="4" class="text-center">沒有交易決策</td></tr>';
            return;
        }
        
        decisions.forEach(decision => {
            const row = document.createElement('tr');
            
            // 根據操作類型設置不同的顏色
            let actionClass = '';
            
            switch (decision.action) {
                case 1:
                    actionClass = 'text-success';
                    break;
                case -1:
                    actionClass = 'text-danger';
                    break;
                case 0:
                    actionClass = 'text-warning';
                    break;
            }
            
            row.innerHTML = `
                <td>${decision.stock_id}</td>
                <td>${decision.stock_id}</td>
                <td class="${actionClass}">${decision.action_name}</td>
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
    
    // 顯示錯誤訊息
    function showError(message) {
        // 創建警告元素
        const alertDiv = document.createElement('div');
        alertDiv.classList.add('alert', 'alert-danger', 'alert-dismissible', 'fade', 'show', 'mt-3');
        alertDiv.setAttribute('role', 'alert');
        alertDiv.innerHTML = `
            <strong>錯誤!</strong> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        // 添加到頁面
        document.querySelector('.container').prepend(alertDiv);
        
        // 5秒後自動關閉
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        }, 5000);
    }
    
    // 顯示警告訊息，帶有確認按鈕
    function showWarning(message, confirmCallback) {
        // 創建警告元素
        const alertDiv = document.createElement('div');
        alertDiv.classList.add('alert', 'alert-warning', 'alert-dismissible', 'fade', 'show', 'mt-3');
        alertDiv.setAttribute('role', 'alert');
        
        const confirmBtn = document.createElement('button');
        confirmBtn.classList.add('btn', 'btn-sm', 'btn-primary', 'ms-3');
        confirmBtn.textContent = '確認';
        confirmBtn.addEventListener('click', function() {
            confirmCallback();
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        });
        
        alertDiv.innerHTML = `
            <strong>警告!</strong> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        alertDiv.insertBefore(confirmBtn, alertDiv.querySelector('.btn-close'));
        
        // 添加到頁面
        document.querySelector('.container').prepend(alertDiv);
        
        // 10秒後自動關閉
        setTimeout(() => {
            if (document.body.contains(alertDiv)) {
                const bsAlert = new bootstrap.Alert(alertDiv);
                bsAlert.close();
            }
        }, 10000);
    }
}); 