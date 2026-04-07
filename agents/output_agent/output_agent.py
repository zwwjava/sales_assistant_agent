from agents.common.common_agent_state import CommonAgentState
from agents.common.logs import log_node

# 从当前包中导入 LoggerManager，用于获取日志记录器实例以输出运行和调试信息
from agents.common.utils.logger import LoggerManager
# 获取全局日志实例，用于在工具加载和调用过程中记录日志
logger = LoggerManager.get_logger()

from pathlib import Path
current_dir = Path(__file__).resolve().parent

def create_output_agent():

    @log_node()
    def output_node(state: CommonAgentState):
        # print(state)

        recommendation = state["recommendation"]
        response = state.get("response")
        # print(message)

        # 待补充功能，输出合法检查，多模态对齐。。。
        # tools = [
        #     get_fundamentals,
        #     get_balance_sheet,
        #     get_cashflow,
        #     get_income_statement,
        # ]

        # 保存历史对话。调用历史记录服务接口（或者工作流增加结点）
        # 临时调用hsitory_agent提供的函数


        if recommendation:
            response = recommendation
        response = {
            "code": 0,
            "response": response,
        }

        return {
            "response": response,
        }

    return output_node
