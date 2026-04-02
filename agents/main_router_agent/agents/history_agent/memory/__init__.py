
import os
from typing import Optional

from agents.main_router_agent.agents.history_agent.memory.postgresql_client import PostgreSQLClient

# PostgreSQL配置
POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DATABASE: str = os.getenv("POSTGRES_DATABASE", "wwbot")
POSTGRES_USERNAME: str = os.getenv("POSTGRES_USERNAME", "postgres")
POSTGRES_PASSWORD: Optional[str] = os.getenv("POSTGRES_PASSWORD")
POSTGRES_MIN_CONN: int = int(os.getenv("POSTGRES_MIN_CONN", "1"))
POSTGRES_MAX_CONN: int = int(os.getenv("POSTGRES_MAX_CONN", "10"))

# 初始化PostgreSQL中间件
pg_client = PostgreSQLClient(
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    database=POSTGRES_DATABASE,
    username=POSTGRES_USERNAME,
    password=POSTGRES_PASSWORD,
    min_conn=POSTGRES_MIN_CONN,
    max_conn=POSTGRES_MAX_CONN
)
