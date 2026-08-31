# -*- coding: utf-8 -*-
"""
綠藝國際學苑 ╳ 老臣聊心室
觀音靈籤調頻系統 - 八大面向生活指引與核心資料模組 (1~100 籤完整支援)
"""
from lots_data import SPECIAL_LOTS

def get_lot_data(lot_num: int) -> dict:
    """
    動態取得符合新版八大生活面向標準格式的籤詩資料 (1~100 籤完整庫)
    """
    if lot_num in SPECIAL_LOTS:
        return SPECIAL_LOTS[lot_num]
    
    # 安全 fallback
    return SPECIAL_LOTS.get(1)
