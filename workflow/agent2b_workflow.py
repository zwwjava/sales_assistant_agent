# Author：zww
# Date ：2026/3/25 16:21
# DESCRIPTION：.主体工作流

from langgraph.graph import StateGraph, START, END

from agents.after_sales_agent.after_sales_agent import create_after_sales_agent
from agents.chat_agent.chat_agent import create_chat_agent
from agents.main_router_agent.main_router_agent import create_main_router_agent
from agents.output_agent.output_agent import create_output_agent
from agents.shopping_agent.shopping_agent import create_shopping_agent
from agents.to_human_agent.to_human_agent import create_to_human_agent
from .dict import AgentNodeType
from workflow.conditional_logic import main_router_cognition, main_router_node_list


class Agents2BWorkflow(StateGraph):
    """Main class that orchestrates the trading agents framework."""

    def __init__(
        self,
        state
    ):
        super().__init__(state)
        main_router = create_main_router_agent()

        chat_agent = create_chat_agent()

        output_agent = create_output_agent()

        to_human_agent = create_to_human_agent()

        shopping_agent = create_shopping_agent()

        after_sales_agent = create_after_sales_agent()

        # 登记节点
        # 主路由结点
        self.add_node(AgentNodeType.MAIN_ROUTER, main_router)
        # 简单聊天智能体
        self.add_node(AgentNodeType.CHAT_AGENT, chat_agent)
        # 转人工智能体
        self.add_node(AgentNodeType.TO_HUMAN_AGENT, to_human_agent)
        # 导购智能体
        self.add_node(AgentNodeType.SHOPPING_AGENT, shopping_agent)
        # 售后智能体
        self.add_node(AgentNodeType.AFTER_SALES_AGENT, after_sales_agent)
        # 输出智能体
        self.add_node(AgentNodeType.OUTPUT_AGENT, output_agent)

        # 登记入口
        self.add_edge(START, AgentNodeType.MAIN_ROUTER)


        # （聊天，购物，售后，人工，结束...）
        # self.add_edge(AgentNodeType.MAIN_ROUTER, AgentNodeType.CHAT_AGENT)
        self.add_conditional_edges(AgentNodeType.MAIN_ROUTER, main_router_cognition, main_router_node_list())
        # 聊天结束
        self.add_edge(AgentNodeType.CHAT_AGENT, AgentNodeType.OUTPUT_AGENT)
        # 购物结束
        self.add_edge(AgentNodeType.SHOPPING_AGENT, AgentNodeType.OUTPUT_AGENT)
        # 售后结束
        self.add_edge(AgentNodeType.AFTER_SALES_AGENT, AgentNodeType.OUTPUT_AGENT)

        # 输出
        self.add_edge(AgentNodeType.OUTPUT_AGENT, END)



