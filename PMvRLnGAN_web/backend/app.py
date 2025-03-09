#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PMvRLnGAN Web 後端應用
"""

from flask import Flask, render_template, jsonify, request
import os
import json
import pandas as pd
import numpy as np
from datetime import datetime

from backend.config import (
    FRONTEND_DIR, TEMPLATES_DIR, STATIC_DIR,
    PMVRLNGAN_DIR, GAT_MODEL_PATH, STOCK_LIST_PATH, TCN_MODEL_PATH,
    DEBUG, SECRET_KEY, TRADING_START_DATE, TRADING_END_DATE
)
from backend.logger import logger
from backend.adapters.trading_adapter import (
    get_trading_decisions as adapter_get_trading_decisions,
    get_valid_date_range,
    is_valid_trading_day,
    is_date_in_range,
    get_nearest_trading_day,
    get_performance_summary as adapter_get_performance_summary
)
from backend.adapters.stock_adapter import (
    get_stock_list as adapter_get_stock_list,
    get_available_quarters as adapter_get_available_quarters
)
from backend.adapters.gat_adapter import (
    get_stock_relationships as adapter_get_stock_relationships
)
from backend.adapters.tcn_adapter import (
    get_compressed_features as adapter_get_compressed_features
)

# 創建 Flask 應用
app = Flask(__name__, 
            static_folder=str(STATIC_DIR),
            template_folder=str(TEMPLATES_DIR))

# 配置應用
app.config['SECRET_KEY'] = SECRET_KEY
app.config['DEBUG'] = DEBUG

# 記錄應用啟動信息
logger.info("PMvRLnGAN Web 應用啟動")
logger.info(f"前端目錄: {FRONTEND_DIR}")
logger.info(f"模板目錄: {TEMPLATES_DIR}")
logger.info(f"靜態文件目錄: {STATIC_DIR}")
logger.info(f"PMvRLnGAN 目錄: {PMVRLNGAN_DIR}")

@app.route('/')
def index():
    """首頁"""
    logger.info("訪問首頁")
    return render_template('index.html')

@app.route('/api/gat/relationships', methods=['GET'])
def get_gat_relationships():
    """獲取股票關係數據"""
    try:
        logger.info("獲取股票關係數據")
        
        # 使用適配器獲取股票關係數據
        result = adapter_get_stock_relationships()
        
        # 檢查是否有錯誤
        if 'error' in result:
            logger.warning(f"獲取股票關係數據失敗: {result['error']}")
            return jsonify({
                'status': 'error',
                'message': result['error'],
                'details': result
            }), 400
        
        return jsonify({
            'status': 'success',
            'data': result
        })
    except Exception as e:
        logger.error(f"獲取股票關係數據失敗: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/stock-picked/list', methods=['GET'])
def get_stock_picked_list():
    """獲取低風險股票列表"""
    try:
        quarter = request.args.get('quarter', None)
        logger.info(f"獲取低風險股票列表，季度: {quarter}")
        
        # 使用適配器獲取股票列表
        result = adapter_get_stock_list(quarter)
        
        # 檢查是否有錯誤
        if 'error' in result:
            logger.warning(f"獲取低風險股票列表失敗: {result['error']}")
            return jsonify({
                'status': 'error',
                'message': result['error'],
                'details': result
            }), 400
        
        return jsonify({
            'status': 'success',
            'data': result
        })
    except Exception as e:
        logger.error(f"獲取低風險股票列表失敗: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/tcn-ae/features', methods=['GET'])
def get_tcn_ae_features():
    """獲取壓縮後的特徵"""
    try:
        stock_id = request.args.get('stock_id', None)
        date = request.args.get('date', None)
        logger.info(f"獲取壓縮後的特徵，股票ID: {stock_id}, 日期: {date}")
        
        if not stock_id:
            logger.warning("獲取壓縮後的特徵失敗: 缺少股票ID")
            return jsonify({
                'status': 'error',
                'message': 'stock_id is required'
            }), 400
        
        # 使用適配器獲取壓縮特徵
        result = adapter_get_compressed_features(stock_id, date)
        
        # 檢查是否有錯誤
        if 'error' in result:
            logger.warning(f"獲取壓縮後的特徵失敗: {result['error']}")
            return jsonify({
                'status': 'error',
                'message': result['error'],
                'details': result
            }), 400
        
        return jsonify({
            'status': 'success',
            'data': result
        })
    except Exception as e:
        logger.error(f"獲取壓縮後的特徵失敗: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/trading/decisions', methods=['GET'])
def get_trading_decisions():
    """獲取交易決策"""
    try:
        date = request.args.get('date', None)
        stock_ids_str = request.args.get('stock_ids', None)
        logger.info(f"獲取交易決策，日期: {date}, 股票IDs: {stock_ids_str}")
        
        if not date:
            logger.warning("獲取交易決策失敗: 缺少日期")
            return jsonify({
                'status': 'error',
                'message': 'date is required'
            }), 400
        
        # 解析股票 ID 列表（如果有）
        stock_ids = None
        if stock_ids_str:
            try:
                stock_ids = stock_ids_str.split(',')
            except Exception as e:
                logger.warning(f"解析股票ID列表失敗: {str(e)}")
        
        # 使用適配器獲取交易決策
        result = adapter_get_trading_decisions(date, stock_ids)
        
        # 檢查是否有錯誤
        if 'error' in result:
            logger.warning(f"獲取交易決策失敗: {result['error']}")
            return jsonify({
                'status': 'error',
                'message': result['error'],
                'details': result
            }), 400
        
        return jsonify({
            'status': 'success',
            'data': result
        })
    except Exception as e:
        logger.error(f"獲取交易決策失敗: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/results/summary', methods=['GET'])
def get_results_summary():
    """獲取綜合結果"""
    try:
        start_date = request.args.get('start_date', None)
        end_date = request.args.get('end_date', None)
        logger.info(f"獲取綜合結果，開始日期: {start_date}, 結束日期: {end_date}")
        
        # 使用適配器獲取績效摘要
        result = adapter_get_performance_summary(start_date, end_date)
        
        # 檢查是否有錯誤
        if 'error' in result:
            logger.warning(f"獲取績效摘要失敗: {result['error']}")
            return jsonify({
                'status': 'error',
                'message': result['error'],
                'details': result
            }), 400
        
        return jsonify({
            'status': 'success',
            'data': result
        })
    except Exception as e:
        logger.error(f"獲取績效摘要失敗: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/trading/valid-dates', methods=['GET'])
def get_valid_trading_dates():
    """獲取有效的交易日期範圍"""
    try:
        logger.info("獲取有效的交易日期範圍")
        date_range = get_valid_date_range()
        return jsonify({
            'status': 'success',
            'data': date_range
        })
    except Exception as e:
        logger.error(f"獲取有效的交易日期範圍失敗: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/stock-picked/quarters', methods=['GET'])
def get_available_quarters():
    """獲取可用的季度列表"""
    try:
        logger.info("獲取可用的季度列表")
        result = adapter_get_available_quarters()
        
        if 'error' in result:
            logger.warning(f"獲取可用的季度列表失敗: {result['error']}")
            return jsonify({
                'status': 'error',
                'message': result['error']
            }), 400
        
        return jsonify({
            'status': 'success',
            'data': result
        })
    except Exception as e:
        logger.error(f"獲取可用的季度列表失敗: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 