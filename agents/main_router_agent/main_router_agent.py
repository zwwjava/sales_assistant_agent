from langchain_core.prompts import PromptTemplate

from agents.common.common_agent_state import CommonAgentState
from agents.common.logs import log_node
from agents.llm_clients import llm
# 从当前包中导入 LoggerManager，用于获取日志记录器实例以输出运行和调试信息
from agents.common.utils.logger import LoggerManager
from agents.main_router_agent.main_router_workflow import MainRouterWorkflow

# 获取全局日志实例，用于在工具加载和调用过程中记录日志
logger = LoggerManager.get_logger()

from pathlib import Path
current_dir = Path(__file__).resolve().parent


def create_main_router_agent():

    graph_builder = MainRouterWorkflow(CommonAgentState)
    main_router_agent = graph_builder.compile()

    def print_graph_img(main_router_agent):
        # 生成状态图
        try:
            with open("main_router_agent_diagram.png", "wb") as f:
                f.write(main_router_agent.get_graph().draw_mermaid_png())
            print("graph build done")
        except Exception as e:
            print(f"graph draw failed, {e}")

    # 工作流
    # print_graph_img(main_router_agent)

    @log_node()
    def main_router_node(state: CommonAgentState):
        """
        主路由结点（该节点还是一个子工作流）
        :param state:
        :return:
        """

        # message = state["message"]

        # TODO 待完善的功能
        # tools = [
        #     输入安全 + 输入重组,
        #     输入模态对齐,
        #     情绪识别,
        #     对话意图识别,
        #     短期记忆
        # ]

        # 方案1 编码workflow到外部工作流
        main_router_agent.invoke(state)

        # 方案2 http调用
        # http 远程调用
        # main_router_node_http(state)

    return main_router_node
