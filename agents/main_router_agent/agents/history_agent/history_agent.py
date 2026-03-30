from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate

from agents.common.common_agent_state import CommonAgentState
from agents.common.logs import log_node

from agents.llm_clients import llm

# 从当前包中导入 LoggerManager，用于获取日志记录器实例以输出运行和调试信息
from agents.common.utils.logger import LoggerManager
# 获取全局日志实例，用于在工具加载和调用过程中记录日志
logger = LoggerManager.get_logger()

from pathlib import Path
current_dir = Path(__file__).resolve().parent

def create_history_agent():
    """
    历史对话
    :return:
    """
    def post_process(str):
        """后处理，解析json之类的处理"""
        return ""

    @log_node()
    def history_node(state: CommonAgentState):
        # user_id = state["user_id"]
        # session_id = state["session_id"]

        # 基于user_id + session_id 从redis中取对话记录
        result = ""

        logger.info("history_agent输出")
        logger.info(result)

        return {
            "history": post_process(result),
        }

    return history_node
