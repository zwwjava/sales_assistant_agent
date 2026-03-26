from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uvicorn
import datetime

from agents.common.common_agent_state import CommonAgentState
from workflow.agent2b_workflow import Agents2BWorkflow

# 创建FastAPI应用
app = FastAPI(title="WWBot 导购机器人 API", version="1.0.0")

# 定义数据模型
class QuestionRequest(BaseModel):
    """用户问题请求模型"""
    user_id: str
    question: str
    session_id: str
    context: Optional[Dict[str, Any]] = None

class AnswerResponse(BaseModel):
    """机器人回答响应模型"""
    # session_id: str
    answer: str
    status: str
    confidence: float
    metadata: Optional[Dict[str, Any]] = None

# 问答处理函数
async def process_question(question: str) -> str:
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
    try:
        graph_builder = Agents2BWorkflow(CommonAgentState)
        graph = graph_builder.compile()

        # 生成状态图
        # try:
        #     with open("agent_diagram.png", "wb") as f:
        #         f.write(graph.get_graph().draw_mermaid_png())
        #     print("graph build done")
        # except Exception as e:
        #     print(f"graph draw failed, {e}")

        state_end = await graph.ainvoke(state)
        # print(state_end["response"].content)
        return state_end["response"].content
    except Exception as e:
        print(e)
    finally:
        # ------- 用于output.log输出，记录输入输出记录 -------------------
        pass


# 定义API路由
@app.post("/v1/chat", response_model=AnswerResponse)
def chat(request: QuestionRequest):
    """问答接口，处理用户问题"""
    try:
        # 处理用户问题
        answer = process_question(request.question)

        # 构建响应
        response = AnswerResponse(
            session_id=request.session_id,
            answer=answer,
            status="success",
            confidence=0.85,
            metadata={
                "user_id": request.user_id,
                "timestamp": datetime.datetime.now().isoformat(),
                "question": request.question
            }
        )

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理问题时发生错误: {str(e)}")


# 定义API路由
@app.get("/v1/chat/{message}", response_model=AnswerResponse)
async def chat(message: str):
    """问答接口，处理用户问题"""
    try:
        # 处理用户问题
        answer = await process_question(message)
        # answer = process_question(message)

        # 构建响应
        response = AnswerResponse(
            answer=answer,
            status="success",
            confidence=0.85,
            metadata={
                "timestamp": datetime.datetime.now().isoformat(),
            }
        )

        return response
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"处理问题时发生错误: {str(e)}")

@app.get("/health")
def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "service": "WWBot Q&A Robot",
        "version": "1.0.0",
        "timestamp": datetime.datetime.now().isoformat()
    }

@app.get("/status")
def status_check():
    """状态检查接口"""
    return {
        "status": "running",
        "service": "WWBot Q&A Robot API",
        "version": "1.0.0",
        "endpoints": {
            "ask": "/api/v1/ask (POST)",
            "health": "/health (GET)",
            "status": "/status (GET)"
        }
    }

if __name__ == "__main__":
    uvicorn.run("web.main:app", host="0.0.0.0", port=8000)
