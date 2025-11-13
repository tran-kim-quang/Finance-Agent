from vnstock import Vnstock
def calculate_sma(ticker: str, start_date: str, end_date: str, window_size: int = 20):
    stock = Vnstock().stock(symbol=ticker, source='VCI')
    df = stock.quote.history(start=start_date, end=end_date)
    
    # Tính SMA
    df['SMA'] = df['close'].rolling(window=window_size).mean()
    
    # Phân tích xu hướng
    current_price = df['close'].iloc[-1]
    current_sma = df['SMA'].iloc[-1]
    trend = "tăng" if current_price > current_sma else "giảm"
    
    return {
        "current_price": current_price,
        "current_sma": current_sma,
        "trend": trend,
        "data": df[['time', 'close', 'SMA']].to_dict(orient='records')
    }
# print(calculate_sma("ACB", "2025-11-1", "2025-11-13", 9))

def calculate_rsi(ticker: str, start_date: str, end_date: str, period: int = 14):
    stock = Vnstock().stock(symbol=ticker, source='VCI')
    df = stock.quote.history(start=start_date, end=end_date)
    
    # Tính Delta
    df['delta'] = df['close'].diff()
    
    # Tách Gain và Loss
    df['gain'] = df['delta'].apply(lambda x: x if x > 0 else 0)
    df['loss'] = df['delta'].apply(lambda x: -x if x < 0 else 0)
    
    # Tính EMA của Gain và Loss
    df['avg_gain'] = df['gain'].ewm(span=period, adjust=False).mean()
    df['avg_loss'] = df['loss'].ewm(span=period, adjust=False).mean()
    
    # Tính RS và RSI
    df['rs'] = df['avg_gain'] / df['avg_loss']
    df['RSI'] = 100 - (100 / (1 + df['rs']))
    
    # Phân tích tín hiệu
    current_rsi = df['RSI'].iloc[-1]
    if current_rsi > 70:
        signal = "Quá mua (Overbought) - Có thể bán"
    elif current_rsi < 30:
        signal = "Quá bán (Oversold) - Có thể mua"
    else:
        signal = "Trung lập"
    
    return {
        "current_rsi": current_rsi,
        "signal": signal,
        "data": df[['time', 'close', 'RSI']].to_dict(orient='records')
    }
# print(calculate_rsi("ACB", "2025-11-1", "2025-11-13", 14))