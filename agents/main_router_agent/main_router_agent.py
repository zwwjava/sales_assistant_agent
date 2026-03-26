from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from agents.common.common_agent_state import CommonAgentState
from agents.llm_clients import llm
# 从当前包中导入 LoggerManager，用于获取日志记录器实例以输出运行和调试信息
from utils.logger import LoggerManager
# 获取全局日志实例，用于在工具加载和调用过程中记录日志
logger = LoggerManager.get_logger()

def create_main_router_agent():

    def main_router_node(state: CommonAgentState):
        message = state["message"]

        # TODO 待完善的功能
        # tools = [
        #     输入安全,
        #     输入模态对齐,
        #     输入重组,
        #     情绪识别,
        #     对话意图识别,
        #     短期记忆
        # ]

        system_prompt = f"""你是一个情绪识别和意图识别专家。
        请分析用户输入，识别用户的**情绪分数**和**意图**。
        情绪分数使用 -1 到 1 的数值：
        - 1：非常正面（极度高兴、兴奋、满意）
        - 0.5：正面（开心、满意、感谢）
        - 0：中性（无情绪波动、陈述事实）
        - -0.5：负面（不满、失望、抱怨）
        - -1：非常负面（愤怒、投诉、威胁）
        意图可选范围：
        - chat_agent：简单聊天智能体（日常聊天、问候、闲聊）
        - to_human_agent：转人工（投诉、不满、需要人工处理）
        - shopping_agent：购物（商品咨询、购买、推荐）
        - after_sales_agent：售后（退换货、维修、退款、投诉）
        
        请以 JSON 格式输出，包含以下字段：
        - sentiment_score：情绪分数（-1 到 1 之间的浮点数）
        - intent：识别出的意图（从上述范围中选择）
        - reason：判断理由（简要说明）
        示例输出：
        {{
          "sentiment_score": "-0.8",
          "intent": "to_human_agent",
          "reason": "用户情绪非常负面，明确要求转人工"
        }}
        """

        agent_message = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]

        result = llm.invoke(agent_message)

        logger.info("main_router输出")
        logger.info(result)

        if len(result.tool_calls) == 0:
            result = result.content

        return {
            "messages": [result],
            "history": "user:lalala\n system:nihao",
            "cognition": "chat",
            # "cognition": "shopping",
            "emotion": 0.5, # 情绪分数
        }

    return main_router_node
