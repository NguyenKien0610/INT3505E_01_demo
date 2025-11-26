import requests
import json
import time

# Địa chỉ của Server nhận (file receiver.py đang chạy)
WEBHOOK_URL = 'http://127.0.0.1:5000/webhook/notify'

def simulate_new_order():
    payload = {
        "event_type": "order_created",
        "timestamp": time.time(),
        "payload": {
            "order_id": "ORD-2024-999",
            "customer": "nguyenvana@email.com",
            "amount": 150.00,
            "items": ["Laptop", "Mouse"]
        }
    }
    
    print(f"🚀 Đang bắn Webhook tới {WEBHOOK_URL}...")
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        print(f"✅ Kết quả từ server: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")

if __name__ == "__main__":
    simulate_new_order()