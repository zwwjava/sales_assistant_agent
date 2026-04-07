import orjson
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate

from agents.common.common_agent_state import CommonAgentState
from agents.llm_clients import llm
# 从当前包中导入 LoggerManager，用于获取日志记录器实例以输出运行和调试信息
from agents.common.utils.logger import LoggerManager
# 获取全局日志实例，用于在工具加载和调用过程中记录日志
logger = LoggerManager.get_logger()

from pathlib import Path
current_dir = Path(__file__).resolve().parent

def create_shopping_agent():
    """
    购物智能体。
    v1:大模型随便返回一个相关的信息。
    v2:【工作流方案】先分析将用户请求分成1个或多个指定商品列表，异步请求单品导购，结果汇总。（智能体方案则先规划，再执行）
    v3:单品导购开发。涉及到推荐算法和检索库内容，（1.用户问题转商品关键词；2.商品关键词调用检索服务）
    :return:
    """
    def shopping_node(state: CommonAgentState):
        message = state["message"]

        # tools = [
        #     get_fundamentals,
        #     get_balance_sheet,
        #     get_cashflow,
        #     get_income_statement,
        # ]

        system_prompt = PromptTemplate.from_file(
            template_file=str(current_dir) + "/prompts/system_prompt.md",
            encoding="utf-8"
        ).template

        agent_message = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]

        result = llm.invoke(agent_message)

        logger.info("shopping_node输出")
        logger.info(result)

        result = orjson.loads(result.content)
        return {
            "recommendation": result
        }

    return shopping_node
