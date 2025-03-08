#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PMvRLnGAN Web 配置文件
"""

import os
from pathlib import Path

# 基本路徑配置
BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = BASE_DIR / 'backend'
FRONTEND_DIR = BASE_DIR / 'frontend'
TEMPLATES_DIR = FRONTEND_DIR / 'templates'
STATIC_DIR = FRONTEND_DIR / 'static'

# 原始 PMvRLnGAN 程序路徑
# 注意：這個路徑需要根據實際情況進行調整
PMVRLNGAN_DIR = Path(os.environ.get('PMVRLNGAN_DIR', '../PMvRLnGAN'))

# 模型文件路徑
GAT_MODEL_PATH = PMVRLNGAN_DIR / 'GAT-main' / 'gat_model.pth'
TCN_MODEL_PATH = PMVRLNGAN_DIR / 'TCN-AE' / 'tcn_20_model.h5'
TRADING_MODEL_PATH = PMVRLNGAN_DIR / 'Trading Agent' / 'models'

# 數據文件路徑
STOCK_LIST_PATH = PMVRLNGAN_DIR / 'Stock-Picked Agent' / 'Low-risk stock list.csv'
TRADE_INFO_PATH = PMVRLNGAN_DIR / 'Trading Agent' / 'tcn_daily_trade_info'

# API 配置
API_PREFIX = '/api'
API_VERSION = 'v1'

# 應用配置
DEBUG = True
SECRET_KEY = 'pmvrlngan-web-secret-key'  # 在生產環境中應該使用環境變量設置

# 日誌配置
LOG_LEVEL = 'INFO'
LOG_FILE = BASE_DIR / 'logs' / 'app.log' 