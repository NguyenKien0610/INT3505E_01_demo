"""
API Versioning và Lifecycle Management Demo
Case Study: Payment API - Migration từ v1 sang v2
"""
from fastapi import FastAPI, Header, Query, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from enum import Enum

app = FastAPI(
    title="Payment API - Versioning Demo",
    description="Demo các chiến lược API versioning và lifecycle management",
    version="2.0.0"
)

# ============================================================================
# MODELS
# ============================================================================

class PaymentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

# V1 Models (Deprecated)
class PaymentRequestV1(BaseModel):
    amount: float
    currency: str = "USD"
    customer_id: str
    description: Optional[str] = None

class PaymentResponseV1(BaseModel):
    payment_id: str
    amount: float
    currency: str
    status: str
    created_at: str

# V2 Models (Current)
class PaymentRequestV2(BaseModel):
    amount: float = Field(..., gt=0, description="Số tiền thanh toán (phải > 0)")
    currency: str = Field(default="USD", pattern="^[A-Z]{3}$")
    customer_id: str = Field(..., min_length=1)
    payment_method: Literal["card", "bank_transfer", "e_wallet"] = "card"
    metadata: Optional[dict] = None
    idempotency_key: Optional[str] = None

class PaymentResponseV2(BaseModel):
    payment_id: str
    amount: float
    currency: str
    status: PaymentStatus
    payment_method: str
    customer_id: str
    created_at: datetime
    updated_at: datetime
    metadata: Optional[dict] = None

# ============================================================================
# MOCK DATABASE
# ============================================================================

payments_db = {}
payment_counter = 1000

def create_payment_record(data: dict) -> dict:
    global payment_counter
    payment_counter += 1
    payment_id = f"PAY_{payment_counter}"
    
    payment = {
        "payment_id": payment_id,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        **data
    }
    payments_db[payment_id] = payment
    return payment

# ============================================================================
# CHIẾN LƯỢC 1: URL PATH VERSIONING (Recommended)
# ============================================================================

@app.get("/")
async def root():
    return {
        "message": "Payment API - Versioning Demo",
        "available_versions": ["v1 (deprecated)", "v2 (current)"],
        "versioning_strategies": {
            "url_path": "/api/v1/payments, /api/v2/payments",
            "header": "X-API-Version: 1 or 2",
            "query_param": "/api/payments?version=1 or 2"
        },
        "documentation": "/docs"
    }

# V1 Endpoints (DEPRECATED)
@app.post(
    "/api/v1/payments",
    response_model=PaymentResponseV1,
    tags=["V1 - Deprecated"],
    deprecated=True,
    summary="⚠️ DEPRECATED - Sử dụng /api/v2/payments"
)
async def create_payment_v1(payment: PaymentRequestV1):
    """
    ⚠️ **DEPRECATED** - API này sẽ bị loại bỏ vào ngày 31/12/2025
    
    **Lý do deprecation:**
    - Thiếu validation cho amount (có thể âm)
    - Không hỗ trợ payment_method
    - Không có idempotency protection
    - Response format không consistent
    
    **Migration guide:**
    - Chuyển sang `/api/v2/payments`
    - Thêm field `payment_method` (required)
    - Sử dụng `idempotency_key` để tránh duplicate payments
    - Response sẽ trả về datetime objects thay vì strings
    
    **Support timeline:**
    - Hiện tại: Vẫn hoạt động nhưng có warning
    - 01/10/2025: Read-only mode
    - 31/12/2025: Ngừng hoàn toàn
    """
    # Simulate old behavior
    payment_data = {
        "amount": payment.amount,
        "currency": payment.currency,
        "customer_id": payment.customer_id,
        "status": "pending",
        "payment_method": "card"  # Default for v1
    }
    
    record = create_payment_record(payment_data)
    
    return PaymentResponseV1(
        payment_id=record["payment_id"],
        amount=record["amount"],
        currency=record["currency"],
        status=record["status"],
        created_at=record["created_at"].isoformat()
    )

@app.get(
    "/api/v1/payments/{payment_id}",
    response_model=PaymentResponseV1,
    tags=["V1 - Deprecated"],
    deprecated=True
)
async def get_payment_v1(payment_id: str):
    """⚠️ DEPRECATED - Sử dụng /api/v2/payments/{payment_id}"""
    if payment_id not in payments_db:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    payment = payments_db[payment_id]
    return PaymentResponseV1(
        payment_id=payment["payment_id"],
        amount=payment["amount"],
        currency=payment["currency"],
        status=payment["status"],
        created_at=payment["created_at"].isoformat()
    )

# V2 Endpoints (CURRENT)
@app.post(
    "/api/v2/payments",
    response_model=PaymentResponseV2,
    tags=["V2 - Current"],
    status_code=201
)
async def create_payment_v2(payment: PaymentRequestV2):
    """
    ✅ **CURRENT VERSION** - Tạo payment mới với đầy đủ features
    
    **Improvements từ V1:**
    - ✅ Validation amount > 0
    - ✅ Hỗ trợ nhiều payment methods
    - ✅ Idempotency protection
    - ✅ Metadata support
    - ✅ Better error handling
    - ✅ Consistent datetime format
    
    **Idempotency:**
    Sử dụng `idempotency_key` để đảm bảo request không bị duplicate.
    Nếu gửi cùng key 2 lần, sẽ trả về kết quả của lần đầu.
    """
    # Check idempotency
    if payment.idempotency_key:
        for p in payments_db.values():
            if p.get("idempotency_key") == payment.idempotency_key:
                return PaymentResponseV2(**p)
    
    payment_data = {
        "amount": payment.amount,
        "currency": payment.currency,
        "customer_id": payment.customer_id,
        "payment_method": payment.payment_method,
        "status": PaymentStatus.PENDING,
        "metadata": payment.metadata,
        "idempotency_key": payment.idempotency_key
    }
    
    record = create_payment_record(payment_data)
    return PaymentResponseV2(**record)

@app.get(
    "/api/v2/payments/{payment_id}",
    response_model=PaymentResponseV2,
    tags=["V2 - Current"]
)
async def get_payment_v2(payment_id: str):
    """✅ Lấy thông tin payment theo ID"""
    if payment_id not in payments_db:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    return PaymentResponseV2(**payments_db[payment_id])

@app.get(
    "/api/v2/payments",
    response_model=list[PaymentResponseV2],
    tags=["V2 - Current"]
)
async def list_payments_v2(
    customer_id: Optional[str] = None,
    status: Optional[PaymentStatus] = None,
    limit: int = Query(default=10, le=100)
):
    """✅ Liệt kê payments với filters"""
    results = list(payments_db.values())
    
    if customer_id:
        results = [p for p in results if p["customer_id"] == customer_id]
    
    if status:
        results = [p for p in results if p["status"] == status]
    
    return [PaymentResponseV2(**p) for p in results[:limit]]

# ============================================================================
# CHIẾN LƯỢC 2: HEADER VERSIONING
# ============================================================================

def get_api_version(x_api_version: Optional[str] = Header(default="2")) -> str:
    """Extract API version từ header"""
    if x_api_version not in ["1", "2"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid API version. Supported: 1, 2"
        )
    return x_api_version

@app.post(
    "/api/payments",
    tags=["Header Versioning"],
    summary="Create payment (version qua header)"
)
async def create_payment_header(
    payment: dict,
    version: str = Depends(get_api_version)
):
    """
    Tạo payment với version được chỉ định qua header `X-API-Version`
    
    **Usage:**
    ```
    curl -X POST /api/payments \\
      -H "X-API-Version: 2" \\
      -H "Content-Type: application/json" \\
      -d '{"amount": 100, "customer_id": "C123", "payment_method": "card"}'
    ```
    """
    if version == "1":
        # V1 logic (simplified)
        return {
            "message": "V1 endpoint (deprecated)",
            "warning": "Please upgrade to V2",
            "data": payment
        }
    else:
        # V2 logic
        return {
            "message": "V2 endpoint (current)",
            "data": payment
        }

# ============================================================================
# CHIẾN LƯỢC 3: QUERY PARAMETER VERSIONING
# ============================================================================

@app.get(
    "/api/payments/{payment_id}/details",
    tags=["Query Parameter Versioning"]
)
async def get_payment_details(
    payment_id: str,
    version: Literal["1", "2"] = Query(default="2", description="API version")
):
    """
    Lấy payment details với version qua query parameter
    
    **Usage:**
    - V1: `/api/payments/PAY_1001/details?version=1`
    - V2: `/api/payments/PAY_1001/details?version=2`
    """
    if payment_id not in payments_db:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    payment = payments_db[payment_id]
    
    if version == "1":
        # V1 format (deprecated)
        return {
            "payment_id": payment["payment_id"],
            "amount": payment["amount"],
            "status": payment["status"],
            "created_at": payment["created_at"].isoformat()
        }
    else:
        # V2 format (current)
        return PaymentResponseV2(**payment)

# ============================================================================
# MIGRATION & DEPRECATION ENDPOINTS
# ============================================================================

@app.get("/api/deprecation-notice", tags=["Lifecycle Management"])
async def deprecation_notice():
    """
    Thông báo deprecation cho developers
    """
    return {
        "title": "API V1 Deprecation Notice",
        "deprecated_version": "v1",
        "current_version": "v2",
        "deprecation_date": "2025-06-01",
        "sunset_date": "2025-12-31",
        "timeline": {
            "2025-06-01": "V1 marked as deprecated (warnings added)",
            "2025-10-01": "V1 becomes read-only (no new payments)",
            "2025-12-31": "V1 completely removed"
        },
        "breaking_changes": [
            {
                "change": "amount validation",
                "v1": "Accepts negative values",
                "v2": "Must be > 0",
                "migration": "Validate amount on client side before sending"
            },
            {
                "change": "payment_method field",
                "v1": "Not required (defaults to 'card')",
                "v2": "Required field",
                "migration": "Add payment_method to all requests"
            },
            {
                "change": "datetime format",
                "v1": "ISO string",
                "v2": "datetime object",
                "migration": "Parse datetime objects in response"
            }
        ],
        "migration_guide_url": "https://docs.example.com/migration/v1-to-v2",
        "support_contact": "api-support@example.com"
    }

@app.get("/api/version-info", tags=["Lifecycle Management"])
async def version_info():
    """Thông tin về các versions hiện có"""
    return {
        "versions": {
            "v1": {
                "status": "deprecated",
                "released": "2024-01-01",
                "deprecated": "2025-06-01",
                "sunset": "2025-12-31",
                "endpoints": [
                    "POST /api/v1/payments",
                    "GET /api/v1/payments/{id}"
                ]
            },
            "v2": {
                "status": "current",
                "released": "2025-06-01",
                "deprecated": None,
                "sunset": None,
                "endpoints": [
                    "POST /api/v2/payments",
                    "GET /api/v2/payments/{id}",
                    "GET /api/v2/payments"
                ],
                "features": [
                    "Idempotency support",
                    "Multiple payment methods",
                    "Enhanced validation",
                    "Metadata support"
                ]
            }
        },
        "recommended_version": "v2"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
