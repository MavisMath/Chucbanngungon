import os
import sys
import json
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from datetime import datetime

# Import SQLite Database Engine
import database
import ai_analyzer

PORT = int(os.environ.get('PORT', 8080))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class SleepSyncAPIHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {self.client_address[0]} - " + (format % args), flush=True)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json_body(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                raw = self.rfile.read(content_length).decode('utf-8')
                return json.loads(raw)
        except Exception as e:
            print("[JSON Parse Error]", e)
        return None

    def do_GET(self):
        try:
            clean_path = self.path.split('?')[0]
            if clean_path == '/api/users':
                self.handle_get_users()
            elif clean_path == '/api/stats':
                self.handle_get_stats()
            elif clean_path == '/api/logs':
                self.handle_get_logs()
            elif clean_path == '/api/diagnoses':
                self.handle_get_diagnoses()
            elif clean_path == '/api/export':
                self.handle_export_db()
            elif clean_path == '/api/database/status':
                self.handle_database_status()
            else:
                # Normal static file
                super().do_GET()
        except Exception as e:
            print("[GET Exception]", e, flush=True)

    def do_POST(self):
        print(f"[HTTP POST] {self.path}", flush=True)
        try:
            clean_path = self.path.split('?')[0]
            if clean_path == '/api/sync':
                self.handle_sync()
            elif clean_path == '/api/auth/login':
                self.handle_login()
            elif clean_path == '/api/auth/register':
                self.handle_register()
            elif clean_path == '/api/users':
                self.handle_save_user()
            elif clean_path == '/api/users/delete':
                self.handle_delete_user()
            elif clean_path == '/api/diagnoses':
                self.handle_save_diagnosis()
            elif clean_path == '/api/logs':
                self.handle_add_log()
            elif clean_path == '/api/reset':
                self.handle_reset_db()
            elif clean_path == '/api/ai/analyze-sleep':
                self.handle_ai_analyze_sleep()
            elif clean_path == '/api/ai/chat':
                self.handle_ai_chat()
            elif clean_path == '/api/ai/voice-journal-intake':
                self.handle_voice_journal_intake()
            else:
                self.send_error(404, "Endpoint Not Found")
        except Exception as e:
            print("[POST Exception]", e, flush=True)
            try:
                self.send_json({"success": False, "error": str(e)}, 500)
            except Exception:
                pass

    # -----------------------------
    # API HANDLERS (SQL BACKED)
    # -----------------------------
    def handle_get_users(self):
        users = database.list_all_users()
        active_id = database.get_active_user_id()
        self.send_json({"success": True, "users": users, "activeUserId": active_id})

    def handle_get_stats(self):
        stats = database.get_stats()
        self.send_json({"success": True, "stats": stats})

    def handle_get_logs(self):
        logs = database.list_service_logs(limit=150)
        self.send_json({"success": True, "logs": logs})

    def handle_get_diagnoses(self):
        diagnoses = database.list_diagnoses(limit=100)
        self.send_json({"success": True, "diagnoses": diagnoses})

    def handle_export_db(self):
        data = database.export_full_database()
        self.send_json(data)

    def handle_database_status(self):
        stats = database.get_stats()
        self.send_json({
            "success": True,
            "engine": "SQLite 3",
            "file": database.DB_FILE,
            "schemaFile": database.SCHEMA_FILE,
            "stats": stats
        })

    def handle_login(self):
        body = self.read_json_body()
        if not body:
            self.send_json({"success": False, "message": "Dữ liệu không hợp lệ"}, 400)
            return

        phone_or_id = body.get("phoneOrId", "").strip()
        password = body.get("password", "").strip()
        device = body.get("device", "Web/Mobile")

        if not phone_or_id:
            self.send_json({"success": False, "message": "Vui lòng nhập tên tài khoản hoặc số điện thoại!"}, 400)
            return

        found_user = database.find_user_for_login(phone_or_id)

        if found_user:
            # Check password if user has password set
            user_pwd = found_user.get("password", "")
            if password and user_pwd and password != user_pwd:
                self.send_json({"success": False, "message": "Mật khẩu không chính xác. Vui lòng thử lại!"}, 401)
                return

            # Update lastLoginAt in SQL database
            database.update_user(found_user["id"], {"lastLoginAt": datetime.now().isoformat()})
            database.set_active_user_id(found_user["id"])

            # Log login event in SQL
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

            # Fetch user's diagnoses from SQL
            user_diags = database.list_diagnoses(user_id=found_user["id"])

            self.send_json({
                "success": True,
                "user": found_user,
                "diagnoses": user_diags,
                "message": f"Chào mừng {found_user['fullName']} đã đăng nhập thành công!"
            })
        else:
            self.send_json({
                "success": False, 
                "message": "Không tìm thấy tài khoản với thông tin này. Bạn vui lòng kiểm tra lại hoặc chuyển sang tab Đăng Ký để tạo tài khoản mới!"
            }, 404)

    def handle_register(self):
        body = self.read_json_body()
        if not body:
            self.send_json({"success": False, "message": "Dữ liệu không hợp lệ"}, 400)
            return

        full_name = body.get("fullName", "").strip()
        phone = body.get("phone", "").strip()
        password = body.get("password", "").strip() or "123456"
        device = body.get("device", "Web Browser")

        if not full_name or not phone:
            self.send_json({"success": False, "message": "Vui lòng nhập họ tên và số điện thoại!"}, 400)
            return

        # Check existing user in SQL database
        existing = database.find_user_for_login(phone)
        if existing:
            self.send_json({
                "success": False, 
                "message": "Số điện thoại/Username này đã được đăng ký. Vui lòng chuyển sang tab Đăng Nhập!"
            }, 409)
            return

        # Insert new user into SQL database
        new_user = database.create_user(body)
        database.set_active_user_id(new_user["id"])

        # Log registration event in SQL
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

        self.send_json({
            "success": True,
            "user": new_user,
            "message": "Đăng ký tài khoản thành công! Dữ liệu đã được lưu trữ an toàn vào Cơ Sở Dữ Liệu SQL."
        })

    def handle_sync(self):
        body = self.read_json_body()
        if body:
            client_users = body.get("users", [])
            client_logs = body.get("serviceUsage", [])
            client_diags = body.get("diagnoses", [])
            device_type = body.get("deviceType", "Thiết bị người dùng")

            # Sync users into SQL
            for cu in client_users:
                cid = cu.get("id")
                if not cid:
                    continue
                existing = database.get_user_by_id(cid)
                if not existing:
                    database.create_user(cu)
                else:
                    database.update_user(cid, cu)

            # Sync logs into SQL
            for cl in client_logs:
                cl["device"] = device_type
                database.add_service_log(cl)

            # Sync diagnoses into SQL
            for cd in client_diags:
                cd["device"] = device_type
                database.save_diagnosis(cd)

        full_data = database.export_full_database()
        self.send_json({
            "success": True,
            "message": "Đồng bộ Cơ Sở Dữ Liệu SQL thành công!",
            "serverTime": datetime.now().isoformat(),
            "data": full_data
        })

    def handle_save_user(self):
        body = self.read_json_body()
        if not body:
            self.send_json({"success": False, "message": "Dữ liệu rỗng"}, 400)
            return

        user_id = body.get("id")
        if user_id and database.get_user_by_id(user_id):
            updated_user = database.update_user(user_id, body)
            self.send_json({"success": True, "message": "Cập nhật người dùng thành công trong SQL!", "user": updated_user})
        else:
            new_user = database.create_user(body)
            self.send_json({"success": True, "message": "Thêm mới người dùng thành công vào SQL!", "user": new_user})

    def handle_delete_user(self):
        body = self.read_json_body()
        if not body or not body.get("userId"):
            self.send_json({"success": False, "message": "Thiếu userId"}, 400)
            return

        target_id = body.get("userId")
        deleted = database.delete_user(target_id)
        if deleted:
            if database.get_active_user_id() == target_id:
                database.set_active_user_id(None)
            self.send_json({"success": True, "message": "Đã xóa người dùng khỏi SQL Database thành công!"})
        else:
            self.send_json({"success": False, "message": "Không tìm thấy người dùng trong SQL"}, 404)

    def handle_save_diagnosis(self):
        body = self.read_json_body()
        if not body:
            self.send_json({"success": False}, 400)
            return

        saved_diag = database.save_diagnosis(body)
        self.send_json({"success": True, "diagnosis": saved_diag})

    def handle_add_log(self):
        body = self.read_json_body()
        if not body:
            self.send_json({"success": False}, 400)
            return

        saved_log = database.add_service_log(body)
        self.send_json({"success": True, "log": saved_log})

    def handle_reset_db(self):
        database.reset_database()
        self.send_json({
            "success": True, 
            "message": "Đã làm sạch Cơ Sở Dữ Liệu SQL! Toàn bộ bảng đã sẵn sàng cho tài khoản người dùng thực."
        })

    def handle_ai_analyze_sleep(self):
        print("[AI Endpoint] Handling analyze sleep request...", flush=True)
        body = self.read_json_body()
        if not body:
            self.send_json({"success": False, "message": "Dữ liệu khảo sát rỗng"}, 400)
            return

        result = ai_analyzer.analyze_sleep_survey(body)
        print(f"[AI Endpoint] Completed: {result.get('aiEngine')} - Score: {result.get('predictedScore')}", flush=True)

        # Save diagnosis to SQL database
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
            "timestamp": datetime.now().isoformat()
        }
        database.save_diagnosis(diag_entry)

        # Log AI analysis service event
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

        self.send_json({"success": True, "analysis": result, "diagnosisId": diag_id})

    def handle_ai_chat(self):
        body = self.read_json_body()
        if not body:
            self.send_json({"success": False, "message": "Tin nhắn rỗng"}, 400)
            return

        query = body.get("message", "").strip()
        user = body.get("user") or {}

        if not query:
            self.send_json({"success": False, "message": "Vui lòng nhập nội dung câu hỏi"}, 400)
            return

        ai_res = ai_analyzer.chat_with_mavis(query, user)
        if ai_res and ai_res.get("success"):
            reply = ai_res.get("reply")
            # Log chat into SQL database
            database.add_service_log({
                "userId": user.get("id"),
                "userName": user.get("fullName", "Khách"),
                "serviceType": "AI_CHATBOT_GEMINI",
                "title": f"Mavis Chat: {query[:35]}...",
                "detail": f"Model: {ai_res.get('model')} - Phản hồi câu hỏi sức khỏe/giấc ngủ.",
                "device": body.get("device", "Web"),
                "icon": "fa-solid fa-comments",
                "badgeColor": "indigo"
            })
            self.send_json({"success": True, "reply": reply, "model": ai_res.get("model")})
        else:
            self.send_json({"success": False, "message": "AI chat fallback"}, 500)

    def handle_voice_journal_intake(self):
        body = self.read_json_body()
        if not body:
            self.send_json({"success": False, "message": "Dữ liệu nhật ký rỗng"}, 400)
            return

        user_text = body.get("message", "").strip()
        current_answers = body.get("currentAnswers") or {}
        history = body.get("history") or []
        user = body.get("user") or {}

        if not user_text:
            self.send_json({"success": False, "message": "Vui lòng nhập hoặc nói nội dung nhật ký"}, 400)
            return

        res = ai_analyzer.extract_journal_intake(user_text, current_answers, history, user)

        # Log into SQL database for transparency
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

        self.send_json(res)


if __name__ == '__main__':
    database.init_db()
    server_address = ('0.0.0.0', PORT)
    httpd = ThreadingHTTPServer(server_address, SleepSyncAPIHandler)
    print(f"Mavis chúc bạn ngủ ngon server running on http://localhost:{PORT}", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
