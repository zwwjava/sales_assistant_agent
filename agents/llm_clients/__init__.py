from .llms import get_llm
# 加载配置信息
from dotenv import load_dotenv
load_dotenv("D:/.env-dev")

llm, llm_embedding = get_llm("qwen")