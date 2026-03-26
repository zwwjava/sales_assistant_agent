# Author：zww
# Date ：2026/3/26 9:33
# DESCRIPTION：.

from agents.common.common_agent_state import CommonAgentState
from .dict import AgentNodeType
from langgraph.graph import END

def main_router_cognition(state: CommonAgentState):
    """
    路由节点，根据意图识别结果进行路由，
    """
    route = AgentNodeType.CHAT_AGENT

    # TODO 根据state中的信息确定跳转的node

    return route

def main_router_node_list():
    # {
    #     "Conservative Analyst": "Conservative Analyst",
    #     "Risk Judge": "Risk Judge",
    # }
    cognition_map = {
        AgentNodeType.CHAT_AGENT: AgentNodeType.CHAT_AGENT,
        AgentNodeType.TO_HUMAN_AGENT: AgentNodeType.TO_HUMAN_AGENT,
        AgentNodeType.SHOPPING_AGENT: AgentNodeType.SHOPPING_AGENT,
        AgentNodeType.AFTER_SALES_AGENT: AgentNodeType.AFTER_SALES_AGENT,
        # "end": END,
    }
    return cognition_map
    # return list(set(cognition_map.values()))
