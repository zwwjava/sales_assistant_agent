import psycopg2
from psycopg2 import pool
from psycopg2.extras import Json, RealDictCursor
from typing import Any, Dict, List, Optional
import json


class PostgreSQLClient:
    """PostgreSQL中间件，提供聊天历史管理功能，支持JSONB格式存储"""
    
    def __init__(self, host: str = "localhost", port: int = 5432, database: str = "wwbot", 
                 username: str = "postgres", password: Optional[str] = None, 
                 min_conn: int = 1, max_conn: int = 10):
        """初始化PostgreSQL连接池
        
        Args:
            host: PostgreSQL主机地址
            port: PostgreSQL端口
            database: 数据库名称
            username: 用户名
            password: 密码
            min_conn: 连接池最小连接数
            max_conn: 连接池最大连接数
        """
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.min_conn = min_conn
        self.max_conn = max_conn
        self.connection_pool: Optional[pool.SimpleConnectionPool] = None
        self.init_connection_pool()
        self.init_tables()
    
    def init_connection_pool(self) -> None:
        """初始化连接池"""
        try:
            self.connection_pool = pool.SimpleConnectionPool(
                minconn=self.min_conn,
                maxconn=self.max_conn,
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.username,
                password=self.password
            )
        except Exception as e:
            raise ConnectionError(f"Failed to create PostgreSQL connection pool: {str(e)}")
    
    def get_connection(self):
        """从连接池获取连接"""
        if not self.connection_pool:
            self.init_connection_pool()
        return self.connection_pool.getconn()
    
    def release_connection(self, conn) -> None:
        """释放连接回连接池"""
        if self.connection_pool and conn:
            self.connection_pool.putconn(conn)
    
    def init_tables(self) -> None:
        """初始化数据库表，创建聊天历史表（如果不存在）"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 创建聊天历史表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id SERIAL PRIMARY KEY,
                    session_id VARCHAR(255) NOT NULL,
                    user_id VARCHAR(255) NOT NULL,
                    message JSONB NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                -- 创建索引以提高查询性能
                CREATE INDEX IF NOT EXISTS idx_chat_history_session_id ON chat_history(session_id);
                CREATE INDEX IF NOT EXISTS idx_chat_history_user_id ON chat_history(user_id);
                CREATE INDEX IF NOT EXISTS idx_chat_history_created_at ON chat_history(created_at);
            """)
            
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            raise Exception(f"Failed to initialize tables: {str(e)}")
        finally:
            if conn:
                self.release_connection(conn)
    
    def save_chat_message(self, session_id: str, user_id: str, message: Dict[str, Any]) -> int:
        """保存聊天消息到数据库
        
        Args:
            session_id: 会话ID
            user_id: 用户ID
            message: 聊天消息内容，将以JSONB格式存储
            
        Returns:
            插入记录的ID
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 插入聊天消息
            cursor.execute("""
                INSERT INTO chat_history (session_id, user_id, message)
                VALUES (%s, %s, %s)
                RETURNING id;
            """, (session_id, user_id, Json(message)))
            
            record_id = cursor.fetchone()[0]
            conn.commit()
            return record_id
        except Exception as e:
            if conn:
                conn.rollback()
            raise Exception(f"Failed to save chat message: {str(e)}")
        finally:
            if conn:
                self.release_connection(conn)
    
    def get_chat_history(self, session_id: str, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """获取指定会话的聊天历史
        
        Args:
            session_id: 会话ID
            limit: 返回记录数限制
            offset: 偏移量
            
        Returns:
            聊天历史记录列表
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # 查询聊天历史
            # cursor.execute("""
            #     SELECT id, session_id, user_id, message, created_at, updated_at
            #     FROM chat_history
            #     WHERE session_id = %s
            #     ORDER BY created_at ASC
            #     LIMIT %s OFFSET %s;
            # """, (session_id, limit, offset))
            # 查询聊天历史
            cursor.execute("""
                            SELECT id, message
                            FROM chat_history
                            WHERE session_id = %s
                            ORDER BY created_at ASC
                            LIMIT %s OFFSET %s;
                        """, (session_id, limit, offset))

            results = cursor.fetchall()
            return results
        except Exception as e:
            raise Exception(f"Failed to get chat history: {str(e)}")
        finally:
            if conn:
                self.release_connection(conn)
    
    def get_chat_history_by_user(self, user_id: str, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """获取指定用户的所有聊天历史
        
        Args:
            user_id: 用户ID
            limit: 返回记录数限制
            offset: 偏移量
            
        Returns:
            聊天历史记录列表
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # 查询用户的所有聊天历史
            cursor.execute("""
                SELECT id, session_id, user_id, message, created_at, updated_at
                FROM chat_history
                WHERE user_id = %s
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s;
            """, (user_id, limit, offset))
            
            results = cursor.fetchall()
            return results
        except Exception as e:
            raise Exception(f"Failed to get user chat history: {str(e)}")
        finally:
            if conn:
                self.release_connection(conn)
    
    def update_chat_message(self, message_id: int, message: Dict[str, Any]) -> int:
        """更新聊天消息
        
        Args:
            message_id: 消息ID
            message: 更新后的消息内容
            
        Returns:
            更新的记录数
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 更新聊天消息
            cursor.execute("""
                UPDATE chat_history
                SET message = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s;
            """, (Json(message), message_id))
            
            affected_rows = cursor.rowcount
            conn.commit()
            return affected_rows
        except Exception as e:
            if conn:
                conn.rollback()
            raise Exception(f"Failed to update chat message: {str(e)}")
        finally:
            if conn:
                self.release_connection(conn)
    
    def delete_chat_message(self, message_id: int) -> int:
        """删除聊天消息
        
        Args:
            message_id: 消息ID
            
        Returns:
            删除的记录数
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 删除聊天消息
            cursor.execute("DELETE FROM chat_history WHERE id = %s;", (message_id,))
            
            affected_rows = cursor.rowcount
            conn.commit()
            return affected_rows
        except Exception as e:
            if conn:
                conn.rollback()
            raise Exception(f"Failed to delete chat message: {str(e)}")
        finally:
            if conn:
                self.release_connection(conn)
    
    def delete_chat_history(self, session_id: str) -> int:
        """删除指定会话的所有聊天历史
        
        Args:
            session_id: 会话ID
            
        Returns:
            删除的记录数
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 删除会话的所有聊天历史
            cursor.execute("DELETE FROM chat_history WHERE session_id = %s;", (session_id,))
            
            affected_rows = cursor.rowcount
            conn.commit()
            return affected_rows
        except Exception as e:
            if conn:
                conn.rollback()
            raise Exception(f"Failed to delete chat history: {str(e)}")
        finally:
            if conn:
                self.release_connection(conn)
    
    def count_chat_messages(self, session_id: str) -> int:
        """统计指定会话的消息数量
        
        Args:
            session_id: 会话ID
            
        Returns:
            消息数量
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 统计消息数量
            cursor.execute("SELECT COUNT(*) FROM chat_history WHERE session_id = %s;", (session_id,))
            count = cursor.fetchone()[0]
            return count
        except Exception as e:
            raise Exception(f"Failed to count chat messages: {str(e)}")
        finally:
            if conn:
                self.release_connection(conn)
    
    def close(self) -> None:
        """关闭连接池"""
        if self.connection_pool:
            self.connection_pool.closeall()
