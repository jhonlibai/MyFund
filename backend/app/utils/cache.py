# -*- coding: UTF-8 -*-

import json
import os
from typing import Dict, Any

class CacheService:
    """缓存服务（单例模式）"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CacheService, cls).__new__(cls)
            cls._instance.__init__()
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.cache_map: Dict[str, Any] = {}
            self.cache_file = "cache/fund_map.json"
            self.last_cache_file = "cache/fund_map_last.json"
            self.ensure_cache_dir()
            self.load_cache()  # 加载缓存数据
            self.initialized = True
    
    def ensure_cache_dir(self):
        """确保缓存目录存在"""
        cache_dir = os.path.dirname(self.cache_file)
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
    
    def load_cache(self):
        """加载缓存数据"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    self.cache_map = json.load(f)
            except Exception as e:
                print(f"加载缓存失败: {e}")
                self.cache_map = {}
    
    def save_cache(self):
        """保存缓存数据"""
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self.cache_map, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"保存缓存失败: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取缓存值"""
        return self.cache_map.get(key, default)
    
    def set(self, key: str, value: Any):
        """设置缓存值"""
        self.cache_map[key] = value
    
    def delete(self, key: str):
        """删除缓存值"""
        if key in self.cache_map:
            del self.cache_map[key]
    
    def get_all(self) -> Dict[str, Any]:
        """获取所有缓存数据"""
        return self.cache_map
    
    def update(self, data: Dict[str, Any]):
        """更新缓存数据"""
        self.cache_map.update(data)
    
    def load_last_cache(self):
        """加载盘后更新的缓存数据"""
        if os.path.exists(self.last_cache_file):
            try:
                with open(self.last_cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载盘后缓存失败: {e}")
                return {}
        return {}
    
    def save_last_cache(self, data: Dict[str, Any]):
        """保存盘后更新的缓存数据"""
        try:
            with open(self.last_cache_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"盘后缓存保存成功")
        except Exception as e:
            print(f"保存盘后缓存失败: {e}")
    
    def get_last_all(self) -> Dict[str, Any]:
        """获取所有盘后缓存数据"""
        return self.load_last_cache()
