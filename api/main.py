import sys
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional

# Fix encoding cho Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Thêm root directory vào path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from agent.agent_handle import ask

# ============ FASTAPI APP ============
app = FastAPI(
    title="Finance Agent API",
    description="API trợ lý tài chính cho thị trường chứng khoán Việt Nam",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Có thể giới hạn origins cụ thể
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ REQUEST/RESPONSE MODELS ============
class QueryRequest(BaseModel):
    query: str = Field(..., description="Câu hỏi tiếng Việt của người dùng")

class QueryResponse(BaseModel):
    answer: str = Field(..., description="Câu trả lời từ agent")

# ============ API ENDPOINTS ============
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "Finance Agent API"
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/query", response_model=QueryResponse)
async def query_agent(request: QueryRequest):
    """
    Endpoint chính để gửi câu hỏi cho agent.
    
    - **query**: Câu hỏi tiếng Việt của người dùng
    
    Returns:
    - **answer**: Câu trả lời từ agent
    """
    try:
        # Gọi agent với câu hỏi
        answer = ask(request.query)
        
        if answer is None:
            raise HTTPException(
                status_code=500,
                detail="Agent không trả về kết quả"
            )
        
        return QueryResponse(answer=answer)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi khi xử lý câu hỏi: {str(e)}"
        )

# ============ RUN SERVER ============
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)