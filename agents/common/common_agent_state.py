# Author：zww
# Date ：2026/3/25 16:07
# DESCRIPTION：.通用的智能体上下文

from langgraph.graph import MessagesState
from typing import TypedDict, List, Annotated, Any


class ConversationHistory(TypedDict):
    request_msg: Annotated[str, "提问信息"]
    response_msg: Annotated[str, "回答信息"]

class CommonAgentState(MessagesState):
    user_id: Annotated[str, "发起对话人的id"]
    session_id: Annotated[str, "整个会话id"]
    conversation_id: Annotated[str, "本次提问id"]
    history: Annotated[List[Any], "聊天历史"]
    message: Annotated[str, "本次提问内容"]
    response: Annotated[str, "最终返回"]
    input_illegal: bool = True
    cognition: Annotated[str, "主识别意图"]

