from typing import Optional, Dict, Any, List
import json
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate

from agents.common.common_agent_state import CommonAgentState
from agents.common.logs import log_node
from agents.llm_clients import llm
from memory import pg_client

# 从当前包中导入 LoggerManager，用于获取日志记录器实例以输出运行和调试信息
from agents.common.utils.logger import LoggerManager

# 获取全局日志实例，用于在工具加载和调用过程中记录日志
logger = LoggerManager.get_logger()

def create_history_agent():
    """
    历史对话
    :return:
    """
    def post_process(history: List[Dict[str, Any]]):
        """后处理，解析json之类的处理"""
        if history:
            result = json.dumps(history, ensure_ascii=False, indent=2)
            return result
        return ""

    @log_node()
    def history_node(state: CommonAgentState):
        user_id = state["user_id"]
        session_id = state["session_id"]
        message = state["message"]

        # 方案一。从redis中取对话记录

        # 方案二。如果实际业务需要持久化就从PostgreSql
        history = pg_client.get_chat_history(session_id)

        logger.info("history_agent输出")
        logger.info(history)

        return {
            "history": post_process(history),
        }

    return history_node

if __name__ == "__main__":
    state = CommonAgentState({
        "message": "你好",
        "user_id": "user_123",
        "session_id": "session_001"
    })
    history = create_history_agent()(state)
    print(history)

