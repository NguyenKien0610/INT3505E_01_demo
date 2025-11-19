"""
Script test cho API Versioning Demo
Chạy: python test_api.py (sau khi start server)
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_section(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_response(response):
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, default=str)}")

def test_root():
    print_section("1. TEST ROOT ENDPOINT")
    response = requests.get(f"{BASE_URL}/")
    print_response(response)

def test_v1_create_payment():
    print_section("2. TEST V1 - CREATE PAYMENT (DEPRECATED)")
    data = {
        "amount": 100.50,
        "currency": "USD",
        "customer_id": "CUST_001",
        "description": "Test payment V1"
    }
    response = requests.post(f"{BASE_URL}/api/v1/payments", json=data)
    print_response(response)
    return response.json().get("payment_id")

def test_v1_get_payment(payment_id):
    print_section("3. TEST V1 - GET PAYMENT (DEPRECATED)")
    response = requests.get(f"{BASE_URL}/api/v1/payments/{payment_id}")
    print_response(response)

def test_v2_create_payment():
    print_section("4. TEST V2 - CREATE PAYMENT (CURRENT)")
    data = {
        "amount": 250.75,
        "currency": "USD",
        "customer_id": "CUST_002",
        "payment_method": "card",
        "metadata": {
            "order_id": "ORD_12345",
            "product": "Premium Subscription"
        }
    }
    response = requests.post(f"{BASE_URL}/api/v2/payments", json=data)
    print_response(response)
    return response.json().get("payment_id")

def test_v2_idempotency():
    print_section("5. TEST V2 - IDEMPOTENCY")
    data = {
        "amount": 99.99,
        "currency": "USD",
        "customer_id": "CUST_003",
        "payment_method": "e_wallet",
        "idempotency_key": "UNIQUE_KEY_12345"
    }
    
    print("Gửi request lần 1:")
    response1 = requests.post(f"{BASE_URL}/api/v2/payments", json=data)
    print_response(response1)
    payment_id_1 = response1.json().get("payment_id")
    
    print("\nGửi request lần 2 với cùng idempotency_key:")
    response2 = requests.post(f"{BASE_URL}/api/v2/payments", json=data)
    print_response(response2)
    payment_id_2 = response2.json().get("payment_id")
    
    print(f"\n✓ Idempotency check: {payment_id_1 == payment_id_2}")
    return payment_id_1

def test_v2_get_payment(payment_id):
    print_section("6. TEST V2 - GET PAYMENT")
    response = requests.get(f"{BASE_URL}/api/v2/payments/{payment_id}")
    print_response(response)

def test_v2_list_payments():
    print_section("7. TEST V2 - LIST PAYMENTS")
    
    print("List tất cả payments:")
    response = requests.get(f"{BASE_URL}/api/v2/payments")
    print_response(response)
    
    print("\nFilter theo customer_id:")
    response = requests.get(f"{BASE_URL}/api/v2/payments?customer_id=CUST_002")
    print_response(response)

def test_header_versioning():
    print_section("8. TEST HEADER VERSIONING")
    
    data = {
        "amount": 150.00,
        "customer_id": "CUST_004"
    }
    
    print("Request với X-API-Version: 1")
    response = requests.post(
        f"{BASE_URL}/api/payments",
        json=data,
        headers={"X-API-Version": "1"}
    )
    print_response(response)
    
    print("\nRequest với X-API-Version: 2")
    response = requests.post(
        f"{BASE_URL}/api/payments",
        json=data,
        headers={"X-API-Version": "2"}
    )
    print_response(response)

def test_query_versioning(payment_id):
    print_section("9. TEST QUERY PARAMETER VERSIONING")
    
    print("Request với version=1:")
    response = requests.get(f"{BASE_URL}/api/payments/{payment_id}/details?version=1")
    print_response(response)
    
    print("\nRequest với version=2:")
    response = requests.get(f"{BASE_URL}/api/payments/{payment_id}/details?version=2")
    print_response(response)

def test_deprecation_notice():
    print_section("10. TEST DEPRECATION NOTICE")
    response = requests.get(f"{BASE_URL}/api/deprecation-notice")
    print_response(response)

def test_version_info():
    print_section("11. TEST VERSION INFO")
    response = requests.get(f"{BASE_URL}/api/version-info")
    print_response(response)

def test_validation_errors():
    print_section("12. TEST VALIDATION ERRORS")
    
    print("Test 1: Amount âm (V2 sẽ reject):")
    data = {
        "amount": -100,
        "currency": "USD",
        "customer_id": "CUST_005",
        "payment_method": "card"
    }
    response = requests.post(f"{BASE_URL}/api/v2/payments", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    print("\nTest 2: Currency không hợp lệ:")
    data = {
        "amount": 100,
        "currency": "US",  # Phải là 3 ký tự
        "customer_id": "CUST_005",
        "payment_method": "card"
    }
    response = requests.post(f"{BASE_URL}/api/v2/payments", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def main():
    print("\n" + "🚀 BẮT ĐẦU TEST API VERSIONING DEMO " + "🚀")
    print("Đảm bảo server đang chạy tại http://localhost:8000")
    
    try:
        # Test basic endpoints
        test_root()
        
        # Test V1 (deprecated)
        payment_id_v1 = test_v1_create_payment()
        if payment_id_v1:
            test_v1_get_payment(payment_id_v1)
        
        # Test V2 (current)
        payment_id_v2 = test_v2_create_payment()
        if payment_id_v2:
            test_v2_get_payment(payment_id_v2)
        
        # Test idempotency
        payment_id_idem = test_v2_idempotency()
        
        # Test list
        test_v2_list_payments()
        
        # Test other versioning strategies
        test_header_versioning()
        if payment_id_v2:
            test_query_versioning(payment_id_v2)
        
        # Test lifecycle management
        test_deprecation_notice()
        test_version_info()
        
        # Test validation
        test_validation_errors()
        
        print("\n" + "✅ HOÀN THÀNH TẤT CẢ TESTS " + "✅")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ LỖI: Không thể kết nối đến server!")
        print("Hãy chạy: python app.py hoặc uvicorn app:app --reload")
    except Exception as e:
        print(f"\n❌ LỖI: {str(e)}")

if __name__ == "__main__":
    main()
