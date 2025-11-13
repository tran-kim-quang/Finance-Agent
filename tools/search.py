from vnstock import Vnstock, Company
from typing import Optional
# import format
def search_ticker_info(
    ticker: str,  # ← CHỈ 1 MÃ, không phải list
    info_type: str = "overview",
    start_date: Optional[str] = None, 
    end_date: Optional[str] = None
):
    # Clean input
    ticker = ticker.strip().upper()
    
    if not ticker:
        return {"error": "ticker không được rỗng"}
    
    try:
        # ============ THÔNG TIN CÔNG TY ============
        if info_type in ["overview", "shareholders", "officers", "subsidiaries", "events", "news"]:
            company = Company(symbol=ticker, source='VCI')
            
            if info_type == "overview":
                data = company.overview()
                return {
                    "ticker": ticker,
                    "data": data.to_dict('records') if hasattr(data, 'to_dict') else data
                }
                
            elif info_type == "shareholders":
                data = company.shareholders()
                return {
                    "ticker": ticker,
                    "data": data.to_dict('records') if hasattr(data, 'to_dict') else data
                }
                
            elif info_type == "officers":
                data = company.officers(filter_by='working')
                return {
                    "ticker": ticker,
                    "data": data.to_dict('records') if hasattr(data, 'to_dict') else data
                }
                
            elif info_type == "subsidiaries":
                data = company.subsidiaries()
                return {
                    "ticker": ticker,
                    "data": data.to_dict('records') if hasattr(data, 'to_dict') else data
                }
                
            elif info_type == "events":
                data = company.events()
                return {
                    "ticker": ticker,
                    "data": data.to_dict('records') if hasattr(data, 'to_dict') else data
                }
                
            elif info_type == "news":
                data = company.news()
                return {
                    "ticker": ticker,
                    "data": data.to_dict('records') if hasattr(data, 'to_dict') else data
                }
        
        # ============ DỮ LIỆU GIÁ & TÀI CHÍNH ============
        else:
            stock = Vnstock().stock(symbol=ticker, source='VCI')
            
            if info_type == "price_history":
                if not start_date or not end_date:
                    return {"error": "Cần start_date và end_date"}
                    
                df = stock.quote.history(start=start_date, end=end_date)
                
                if df is not None and len(df) > 0:
                    return {
                        "ticker": ticker,
                        "data": df.to_dict('records')
                    }
                else:
                    return {"error": "Không có dữ liệu"}
                    
            elif info_type == "financial_ratio":
                data = stock.finance.ratio(period='year')
                return {
                    "ticker": ticker,
                    "data": data.to_dict('records') if hasattr(data, 'to_dict') else data
                }
                
            elif info_type == "income_statement":
                data = stock.finance.income_statement(period='year', lang='vi')
                return {
                    "ticker": ticker,
                    "data": data.to_dict('records') if hasattr(data, 'to_dict') else data
                }
                
            elif info_type == "balance_sheet":
                data = stock.finance.balance_sheet(period='year', lang='vi')
                return {
                    "ticker": ticker,
                    "data": data.to_dict('records') if hasattr(data, 'to_dict') else data
                }
                
            elif info_type == "cashflow":
                data = stock.finance.cash_flow(period='year', lang='vi')
                return {
                    "ticker": ticker,
                    "data": data.to_dict('records') if hasattr(data, 'to_dict') else data
                }
                
            else:
                return {"error": f"info_type '{info_type}' không hợp lệ"}
                
    except Exception as e:
        return {"ticker": ticker, "error": str(e)}


# result = search_ticker_info("VCB", "subsidiaries")
# print(result)
# company = Company(symbol="VCB", source='VCI')
# print(company.subsidiaries())