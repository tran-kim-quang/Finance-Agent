## Requirements
- Python 3.12
- Ollama

## Clone và tạo môi trường
```
git clone https://github.com/tran-kim-quang/Finance-Agent.git
cd finance_agent

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Sử dụng qua REST API
```
cd api
uvicorn api.main:app --reload --host
```
Truy cập cổng `http://localhost:8000/docs` để test API `/query`

## Scripts test mẫu
[Sample QA](api\api.png)

[Code](scripts_test.py)

## Kiến trúc
- Xây dựng 2 [Tools](tools) gồm:
    - `search` - Sử dụng vnstock để lấy các thông tin cần thiết
    - `analyze_cal` - Công thức tính SMA và RSI
      
