"""
Load Test Script - Python version of loadtest.js (k6)
Sử dụng locust hoặc requests + threading để thực hiện load test
"""
import requests
import time
import threading
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "http://localhost:3000"
VUS = 10  # 10 người dùng ảo
DURATION = 30  # Thời gian test (giây)

# Kết quả test
results = {
    "GET_all": {"success": 0, "fail": 0, "times": []},
    "POST": {"success": 0, "fail": 0, "times": []},
    "GET_one": {"success": 0, "fail": 0, "times": []},
    "PUT": {"success": 0, "fail": 0, "times": []},
    "DELETE": {"success": 0, "fail": 0, "times": []},
}
lock = threading.Lock()

def record_result(operation: str, success: bool, response_time: float):
    with lock:
        if success:
            results[operation]["success"] += 1
        else:
            results[operation]["fail"] += 1
        results[operation]["times"].append(response_time)

def run_test_iteration(vu_id: int):
    """Chạy một vòng test cho một virtual user"""
    try:
        # 1️⃣ GET: lấy tất cả sản phẩm
        start = time.time()
        res = requests.get(f"{BASE_URL}/products")
        response_time = time.time() - start
        record_result("GET_all", res.status_code == 200, response_time)
        time.sleep(0.3)

        # 2️⃣ POST: tạo 1 sản phẩm mới
        start = time.time()
        res = requests.post(
            f"{BASE_URL}/products",
            json={"name": f"PerfTest_{vu_id}_{int(time.time()*1000)}", "price": 99}
        )
        response_time = time.time() - start
        record_result("POST", res.status_code == 201, response_time)
        
        created_product = res.json()
        product_id = created_product.get("id")
        time.sleep(0.3)

        # 3️⃣ GET: lấy sản phẩm vừa tạo
        start = time.time()
        res = requests.get(f"{BASE_URL}/products/{product_id}")
        response_time = time.time() - start
        record_result("GET_one", res.status_code == 200, response_time)
        time.sleep(0.3)

        # 4️⃣ PUT: cập nhật sản phẩm vừa tạo
        start = time.time()
        res = requests.put(
            f"{BASE_URL}/products/{product_id}",
            json={"name": "UpdatedProduct", "price": 120}
        )
        response_time = time.time() - start
        record_result("PUT", res.status_code == 200, response_time)
        time.sleep(0.3)

        # 5️⃣ DELETE: xoá sản phẩm vừa tạo
        start = time.time()
        res = requests.delete(f"{BASE_URL}/products/{product_id}")
        response_time = time.time() - start
        record_result("DELETE", res.status_code in [200, 204], response_time)
        time.sleep(0.3)

    except Exception as e:
        print(f"Error in VU {vu_id}: {e}")

def virtual_user(vu_id: int, end_time: float):
    """Mô phỏng một virtual user chạy liên tục trong thời gian test"""
    while time.time() < end_time:
        run_test_iteration(vu_id)

def print_results():
    """In kết quả test"""
    print("\n" + "="*60)
    print("📊 KẾT QUẢ LOAD TEST")
    print("="*60)
    
    total_requests = 0
    total_success = 0
    
    for operation, data in results.items():
        success = data["success"]
        fail = data["fail"]
        total = success + fail
        total_requests += total
        total_success += success
        
        if data["times"]:
            avg_time = statistics.mean(data["times"]) * 1000
            min_time = min(data["times"]) * 1000
            max_time = max(data["times"]) * 1000
            p95_time = sorted(data["times"])[int(len(data["times"]) * 0.95)] * 1000 if len(data["times"]) > 1 else avg_time
        else:
            avg_time = min_time = max_time = p95_time = 0
        
        success_rate = (success / total * 100) if total > 0 else 0
        
        print(f"\n{operation}:")
        print(f"  ✅ Success: {success} | ❌ Fail: {fail} | Rate: {success_rate:.1f}%")
        print(f"  ⏱️  Avg: {avg_time:.2f}ms | Min: {min_time:.2f}ms | Max: {max_time:.2f}ms | P95: {p95_time:.2f}ms")
    
    print("\n" + "-"*60)
    overall_rate = (total_success / total_requests * 100) if total_requests > 0 else 0
    print(f"📈 TỔNG KẾT: {total_requests} requests | {total_success} success | {overall_rate:.1f}% success rate")
    print("="*60)

def main():
    print(f"🚀 Bắt đầu Load Test với {VUS} virtual users trong {DURATION} giây...")
    print(f"🎯 Target: {BASE_URL}")
    
    end_time = time.time() + DURATION
    
    # Tạo và chạy các virtual users
    threads = []
    for vu_id in range(VUS):
        t = threading.Thread(target=virtual_user, args=(vu_id, end_time))
        threads.append(t)
        t.start()
    
    # Đợi tất cả threads hoàn thành
    for t in threads:
        t.join()
    
    print_results()

if __name__ == "__main__":
    main()
