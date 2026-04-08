# 从 dataclasses 模块导入 dataclass 装饰器，用于简化数据类的定义
from dataclasses import dataclass


# 使用 @dataclass 定义运行时上下文数据模型，用于在 Agent/工具执行时传递用户相关信息
@dataclass
class Context:
    # 表示用户唯一标识，用于在会话、工具调用等场景中区分不同用户
    user_id: str

# 使用 @dataclass 定义 Agent 的结构化响应数据模型
@dataclass
class ResponseFormat:
    product_name: str
    brand: str
    price: str
    reason: str
    description: str
