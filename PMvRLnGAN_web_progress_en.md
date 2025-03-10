# PMvRLnGAN Website Development Progress Report

> **Note**: This document provides an overview of the PMvRLnGAN website development. For more detailed development process and log records, please refer to the "VIII. Development Log" section in [PMvRLnGAN_web_planning.md](PMvRLnGAN_web_planning.md).

## Summary

This report documents the development progress of the PMvRLnGAN system from original code to web interface. As of now, I have completed most of the backend core functionality development, including transaction adapters, stock adapters, and related API endpoint implementations. The system architecture design and basic functions are ready, the frontend basic framework has also been established, and the final backend functionality refinement work is in progress.

## Table of Contents

- [Original Code Analysis](#original-code-analysis)
- [Implemented Features](#implemented-features)
- [Test Results](#test-results)
- [Data Source Analysis](#data-source-analysis)
- [Development Timeline](#development-timeline)
- [Development Progress Tracking](#development-progress-tracking)
- [Next Phase Work](#next-phase-work)
- [Data Processing Strategy](#data-processing-strategy)



## Original Code Analysis

Before developing the website, I first analyzed the original PMvRLnGAN code, which consists of four main parts:

1. **GAT (Graph Attention Network)**
   - Function: Analyzes the relationships between stocks, generates stock relationship matrices
   - Key files: `gat_model.pth` (pre-trained model) and `edge.py` (script for generating relationship matrices)
   - Output: 74x74 stock pair relationship matrix

2. **Stock-Picked Agent**
   - Function: Selects the stock combination with minimal risk
   - Key files: `Low-risk stock list.csv` (pre-selected low-risk stock list)
   - Output: List of low-risk stocks selected for each quarter

3. **TCN-AE (Temporal Convolutional Network Autoencoder)**
   - Function: Compresses stock technical indicators, extracts features
   - Key files: `tcn_20_model.h5` (pre-trained model)
   - Output: Compressed 20-dimensional feature vector

4. **Trading Agent**
   - Function: Generates daily trading decisions based on low-risk stock lists and compressed features
   - Key files: `trading_agent_model.zip` (pre-trained model)
   - Output: Daily trading decisions (buy/sell quantities)

The original code mainly exists in the form of Jupyter Notebooks, requiring manual execution of multiple steps to obtain complete analysis results. My goal is to integrate these functions into a website, allowing users to execute the entire system through simple button operations.

## Implemented Features

### Backend API Endpoints

I have implemented the following API endpoints:

| API Endpoint | Method | Function | Parameters | Status |
|---------|------|------|------|------|
| `/api/trading/valid-dates` | GET | Get valid trading date range | None | ✅ Completed |
| `/api/stock-picked/quarters` | GET | Get available quarters list | None | ✅ Completed |
| `/api/stock-picked/list` | GET | Get low-risk stock list | `quarter` (optional) | ✅ Completed |
| `/api/trading/decisions` | GET | Get trading decisions for specified date | `date`, `stock_ids` (optional) | ✅ Completed |
| `/api/results/summary` | GET | Get performance summary | `start_date`, `end_date` | ✅ Completed |
| `/api/gat/relationships` | GET | Get stock relationship data | None | ⏳ In Progress |
| `/api/tcn-ae/features` | GET | Get compressed features | `stock_id` | ⏳ In Progress |

### Adapter Modules

I have developed the following adapter modules to connect the original code and website API:

1. **Stock Adapter (stock_adapter.py)**
   - ✅ Implemented low-risk stock list reading functionality
   - ✅ Implemented quarter selector functionality
   - ✅ Added error handling and logging

2. **Trading Adapter (trading_adapter.py)**
   - ✅ Implemented date range limitation and valid trading day checking functionality
   - ✅ Implemented trading decision retrieval functionality
   - ✅ Implemented performance summary functionality
   - ✅ Optimized data reading methods

3. **GAT Adapter (gat_adapter.py)**
   - ⏳ Implementing stock relationship data reading functionality
   - ⏳ Implementing relationship weight calculation functionality

4. **TCN-AE Adapter (tcn_adapter.py)**
   - ⏳ Implementing compressed feature reading functionality
   - ⏳ Implementing feature vector processing functionality

### Frontend Pages

I have implemented the following frontend pages and functionalities:

1. **Main Page (index.html)**
   - ✅ System introduction section
   - ✅ Analysis results display area (using tabs to switch between different content)
   - ✅ Responsive design, adapting to different devices

2. **Frontend Interaction (main.js)**
   - ✅ Start analysis button functionality
   - ✅ Quarter selector functionality
   - ✅ Trading date selector functionality
   - ✅ Communication with backend APIs
   - ✅ Data display and update functionality

3. **Style Design (main.css)**
   - ✅ Basic page styles
   - ✅ Table and card styles
   - ✅ Responsive adjustments

### Displayable Content

The website will be able to display the following content:

1. **Low-Risk Stock List**
   - ✅ Low-risk stocks selected for each quarter
   - ✅ Stock code, name, risk value, and weight
   - ✅ Quarter selector, can switch between different quarters' data

2. **Trading Decisions**
   - ✅ Trading decisions for each trading day
   - ✅ Buy, sell, or hold operation recommendations
   - ✅ Trading quantities and prices
   - ✅ Date selector, can select decisions for different dates

3. **Performance Summary**
   - ✅ Portfolio performance indicators
   - ✅ Total return rate, annualized return rate, Sharpe ratio, and maximum drawdown
   - ✅ Performance chart, showing portfolio value changes

4. **Stock Relationship Network**
   - ⏳ Visualization of relationships between stocks
   - ⏳ Relationship strength and direction

5. **Technical Indicator Analysis**
   - ⏳ Visualization of compressed feature vectors
   - ⏳ Feature importance analysis

## Test Results

I developed the test script `test_adapter.py` to test adapter functionality and API endpoints. The test results are as follows:

### Functional Test Results

| Test Item | Result | Notes |
|---------|------|------|
| Load Trading Dates | ✅ Success | Successfully loaded 11 trading days |
| Get Valid Date Range | ✅ Success | Range: 2021-11-15 to 2024-05-16 |
| Date Validation | ✅ Success | Correctly identified valid and invalid dates |
| Get Trading Decisions | ✅ Success | Successfully retrieved 33 decisions |
| Get Performance Summary | ✅ Success | Successfully generated performance indicators |
| Get Available Quarters | ✅ Success | Successfully retrieved 8 quarters |
| Get Low-Risk Stock List | ✅ Success | Successfully retrieved 33 stocks |

### API Endpoint Test Results

| API Endpoint | Result | Notes |
|---------|------|------|
| `/api/trading/valid-dates` | ✅ Success | Returned correct date range |
| `/api/stock-picked/quarters` | ✅ Success | Returned correct quarters list |
| `/api/stock-picked/list` | ✅ Success | Returned correct stock list |
| `/api/trading/decisions` | ✅ Success | Returned correct trading decisions |
| `/api/results/summary` | ✅ Success | Returned correct performance summary |

## Data Source Analysis

I conducted a detailed analysis of the data sources used by the website, distinguishing between real data and simulated data:

### Data Source Overview

| Module | Function/Data | Source Type | Data Location/Generation Method | Web Page Location |
|------|-----------|----------|-------------------|--------------|
| **Stock Adapter** | Low-risk stock list | ✅ Real data | `PMvRLnGAN/Trading Agent/Low-risk stock list.csv` | "Low-Risk Stock List" page |
| | Quarters list | ✅ Real data | Extracted from low-risk stock list | Quarter selector dropdown menu |
| | Stock names and codes | ✅ Real data | Extracted from low-risk stock list | All pages |
| | Stock risk assessment | ⚠️ Simulated data | Randomly generated risk values | "Low-Risk Stock List" page |
| **Trading Adapter** | Trading date range | ✅ Real data | Extracted from low-risk stock list | "Trading Decisions" page |
| | Valid trading day check | ✅ Real data | Validation based on real trading dates | "Trading Decisions" page |
| | Trading decisions | ⚠️ Partially real | `trading_decisions_examples.csv` (only includes limited dates from 2024-05-17 to 2024-06-04) | "Trading Decisions" page |
| | Performance summary | ⚠️ Simulated data | Randomly generated performance indicators | "Performance Summary" page |
| **GAT Adapter** | Stock relationship data | ⚠️ Simulated data | Randomly generated relationship matrix | "Stock Relationship Network" page |
| | Relationship weights | ⚠️ Simulated data | Randomly generated weight values | "Stock Relationship Network" page |
| **TCN-AE Adapter** | Compressed features | ⚠️ Simulated data | Randomly generated feature vectors | "Technical Indicator Analysis" page |
| | Feature vectors | ⚠️ Simulated data | Randomly generated feature vectors | "Technical Indicator Analysis" page |

I implemented a data source control mechanism, controlling the data source through the `USE_MOCK_DATA` variable in the configuration file `config.py`. When set to `False`, the system will first try to read real data files, and if not found, automatically fall back to using simulated data.

## Development Timeline

### : Basic Infrastructure Design
- ✅ Analyzed the original PMvRLnGAN code structure and execution flow
- ✅ Designed the system architecture (frontend, backend, data flow)
- ✅ Selected the technology stack: Flask as the backend framework, pure HTML/CSS/JavaScript as the frontend technology
- ✅ Established the development environment and basic project structure
- ✅ Tested the feasibility of directly reading pre-trained models and result files

### : Stock Adapter Development
- ✅ Implemented low-risk stock list reading functionality
- ✅ Implemented quarter selector functionality
- ✅ Developed `/api/stock-picked/quarters` and `/api/stock-picked/list` API endpoints
- ✅ Added error handling and logging functionality

### : Trading Adapter Development
- ✅ Implemented date range limitation and valid trading day checking functionality
- ✅ Implemented trading decision retrieval functionality
- ✅ Optimized the trading adapter, removed unnecessary tcn_daily_trade_info.7z extraction code
- ✅ Modified the trading adapter to directly read trading dates and stock data from Low-risk stock list.csv
- ✅ Developed `/api/trading/valid-dates` and `/api/trading/decisions` API endpoints

### : Performance Summary Functionality Development
- ✅ Implemented performance summary functionality, providing simulated performance data
- ✅ Developed `/api/results/summary` API endpoint
- ✅ Modified train trade agent.ipynb, added model and trading decision saving code

### : Test Script Development
- ✅ Created test_adapter.py test script
- ✅ Fixed errors in the test script to ensure correct handling of API returned data structures
- ✅ Completed functional testing of trading adapter and stock adapter
- ✅ Completed testing of all implemented API endpoints

### : Frontend Basic Framework Development
- ✅ Designed and implemented the main page HTML structure
- ✅ Implemented basic CSS styles
- ✅ Developed frontend JavaScript interaction functionality
- ✅ Implemented basic communication with backend APIs


## Development Progress Tracking

I divided the development plan into five phases, and the current progress is as follows:

### Phase One: Basic Infrastructure Design
- ✅ Design system architecture (frontend, backend, data flow)
- ✅ Select technology stack
- ✅ Establish development environment
- ✅ Create basic project structure
- ✅ Test the feasibility of directly reading pre-trained models and result files
- **Completion: 100%**

### Phase Two: Backend Development - Core Functionality
- ✅ Implement `/api/trading/valid-dates` endpoint
- ✅ Implement `/api/stock-picked/quarters` endpoint
- ✅ Implement `/api/stock-picked/list` endpoint
- ✅ Implement `/api/trading/decisions` endpoint
- ✅ Implement `/api/results/summary` endpoint
- ⏳ Implement `/api/gat/relationships` endpoint
- ⏳ Implement `/api/tcn-ae/features` endpoint
- ✅ Implement result storage and retrieval mechanism
- ✅ Handle errors and exceptions
- ✅ Add basic logging functionality
- **Completion: 90%**

### Phase Three: Frontend Development - Basic Interface
- ✅ Design and implement main page (HTML/CSS)
- ✅ Implement execution button and basic interaction (JavaScript)
- ✅ Design layout for result display pages
- ✅ Implement basic communication with backend APIs
- ⏳ Refine frontend error handling and user prompts
- **Completion: 80%**

### Phase Four: Result Visualization and User Experience Optimization
- ✅ Implement visualization of stock selection results (tables)
- ✅ Implement visualization of trading decisions (tables)
- ✅ Implement visualization of performance summary (charts)
- ⏳ Implement visualization of stock relationship network
- ⏳ Implement visualization of technical indicator analysis
- ⏳ Add loading indicators and progress prompts
- ⏳ Optimize error prompts and user guidance
- ⏳ Ensure responsive design works properly on different devices
- **Completion: 40%**

### Phase Five: Integration Testing and Deployment
- ⏳ Conduct end-to-end testing
- ⏳ Fix discovered issues
- ⏳ Prepare deployment environment
- ⏳ Deploy system and conduct final testing
- **Completion: 0%**

## Next Phase Work

I plan to complete the following tasks in the upcoming work:

### Priority Tasks (Complete Phase Two)
1. **Complete GAT Adapter**
   - [ ] Implement functionality to read stock relationship data
   - [ ] Implement `/api/gat/relationships` API endpoint

2. **Complete TCN-AE Adapter**
   - [ ] Implement functionality to read compressed features
   - [ ] Implement `/api/tcn-ae/features` API endpoint

3. **Conduct Comprehensive Testing**
   - [ ] Test interoperability of all API endpoints
   - [ ] Ensure all functionalities work properly in various scenarios

4. **Refine Documentation**
   - [ ] Update API documentation
   - [ ] Improve code comments

### Subsequent Tasks (Complete Phases Three and Four)
1. **Refine Frontend Functionality**
   - [ ] Refine frontend error handling
   - [ ] Add user prompts and guidance
   - [ ] Optimize responsive design

2. **Implement Advanced Visualization**
   - [ ] Implement visualization of stock relationship network
   - [ ] Implement visualization of technical indicator analysis
   - [ ] Optimize interactive functionality of performance charts

## Data Processing Strategy

To ensure the website can display real analysis results, I designed a "preprocessing + direct reading" data processing strategy:

### Preprocessing Stage (One-time Execution)

1. **GAT Relationship Matrix Generation**
   - [ ] Execute `edge.py` script
   - [ ] Generate `relationships.json` file

2. **TCN-AE Feature Compression**
   - [ ] Execute `TCN-AE predict data.ipynb` script
   - [ ] Generate compressed feature files

3. **Trading Agent Decision Generation**
   - [x] Modify saving code in `train trade agent.ipynb`
   - [ ] Generate complete trading decision files

### Website Stage (Direct Reading of Preprocessing Results)

1. **GAT Adapter**
   - [ ] Directly read `relationships.json` file
   - [ ] No need to execute GAT model

2. **Stock-Picked Adapter**
   - [x] Directly read `Low-risk stock list.csv` file
   - [x] No need to execute Stock-Picked Agent

3. **TCN-AE Adapter**
   - [ ] Directly read compressed feature files
   - [ ] No need to execute TCN-AE model

4. **Trading Adapter**
   - [x] Directly read `trading_decisions_examples.csv` file
   - [x] No need to execute Trading Agent

The advantages of this strategy are:
- Simplifies development process
- Improves website performance
- Reduces runtime errors
- Ensures result consistency

Through this approach, I can ensure that the website displays real analysis results while avoiding the overhead of repeatedly executing complex calculations. 