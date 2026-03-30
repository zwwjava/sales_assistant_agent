from langchain_core.prompts import PromptTemplate

from agents.common.common_agent_state import CommonAgentState
from agents.common.logs import log_node
from agents.llm_clients import llm
# 从当前包中导入 LoggerManager，用于获取日志记录器实例以输出运行和调试信息
from agents.common.utils.logger import LoggerManager
# 获取全局日志实例，用于在工具加载和调用过程中记录日志
logger = LoggerManager.get_logger()

from pathlib import Path
current_dir = Path(__file__).resolve().parent

def create_main_cognition_agent():
    """
    意图识别
    :return:
    """

    @log_node()
    def main_cognition_node(state: CommonAgentState):
        """
        主路由的意图识别
        :param state:
        :return:
        """
        message = state["message"]

        system_prompt = PromptTemplate.from_file(
            template_file=str(current_dir) + "/prompts/system_main_cognition.md",
            encoding="utf-8"
        ).template

        agent_message = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]

        result = llm.invoke(agent_message)

        logger.info("main_cognition输出")
        logger.info(result)

        if len(result.tool_calls) == 0:
            result = result.content

        return {
            "cognition": result
        }

    return main_cognition_node
