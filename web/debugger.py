# Author：zww
# Date ：2026/3/26 14:57
# DESCRIPTION：.
# Author：zww
# Date ：2026/3/26 14:47
# DESCRIPTION：.
from agents.common.common_agent_state import CommonAgentState
from workflow.agent2b_workflow import Agents2BWorkflow
# 从当前包中导入 LoggerManager，用于获取日志记录器实例以输出运行和调试信息
from utils.logger import LoggerManager
# 获取全局日志实例，用于在工具加载和调用过程中记录日志
logger = LoggerManager.get_logger()

# 问答处理函数
def process_question(question: str) -> str:
    """处理用户问题的核心逻辑
    这里可以替换为实际的问答逻辑，例如调用大模型或知识库查询
    Args:
        question: 用户提出的问题
    Returns:
        机器人的回答
    """
    state = CommonAgentState({
        "message": "你好",
    })
    graph_builder = Agents2BWorkflow(CommonAgentState)
    agent = graph_builder.compile()

    # 生成状态图
    # try:
    #     with open("agent_diagram.png", "wb") as f:
    #         f.write(graph.get_graph().draw_mermaid_png())
    #     print("graph build done")
    # except Exception as e:
    #     print(f"graph draw failed, {e}")

    state_end = agent.invoke(state)
    logger.info("workflow结束")
    logger.info(state_end)
    return state_end

process_question("你好")