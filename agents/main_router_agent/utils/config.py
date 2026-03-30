# 导入操作系统模块，用于处理文件路径、环境变量等与操作系统相关的功能
import os

# 定义一个统一配置类，用于集中管理项目中的所有常量配置
class Config:

    # Milvus数据库相关参数
    MILVUS_URI = "http://localhost:19530"
    MILVUS_DB_NAME = "milvus_database"
    MILVUS_COLLECTION_NAME = "my_collection_demo_chunked"

    # MCP Server服务器参数
    MCP_SERVER_HOST = "127.0.0.1"
    MCP_SERVER_PORT = 8010
