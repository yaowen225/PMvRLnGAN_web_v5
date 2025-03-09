"""
適配器模組初始化文件
用於連接原始程式碼和網站界面
"""

from . import stock_adapter
from . import trading_adapter

__all__ = ['stock_adapter', 'trading_adapter', 'gat_adapter', 'tcn_adapter'] 