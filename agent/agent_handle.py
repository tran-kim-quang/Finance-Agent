import sys
import os
from typing import Any
import dotenv
from pathlib import Path
from datetime import datetime, timedelta

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from langchain.agents import create_agent
from langchain_core.tools import StructuredTool
from langchain_ollama import ChatOllama
from tools.analyze_cal import calculate_rsi, calculate_sma
from tools.search import search_ticker_info
from input_type.input_schema import TickerInfoInput, SMAInput, RSIInput

# Tools
tools = [
    StructuredTool.from_function(
        func=search_ticker_info,
        name="search_ticker_info",
        description='Lấy data về 1 mã CK. Nhận: ticker (string như "VIC"), info_type (overview/price_history/shareholders/officers/subsidiaries/events/news), start_date, end_date. Để so sánh nhiều mã, gọi tool nhiều lần.',
        args_schema=TickerInfoInput
    ),
    StructuredTool.from_function(
        func=calculate_sma,
        name="calculate_sma",
        description="Tính SMA cho 1 mã. Cần: ticker, start_date, end_date",
        args_schema=SMAInput
    ),
    StructuredTool.from_function(
        func=calculate_rsi,
        name="calculate_rsi",
        description="Tính RSI cho 1 mã. Cần: ticker, start_date, end_date",
        args_schema=RSIInput
    )
]

# Call LLM
dotenv.load_dotenv()
llm = ChatOllama(
    model=os.getenv("model"),
    base_url="http://localhost:11434",
    temperature=0.1
)

# Prompt
current_date = datetime.now().strftime('%Y-%m-%d')
# current_year = datetime.now().year
# current_month = datetime.now().month

system_prompt = f"""Bạn là trợ lý tài chính chuyên nghiệp tại Việt Nam. Hôm nay: {current_date}

CÔNG CỤ:

search_ticker_info: Lấy data mã CK (chỉ 1 mã/lần)

calculate_sma: Tính SMA

calculate_rsi: Tính RSI

QUY TRÌNH:

Gọi tools → Nhận data

Format data thành bảng đẹp

Thêm opening + closing

FORMAT OUTPUT:

Hiển thị nội dung kết quả có được từ công cụ dưới dạng bảng và không đổi tên cột, không thêm cột. Hiển thị lần lượt các cột giống như bảng mẫu có được từ công cụ.

LƯU Ý:

Phản hồi đúng nội dung yêu cầu của người dùng

Xử lý thời gian: 1 tuần = 7 ngày, 1 tháng = 30 ngày

So sánh nhiều mã: Gọi tool nhiều lần

Tự động chọn columns phù hợp với query

Luôn format số có dấu phẩy

100% tiếng Việt"""

agent_executor = create_agent(llm, tools, system_prompt=system_prompt)

def ask(query):
    result = agent_executor.invoke({"messages": [("user", query)]})
    for _, msg in enumerate[Any](result["messages"], 1):
        if msg.type == "ai" and msg.content:
            return msg.content
    return None
