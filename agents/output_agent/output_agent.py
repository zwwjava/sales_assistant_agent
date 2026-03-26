from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from agents.common.common_agent_state import CommonAgentState
from agents.llm_clients import llm

# 从当前包中导入 LoggerManager，用于获取日志记录器实例以输出运行和调试信息
from utils.logger import LoggerManager
# 获取全局日志实例，用于在工具加载和调用过程中记录日志
logger = LoggerManager.get_logger()

def create_output_agent():
    def output_node(state: CommonAgentState):
        # print(state)
        message = state["messages"][-1]
        # print(message)

        # tools = [
        #     get_fundamentals,
        #     get_balance_sheet,
        #     get_cashflow,
        #     get_income_statement,
        # ]

        # 待补充功能，输出合法检查，多模态对齐。。。
        system_prompt = f"""
                你是一个输出校验专家，将用户的输出满足格式要求：严格 JSON，不允许添加额外内容。
                
                字段说明：
                - code：状态码（0成功，-1失败）
                - response：提示信息
                
                示例：
                {{
                  "code": 0,
                  "response": "很高兴见到您"
                }}
                """

        # agent_message = [
        #     {"role": "system", "content": system_prompt},
        #     {"role": "user", "content": message}
        # ]
        # result = llm.invoke(agent_message)

        # print("output_agent输出")
        # print(result)

        # if len(result.tool_calls) == 0:
        #     result = result.content

        return {
            "response": message,
        }

    return output_node
