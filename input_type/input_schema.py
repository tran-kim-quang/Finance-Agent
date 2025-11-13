from pydantic import BaseModel, Field
from typing import Optional

class TickerInfoInput(BaseModel):
    ticker: str = Field(description="MÃ chứng khoán (VD: VIC, HPG, ACB)")
    info_type: str = Field(
        default="overview",
        description="Loại thông tin: overview (tổng quan), price_history (lịch sử giá), shareholders (cổ đông lớn), officers (ban lãnh đạo), subsidiaries (công ty con), events (sự kiện), news (tin tức)"
    )
    start_date: Optional[str] = Field(
        default=None, 
        description="Ngày bắt đầu YYYY-MM-DD (bắt buộc cho price_history)"
    )
    end_date: Optional[str] = Field(
        default=None, 
        description="Ngày kết thúc YYYY-MM-DD (bắt buộc cho price_history)"
    )

class SMAInput(BaseModel):
    ticker: str = Field(description="Mã chứng khoán")
    start_date: str = Field(description="Ngày bắt đầu (YYYY-MM-DD)")
    end_date: str = Field(description="Ngày kết thúc (YYYY-MM-DD)")
    window_size: int = Field(default=20, description="Số ngày cho window size")

class RSIInput(BaseModel):
    ticker: str = Field(description="Mã chứng khoán")
    start_date: str = Field(description="Ngày bắt đầu (YYYY-MM-DD)")
    end_date: str = Field(description="Ngày kết thúc (YYYY-MM-DD)")
    period: int = Field(default=14, description="Số ngày cho period của RSI")