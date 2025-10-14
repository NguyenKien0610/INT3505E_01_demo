# 🧩 Week 02 — REST Architecture Demo (4 Versions)

Thư mục này chứa **4 phiên bản demo** thể hiện sự phát triển tuần tự của các nguyên tắc REST Architecture.

---

## 📁 Cấu trúc thư mục

```bash
Week02/
├── v1_client_server/       # Client–Server
├── v2_stateless/           # + Stateless
├── v3_cacheable_uniform/   # + Cacheable + Uniform Interface
├── v4_full_rest/           # + Layered System + Code-on-Demand
└── README.md               # File này
🚀 Evolution Timeline
🟦 V1: Client–Server
Port: 5000

✅ Client–Server separation
✅ Basic HTTP endpoints
✅ Simple in-memory storage

🟩 V2: + Stateless
Port: 5001

✅ Client–Server
✅ Stateless (no server-side sessions)
✅ Complete request information
✅ Query parameters for filtering

🟨 V3: + Cacheable + Uniform Interface
Port: 5002

✅ Client–Server
✅ Stateless
✅ Cacheable (ETag, Cache-Control)
✅ Uniform Interface (standard URIs, HTTP codes)
✅ Conditional requests (304 Not Modified)
✅ Optimistic concurrency control

🟥 V4: + Layered System + Code-on-Demand
Port: 5003

✅ Client–Server
✅ Stateless
✅ Cacheable
✅ Uniform Interface
✅ Layered System (middleware, logging, monitoring)
✅ Code-on-Demand (dynamic client scripts)
✅ HATEOAS hypermedia links
✅ Pagination with navigation
✅ Health monitoring

🧪 Quick Test — Run All Versions
Terminal commands
bash
Sao chép mã
# Terminal 1
cd v1_client_server && python app.py

# Terminal 2
cd v2_stateless && python app.py

# Terminal 3
cd v3_cacheable_uniform && python app.py

# Terminal 4
cd v4_full_rest && python app.py
🌐 URLs
Version	Port	URL
🟦 V1	5000	http://localhost:5000
🟩 V2	5001	http://localhost:5001
🟨 V3	5002	http://localhost:5002
🟥 V4	5003	http://localhost:5003

🎯 Mục tiêu từng phiên bản
Version	Trọng tâm
🟦 V1	Hiểu nguyên tắc Client–Server separation
🟩 V2	Minh họa Stateless communication pattern
🟨 V3	Giới thiệu HTTP caching và Uniform Interface
🟥 V4	REST hoàn chỉnh — có Layered System, Code-on-Demand, Pagination, Hypermedia