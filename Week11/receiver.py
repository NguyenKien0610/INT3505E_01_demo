from flask import Flask, request, jsonify

app = Flask(__name__)

# Đây là endpoint (URL) mà bên thứ 3 sẽ gọi vào khi có sự kiện
@app.route('/webhook/notify', methods=['POST'])
def receive_webhook():
    data = request.json
    print("------------------------------------------")
    print(f"📡 Đã nhận được Webhook Event: {data.get('event_type')}")
    
    # Giả lập logic xử lý thông báo
    if data.get('event_type') == 'order_created':
        order_id = data.get('payload').get('order_id')
        amount = data.get('payload').get('amount')
        print(f"📧 Đang gửi email xác nhận đơn hàng #{order_id} trị giá ${amount}...")
        return jsonify({"status": "success", "message": "Email sent"}), 200
    
    return jsonify({"status": "ignored"}), 200

if __name__ == '__main__':
    # Chạy server ở cổng 5000
    app.run(port=5000, debug=True)