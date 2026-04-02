import redis
from typing import Any, Dict, Optional
import json


class RedisMiddleware:
    """Redis中间件，提供缓存和会话管理功能"""
    
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0, password: Optional[str] = None):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.client: Optional[redis.Redis] = None
        self.connect()
    
    def connect(self) -> None:
        """连接Redis服务器"""
        try:
            self.client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
                decode_responses=True
            )
            # 测试连接
            self.client.ping()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Redis: {str(e)}")
    
    def get(self, key: str) -> Optional[Any]:
        """获取键值"""
        if not self.client:
            self.connect()
        
        value = self.client.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None
    
    def set(self, key: str, value: Any, expire_seconds: Optional[int] = None) -> bool:
        """设置键值"""
        if not self.client:
            self.connect()
        
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        
        if expire_seconds:
            return self.client.setex(key, expire_seconds, value)
        else:
            return self.client.set(key, value)
    
    def delete(self, key: str) -> bool:
        """删除键"""
        if not self.client:
            self.connect()
        
        return bool(self.client.delete(key))
    
    def exists(self, key: str) -> bool:
        """检查键是否存在"""
        if not self.client:
            self.connect()
        
        return bool(self.client.exists(key))
    
    def close(self) -> None:
        """关闭Redis连接"""
        if self.client:
            self.client.close()
            self.client = None
