from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from agents.llm_clients import llm

# 从当前包中导入 LoggerManager，用于获取日志记录器实例以输出运行和调试信息
from utils.logger import LoggerManager
# 获取全局日志实例，用于在工具加载和调用过程中记录日志
logger = LoggerManager.get_logger()

def create_chat_agent():
    def chat_node(state):
        message = state["message"]

        # tools = [
        #     get_fundamentals,
        #     get_balance_sheet,
        #     get_cashflow,
        #     get_income_statement,
        # ]

        system_prompt = f"""
        你是电商客服，高情商聊天机器人。
        职责：
        - 购物咨询：热情推荐，耐心解答
        - 售后问题：先安抚情绪，再高效解决
        - 转人工：礼貌确认，顺畅交接
        
        回复风格：温暖、专业、有耐心，让用户感到被重视。
        """

        agent_message = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
        result = llm.invoke(agent_message)

        logger.info("chat_agent输出")
        logger.info(result)

        if len(result.tool_calls) == 0:
            result = result.content

        return {
            "messages": [result],
        }

    return chat_node
