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

from backend.config import (
    FRONTEND_DIR, TEMPLATES_DIR, STATIC_DIR,
    PMVRLNGAN_DIR, GAT_MODEL_PATH, STOCK_LIST_PATH, TCN_MODEL_PATH,
    DEBUG, SECRET_KEY
)
from backend.logger import logger

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
        # 這裡應該是從預訓練模型或結果文件中讀取股票關係數據
        # 為了示例，我們返回一個模擬的數據
        return jsonify({
            'status': 'success',
            'data': {
                'relationships': 'GAT relationships data will be here'
            }
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
        # 這裡應該是從預訓練模型或結果文件中讀取低風險股票列表
        # 為了示例，我們返回一個模擬的數據
        return jsonify({
            'status': 'success',
            'data': {
                'quarter': quarter,
                'stocks': ['Stock1', 'Stock2', 'Stock3']
            }
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
        logger.info(f"獲取壓縮後的特徵，股票ID: {stock_id}")
        
        if not stock_id:
            logger.warning("獲取壓縮後的特徵失敗: 缺少股票ID")
            return jsonify({
                'status': 'error',
                'message': 'stock_id is required'
            }), 400
        
        # 這裡應該是從預訓練模型或結果文件中讀取壓縮後的特徵
        # 為了示例，我們返回一個模擬的數據
        return jsonify({
            'status': 'success',
            'data': {
                'stock_id': stock_id,
                'features': [0.1, 0.2, 0.3, 0.4, 0.5]
            }
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
        stock_ids = request.args.get('stock_ids', None)
        logger.info(f"獲取交易決策，日期: {date}, 股票IDs: {stock_ids}")
        
        if not date:
            logger.warning("獲取交易決策失敗: 缺少日期")
            return jsonify({
                'status': 'error',
                'message': 'date is required'
            }), 400
        
        # 這裡應該是從預訓練模型或結果文件中讀取交易決策
        # 為了示例，我們返回一個模擬的數據
        return jsonify({
            'status': 'success',
            'data': {
                'date': date,
                'decisions': {
                    'Stock1': {'action': 'buy', 'quantity': 100},
                    'Stock2': {'action': 'sell', 'quantity': 50},
                    'Stock3': {'action': 'hold', 'quantity': 0}
                }
            }
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
        
        if not start_date or not end_date:
            logger.warning("獲取綜合結果失敗: 缺少開始日期或結束日期")
            return jsonify({
                'status': 'error',
                'message': 'start_date and end_date are required'
            }), 400
        
        # 這裡應該是從預訓練模型或結果文件中讀取綜合結果
        # 為了示例，我們返回一個模擬的數據
        return jsonify({
            'status': 'success',
            'data': {
                'start_date': start_date,
                'end_date': end_date,
                'total_return': 0.15,
                'sharpe_ratio': 1.2,
                'max_drawdown': 0.05
            }
        })
    except Exception as e:
        logger.error(f"獲取綜合結果失敗: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=DEBUG) 