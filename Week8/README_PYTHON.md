# Week8 - Python Version

Chuyển đổi từ Node.js sang Python.

## Cài đặt

```bash
cd Week8
pip install -r requirements.txt
```

## Chạy Server

```bash
python app.py
# Server chạy tại http://localhost:3000
```

## Chạy Unit Tests

```bash
pytest test_server.py -v
```

## Chạy Load Test

```bash
# Đảm bảo server đang chạy trước
python loadtest.py
```

## Chạy API Tests (Postman collection)

```bash
python run_tests.py
```

## Mapping Files

| Node.js | Python |
|---------|--------|
| app.js / server.js | app.py |
| server.test.js (Jest) | test_server.py (pytest) |
| loadtest.js (k6) | loadtest.py (threading) |
| run_tests.js (newman) | run_tests.py |
