-- PostgreSQL数据库初始化脚本
-- 用途：创建数据库、表结构、索引和示例数据

-- 1. 创建数据库
CREATE DATABASE IF NOT EXISTS agent2b
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TEMPLATE = template0
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

-- 连接到新创建的数据库
\c agent2b;

-- 2. 创建聊天历史表
CREATE TABLE IF NOT EXISTS chat_history (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    message JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. 创建索引
-- 会话ID索引
CREATE INDEX IF NOT EXISTS idx_chat_history_session_id ON chat_history(session_id);

-- 用户ID索引
CREATE INDEX IF NOT EXISTS idx_chat_history_user_id ON chat_history(user_id);

-- 创建时间索引
-- CREATE INDEX IF NOT EXISTS idx_chat_history_created_at ON chat_history(created_at);

-- JSONB字段的GIN索引，用于高效查询JSONB字段内的键
CREATE INDEX IF NOT EXISTS idx_chat_history_message ON chat_history USING GIN(message);

-- JSONB字段特定键的索引，用于经常查询的字段
-- CREATE INDEX IF NOT EXISTS idx_chat_history_message_type ON chat_history ((message->>'type'));
-- CREATE INDEX IF NOT EXISTS idx_chat_history_message_timestamp ON chat_history ((message->>'timestamp'));

-- 4. 插入示例数据
INSERT INTO chat_history (session_id, user_id, message) VALUES
-- 会话1：用户询问电子产品
('session_001', 'user_123', '{
    "type": "user",
    "content": "你好，我想买一台手机，有什么推荐吗？",
    "timestamp": "2026-04-01T09:00:00"
}'),
('session_001', 'user_123', '{
    "type": "bot",
    "content": "您好！请问您预算大概是多少？对品牌有偏好吗？",
    "timestamp": "2026-04-01T09:00:05",
    "confidence": 0.9
}'),
('session_001', 'user_123', '{
    "type": "user",
    "content": "预算5000左右，想要拍照好的手机",
    "timestamp": "2026-04-01T09:00:15",
    "context": {"preference": "photography", "budget": 5000}
}'),
('session_001', 'user_123', '{
    "type": "bot",
    "content": "推荐您考虑品牌X的Pro系列，拍照性能非常出色！",
    "timestamp": "2026-04-01T09:00:20",
    "confidence": 0.85,
    "recommended_products": ["product_001", "product_002"]
}'),

-- 会话2：用户询问服装
('session_002', 'user_456', '{
    "type": "user",
    "content": "我需要一件正式场合穿的衬衫",
    "timestamp": "2026-04-01T10:30:00"
}'),
('session_002', 'user_456', '{
    "type": "bot",
    "content": "好的，请问您喜欢什么颜色？尺码是多少？",
    "timestamp": "2026-04-01T10:30:05",
    "confidence": 0.92
}'),
('session_002', 'user_456', '{
    "type": "user",
    "content": "蓝色，L码，最好是纯棉的",
    "timestamp": "2026-04-01T10:30:15",
    "context": {"color": "blue", "size": "L", "material": "cotton"}
}'),

-- 会话3：用户询问家居用品
('session_003', 'user_789', '{
    "type": "user",
    "content": "我正在装修客厅，想买一张沙发",
    "timestamp": "2026-04-01T14:00:00"
}'),
('session_003', 'user_789', '{
    "type": "bot",
    "content": "太好了！我们有多种款式的沙发，请问您喜欢什么风格的？",
    "timestamp": "2026-04-01T14:00:05",
    "confidence": 0.88
}'),
('session_003', 'user_789', '{
    "type": "user",
    "content": "现代简约风格，三人座的",
    "timestamp": "2026-04-01T14:00:15",
    "context": {"style": "modern", "size": "three-seater"}
}'),

-- 会话4：用户询问家具
('session_004', 'user_101', '{
    "type": "user",
    "content": "你们有实木餐桌吗？",
    "timestamp": "2026-04-01T16:45:00"
}'),
('session_004', 'user_101', '{
    "type": "bot",
    "content": "有的！我们有橡木、胡桃木、樱桃木等多种材质的实木餐桌。",
    "timestamp": "2026-04-01T16:45:05",
    "confidence": 0.95
}');

-- 5. 创建更新时间触发器函数
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 6. 创建更新时间触发器
CREATE TRIGGER update_chat_history_updated_at 
    BEFORE UPDATE ON chat_history 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 7. 查询验证
SELECT 
    id,
    session_id,
    user_id,
    message->>'type' as message_type,
    message->>'content' as content,
    created_at
FROM chat_history
ORDER BY created_at;

-- 显示统计信息
SELECT 
    session_id,
    COUNT(*) as message_count,
    MIN(created_at) as first_message,
    MAX(created_at) as last_message
FROM chat_history
GROUP BY session_id
ORDER BY first_message;

-- 显示用户统计
SELECT 
    user_id,
    COUNT(DISTINCT session_id) as session_count,
    COUNT(*) as total_messages
FROM chat_history
GROUP BY user_id;
