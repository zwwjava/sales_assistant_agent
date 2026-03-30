# Author：zww
# Date ：2026/3/27 17:37
# DESCRIPTION：.
# Author：zww
# Date ：2026/3/25 16:21
# DESCRIPTION：.主体工作流

from langgraph.graph import StateGraph, START, END

from agents.main_router_agent.agents.history_agent.history_agent import create_history_agent
from agents.main_router_agent.agents.input_check_agent.input_check_agent import create_input_check_agent
from agents.main_router_agent.agents.main_cognition_agent.main_cognition_agent import create_main_cognition_agent


class MainRouterWorkflow(StateGraph):
    """Main class that orchestrates the trading agents framework."""

    def __init__(
        self,
        state
    ):
        super().__init__(state)

        # tools = [
        #     输入安全 + 输入重组,
        #     输入模态对齐,
        #     情绪识别 + 对话意图识别,
        #     短期记忆
        #     用户画像
        # ]

        # 短期记忆
        history_agent = create_history_agent()
        
        # 输入安全 + 输入重组
        input_check_agent = create_input_check_agent()

        # 模态对齐 TODO

        # 情绪识别 + 对话意图识别
        main_cognition_agent = create_main_cognition_agent()

        # 用户画像 TODO

        # 登记节点
        # 输入安全 + 输入重组
        self.add_node("input_check", input_check_agent)
        # 情绪识别 + 对话意图识别
        self.add_node("main_cognition", main_cognition_agent)
        # 短期记忆
        self.add_node("history_agent", history_agent)

        # 登记边
        self.add_edge(START, "history_agent")
        self.add_edge("history_agent", "input_check")
        self.add_edge("input_check", "main_cognition")
        self.add_edge("main_cognition", END)




