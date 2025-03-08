#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PMvRLnGAN Web 應用啟動腳本
"""

import os
import sys
from backend.app import app
from backend.config import DEBUG
from backend.logger import logger

if __name__ == "__main__":
    # 設置環境變量
    os.environ.setdefault("FLASK_ENV", "development" if DEBUG else "production")
    
    # 獲取命令行參數
    port = 5000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            logger.warning(f"無效的端口號: {sys.argv[1]}，使用默認端口 5000")
    
    # 啟動應用
    logger.info(f"啟動 PMvRLnGAN Web 應用於 http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=DEBUG) 