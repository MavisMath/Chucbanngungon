import os
import sys
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime

PORT = int(os.environ.get('PORT', 8080))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, 'server_database.json')

# Default Seed Data if DB file does not exist
DEFAULT_DB = {
    "users": [
        {
            "id": "user_hungnv",
            "fullName": "Nguyễn Văn Hùng",
            "verified": True,
            "role": "Kỹ Sư IT & Công Trình",
            "bio": "Thức khuya & mê cà phê • Đang cải thiện giấc ngủ sâu NREM 💤",
            "age": "30 tuổi (Nam)",
            "gender": "Nam",
            "occupation": "Kỹ Sư IT & Công Trình",
            "phone": "0981 234 567",
            "email": "hung.nguyen@example.com",
            "password": "123456",
            "targetBedtime": "23:00",
            "wakeTime": "06:30",
            "fitnessLevel": "Trung bình",
            "healthConditions": [
                "Đau mỏi cổ vai gáy",
                "Căng thẳng deadline",
                "Ngồi nhiều máy tính"
            ],
            "avatarType": "programmer_laptop",
            "createdAt": "2026-10-20T08:00:00.000Z",
            "lastLoginAt": "2026-10-24T18:00:00.000Z"
        },
        {
            "id": "user_maitt",
            "fullName": "Trần Thị Mai",
            "verified": True,
            "role": "Trưởng Phòng Nhân Sự",
            "bio": "Dễ thức giấc nửa đêm • Mục tiêu ngủ thẳng giấc 7 tiếng 🌸",
            "age": "38 tuổi (Nữ)",
            "gender": "Nữ",
            "occupation": "Trưởng Phòng Nhân Sự",
            "phone": "0912 345 678",
            "email": "mai.tran@example.com",
            "password": "123456",
            "targetBedtime": "22:00",
            "wakeTime": "06:00",
            "fitnessLevel": "Khá",
            "healthConditions": [
                "Khó ngủ sau 1h sáng",
                "Áp lực công việc",
                "Bốc hỏa tiền mãn kinh nhẹ"
            ],
            "avatarType": "woman_professional",
            "createdAt": "2026-10-21T09:30:00.000Z",
            "lastLoginAt": "2026-10-24T18:15:00.000Z"
        }
    ],
    "activeUserId": "user_hungnv",
    "serviceUsage": [
        {
            "id": 1,
            "userId": "user_hungnv",
            "userName": "Nguyễn Văn Hùng",
            "serviceType": "AUTH_LOGIN",
            "title": "Đăng nhập hệ thống",
            "detail": "Tài khoản Nguyễn Văn Hùng đã đăng nhập và đồng bộ từ thiết bị.",
            "timestamp": "2026-10-24T18:00:00.000Z",
            "device": "Web Browser"
        },
        {
            "id": 2,
            "userId": "user_hungnv",
            "userName": "Nguyễn Văn Hùng",
            "serviceType": "DIAGNOSIS_5PILLARS",
            "title": "Khảo sát 5 Trụ Cột Y Khoa",
            "detail": "Điểm dự báo giấc ngủ 68%. Mức độ stress trung bình, đau cổ vai gáy.",
            "timestamp": "2026-10-24T19:30:00.000Z",
            "device": "Mobile App (PWA)"
        },
        {
            "id": 3,
            "userId": "user_hungnv",
            "userName": "Nguyễn Văn Hùng",
            "serviceType": "AI_CHATBOT_GEMINI",
            "title": "Hỏi đáp Trợ lý AI Gemini",
            "detail": "Hỏi về thực phẩm ăn tối hỗ trợ giấc ngủ tự nhiên.",
            "timestamp": "2026-10-24T20:15:00.000Z",
            "device": "Mobile App (PWA)"
        }
    ],
    "diagnoses": []
}

def load_db():
    if not os.path.exists(DB_FILE):
        save_db(DEFAULT_DB)
        return DEFAULT_DB
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print("[Server DB Load Error]", e)
        return DEFAULT_DB

def save_db(data):
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print("[Server DB Save Error]", e)
        return False

class SleepSyncAPIHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {self.client_address[0]} - " + (format % args), flush=True)

    def do_OPTIONS(self):
        print(f"[HTTP OPTIONS] {self.path}", flush=True)
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

    def do_GET(self):
        print(f"[HTTP GET] {self.path}", flush=True)
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
            else:
                # Normal static file
                super().do_GET()
        except Exception as e:
            print("[GET Exception]", e, flush=True)

    def do_POST(self):
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
            else:
                self.send_error(404, "Endpoint Not Found")
        except Exception as e:
            print("[POST Exception]", e)

    def read_json_body(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                raw = self.rfile.read(content_length).decode('utf-8')
                return json.loads(raw)
        except Exception as e:
            print("[JSON Parse Error]", e)
        return None

    # -----------------------------
    # API HANDLERS
    # -----------------------------
    def handle_get_users(self):
        db = load_db()
        self.send_json({"success": True, "users": db.get("users", []), "activeUserId": db.get("activeUserId")})

    def handle_get_stats(self):
        db = load_db()
        users = db.get("users", [])
        logs = db.get("serviceUsage", [])
        diags = db.get("diagnoses", [])
        
        guardrail_count = sum(1 for l in logs if 'GUARDRAIL' in str(l.get('serviceType', '')))
        ai_chat_count = sum(1 for l in logs if 'AI_CHAT' in str(l.get('serviceType', '')))
        diag_count = len(diags) + sum(1 for l in logs if 'DIAGNOSIS' in str(l.get('serviceType', '')))

        stats = {
            "totalUsers": len(users),
            "totalDiagnoses": diag_count,
            "totalAiChats": ai_chat_count,
            "totalGuardrailBlocks": guardrail_count,
            "totalLogs": len(logs),
            "lastSync": datetime.now().strftime("%H:%M:%S %d/%m/%Y"),
            "serverStatus": "Online (Đồng bộ Cloud hoạt động)"
        }
        self.send_json({"success": True, "stats": stats})

    def handle_get_logs(self):
        db = load_db()
        self.send_json({"success": True, "logs": db.get("serviceUsage", [])})

    def handle_get_diagnoses(self):
        db = load_db()
        self.send_json({"success": True, "diagnoses": db.get("diagnoses", [])})

    def handle_export_db(self):
        db = load_db()
        self.send_json(db)

    def handle_login(self):
        body = self.read_json_body()
        if not body:
            self.send_json({"success": False, "message": "Dữ liệu không hợp lệ"}, 400)
            return

        phone_or_id = body.get("phoneOrId", "").strip()
        password = body.get("password", "").strip()
        db = load_db()
        found_user = None

        clean_input = phone_or_id.replace(" ", "").lower()
        for u in db.get("users", []):
            u_id = (u.get("id") or "").lower()
            u_phone = (u.get("phone") or "").replace(" ", "").lower()
            u_email = (u.get("email") or "").lower()
            u_name = (u.get("fullName") or "").lower()
            u_username = (u.get("username") or "").lower()
            if (
                clean_input in [u_id, u_id.replace("user_", ""), u_phone, u_email, u_username]
                or ("user_" + clean_input) == u_id
                or phone_or_id.lower() == u_name
            ):
                found_user = u
                break

        if found_user:
            # Check password if provided and user has password
            user_pwd = found_user.get("password", "123456")
            if password and user_pwd and password != user_pwd:
                self.send_json({"success": False, "message": "Mật khẩu không chính xác. Vui lòng thử lại!"}, 401)
                return

            found_user["lastLoginAt"] = datetime.now().isoformat()
            db["activeUserId"] = found_user["id"]

            # Log login event
            device = body.get("device", "Web/Mobile")
            db.setdefault("serviceUsage", []).insert(0, {
                "id": int(datetime.now().timestamp() * 1000),
                "userId": found_user["id"],
                "userName": found_user["fullName"],
                "serviceType": "AUTH_LOGIN",
                "title": "Đăng nhập tài khoản",
                "detail": f"Người dùng {found_user['fullName']} đã đăng nhập thành công vào hệ thống.",
                "timestamp": datetime.now().isoformat(),
                "device": device
            })

            save_db(db)

            # Return user's past diagnoses if any
            user_diags = [d for d in db.get("diagnoses", []) if d.get("userId") == found_user["id"]]

            self.send_json({
                "success": True,
                "user": found_user,
                "diagnoses": user_diags,
                "message": f"Chào mừng {found_user['fullName']} đã đăng nhập thành công!"
            })
        else:
            self.send_json({"success": False, "message": "Không tìm thấy tài khoản với thông tin này. Bạn vui lòng kiểm tra lại hoặc chuyển sang tab Đăng ký!"}, 404)

    def handle_register(self):
        body = self.read_json_body()
        if not body:
            self.send_json({"success": False, "message": "Dữ liệu không hợp lệ"}, 400)
            return

        full_name = body.get("fullName", "").strip()
        phone = body.get("phone", "").strip()
        password = body.get("password", "").strip() or "123456"

        if not full_name or not phone:
            self.send_json({"success": False, "message": "Vui lòng nhập họ tên và số điện thoại!"}, 400)
            return

        db = load_db()
        users = db.setdefault("users", [])

        # Check existing phone or id
        for u in users:
            if u.get("phone") == phone:
                self.send_json({"success": False, "message": "Số điện thoại này đã được đăng ký trong hệ thống. Vui lòng chuyển sang tab Đăng Nhập!"}, 409)
                return

        new_user = {
            "id": "user_" + str(int(datetime.now().timestamp())),
            "fullName": full_name,
            "phone": phone,
            "password": password,
            "email": body.get("email", ""),
            "verified": True,
            "role": body.get("role", "Thành viên SleepSync"),
            "bio": body.get("bio", "Mục tiêu cải thiện chất lượng giấc ngủ sâu NREM 💤"),
            "age": body.get("age", "28 tuổi"),
            "gender": body.get("gender", "Khác"),
            "occupation": body.get("occupation", body.get("role", "Tự do")),
            "targetBedtime": body.get("targetBedtime", "23:00"),
            "wakeTime": body.get("wakeTime", "06:30"),
            "fitnessLevel": body.get("fitnessLevel", "Trung bình"),
            "healthConditions": body.get("healthConditions", ["Sức khỏe ổn định"]),
            "avatarType": body.get("avatarType", "programmer_laptop"),
            "createdAt": datetime.now().isoformat(),
            "lastLoginAt": datetime.now().isoformat()
        }

        users.append(new_user)
        db["activeUserId"] = new_user["id"]

        device = body.get("device", "Web Browser")
        db.setdefault("serviceUsage", []).insert(0, {
            "id": int(datetime.now().timestamp() * 1000),
            "userId": new_user["id"],
            "userName": new_user["fullName"],
            "serviceType": "AUTH_REGISTER",
            "title": "Đăng ký thành viên mới",
            "detail": f"Thành viên mới {new_user['fullName']} ({new_user['phone']}) đã tạo tài khoản và đồng bộ thành công.",
            "timestamp": datetime.now().isoformat(),
            "device": device
        })

        save_db(db)
        self.send_json({
            "success": True,
            "user": new_user,
            "message": "Đăng ký tài khoản thành công! Dữ liệu đã được lưu trữ vào Database."
        })

    def handle_sync(self):
        body = self.read_json_body()
        db = load_db()

        if body:
            client_users = body.get("users", [])
            client_logs = body.get("serviceUsage", [])
            client_diags = body.get("diagnoses", [])
            device_type = body.get("deviceType", "Thiết bị người dùng")

            # Merge Users
            user_map = {u["id"]: u for u in db.get("users", [])}
            for cu in client_users:
                cid = cu.get("id")
                if not cid:
                    continue
                if cid not in user_map:
                    user_map[cid] = cu
                else:
                    user_map[cid].update(cu)

            db["users"] = list(user_map.values())

            # Merge Logs
            existing_log_ids = {l.get("id") for l in db.get("serviceUsage", [])}
            for cl in client_logs:
                if cl.get("id") not in existing_log_ids:
                    cl["device"] = device_type
                    db.setdefault("serviceUsage", []).append(cl)

            db["serviceUsage"] = sorted(db.get("serviceUsage", []), key=lambda x: str(x.get("timestamp", "")), reverse=True)[:150]

            # Merge Diagnoses
            existing_diag_ids = {d.get("id") for d in db.get("diagnoses", [])}
            for cd in client_diags:
                if cd.get("id") not in existing_diag_ids:
                    db.setdefault("diagnoses", []).append(cd)

            save_db(db)

        self.send_json({
            "success": True,
            "message": "Đồng bộ đám mây thành công!",
            "serverTime": datetime.now().isoformat(),
            "data": db
        })

    def handle_save_user(self):
        body = self.read_json_body()
        if not body:
            self.send_json({"success": False, "message": "Dữ liệu rỗng"}, 400)
            return

        db = load_db()
        users = db.setdefault("users", [])
        user_id = body.get("id")

        if user_id:
            updated = False
            for idx, u in enumerate(users):
                if u.get("id") == user_id:
                    users[idx].update(body)
                    users[idx]["updatedAt"] = datetime.now().isoformat()
                    updated = True
                    break
            if not updated:
                users.append(body)
        else:
            new_id = "user_" + str(int(datetime.now().timestamp()))
            body["id"] = new_id
            body["createdAt"] = datetime.now().isoformat()
            users.append(body)

        save_db(db)
        self.send_json({"success": True, "message": "Lưu người dùng thành công!", "user": body})

    def handle_delete_user(self):
        body = self.read_json_body()
        if not body or not body.get("userId"):
            self.send_json({"success": False, "message": "Thiếu userId"}, 400)
            return

        target_id = body.get("userId")
        db = load_db()
        users = db.get("users", [])
        new_users = [u for u in users if u.get("id") != target_id]

        if len(new_users) == len(users):
            self.send_json({"success": False, "message": "Không tìm thấy người dùng"}, 404)
            return

        db["users"] = new_users
        if db.get("activeUserId") == target_id:
            db["activeUserId"] = new_users[0]["id"] if new_users else None

        save_db(db)
        self.send_json({"success": True, "message": "Đã xóa người dùng thành công!"})

    def handle_save_diagnosis(self):
        body = self.read_json_body()
        if not body:
            self.send_json({"success": False}, 400)
            return

        db = load_db()
        diags = db.setdefault("diagnoses", [])
        body["id"] = body.get("id") or int(datetime.now().timestamp() * 1000)
        body["timestamp"] = body.get("timestamp") or datetime.now().isoformat()
        diags.append(body)
        save_db(db)
        self.send_json({"success": True, "diagnosis": body})

    def handle_add_log(self):
        body = self.read_json_body()
        if not body:
            self.send_json({"success": False}, 400)
            return

        db = load_db()
        logs = db.setdefault("serviceUsage", [])
        body["id"] = body.get("id") or int(datetime.now().timestamp() * 1000)
        body["timestamp"] = body.get("timestamp") or datetime.now().isoformat()
        logs.insert(0, body)
        save_db(db)
        self.send_json({"success": True, "log": body})

    def handle_reset_db(self):
        save_db(DEFAULT_DB)
        self.send_json({"success": True, "message": "Đã thiết lập lại database về mặc định!"})


if __name__ == '__main__':
    server_address = ('0.0.0.0', PORT)
    httpd = HTTPServer(server_address, SleepSyncAPIHandler)
    print(f"SleepSync server running on http://localhost:{PORT}", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
