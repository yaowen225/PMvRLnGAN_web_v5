#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PMvRLnGAN Web 日誌模塊
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from backend.config import LOG_LEVEL, LOG_FILE

# 確保日誌目錄存在
log_dir = Path(LOG_FILE).parent
if not log_dir.exists():
    os.makedirs(log_dir, exist_ok=True)

# 配置日誌格式
log_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 創建日誌處理器
file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=10485760,  # 10MB
    backupCount=5,
    encoding='utf-8'
)
file_handler.setFormatter(log_format)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_format)

# 創建日誌記錄器
logger = logging.getLogger('pmvrlngan_web')
logger.setLevel(getattr(logging, LOG_LEVEL))
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 導出日誌記錄器
__all__ = ['logger'] 