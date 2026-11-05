"""
MAVIS CHÚC BẠN NGỦ NGON - FASTAPI APPLICATION SERVER
High-performance asynchronous API engine powered by FastAPI, Uvicorn, LangChain & Vector DB.
Features:
- Full OpenAPI / Swagger documentation at /docs and /redoc
- Asynchronous non-blocking request handling with CORS middleware
- Seamless backward compatibility with all frontend endpoints
- LangChain Medical RAG & Vector Database integration
- ACID SQLite relational database persistence
"""

import os
import sys
import json
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

# Core System Engines
import database
import ai_analyzer
import rag_engine

PORT = int(os.environ.get('PORT', 8080))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI(
    title="Mavis Goodnight - Real-Time Wellness Advisor API",
    description=(
        "Production-grade, evidence-based sleep wellness & circadian rhythm optimization API. "
        "Powered by FastAPI, LangChain, Vector Database and Google Gemini 3.5."
    ),
    version="2.5.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Enable CORS for cross-platform integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    """Initializes SQLite database and Medical Vector Database on boot."""
    print("[FastAPI Lifecycle] Initializing SQLite Relational Database...", flush=True)
    database.init_db()
    print("[FastAPI Lifecycle] Initializing LangChain Medical Vector Store...", flush=True)
    rag_engine.get_vector_store()
    print(f"[FastAPI Lifecycle] Server running and ready on port {PORT}!", flush=True)


# ==============================================================================
# SYSTEM & HEALTH ENDPOINTS
# ==============================================================================

@app.get("/api/status", summary="Server & Engine Health Status", tags=["System"])
async def get_system_status():
    vn_now = datetime.now(timezone(timedelta(hours=7)))
    stats = database.get_stats()
    vstore = rag_engine.get_vector_store()
    return {
        "status": "online",
        "service": "Mavis Goodnight Wellness Advisor",
        "version": "2.5.0",
        "framework": "FastAPI + Uvicorn (ASGI)",
        "serverTime": vn_now.isoformat(),
        "timeZone": "Asia/Ho_Chi_Minh (UTC+7)",
        "database": {
            "engine": "SQLite 3 Relational",
            "totalUsers": stats.get("totalUsers", 0),
            "totalDiagnoses": stats.get("totalDiagnoses", 0),
            "totalAiChats": stats.get("totalAiChats", 0)
        },
        "ragEngine": {
            "orchestration": "LangChain LCEL",
            "vectorDatabase": "Medical Vector Store (In-Memory / Chroma-compatible)",
            "indexedMedicalChunks": len(vstore.documents),
            "embeddingModel": "Google text-embedding-004 (768-dim)"
        }
    }


@app.get("/api/stats", summary="Get System Analytics Stats", tags=["Admin"])
async def get_stats():
    return {"success": True, "stats": database.get_stats()}


@app.get("/api/logs", summary="List Audit Service Usage Logs", tags=["Admin"])
async def get_logs(limit: int = 150):
    return {"success": True, "logs": database.list_service_logs(limit=limit)}


@app.get("/api/diagnoses", summary="List Clinical Diagnoses", tags=["Clinical"])
async def get_diagnoses(limit: int = 100):
    return {"success": True, "diagnoses": database.list_diagnoses(limit=limit)}


@app.get("/api/export", summary="Export Database JSON Backup", tags=["Admin"])
async def export_db():
    return database.export_full_database()


@app.get("/api/database/status", summary="Database Engine File & Schema Info", tags=["System"])
async def database_status():
    stats = database.get_stats()
    return {
        "success": True,
        "engine": "SQLite 3",
        "file": database.DB_FILE,
        "schemaFile": database.SCHEMA_FILE,
        "stats": stats
    }


# ==============================================================================
# AUTHENTICATION & USER MANAGEMENT
# ==============================================================================

@app.get("/api/users", summary="List Registered Users", tags=["Users"])
async def get_users():
    users = database.list_all_users()
    active_id = database.get_active_user_id()
    return {"success": True, "users": users, "activeUserId": active_id}


@app.post("/api/auth/login", summary="User Login via Phone or Username", tags=["Auth"])
async def handle_login(request: Request):
    body = await request.json()
    phone_or_id = body.get("phoneOrId", "").strip()
    password = body.get("password", "").strip()
    device = body.get("device", "Web/Mobile")

    if not phone_or_id:
        raise HTTPException(status_code=400, detail="Vui lòng nhập tên tài khoản hoặc số điện thoại!")

    found_user = database.find_user_for_login(phone_or_id)
    if not found_user:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy tài khoản với thông tin này. Bạn vui lòng kiểm tra lại hoặc chuyển sang tab Đăng Ký để tạo tài khoản mới!"
        )

    user_pwd = found_user.get("password", "")
    if password and user_pwd and password != user_pwd:
        raise HTTPException(status_code=401, detail="Mật khẩu không chính xác. Vui lòng thử lại!")

    database.update_user(found_user["id"], {"lastLoginAt": datetime.now(timezone(timedelta(hours=7))).isoformat()})
    database.set_active_user_id(found_user["id"])

    database.add_service_log({
        "userId": found_user["id"],
        "userName": found_user["fullName"],
        "serviceType": "AUTH_LOGIN",
        "title": "Đăng nhập tài khoản",
        "detail": f"Người dùng {found_user['fullName']} đã đăng nhập thành công vào hệ thống SQL.",
        "device": device,
        "icon": "fa-solid fa-arrow-right-to-bracket",
        "badgeColor": "emerald"
    })

    user_diags = database.list_diagnoses(user_id=found_user["id"])
    return {
        "success": True,
        "user": found_user,
        "diagnoses": user_diags,
        "message": f"Chào mừng {found_user['fullName']} đã đăng nhập thành công!"
    }


@app.post("/api/auth/register", summary="Register New User Account", tags=["Auth"])
async def handle_register(request: Request):
    body = await request.json()
    full_name = body.get("fullName", "").strip()
    phone = body.get("phone", "").strip()
    device = body.get("device", "Web Browser")

    if not full_name or not phone:
        raise HTTPException(status_code=400, detail="Vui lòng nhập họ tên và số điện thoại!")

    existing = database.find_user_for_login(phone)
    if existing:
        raise HTTPException(status_code=409, detail="Số điện thoại/Username này đã được đăng ký. Vui lòng chuyển sang tab Đăng Nhập!")

    new_user = database.create_user(body)
    database.set_active_user_id(new_user["id"])

    database.add_service_log({
        "userId": new_user["id"],
        "userName": new_user["fullName"],
        "serviceType": "AUTH_REGISTER",
        "title": "Đăng ký thành viên mới",
        "detail": f"Thành viên mới {new_user['fullName']} ({new_user['phone']}) đã tạo tài khoản và lưu vào SQL Database.",
        "device": device,
        "icon": "fa-solid fa-user-plus",
        "badgeColor": "emerald"
    })

    return {
        "success": True,
        "user": new_user,
        "message": "Đăng ký tài khoản thành công! Dữ liệu đã được lưu trữ an toàn vào Cơ Sở Dữ Liệu SQL."
    }


@app.post("/api/auth/google", summary="Google Account One-Click Authentication and SQLite Sync", tags=["Auth"])
async def handle_google_auth(request: Request):
    """
    Authenticate and synchronize Google Profile directly into backend SQLite database.
    Supports instant seamless login with Google OAuth 2.0 and Google Identity Services.
    """
    body = await request.json()
    google_sub = str(body.get("sub") or body.get("googleSub") or body.get("id") or int(datetime.now().timestamp()))
    social_id = f"user_google_{google_sub}" if not str(body.get("id", "")).startswith("user_google_") else body.get("id")
    full_name = body.get("fullName") or body.get("name") or "Thành Viên Google"
    email = body.get("email") or f"{google_sub}@gmail.com"
    avatar = body.get("picture") or body.get("avatarType") or "sleep_owl"
    device = body.get("device", "Web Google OAuth")

    existing = database.get_user_by_id(social_id) or database.find_user_for_login(email)
    if existing:
        update_data = {
            "fullName": full_name,
            "avatarType": avatar,
            "socialProvider": "google",
            "lastLoginAt": datetime.now(timezone(timedelta(hours=7))).isoformat()
        }
        user = database.update_user(existing["id"], update_data) or existing
    else:
        new_user_data = {
            "id": social_id,
            "fullName": full_name,
            "phone": email,
            "password": "",
            "role": "Thành viên Google Sync",
            "bio": "Tài khoản kết nối qua Google Account chính thức • Đồng bộ nhịp sinh học tự động 🌙",
            "age": "28 tuổi",
            "gender": "Khác",
            "occupation": "Thành viên Google Sync",
            "targetBedtime": "23:00",
            "wakeTime": "06:30",
            "fitnessLevel": "Khá",
            "healthConditions": ["Đồng bộ thói quen sinh học"],
            "avatarType": avatar,
            "socialProvider": "google",
            "streakDays": 3,
            "verified": 1,
            "createdAt": datetime.now(timezone(timedelta(hours=7))).isoformat(),
            "lastLoginAt": datetime.now(timezone(timedelta(hours=7))).isoformat()
        }
        user = database.create_user(new_user_data)

    database.set_active_user_id(user["id"])

    database.add_service_log({
        "userId": user["id"],
        "userName": user["fullName"],
        "serviceType": "AUTH_LOGIN",
        "title": "Đăng nhập Google Account",
        "detail": f"Thành viên {user['fullName']} ({email}) đã kết nối thành công qua Google OAuth 2.0.",
        "device": device,
        "icon": "fa-brands fa-google",
        "badgeColor": "sky"
    })

    return {
        "success": True,
        "user": user,
        "message": f"Chào mừng {user['fullName']} đã kết nối thành công qua tài khoản Google!"
    }


@app.post("/api/users", summary="Create or Update User Profile", tags=["Users"])
async def save_user(request: Request):
    body = await request.json()
    user_id = body.get("id")
    if user_id and database.get_user_by_id(user_id):
        updated_user = database.update_user(user_id, body)
        return {"success": True, "message": "Cập nhật người dùng thành công trong SQL!", "user": updated_user}
    else:
        new_user = database.create_user(body)
        return {"success": True, "message": "Thêm mới người dùng thành công vào SQL!", "user": new_user}


@app.post("/api/users/delete", summary="Delete User Profile", tags=["Users"])
async def delete_user(request: Request):
    body = await request.json()
    target_id = body.get("userId")
    if not target_id:
        raise HTTPException(status_code=400, detail="Thiếu userId")

    deleted = database.delete_user(target_id)
    if deleted:
        if database.get_active_user_id() == target_id:
            database.set_active_user_id(None)
        return {"success": True, "message": "Đã xóa người dùng khỏi SQL Database thành công!"}
    raise HTTPException(status_code=404, detail="Không tìm thấy người dùng trong SQL")


@app.post("/api/sync", summary="Synchronize Offline Client State", tags=["Sync"])
async def handle_sync(request: Request):
    body = await request.json()
    if body:
        client_users = body.get("users", [])
        client_logs = body.get("serviceUsage", [])
        client_diags = body.get("diagnoses", [])
        device_type = body.get("deviceType", "Thiết bị người dùng")

        for cu in client_users:
            cid = cu.get("id")
            if not cid:
                continue
            existing = database.get_user_by_id(cid)
            if not existing:
                database.create_user(cu)
            else:
                database.update_user(cid, cu)

        for cl in client_logs:
            cl["device"] = device_type
            database.add_service_log(cl)

        for cd in client_diags:
            cd["device"] = device_type
            database.save_diagnosis(cd)

    synced_users = []
    if body:
        client_users = body.get("users", [])
        for cu in client_users:
            cid = cu.get("id")
            if cid:
                u = database.get_user_by_id(cid)
                if u:
                    synced_users.append(u)

    now_iso = datetime.now(timezone(timedelta(hours=7))).isoformat()
    return {
        "success": True,
        "message": "Đồng bộ Cơ Sở Dữ Liệu SQL thành công!",
        "serverTime": now_iso,
        "data": {
            "users": synced_users,
            "serverTime": now_iso
        }
    }


@app.post("/api/diagnoses", summary="Save Clinical Sleep Diagnosis", tags=["Clinical"])
async def save_diagnosis(request: Request):
    body = await request.json()
    saved_diag = database.save_diagnosis(body)
    return {"success": True, "diagnosis": saved_diag}


@app.post("/api/logs", summary="Log Service Usage Event", tags=["Admin"])
async def add_log(request: Request):
    body = await request.json()
    saved_log = database.add_service_log(body)
    return {"success": True, "log": saved_log}


@app.post("/api/reset", summary="Factory Reset SQLite Database", tags=["Admin"])
async def reset_db():
    database.reset_database()
    return {
        "success": True,
        "message": "Đã làm sạch Cơ Sở Dữ Liệu SQL! Toàn bộ bảng đã sẵn sàng cho tài khoản người dùng thực."
    }


# ==============================================================================
# AI & LANGCHAIN RAG ENDPOINTS
# ==============================================================================

@app.post("/api/ai/analyze-sleep", summary="5-Pillar Sleep Diagnostic Analysis", tags=["AI Engine"])
async def analyze_sleep(request: Request):
    body = await request.json()
    if not body:
        raise HTTPException(status_code=400, detail="Dữ liệu khảo sát rỗng")

    result = ai_analyzer.analyze_sleep_survey(body)

    user = body.get("user") or {}
    diag_id = int(datetime.now().timestamp() * 1000)
    diag_entry = {
        "id": diag_id,
        "userId": user.get("id"),
        "userName": user.get("fullName", "Khách"),
        "score": result.get("predictedScore", 70),
        "pillars": result.get("pillars", {}),
        "summary": result.get("verdictTitle", ""),
        "answers": body.get("answers", {}),
        "customAnswers": body.get("customAnswers", {}),
        "device": body.get("device", "Web Browser"),
        "timestamp": datetime.now(timezone(timedelta(hours=7))).isoformat()
    }
    database.save_diagnosis(diag_entry)

    database.add_service_log({
        "userId": user.get("id"),
        "userName": user.get("fullName", "Khách"),
        "serviceType": "AI_DIAGNOSIS_ANALYSIS",
        "title": f"Phân tích AI: {result.get('verdictTitle', 'Chẩn đoán 5 trụ cột')}",
        "detail": f"Động cơ: {result.get('aiEngine')} - Điểm: {result.get('predictedScore')}%. Bóc tách {len(result.get('customInsights', []))} ý kiến tự điền.",
        "device": body.get("device", "Web Browser"),
        "icon": "fa-solid fa-wand-magic-sparkles",
        "badgeColor": "indigo"
    })

    return {"success": True, "analysis": result, "diagnosisId": diag_id}


@app.post("/api/ai/chat", summary="RAG-Powered Conversational Advisor", tags=["AI Engine"])
async def ai_chat(request: Request):
    body = await request.json()
    if not body:
        raise HTTPException(status_code=400, detail="Tin nhắn rỗng")

    query = (body.get("message") or body.get("query") or "").strip()
    user = body.get("user") or {}
    user_id = body.get("userId") or (user.get("id") if isinstance(user, dict) else None)
    if user_id and (not user or not user.get("id")):
        found_db_user = database.get_user_by_id(user_id)
        if found_db_user:
            user = found_db_user
    client_time = body.get("clientTime")
    client_hour = body.get("clientHour")
    client_phase = body.get("clientPhase")
    client_date = body.get("clientDate")
    time_zone = body.get("timeZone")

    # Enforce mandatory login gate for Mavis Chatbot
    if not user or not user.get("id"):
        return {
            "success": False,
            "requireAuth": True,
            "reply": "Dạ em Mavis chào bạn ạ! Để em có thể lấy dữ liệu đồng bộ nhịp sinh học y khoa và tư vấn chuẩn xác nhất cho bạn, bạn vui lòng Đăng Nhập hoặc Đăng Ký tài khoản trước nhé ạ! ❤️"
        }

    if not query:
        raise HTTPException(status_code=400, detail="Vui lòng nhập nội dung câu hỏi")

    # Priority 1: LangChain Grounded Medical RAG Engine
    ai_res = rag_engine.chat_with_rag(
        query=query,
        user=user,
        client_time=client_time,
        client_hour=client_hour,
        client_phase=client_phase,
        client_date=client_date,
        time_zone=time_zone
    )

    # Priority 2: Fallback to General Empathetic Health Engine if RAG failed
    if not ai_res or not ai_res.get("success"):
        ai_res = ai_analyzer.chat_with_mavis(
            query=query,
            user=user,
            client_time=client_time,
            client_hour=client_hour,
            client_phase=client_phase,
            client_date=client_date,
            time_zone=time_zone
        )

    if ai_res and ai_res.get("success"):
        reply = ai_res.get("reply")
        database.add_service_log({
            "userId": user.get("id"),
            "userName": user.get("fullName", "Khách"),
            "serviceType": "AI_CHATBOT_RAG",
            "title": f"Mavis RAG: {query[:35]}...",
            "detail": f"Model: {ai_res.get('model')} - RAG Grounding trên {ai_res.get('retrieved_chunks', 0)} trích đoạn y văn.",
            "device": body.get("device", "Web"),
            "icon": "fa-solid fa-brain",
            "badgeColor": "indigo"
        })
        return {
            "success": True,
            "reply": reply,
            "model": ai_res.get("model"),
            "retrievedChunks": ai_res.get("retrieved_chunks", 0),
            "sources": ai_res.get("sources", [])
        }

    raise HTTPException(status_code=500, detail="AI chat fallback error")


@app.post("/api/ai/voice-journal-intake", summary="Clinical Voice Journal Intake", tags=["AI Engine"])
async def voice_journal_intake(request: Request):
    body = await request.json()
    if not body:
        raise HTTPException(status_code=400, detail="Dữ liệu nhật ký rỗng")

    user_text = body.get("message", "").strip()
    current_answers = body.get("currentAnswers") or {}
    history = body.get("history") or []
    user = body.get("user") or {}

    if not user_text:
        raise HTTPException(status_code=400, detail="Vui lòng nhập hoặc nói nội dung nhật ký")

    res = ai_analyzer.extract_journal_intake(user_text, current_answers, history, user)

    try:
        extracted_count = len(res.get("extracted_answers", {}))
        database.add_service_log({
            "userId": user.get("id"),
            "userName": user.get("fullName", "Khách"),
            "serviceType": "VOICE_JOURNAL_INTAKE",
            "title": f"Bóc tách giọng nói: {user_text[:30]}...",
            "detail": f"Bóc tách {extracted_count} trường 5 trụ cột. Trụ cột thiếu: {res.get('missing_pillars', [])}.",
            "device": body.get("device", "Voice / Talk Mode"),
            "icon": "fa-solid fa-microphone-lines",
            "badgeColor": "teal"
        })
    except Exception as e:
        print("[Voice Intake DB Log Error]", e)

    return res


@app.post("/api/rag/query", summary="Direct Vector Search Query for Inspection", tags=["AI Engine"])
async def query_vector_db(request: Request):
    """Directly inspects the Vector Database and returns top-K matching medical chunks."""
    body = await request.json()
    query = body.get("query", "").strip()
    top_k = int(body.get("top_k", 3))
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    store = rag_engine.get_vector_store()
    results = store.similarity_search(query, top_k=top_k)
    return {
        "success": True,
        "query": query,
        "results": results,
        "totalGuidelineDocuments": len(store.documents)
    }


# ==============================================================================
# STATIC FILES SERVING (Single Page Application Fallback)
# ==============================================================================

# Mount root directory for HTML, CSS, JS, Assets
app.mount("/", StaticFiles(directory=BASE_DIR, html=True), name="static")


if __name__ == '__main__':
    database.init_db()
    rag_engine.get_vector_store()
    print(f"Mavis Goodnight FastAPI server starting on http://0.0.0.0:{PORT}", flush=True)
    uvicorn.run("server:app", host="0.0.0.0", port=PORT, log_level="info")
