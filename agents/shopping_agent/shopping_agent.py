# Author：zww
# Date ：2026/4/8 16:30
# DESCRIPTION：.导购智能体

# 从 LangChain 导入 create_agent 方法，用于创建智能体（Agent）
from langchain.agents import create_agent
# 从 langchain_core.prompts 模块中导入
# PromptTemplate 用于构建单条文本提示模板,通过占位符+format 的方式动态生成提示词
# ChatPromptTemplate 用于构建多轮对话风格的提示模板,支持 system/human 等多种角色消息组合
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
# 从 LangGraph 导入内存检查点存储器，用于短期记忆与会话状态持久化
from langgraph.checkpoint.memory import InMemorySaver
# 从 LangChain 导入 ToolStrategy，用于指定代理使用“工具调用”的结构化输出格式
from langchain.agents.structured_output import ToolStrategy
from agents.llm_clients import llm
# 从当前包中导入 LoggerManager，用于获取日志记录器实例以输出运行和调试信息
from agents.common.utils.logger import LoggerManager
from agents.shopping_agent.utils.models import Context, ResponseFormat
import orjson

from agents.shopping_agent.utils.tools import get_tools

# 获取全局日志实例，用于在工具加载和调用过程中记录日志
logger = LoggerManager.get_logger()

from pathlib import Path
current_dir = Path(__file__).resolve().parent


# 获取当前智能体可用的工具列表
tools = get_tools()

async def invoke_shopping_agent(message: str):

    # tools = [
    #     get_fundamentals,
    #     get_balance_sheet,
    #     get_cashflow,
    #     get_income_statement,
    # ]

    system_prompt = PromptTemplate.from_file(
        template_file=str(current_dir) + "/prompts/system_prompt.md",
        encoding="utf-8"
    )
    # 替换提示词中的占位符
    # system_prompt = system_prompt.format_messages(question=raw_question, name=name)
    # 直接转字符串
    system_prompt = system_prompt.template

    agent_message = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message}
    ]

    agent = create_agent(
        model=llm,
        system_prompt=system_prompt,
        # tools=tools,
        context_schema=Context,
        response_format=ToolStrategy(ResponseFormat)
    )

    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": message}]},
        context=Context(user_id="1")
    )

    logger.info("shopping_node输出")
    logger.info(response)
    result = str(response.get("structured_response"))
    return result

# if __name__ == "__main__":
#     invoke_shopping_agent("衣服")
