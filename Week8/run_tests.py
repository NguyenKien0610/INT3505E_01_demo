"""
Run Postman Collection Tests - Python version of run_tests.js
Sử dụng newman qua subprocess hoặc requests để chạy tests
"""
import subprocess
import sys
import os

def run_newman_tests():
    """Chạy Postman collection tests bằng newman"""
    collection_path = os.path.join(os.path.dirname(__file__), "Product_API_Tests.postman_collection.json")
    report_path = os.path.join(os.path.dirname(__file__), "report.html")
    
    try:
        # Chạy newman với reporters
        result = subprocess.run([
            "newman", "run", collection_path,
            "--reporters", "cli,htmlextra",
            "--reporter-htmlextra-export", report_path
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        if result.returncode == 0:
            print(f"✅ Test suite completed. Report saved at {report_path}")
        else:
            print("❌ Test suite failed!")
            sys.exit(1)
            
    except FileNotFoundError:
        print("❌ Newman không được cài đặt. Chạy: npm install -g newman newman-reporter-htmlextra")
        print("\n🔄 Đang chạy tests bằng Python requests thay thế...")
        run_python_tests()

def run_python_tests():
    """Chạy tests bằng Python requests (thay thế cho newman)"""
    import requests
    import json
    
    BASE_URL = "http://localhost:3000"
    results = []
    
    print("\n" + "="*50)
    print("🧪 RUNNING API TESTS")
    print("="*50)
    
    # Test 1: GET all products
    print("\n📋 Test 1: GET /products")
    try:
        res = requests.get(f"{BASE_URL}/products")
        passed = res.status_code == 200 and len(res.json()) > 0
        results.append(("GET /products", passed))
        print(f"   {'✅ PASSED' if passed else '❌ FAILED'} - Status: {res.status_code}")
    except Exception as e:
        results.append(("GET /products", False))
        print(f"   ❌ FAILED - Error: {e}")
    
    # Test 2: GET product by ID
    print("\n📋 Test 2: GET /products/1")
    try:
        res = requests.get(f"{BASE_URL}/products/1")
        passed = res.status_code == 200 and res.json().get("name") == "Book"
        results.append(("GET /products/1", passed))
        print(f"   {'✅ PASSED' if passed else '❌ FAILED'} - Status: {res.status_code}")
    except Exception as e:
        results.append(("GET /products/1", False))
        print(f"   ❌ FAILED - Error: {e}")
    
    # Test 3: POST new product
    print("\n📋 Test 3: POST /products")
    created_id = None
    try:
        res = requests.post(f"{BASE_URL}/products", json={"name": "TestProduct", "price": 99})
        passed = res.status_code == 201 and "id" in res.json()
        created_id = res.json().get("id")
        results.append(("POST /products", passed))
        print(f"   {'✅ PASSED' if passed else '❌ FAILED'} - Status: {res.status_code}, ID: {created_id}")
    except Exception as e:
        results.append(("POST /products", False))
        print(f"   ❌ FAILED - Error: {e}")
    
    # Test 4: PUT update product
    print("\n📋 Test 4: PUT /products/:id")
    try:
        res = requests.put(f"{BASE_URL}/products/{created_id}", json={"price": 120})
        passed = res.status_code == 200 and res.json().get("price") == 120
        results.append(("PUT /products/:id", passed))
        print(f"   {'✅ PASSED' if passed else '❌ FAILED'} - Status: {res.status_code}")
    except Exception as e:
        results.append(("PUT /products/:id", False))
        print(f"   ❌ FAILED - Error: {e}")
    
    # Test 5: DELETE product
    print("\n📋 Test 5: DELETE /products/:id")
    try:
        res = requests.delete(f"{BASE_URL}/products/{created_id}")
        passed = res.status_code in [200, 204]
        results.append(("DELETE /products/:id", passed))
        print(f"   {'✅ PASSED' if passed else '❌ FAILED'} - Status: {res.status_code}")
    except Exception as e:
        results.append(("DELETE /products/:id", False))
        print(f"   ❌ FAILED - Error: {e}")
    
    # Test 6: GET not found
    print("\n📋 Test 6: GET /products/999999 (Not Found)")
    try:
        res = requests.get(f"{BASE_URL}/products/999999")
        passed = res.status_code == 404
        results.append(("GET /products/999999", passed))
        print(f"   {'✅ PASSED' if passed else '❌ FAILED'} - Status: {res.status_code}")
    except Exception as e:
        results.append(("GET /products/999999", False))
        print(f"   ❌ FAILED - Error: {e}")
    
    # Summary
    print("\n" + "="*50)
    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)
    print(f"📊 SUMMARY: {passed_count}/{total_count} tests passed")
    print("="*50)
    
    # Generate simple HTML report
    generate_html_report(results)

def generate_html_report(results):
    """Tạo báo cáo HTML đơn giản"""
    report_path = os.path.join(os.path.dirname(__file__), "report.html")
    
    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>API Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .passed {{ color: green; }}
        .failed {{ color: red; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        .summary {{ font-size: 24px; margin: 20px 0; }}
    </style>
</head>
<body>
    <h1>🧪 API Test Report</h1>
    <div class="summary">
        <span class="passed">✅ Passed: {passed_count}</span> | 
        <span class="failed">❌ Failed: {total_count - passed_count}</span>
    </div>
    <table>
        <tr><th>Test</th><th>Result</th></tr>
"""
    
    for test_name, passed in results:
        status = '<span class="passed">✅ PASSED</span>' if passed else '<span class="failed">❌ FAILED</span>'
        html += f"        <tr><td>{test_name}</td><td>{status}</td></tr>\n"
    
    html += """    </table>
</body>
</html>"""
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"\n✅ Report saved at {report_path}")

if __name__ == "__main__":
    run_newman_tests()
