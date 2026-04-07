from typing import Optional, Dict, Any, List
import orjson
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate

from agents.common.common_agent_state import CommonAgentState
from agents.common.logs import log_node
from agents.llm_clients import llm
from agents.main_router_agent.agents.history_agent.memory import pg_client

# 从当前包中导入 LoggerManager，用于获取日志记录器实例以输出运行和调试信息
from agents.common.utils.logger import LoggerManager

# 获取全局日志实例，用于在工具加载和调用过程中记录日志
logger = LoggerManager.get_logger()

def save_history(state: CommonAgentState):
    message = state.get("message")
    history = state.get("history")
    session_id = state.get("session_id")
    response = state.get("response")

    if history:
        pg_client.update_chat_message(session_id, history)
    else:
        pg_client.save_chat_message(session_id, response)

def create_history_agent():
    """
    历史对话
    :return:
    """
    def post_process(history: List[Dict[str, Any]]):
        """后处理，解析json之类的处理"""
        if history:
            result = orjson.dumps(history).decode("utf-8")
            return result
        return None

    @log_node()
    def history_node(state: CommonAgentState):
        user_id = state.get("user_id")
        session_id = state.get("session_id")
        message = state.get("message")

        # 方案一。从redis中取对话记录

        # 方案二。如果实际业务需要持久化就从PostgreSql
        history = pg_client.get_chat_history(session_id)
        history = post_process(history)

        logger.info("history_agent输出")
        logger.info(history)

        return {
            "history": history,
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

