"""
MAVIS CHÚC BẠN NGỦ NGON - REAL-TIME HYPER-PERSONALIZED CLINICAL ANALYZER
Dual-Engine System:
1. Cloud Engine: Google Gemini API (using user-provided key & Gemini 3.5 models)
2. Local Smart Semantic Engine: Deep Rule-based & Semantic Vietnamese NLP Parser
   (Runs 100% offline with zero external API key requirements).
"""

import os
import re
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

# Google Gemini API Key is loaded securely from environment variable or .env file
DEFAULT_GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "")

def load_env():
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        k, v = line.split('=', 1)
                        k = k.strip()
                        v = v.strip().strip('"').strip("'")
                        if k and not os.environ.get(k):
                            os.environ[k] = v
        except Exception:
            pass

load_env()

# Safety Guardrails: Strictly forbidden medicine / supplement patterns
FORBIDDEN_PATTERNS = [
    r'\b(thu[ố][c|k]|thuoc)\b',
    r'\b(thu[ố]c ng[ủu]|thuoc ngu)\b',
    r'\b(thu[ố]c an th[ầ]n|thuoc an than)\b',
    r'\b(th[ự]c ph[ẩ]m ch[ứ]c n[ắ]ng|thuc pham chuc nang|tpcn)\b',
    r'\b(seduxen|stilnox|rotunda|valium|lexomil|ambien|olanzapine|diazepam)\b'
]

def check_guardrails(text):
    """Returns True if text violates safety guidelines."""
    if not text:
        return False
    lower = text.lower()
    return any(re.search(p, lower, re.IGNORECASE) for p in FORBIDDEN_PATTERNS)



def build_targeted_health_advice(answers, user_bedtime="23:00"):
    """
    Builds strictly personalized, symptom-specific solutions based ONLY
    on what the user actually reported. Never recommends for conditions the user does not have.
    """
    ans = answers or {}
    def has(key, val):
        v = ans.get(key)
        if isinstance(v, list):
            return val in v
        return v == val

    items = []

    # 1. Điện thoại trên giường / Nghiện màn hình TikTok/FB
    if has("bed_phone", "lướt_tiktok_fb") or has("env_light", "screen_heavy"):
        items.append(
            "<p><strong>📱 Cắt Đứt Vòng Lặp Dopamine & Cai Nghiện Điện Thoại Giường Ngủ:</strong> "
            "Kích hoạt chế độ Grayscale (màn hình đen trắng) từ 21:00 để triệt tiêu sức hút thị giác của video ngắn TikTok/Facebook. "
            f"Cắm sạc điện thoại ở bàn làm việc cách giường ít nhất 2 mét trước {user_bedtime} để phá vỡ phản xạ với tay lướt màn hình ban đêm. "
            "Dùng đồng hồ báo thức rời thay vì để điện thoại ngay đầu giường.</p>"
        )

    # 2. Căng thẳng / Suy nghĩ miên man / Trạng thái cảm xúc
    if has("stress_level", "medium") or has("stress_level", "high") or has("mood_state", "anxious") or has("mood_state", "brain_fog"):
        items.append(
            "<p style=\"margin-top:0.4rem;\"><strong>🧠 Xả Trầm Não Bộ (Brain Dump) & Giảm Cortisol:</strong> "
            "Dành 3 phút trước khi ngủ viết toàn bộ suy nghĩ, nỗi lo và danh sách việc cần làm ngày mai ra 1 cuốn sổ tay (kỹ thuật Brain Dump) "
            "để dọn sạch bộ nhớ đệm của vỏ não trước trán. Kết hợp bài tập thở 4-7-8 (hít 4s - giữ 7s - thở 8s) để kích hoạt hệ thần kinh đối giao cảm.</p>"
        )

    # 3. Trào ngược dạ dày (GERD) - CHỈ hiển thị nếu người dùng THỰC SỰ chọn hoặc ăn tối quá muộn
    if has("chronic_condition", "gerd") or has("dinner_habit", "heavy_late"):
        items.append(
            "<p style=\"margin-top:0.4rem;\"><strong>🫀 Khắc Phục Trào Ngược Axit Dạ Dày (GERD):</strong> "
            "Ăn tối trước giờ ngủ ít nhất 3 tiếng. Khi ngủ, nằm nghiêng sang bên TRÁI "
            "(tư thế này giữ van tâm vị cơ thắt thực quản nằm phía trên mức dịch vị axit, chống trào ngược tự nhiên). "
            "Kê đầu giường hoặc gối nâng cao thêm 10-15cm.</p>"
        )

    # 4. Đau mỏi cổ vai gáy - CHỈ hiển thị nếu người dùng THỰC SỰ bị
    if has("physical_pain", "neck_back_pain") or "neck" in str(ans.get("physical_pain", [])):
        items.append(
            "<p style=\"margin-top:0.4rem;\"><strong>🦴 Khắc Phục Đau Mỏi Cổ Vai Gáy:</strong> "
            "Dùng gối cao vừa phải (7-10cm) nâng đỡ đường cong sinh lý cột sống cổ C1-C7. Tránh tuyệt đối tư thế nằm sấp. "
            "Đặt 1 chiếc gối mỏng dưới khớp gối khi nằm ngửa để giải tỏa áp lực đĩa đệm cột sống thắt lưng.</p>"
        )

    # 5. Đau đầu căng thẳng
    if has("physical_pain", "headache"):
        items.append(
            "<p style=\"margin-top:0.4rem;\"><strong>💆 Giảm Đau Đầu Căng Thẳng:</strong> "
            "Chườm ấm vùng mắt và trán 5 phút trước giờ ngủ, kết hợp day ấn nhẹ huyệt Thái Dương và huyệt Phong Trì sau gáy "
            "để giải tỏa co thắt mạch máu não và thư giãn màng não.</p>"
        )

    # 6. Nhiệt độ phòng nóng hoặc Bốc hỏa mãn kinh
    if has("env_temp", "hot") or has("hormone_state", "menopause_hotflash"):
        items.append(
            "<p style=\"margin-top:0.4rem;\"><strong>❄️ Khắc Phục Nhiệt Độ Nóng & Bốc Hỏa:</strong> "
            "Cài đặt điều hòa ở mức lý tưởng 24-26°C hoặc dùng quạt nhẹ thoảng chân. "
            "Tắm nước ấm trước giờ ngủ 45 phút để kích hoạt cơ chế giãn mạch ngoại vi, giúp cơ thể hạ nhiệt độ trung tâm 1°C khi vào giường.</p>"
        )

    # 7. Tiểu đêm
    if has("chronic_condition", "nocturia") or has("dinner_habit", "drink_lots_water"):
        items.append(
            "<p style=\"margin-top:0.4rem;\"><strong>🚽 Khắc Phục Thức Giấc Tiểu Đêm:</strong> "
            "Cắt giảm toàn bộ lượng nước uống sau 20:00. Áp dụng kỹ thuật 'đi tiểu kép' (Double Voiding): "
            f"1 lần lúc chuẩn bị ngủ và 1 lần nữa sát lúc bước lên giường lúc {user_bedtime}.</p>"
        )

    # 8. Cà phê muộn
    if has("caffeine_usage", "late_high") or has("caffeine_usage", "medium_afternoon"):
        items.append(
            "<p style=\"margin-top:0.4rem;\"><strong>☕ Quản Trị Cữ Caffeine:</strong> "
            f"Dừng nạp cà phê/trà đậm ít nhất 8 tiếng trước giờ ngủ {user_bedtime} để gan đào thải hoàn toàn Caffeine, "
            "giúp thụ thể Adenosine tự nhiên gắn kết tạo áp lực buồn ngủ sinh học.</p>"
        )

    # Fallback nếu người dùng hoàn toàn khỏe mạnh và không có thói quen xấu nào
    if not items:
        items.append(
            "<p>✨ <strong>Thể Trạng & Thói Quen Rất Tốt:</strong> Bạn không gặp vấn đề bệnh lý hay đau nhức cơ thể. "
            f"Chỉ cần duy trì phòng ngủ thoáng mát (24-26°C), giữ nhịp sinh học đều đặn và cất điện thoại trước {user_bedtime} "
            "là bạn sẽ duy trì được giấc ngủ sâu NREM tối ưu nhất.</p>"
        )

    return "".join(items)


def build_tailored_desk_exercises(answers):
    """
    Returns desk exercises strictly tailored to physical pain and habits.
    If user has NO neck/back pain, NEVER recommends Chin-Tuck C5-C7!
    Instead provides Eye relief (20-20-20), Box Breathing, and full-body stretch.
    """
    ans = answers or {}
    def has(key, val):
        v = ans.get(key)
        if isinstance(v, list):
            return val in v
        return v == val

    has_neck = has("physical_pain", "neck_back_pain") or "neck" in str(ans.get("physical_pain", []))

    if has_neck:
        return [
            "<strong>Động tác Chin-Tuck (1 phút):</strong> Ngồi thẳng lưng, thu cằm về phía sau như tạo 2 cằm, giữ 5 giây rồi thả lỏng. Lặp lại 5 lần để giải tỏa chèn ép rễ thần kinh đốt sống cổ C5-C7.",
            "<strong>Mở Ngực & Xương Bả Vai (1 phút):</strong> Đan hai tay ra sau gáy, hít sâu ưỡn ngực mở rộng hai khuỷu tay sang hai bên, thở ra từ từ để kéo giãn cơ ngực và giải phóng vai gáy.",
            "<strong>Kéo Giãn Thắt Lưng Tại Ghế (1 phút):</strong> Ngồi xoay thân người nhẹ nhàng sang trái rồi sang phải, tay giữ vào thành ghế để giải tỏa áp lực đĩa đệm thắt lưng."
        ]
    else:
        return [
            "<strong>Quy Tắc Thư Giãn Mắt 20-20-20 (Khi làm việc & dùng điện thoại):</strong> Cứ sau 20 phút nhìn màn hình, hướng tầm mắt nhìn một vật cách xa 6 mét trong 20 giây để thư giãn cơ thể mi mắt.",
            "<strong>Thở Hộp Vuông Box Breathing 4-4-4-4 (3 phút):</strong> Hít vào 4 giây - Nín thở 4 giây - Thở ra 4 giây - Nín thở 4 giây. Giúp hạ nhịp tim, giảm mệt mỏi và reset hệ thần kinh đang căng thẳng.",
            "<strong>Vươn Vai & Giãn Toàn Thân Tại Chỗ (1 phút):</strong> Đan hai tay vươn thẳng lên cao qua đầu, hít sâu kéo căng toàn bộ cơ liên sườn và cột sống để kích thích máu huyết lưu thông."
        ]


def ensure_full_micro_schedule(schedule_tasks, current_hour, current_time_str, user_bedtime, answers):
    """
    Guarantees a complete, chronotherapeutic roadmap of 4-6 micro-actions
    starting from the user's CURRENT time of day through bedtime.
    Strictly tailors content to user answers and eliminates advice for non-existent diseases.
    """
    has_gerd = False
    has_caffeine = False
    has_neck = False
    has_bed_phone = False

    if isinstance(answers, dict):
        if answers.get("chronic_condition") == "gerd" or "gerd" in str(answers.get("chronic_condition", [])) or answers.get("dinner_habit") == "heavy_late":
            has_gerd = True
        if answers.get("caffeine_usage") in ["late_high", "medium_afternoon"]:
            has_caffeine = True
        if "neck" in str(answers.get("physical_pain", [])) or answers.get("physical_pain") == "neck_shoulder" or "neck_back_pain" in str(answers.get("physical_pain", [])):
            has_neck = True
        if "lướt" in str(answers.get("bed_phone", [])) or "tiktok" in str(answers.get("bed_phone", [])) or answers.get("bed_phone") == "lướt_tiktok_fb":
            has_bed_phone = True

    # First, sanitize any tasks passed in from AI to strip hallucinated conditions
    if isinstance(schedule_tasks, list):
        for t in schedule_tasks:
            t_title = str(t.get("title", ""))
            t_desc = str(t.get("desc", ""))
            if not has_gerd:
                if "gerd" in t_title.lower() or "trào ngược" in t_title.lower():
                    t["title"] = "🚶 Vi-đi bộ 5 phút sau ăn trưa & Thư giãn"
                if "gerd" in t_desc.lower() or "trào ngược" in t_desc.lower():
                    t["desc"] = "Đi dạo nhẹ nhàng 5 phút kích thích tiêu hóa bữa trưa êm ái, chợp mắt Power Nap tối đa 15-20 phút để phục hồi năng lượng não bộ."
            if not has_neck:
                if "chin-tuck" in t_title.lower() or "c5-c7" in t_title.lower() or "cổ vai gáy" in t_title.lower():
                    t["title"] = "🧘 Thư giãn mắt 20-20-20 & Bài tập thở Box Breathing 4-4-4-4"
                if "c5-c7" in t_desc.lower() or "thu cằm" in t_desc.lower() or "đốt sống cổ" in t_desc.lower():
                    t["desc"] = "Nhìn xa 6m trong 20 giây giải tỏa áp lực điều tiết của mắt khi nhìn màn hình, kết hợp 3 phút thở 4 thì để xoa dịu hệ thần kinh và hạ hormone căng thẳng."

    pool = []

    # 1. Trưa (11:00 - 13:00)
    if current_hour <= 12:
        pool.append({
            "id": "m_noon",
            "time": "12:15 - 12:20 (5 phút sau ăn trưa)",
            "tag": "Chống trào ngược & Nhu động ruột" if has_gerd else "Đi dạo nhẹ & Phục hồi",
            "title": "🚶 Vi-đi bộ 5 phút quanh văn phòng (Chống trào ngược axit)" if has_gerd else "🚶 Đi dạo nhẹ nhàng 5 phút & Chợp mắt Power-Nap 15-20 phút",
            "desc": (
                "Giúp cơ thắt thực quản dưới đóng kín, hỗ trợ tiêu hóa thức ăn và ngăn trào ngược axit dạ dày (GERD). Chợp mắt Power Nap tối đa 15-20 phút."
                if has_gerd else
                "Đi dạo nhẹ nhàng giúp kích thích nhu động ruột tiêu hóa bữa trưa êm ái, sau đó chợp mắt ngắn 15-20 phút để phục hồi sự tỉnh táo cho não bộ mà không làm mất áp lực ngủ tối."
            )
        })

    # 2. Đầu chiều (13:00 - 14:30)
    if current_hour <= 14:
        pool.append({
            "id": "m_curfew",
            "time": "14:00 (1 phút tại bàn làm việc)",
            "tag": "Caffeine Curfew",
            "title": "🚰 Chốt cữ Caffeine - Đổi sang nước ấm hoặc trà hoa cúc",
            "desc": f"Đảm bảo khoảng cách 8-9 tiếng trước giờ ngủ {user_bedtime} để Adenosine tự nhiên tích tụ kịp thời trong não bộ, gan đào thải hết chất kích thích."
        })

    # 3. Xế chiều (14:30 - 16:30)
    if current_hour <= 16:
        pool.append({
            "id": "m_afternoon",
            "time": "15:45 - 15:50 (5 phút xả áp lực)",
            "tag": "Giải tỏa đốt sống cổ & Cortisol" if has_neck else "Thư giãn mắt & Reset năng lượng",
            "title": "🧘 Bài tập Chin-Tuck 10 lần + Giãn cơ cổ vai gáy" if has_neck else "🧘 Thư giãn mắt 20-20-20 & Bài tập thở Box Breathing 4-4-4-4",
            "desc": (
                "Thu cằm về sau giữ 5 giây giải phóng chèn ép rễ thần kinh đốt sống cổ C5-C7, giảm áp lực do ngồi lâu."
                if has_neck else
                "Nhìn xa 6m trong 20 giây giải tỏa áp lực điều tiết của mắt khi nhìn màn hình máy tính/điện thoại, kết hợp 3 phút thở 4 thì để xoa dịu hệ thần kinh và hạ hormone căng thẳng."
            )
        })

    # 4. Bữa tối & Hoàng hôn (17:30 - 19:30)
    if current_hour <= 19:
        pool.append({
            "id": "m_dinner",
            "time": "18:30 - 19:00 (Bữa tối nhanh)",
            "tag": "Dinh dưỡng Tryptophan & Tiêu hóa",
            "title": "🥗 Bữa tối thanh đạm giàu Magie & Cắt giảm nước sau 20:00",
            "desc": "Trứng luộc lòng đào / Ức gà + Canh rau bina/rau ngót + 1 quả kiwi tráng miệng. Cắt giảm uống nhiều nước sau 20:00 để tránh thức giấc tiểu đêm."
        })

    # 5. Tiền ngủ (21:00 - 22:15)
    pre_bed_hour = int(user_bedtime.split(':')[0]) - 1 if ':' in user_bedtime else 22
    pool.append({
        "id": "m_pre_bed",
        "time": f"{pre_bed_hour}:00 - {pre_bed_hour}:15 (30p trước ngủ)",
        "tag": "Cắt vòng lặp Dopamine màn hình" if has_bed_phone else "Digital Sunset & Hạ thân nhiệt",
        "title": "📱 Kích hoạt Grayscale & Cất điện thoại cách xa giường 2m" if has_bed_phone else "🛀 Tắm nước ấm 10 phút & Kích hoạt Digital Sunset",
        "desc": (
            "Chuyển màn hình điện thoại sang chế độ đen trắng (Grayscale) và cắm sạc ở bàn làm việc cách xa giường ngủ, ngăn thói quen lướt TikTok/FB trên giường."
            if has_bed_phone else
            "Nước ấm kích hoạt giãn mạch ngoại vi, hạ thân nhiệt trung tâm 1°C để cơ thể chuyển sang trạng thái ngủ sâu. Cất điện thoại xa giường."
        )
    })

    # 6. Vào giường ru ngủ
    pool.append({
        "id": "m_bedtime",
        "time": f"{user_bedtime} (Vào giường ngủ)",
        "tag": "Sóng não Delta & Ru ngủ",
        "title": "🎧 Bật sóng não Delta 4Hz ru ngủ & Hít thở 4-7-8",
        "desc": "Bật máy phát âm thanh sóng não ru ngủ trên ứng dụng, điều chỉnh phòng 24-26°C, nhắm mắt thả lỏng toàn thân để chìm vào giấc ngủ phục hồi."
    })

    # If AI provided at least 4 items and covers daytime when current_hour is daytime, validate it
    if isinstance(schedule_tasks, list) and len(schedule_tasks) >= 4:
        has_daytime_task = any(
            any(k in (str(t.get("time", "")) + str(t.get("title", ""))) for k in ["11:", "12:", "13:", "14:", "15:", "16:", "17:", "18:", "trưa", "chiều"])
            for t in schedule_tasks
        )
        if has_daytime_task or current_hour >= 18:
            return schedule_tasks

    # If AI returned fewer tasks or missing daytime, intelligently merge with pool
    if isinstance(schedule_tasks, list) and len(schedule_tasks) > 0:
        existing_str = " ".join(str(t.get("time", "")) + str(t.get("title", "")) for t in schedule_tasks)
        earlier_tasks = [p for p in pool if not any(p["time"][:5] in existing_str for _ in [0])]
        combined = earlier_tasks + schedule_tasks
        return combined[:6]

    return pool


def analyze_sleep_survey(payload):
    """
    Main entry point for AI analysis.
    Returns a structured dictionary of personalized insights, score, and real-time advice.
    """
    answers = payload.get("answers", {})
    custom_answers = payload.get("customAnswers", {}) or {}
    user = payload.get("user", {}) or {}

    # Extract current time in Vietnam local timezone
    client_local_hour = payload.get("localHour")
    client_local_time = payload.get("localTime") or payload.get("currentTime")

    current_hour = None
    current_time_str = None

    if client_local_hour is not None:
        try:
            current_hour = int(client_local_hour)
        except Exception:
            pass

    if client_local_time and isinstance(client_local_time, str):
        match = re.search(r"(\d{1,2}):(\d{2})", client_local_time)
        if match and "T" not in client_local_time:
            current_time_str = f"{int(match.group(1)):02d}:{match.group(2)}"
            if current_hour is None:
                current_hour = int(match.group(1))

    # If client passed ISO string or missing, use Vietnam timezone UTC+7
    if not current_time_str or current_hour is None:
        vn_time = datetime.now(timezone(timedelta(hours=7)))
        current_time_str = vn_time.strftime("%H:%M")
        current_hour = vn_time.hour

    # Priority 1: Cloud Gemini AI (if key is set in payload, env, or default)
    api_key = payload.get("apiKey") or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or DEFAULT_GEMINI_KEY
    if api_key:
        try:
            cloud_result = run_gemini_analysis(api_key, answers, custom_answers, user, current_hour, current_time_str)
            if cloud_result:
                model_used = cloud_result.get("geminiModelUsed", "3.5-flash")
                cloud_result["aiEngine"] = f"Google Gemini AI ({model_used})"
                cloud_result["aiEngineBadge"] = f"✨ Google Gemini Cloud AI ({model_used})"
                return cloud_result
        except Exception as e:
            print(f"[AI Analyzer] Gemini API fallback to Smart Semantic Engine: {e}", flush=True)

    # Priority 2: High-Performance Smart Semantic NLP Engine (Offline fallback)
    semantic_result = run_semantic_nlp_analysis(answers, custom_answers, user, current_hour, current_time_str)
    semantic_result["aiEngine"] = "Mavis Smart Semantic Engine (Local AI)"
    semantic_result["aiEngineBadge"] = "⚡ Smart Semantic NLP (Local AI - Tối ưu tiếng Việt)"
    return semantic_result


# ==============================================================================
# ENGINE 1: CLOUD GEMINI GENERATIVE ANALYSIS
# ==============================================================================

def run_gemini_analysis(api_key, answers, custom_answers, user, current_hour, current_time_str):
    user_name = user.get("fullName") or "Bạn"
    user_role = user.get("occupation") or user.get("role") or "Tự do"
    user_bedtime = user.get("targetBedtime") or "23:00"
    user_age = user.get("age") or "Trưởng thành"

    # Filter non-empty custom answers
    active_custom = {k: v.strip() for k, v in custom_answers.items() if v and v.strip()}

    period_label = (
        "Buổi sáng sớm" if 5 <= current_hour < 9 else
        "Buổi sáng" if 9 <= current_hour < 11 else
        "Buổi trưa (Ăn trưa & Nghỉ trưa)" if 11 <= current_hour < 14 else
        "Buổi chiều (Xế chiều)" if 14 <= current_hour < 17 else
        "Hoàng hôn & Bữa tối" if 17 <= current_hour < 20 else
        "Tiền ngủ (Chuẩn bị ngủ)" if 20 <= current_hour < 23 else
        "Đêm muộn"
    )

    prompt = f"""Bạn là Mavis - Trợ lý AI Giác Quan & Nhịp Sinh Học Y Khoa của Mavis chúc bạn ngủ ngon.
Nhiệm vụ: Phân tích kết quả khảo sát 5 trụ cột y khoa giấc ngủ của người dùng, ĐẶC BIỆT chú trọng giải mã các câu trả lời tự gõ ở mục 'Khác' và đưa ra lời khuyên cá nhân hóa ngay tại thời điểm thực này.

THÔNG TIN NGƯỜI DÙNG & MỐC THỜI GIAN THỰC (BẮT BUỘC ĐỐI CHIẾU CHÍNH XÁC):
- Họ tên: {user_name}
- Nghề nghiệp: {user_role}
- Tuổi tác: {user_age}
- Giờ đi ngủ mục tiêu: {user_bedtime}
- THỜI ĐIỂM THỰC HIỆN KHẢO SÁT: {current_time_str} ({period_label}, Khung giờ: {current_hour}h)

CÂU TRẢ LỜI 5 TRỤ CỘT:
{json.dumps(answers, ensure_ascii=False, indent=2)}

ĐẶC BIỆT QUAN TRỌNG - NỘI DUNG TỰ GÕ Ở MỤC 'KHÁC':
{json.dumps(active_custom, ensure_ascii=False, indent=2) if active_custom else "Người dùng không nhập thêm mục khác."}

NGUYÊN TẮC BẢO VỆ PHÁP LÝ & AN TOÀN Y TẾ:
- TUYỆT ĐỐI KHÔNG tư vấn, không kê đơn, không nhắc tới bất kỳ loại thuốc ngủ hay thực phẩm chức năng (TPCN, viên uống) nào.
- Chỉ tư vấn giải pháp nhịp sinh học tự nhiên, dinh dưỡng bữa ăn thường ngày, vi-vận động 2-5 phút, ánh sáng, nhiệt độ phòng.

QUY TẮC CỐT LÕI VỀ CÁ NHÂN HÓA - TUYỆT ĐỐI KHÔNG KHUYÊN BỆNH NGƯỜI DÙNG KHÔNG BỊ:
- ĐẶC BIỆT LƯU Ý VỀ BỆNH LÝ & CƠ THỂ:
  + Nếu người dùng trả lời `physical_pain: ["none"]` hoặc không chọn đau cổ vai gáy: TUYỆT ĐỐI KHÔNG được đưa ra bất kỳ lời khuyên nào về đau cổ vai gáy, đốt sống cổ C5-C7 hay các bài tập thoái hóa cổ. Thay vào đó, 'deskExercises' BẮT BUỘC là các bài tập: Thư giãn mắt 20-20-20 khi dùng điện thoại/máy tính, Thở chậm Box Breathing 4-4-4-4, Vươn vai giãn toàn thân tại chỗ.
  + Nếu người dùng trả lời `chronic_condition: ["none"]` hoặc không chọn GERD: TUYỆT ĐỐI KHÔNG được nhắc đến trào ngược axit dạ dày, cơ thắt thực quản GERD hay áp lực tiêu hóa dạ dày.
  + Nếu người dùng trả lời `dinner_habit: ["light_early"]`: Tuyệt đối KHÔNG khuyên giải pháp chống đầy bụng khó tiêu do ăn muộn.
- TẬP TRUNG TỐI ĐA VÀO ĐÚNG VẤN ĐỀ NGƯỜI DÙNG THỰC SỰ GẶP PHẢI:
  + Nếu người dùng chọn `bed_phone: ["lướt_tiktok_fb"]` hoặc `env_light: ["screen_heavy"]`: Trong 'targetedHealth', BẮT BUỘC phải tư vấn giải pháp đặc trị cắt cơn nghiện màn hình trước khi ngủ (bật Grayscale đen trắng từ 21h, đặt sạc điện thoại cách giường 2m, dùng đồng hồ báo thức vật lý).
  + Nếu người dùng chọn `stress_level: ["medium" hoặc "high"]` hoặc `mood_state: ["anxious" hoặc "brain_fog"]`: Trong 'targetedHealth', BẮT BUỘC tư vấn kỹ thuật xả rác não bộ (Brain Dump) 3 phút với sổ tay và bài tập thở 4-7-8 hạ nồng độ Cortisol.
  + Nếu người dùng chọn `caffeine_usage: ["late_high" hoặc "medium_afternoon"]`: Khuyên về Caffeine Curfew trước 8 tiếng.
  + Nếu người dùng chọn `env_temp: ["hot"]`: Khuyên về hạ nhiệt độ phòng 24-26°C và cơ chế hạ thân nhiệt trung tâm.

QUY TẮC BẮT BUỘC VỀ ĐỒNG BỘ THỜI GIAN THỰC (REALTIME CHRONOTHERAPY):
1. 'realtimeActionNow': BẮT BUỘC là lời khuyên hành động NGAY BÂY GIỜ phù hợp chính xác với khung giờ {current_time_str} ({period_label}).
   - Hiện tại là {period_label} ({current_time_str}): Tuyệt đối KHÔNG được khuyên sai lệch (ví dụ KHÔNG ĐƯỢC nói là sáng sớm hay đêm muộn khi đang là {period_label})!
   - Nếu là Buổi trưa ({current_time_str}): Khuyên ăn trưa thanh đạm, chốt cữ cà phê trước 12:00, đi bộ nhẹ 5 phút kích thích tiêu hóa (chống trào ngược chỉ nếu có bệnh GERD), chợp mắt power-nap 15-20 phút.
   - Nếu là Buổi chiều: Khuyên dừng nạp caffeine, 3 phút xoa dịu thần kinh / thư giãn mắt hoặc thả lỏng vai gáy (chỉ nếu có đau mỏi), uống nước ấm.
   - Nếu là Hoàng hôn / Tối: Thực đơn ăn tối giàu Tryptophan, cắt giảm uống nước sau 20:00.
   - Nếu là Tiền ngủ / Đêm: Cắt cơn nghiện lướt điện thoại nếu có, kích hoạt Digital Sunset, tắm nước ấm 10 phút, bật sóng não Delta 4Hz.

2. 'microSchedule': Lịch trình vi-hành động (2-5 phút) BẮT BUỘC PHẢI BẮT ĐẦU TỪ THỜI ĐIỂM HIỆN TẠI ({current_time_str}) VÀ DÀN TRẢI DẦN ĐẾN GIỜ ĐI NGỦ ({user_bedtime}).
   - Phải có ĐỦ TỪ 4 ĐẾN 5 VI-HÀNH ĐỘNG trải đều các mốc (Trưa -> Đầu chiều -> Xế chiều -> Bữa tối -> Tiền ngủ).
   - TUYỆT ĐỐI KHÔNG chỉ đưa 1-2 hành động lúc 22h đêm khi người dùng đang làm khảo sát vào ban ngày! Người dùng cần có hành động ngay trưa nay và chiều nay.

YÊU CẦU ĐẦU RA: Trả về ĐÚNG MỘT JSON OBJECT duy nhất (không bọc trong markdown codeblock), theo schema sau:
{{
  "predictedScore": 72,
  "verdictTitle": "Tiêu đề ngắn dự báo giấc ngủ đêm nay",
  "verdictDesc": "Mô tả tổng quan nguyên nhân ảnh hưởng",
  "latency": 20,
  "deepSleepPct": 16,
  "remSleepPct": 20,
  "pillars": {{
    "p1_stress": 45,
    "p2_env": 30,
    "p3_lifestyle": 60,
    "p4_physio": 35,
    "p5_health": 40
  }},
  "customInsights": [
    {{
      "pillarName": "Tên trụ cột (Tâm lý / Môi trường / Lối sống / Bệnh lý)",
      "userTypedText": "Trích dẫn nguyên văn người dùng gõ",
      "badge": "Nhãn phân loại ngắn gọn",
      "biologicalImpact": "Tác động sinh học đến Adenosine/Cortisol/Melatonin",
      "actionableSolution": "Hành động khắc phục phi dược lý cụ thể, dễ làm"
    }}
  ],
  "realtimeActionNow": "Lời khuyên hành động ngay lập tức tại mốc {current_time_str} ({period_label})",
  "microSchedule": [
    {{
      "time": "12:15 - 12:20",
      "title": "Tên vi-hành động 2-5 phút",
      "desc": "Chi tiết hướng dẫn",
      "tag": "Thẻ phân loại"
    }}
  ],
  "nutritionAdvice": {{
    "dinnerItems": ["Món 1", "Món 2", "Món 3"],
    "targetedHealth": "Giải pháp dinh dưỡng và phòng ngủ",
    "deskExercises": [
      "Động tác 1",
      "Động tác 2"
    ]
  }}
}}
"""

    models_to_try = [
        'gemini-3.5-flash-lite',
        'gemini-3.1-flash-lite',
        'gemini-3.5-flash',
        'gemma-4-26b-a4b-it',
        'gemini-flash-latest'
    ]

    has_gerd_flag = (answers.get("chronic_condition") == "gerd") or ("gerd" in str(answers.get("chronic_condition", []))) or (answers.get("dinner_habit") == "heavy_late") or ("heavy_late" in str(answers.get("dinner_habit", [])))
    has_neck_flag = ("neck" in str(answers.get("physical_pain", []))) or (answers.get("physical_pain") == "neck_shoulder") or ("neck_back_pain" in str(answers.get("physical_pain", [])))

    for model_name in models_to_try:
        try:
            gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
            payload_data = json.dumps({
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.2, "maxOutputTokens": 2048}
            }).encode('utf-8')

            req = urllib.request.Request(gemini_url, data=payload_data, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=14.0) as resp:
                res_json = json.loads(resp.read().decode('utf-8'))
                raw_text = res_json['candidates'][0]['content']['parts'][0]['text'].strip()

                # Clean markdown wrapper
                if "```json" in raw_text:
                    raw_text = raw_text.split("```json", 1)[1].split("```", 1)[0].strip()
                elif "```" in raw_text:
                    raw_text = raw_text.split("```", 1)[1].split("```", 1)[0].strip()

                parsed = json.loads(raw_text)

                # Check guardrails
                if check_guardrails(json.dumps(parsed)):
                    continue

                # Normalize fields
                if "latency" not in parsed and "latencyMinutes" in parsed:
                    parsed["latency"] = parsed["latencyMinutes"]
                if "latencyMinutes" not in parsed and "latency" in parsed:
                    parsed["latencyMinutes"] = parsed["latency"]

                if "pillars" not in parsed:
                    parsed["pillars"] = {
                        "p1_stress": 50, "p2_env": 30, "p3_lifestyle": 55, "p4_physio": 30, "p5_health": 35
                    }

                # Sanity check: Ensure realtimeActionNow matches actual current hour and symptoms
                rt_now = str(parsed.get("realtimeActionNow", ""))
                if 11 <= current_hour < 14:
                    if any(w in rt_now.lower() for w in ["sáng sớm", "04:", "03:", "02:", "đêm muộn", "chuẩn bị ngủ", "chúc bạn ngủ"]):
                        digest_tip = "đứng dậy đi dạo nhẹ nhàng 5 phút để chống trào ngược axit dạ dày (GERD)" if has_gerd_flag else "đứng dậy đi dạo nhẹ nhàng 5 phút kích thích tiêu hóa êm ái"
                        parsed["realtimeActionNow"] = f"🥪 <strong>Khung giờ hiện tại ({current_time_str} - Buổi trưa):</strong> Thời điểm vàng nạp lại năng lượng & chốt cữ Caffeine. Bữa trưa ăn thanh đạm, {digest_tip}. Ngủ trưa chớp nhoáng (Power Nap) đúng 15-20 phút, không ngủ quá 30 phút để bảo tồn áp lực buồn ngủ ban đêm."

                # Ensure microSchedule is complete and covers daytime to bedtime
                parsed["microSchedule"] = ensure_full_micro_schedule(
                    parsed.get("microSchedule", []),
                    current_hour,
                    current_time_str,
                    user_bedtime,
                    answers
                )

                if "nutritionAdvice" in parsed:
                    na = parsed["nutritionAdvice"]
                    if "dinnerItems" not in na and "dinnerHighlights" in na:
                        na["dinnerItems"] = na["dinnerHighlights"]
                    
                    # Strictly tailor targetedHealth & deskExercises so diseases user does NOT have are never displayed
                    curr_th = str(na.get("targetedHealth", "") or na.get("targetedCare", "")).lower()
                    need_rebuild_th = False
                    if not has_gerd_flag and ("gerd" in curr_th or "trào ngược" in curr_th or "dạ dày" in curr_th):
                        need_rebuild_th = True
                    if not has_neck_flag and ("c5-c7" in curr_th or "đốt sống cổ" in curr_th or "cổ vai gáy" in curr_th):
                        need_rebuild_th = True
                    if ("lướt" in str(answers.get("bed_phone", [])) or "tiktok" in str(answers.get("bed_phone", []))) and ("điện thoại" not in curr_th and "grayscale" not in curr_th and "tiktok" not in curr_th):
                        need_rebuild_th = True
                    
                    if need_rebuild_th or not na.get("targetedHealth"):
                        na["targetedHealth"] = build_targeted_health_advice(answers, user_bedtime)
                        na["targetedCare"] = na["targetedHealth"]

                    # For desk exercises, ensure no chin-tuck / C5-C7 if user has no neck pain
                    curr_exercises = na.get("deskExercises", [])
                    if not has_neck_flag:
                        if any(k in str(curr_exercises).lower() for k in ["c5-c7", "chin-tuck", "đốt sống cổ", "cổ vai gáy", "khớp cổ"]):
                            na["deskExercises"] = build_tailored_desk_exercises(answers)
                    if not na.get("deskExercises"):
                        na["deskExercises"] = build_tailored_desk_exercises(answers)

                parsed["geminiModelUsed"] = model_name
                return parsed

                parsed["geminiModelUsed"] = model_name
                return parsed
        except Exception as e:
            print(f"[Gemini API] Error with model {model_name}: {e}", flush=True)
            continue

    return None


# ==============================================================================
# ENGINE 2: SMART SEMANTIC VIETNAMESE NLP ENGINE (ZERO API KEY REQUIRED)
# ==============================================================================

def run_semantic_nlp_analysis(answers, custom_answers, user, current_hour, current_time_str):
    user_name = user.get("fullName") or "Bạn"
    user_role = user.get("occupation") or user.get("role") or "Tự do"
    user_bedtime = user.get("targetBedtime") or "23:00"
    
    # Calculate Base Scores for 5 Pillars
    p1 = 30
    p2 = 20
    p3 = 20
    p4 = 15
    p5 = 10

    # Helper for answers
    def has(key, val):
        v = answers.get(key)
        if isinstance(v, list):
            return val in v
        return v == val

    if has('stress_level', 'high'): p1 += 40
    elif has('stress_level', 'medium'): p1 += 15
    if has('mood_state', 'anxious'): p1 += 25

    if has('env_light', 'screen_heavy'): p2 += 35
    if has('env_temp', 'hot'): p2 += 30
    if has('env_noise', 'noisy'): p2 += 25

    if has('caffeine_usage', 'late_high'): p3 += 35
    if has('dinner_habit', 'heavy_late'): p3 += 25
    if has('bed_phone', 'lướt_tiktok_fb'): p3 += 20

    if has('age_group', 'middle_aged'): p4 += 25
    if has('hormone_state', 'menopause_hotflash'): p4 += 40

    if has('physical_pain', 'neck_back_pain'): p5 += 35
    if has('chronic_condition', 'gerd'): p5 += 35
    if has('chronic_condition', 'nocturia'): p5 += 30

    # -------------------------------------------------------------
    # Deep Semantic NLP Analysis on Free-text in "Khác..."
    # -------------------------------------------------------------
    custom_insights = []
    penalty_from_custom = 0

    pillar_map = {
        'stress_level': 'Tâm Lý & Áp Lực',
        'mood_state': 'Trạng Thái Cảm Xúc',
        'env_light': 'Ánh Sáng Phòng Ngủ',
        'env_temp': 'Nhiệt Độ Môi Trường',
        'env_noise': 'Tiếng Ồn Xung Quanh',
        'caffeine_usage': 'Chất Kích Thích (Caffeine)',
        'alcohol_nicotine': 'Cồn & Nicotine',
        'dinner_habit': 'Thói Quen Bữa Tối',
        'bed_phone': 'Thiết Bị Điện Tử',
        'age_group': 'Sinh Lý & Nhóm Tuổi',
        'hormone_state': 'Nội Tiết Tố',
        'physical_pain': 'Đau Nhức Thể Chất',
        'chronic_condition': 'Bệnh Lý Mãn Tính'
    }

    for q_key, raw_text in custom_answers.items():
        if not raw_text or not raw_text.strip():
            continue
        
        text = raw_text.strip()
        lower = text.lower()
        cat_name = pillar_map.get(q_key, "Yếu Tố Bổ Sung")
        insight = None

        # 1. Ca đêm / Trực / Làm muộn / Overtime
        if any(w in lower for w in ['ca đêm', 'trực', 'tăng ca', 'deadline', 'làm khuya', 'ot', 'xoay ca']):
            penalty_from_custom += 12
            insight = {
                "pillarName": cat_name,
                "userTypedText": text,
                "badge": "Ca Đêm & Giờ Giấc Bất Định",
                "biologicalImpact": "Nhịp sinh học bị đảo ngược, trục HPA liên tục phóng thích Cortisol vào ban đêm khiến đồng hồ sinh học tại nhân SCN bị lệch pha.",
                "actionableSolution": "Dùng rèm cản sáng 100% hoặc bịt mắt khi ngủ bù ban ngày. Đeo kính chống ánh sáng xanh khi làm ca đêm và ăn nhẹ dễ tiêu (cháo yến mạch, chuối) trước ca trực."
            }
        
        # 2. Con nhỏ / Em bé / Cho bú / Quấy khóc
        elif any(w in lower for w in ['con nhỏ', 'em bé', 'cho bú', 'chăm con', 'sơ sinh', 'quấy']):
            penalty_from_custom += 10
            insight = {
                "pillarName": cat_name,
                "userTypedText": text,
                "badge": "Chăm Sóc Trẻ Nhỏ",
                "biologicalImpact": "Giấc ngủ bị chia nhỏ thành nhiều pha ngắn, thiếu hụt giai đoạn ngủ sâu NREM 3 & 4 để phục hồi tế bào não.",
                "actionableSolution": "Áp dụng kỹ thuật 'Ngủ theo chu kỳ 90 phút' cùng con. Bật tiếng ồn hồng (Pink Noise) hoặc tiếng mưa rào để giúp cả mẹ và bé ngủ sâu hơn."
            }

        # 3. Trà sữa / Matcha / Nước ngọt / Ăn đêm
        elif any(w in lower for w in ['trà sữa', 'matcha', 'bò húc', 'nước ngọt', 'mì tôm', 'ăn đêm', 'lẩu', 'đồ ngọt']):
            penalty_from_custom += 8
            insight = {
                "pillarName": cat_name,
                "userTypedText": text,
                "badge": "Đường & Caffeine Tiềm Ẩn",
                "biologicalImpact": "Trà sữa và matcha chứa hàm lượng caffeine đáng kể kèm đường đơn cao, gây sốc đường huyết và chặn thụ thể buồn ngủ Adenosine.",
                "actionableSolution": "Uống ngay 1 cốc nước ấm 250ml pha loãng vài giọt chanh để hỗ trợ thận thanh lọc. Đứng thư giãn nhẹ nhàng 10 phút, không nằm ngay."
            }

        # 4. Tê bì / Chuột rút / Đau cơ khớp / Thoát vị
        elif any(w in lower for w in ['tê bì', 'chuột rút', 'khớp', 'thoát vị', 'chân', 'lưng', 'bắp chân', 'gối']):
            penalty_from_custom += 10
            insight = {
                "pillarName": cat_name,
                "userTypedText": text,
                "badge": "Tuần Hoàn Máu & Cơ Xương",
                "biologicalImpact": "Chèn ép rễ thần kinh và ứ trệ tuần hoàn tĩnh mạch ngoại vi khi nằm yên, kích thích các cơn co rút giật mình ban đêm.",
                "actionableSolution": "Kê một chiếc gối ôm mỏng dưới bắp chân để nâng cao chân 10cm hỗ trợ máu về tim. Xoa bóp bắp chân bằng tay ấm 3 phút trước khi ngủ."
            }

        # 5. Cảm xúc / Cãi nhau / Bồn chồn / Lo lắng / Chia tay
        elif any(w in lower for w in ['cãi nhau', 'chia tay', 'lo lắng', 'bồn chồn', 'người yêu', 'bực', 'tức', 'suy nghĩ']):
            penalty_from_custom += 12
            insight = {
                "pillarName": cat_name,
                "userTypedText": text,
                "badge": "Căng Thẳng Cảm Xúc Kích Hoạt",
                "biologicalImpact": "Hạch hạnh nhân (Amygdala) hoạt động quá mức, giữ hệ thần kinh giao cảm luôn trong trạng thái 'chiến đấu hoặc bỏ chạy' (Fight or Flight).",
                "actionableSolution": "Thực hiện ngay bài thở 4-7-8 (Hít 4s, nín 7s, thở 8s) liên tục 4 chu kỳ trên giường để ép nhịp tim giảm xuống ngưỡng thư giãn."
            }

        # 6. Môi trường (Ồn, nóng, phòng trọ, hàng xóm)
        elif any(w in lower for w in ['phòng trọ', 'hàng xóm', 'tiếng', 'ồn', 'nóng', 'chó sủa', 'công trường']):
            penalty_from_custom += 8
            insight = {
                "pillarName": cat_name,
                "userTypedText": text,
                "badge": "Nhiễu Loạn Ngoại Cảnh",
                "biologicalImpact": "Vỏ thính giác liên tục truyền xung điện cảnh báo lên não, ngăn cản não bộ bước vào pha sóng não Delta chậm.",
                "actionableSolution": "Bật âm thanh Sóng Não Delta 4Hz kết hợp tiếng mưa rào trong ứng dụng để tạo màng chắn âm học (acoustic mask) triệt tiêu tiếng ồn bên ngoài."
            }

        # Generic semantic fallback for custom text
        else:
            penalty_from_custom += 6
            insight = {
                "pillarName": cat_name,
                "userTypedText": text,
                "badge": "Đặc Điểm Cá Nhân",
                "biologicalImpact": f"Yếu tố '{text}' tác động riêng biệt đến sự cân bằng dẫn truyền thần kinh trước giờ ngủ.",
                "actionableSolution": f"Dành 10 phút thư giãn phi màn hình trước giờ ngủ {user_bedtime}, giữ không gian ngủ thoáng mát để cân bằng lại cơ thể."
            }

        if insight:
            custom_insights.append(insight)

    # Calculate final adjusted score
    total_penalty = (p1 * 0.26) + (p2 * 0.16) + (p3 * 0.24) + (p4 * 0.12) + (p5 * 0.14) + penalty_from_custom
    predicted_score = max(28, min(95, round(100 - total_penalty)))

    # Metrics estimation
    latency = 14 + (p1 // 6) + (penalty_from_custom // 2)
    deep_sleep = max(9, min(24, round(23 - (p1 * 0.08) - (penalty_from_custom * 0.15))))
    rem_sleep = max(11, min(24, round(21 - (p3 * 0.07) - (p2 * 0.04))))

    # Real-time action based on CURRENT local hour
    if 5 <= current_hour < 11:
        rt_action = f"☀️ <strong>Khung giờ hiện tại ({current_time_str} - Buổi sáng):</strong> Bạn đang ở pha đỉnh tiết Cortisol. Hãy chốt cữ cà phê trước 10:30, uống 1 cốc nước ấm 300ml và đón ánh nắng tự nhiên 10 phút để cài đặt nhịp sinh học cho giấc ngủ tối nay."
    elif 11 <= current_hour < 14:
        noon_tip = "đứng dậy đi dạo nhẹ nhàng 5 phút để tránh trào ngược dạ dày (GERD)" if (has('chronic_condition', 'gerd') or has('dinner_habit', 'heavy_late')) else "đứng dậy đi dạo nhẹ nhàng 5 phút kích thích tiêu hóa êm ái"
        rt_action = f"🥪 <strong>Khung giờ hiện tại ({current_time_str} - Buổi trưa):</strong> Thời điểm vàng nạp lại năng lượng & chốt cữ Caffeine. Bữa trưa ăn thanh đạm, {noon_tip}. Ngủ trưa chớp nhoáng (Power Nap) đúng 15-20 phút, không ngủ quá 30 phút để bảo tồn áp lực buồn ngủ ban đêm."
    elif 14 <= current_hour < 17:
        afternoon_tip = "làm động tác Chin-Tuck giãn cơ cổ vai gáy" if has('physical_pain', 'neck_back_pain') else "áp dụng quy tắc mắt 20-20-20 & thở Box Breathing xoa dịu thần kinh"
        rt_action = f"⏳ <strong>Khung giờ hiện tại ({current_time_str} - Buổi chiều):</strong> Điểm trũng thể lực. Dừng nhìn màn hình 3 phút, {afternoon_tip}. Tuyệt đối không nạp thêm cà phê hay nước ngọt sau 14:00."
    elif 17 <= current_hour < 21:
        rt_action = f"🌅 <strong>Khung giờ hiện tại ({current_time_str} - Hoàng hôn & Tối):</strong> Tuyến tùng chuẩn bị tiết melatonin. Bữa tối kết thúc trước 19:30 với thực phẩm giàu Tryptophan (trứng luộc, ức gà, canh rau bina). Uống ít nước sau 20:00 để tránh tiểu đêm."
    elif 21 <= current_hour < 23:
        rt_action = f"🌙 <strong>Khung giờ hiện tại ({current_time_str} - Tiền ngủ):</strong> Kích hoạt 'Digital Sunset' ngay! Chuyển màn hình điện thoại sang ánh sáng vàng ấm, bật điều hòa 24-26°C. Tắm nước ấm 10 phút để hạ thân nhiệt trung tâm trước mốc {user_bedtime}."
    else:
        rt_action = f"💤 <strong>Khung giờ hiện tại ({current_time_str} - Đêm muộn):</strong> Đã qua giờ vàng tiết Melatonin! Cất điện thoại xa tầm tay ngay lập tức, bật âm thanh Sóng Não Delta 4Hz trong ứng dụng và nhắm mắt hít thở chậm 4-7-8 để não bộ chìm vào giấc ngủ phục hồi."

    # Verdict
    if predicted_score >= 80:
        verdict_title = "Dự Báo: Giấc Ngủ Phục Hồi Tối Ưu Đêm Nay"
        verdict_desc = f"Chào {user_name}, các chỉ số của bạn ở ngưỡng an toàn. Giấc ngủ sẽ hỗ trợ tái tạo não bộ và đào thải độc tố thần kinh hiệu quả."
    elif predicted_score >= 60:
        verdict_title = "Cảnh Báo: Nguy Cơ Khó Vào Giấc Hoặc Ngủ Chập Chờn"
        verdict_desc = f"Chào {user_name}, phát hiện nguy cơ kích thích giao cảm từ các yếu tố bạn chia sẻ. Hãy thực hiện ngay các vi-hành động AI đề xuất."
    else:
        verdict_title = "Báo Động Kém: Nguy Cơ Mất Ngủ & Mệt Mỏi Sáng Mai"
        verdict_desc = f"Hệ thần kinh đang bị kích thích mạnh kết hợp các vấn đề riêng bạn vừa gõ. Cần áp dụng quy trình cấp cứu giấc ngủ trước mốc {user_bedtime}."

    # Micro schedule tailored to current time of day
    micro_schedule = ensure_full_micro_schedule(
        [],
        current_hour,
        current_time_str,
        user_bedtime,
        answers
    )

    targeted_health_content = build_targeted_health_advice(answers, user_bedtime)
    tailored_exercises = build_tailored_desk_exercises(answers)

    return {
        "predictedScore": predicted_score,
        "verdictTitle": verdict_title,
        "verdictDesc": verdict_desc,
        "latency": latency,
        "latencyMinutes": latency,
        "deepSleepPct": deep_sleep,
        "remSleepPct": rem_sleep,
        "pillars": {
            "p1_stress": min(100, p1 + (penalty_from_custom // 2)),
            "p2_env": min(100, p2),
            "p3_lifestyle": min(100, p3 + (penalty_from_custom // 3)),
            "p4_physio": min(100, p4),
            "p5_health": min(100, p5 + (penalty_from_custom // 3))
        },
        "customInsights": custom_insights,
        "realtimeActionNow": rt_action,
        "microSchedule": micro_schedule,
        "nutritionAdvice": {
            "dinnerItems": [
                "2 quả trứng gà luộc lòng đào (giàu Melatonin & Tryptophan tự nhiên)",
                "Canh rau bina hoặc canh rau ngót luộc (giàu Magie tự nhiên giãn cơ bắp)",
                "1-2 quả Kiwi tráng miệng (giúp tăng thời lượng ngủ sâu NREM)"
            ],
            "dinnerHighlights": [
                "2 quả trứng gà luộc lòng đào (giàu Melatonin & Tryptophan tự nhiên)",
                "Canh rau bina hoặc canh rau ngót luộc (giàu Magie tự nhiên giãn cơ bắp)",
                "1-2 quả Kiwi tráng miệng (giúp tăng thời lượng ngủ sâu NREM)"
            ],
            "targetedHealth": targeted_health_content,
            "targetedCare": targeted_health_content,
            "deskExercises": tailored_exercises
        }
    }


# ==============================================================================
# GENERAL CONVERSATIONAL AI HEALTH & SLEEP ASSISTANT (MAVIS CHATBOT)
# ==============================================================================

def chat_with_mavis(query, user=None, history=None):
    """
    Empathetic, knowledgeable, and diverse health & sleep chatbot with Gemini 3.5 AI.
    Answers comfortably on health, sleep, nutrition, physiology, mental wellness, and recovery.
    """
    user = user or {}
    user_name = user.get("fullName") or "Bạn"
    user_role = user.get("occupation") or user.get("role") or "người dùng"
    user_bedtime = user.get("targetBedtime") or "23:00"
    user_conditions = user.get("healthConditions") or []
    if isinstance(user_conditions, list):
        user_cond_str = ", ".join(user_conditions) if user_conditions else "Sức khỏe bình thường"
    else:
        user_cond_str = str(user_conditions)

    current_hour = datetime.now().hour
    current_time_str = datetime.now().strftime("%H:%M")

    system_instruction = f"""Bạn là Mavis - Bé Trợ Lý AI Chăm Sóc Sức Khỏe & Giấc Ngủ Thông Minh của Mavis chúc bạn ngủ ngon.
Tính cách của bạn: Ngọt ngào, ấm áp, thông minh, tận tâm và khoa học như một người bạn thân kiêm chuyên gia sức khỏe gia đình.

BẠN ĐƯỢC PHÉP TRẢ LỜI THOẢI MÁI, ĐA DẠNG VÀ TẬN TÌNH VỀ MỌI CHỦ ĐỀ SỨC KHỎE:
1. Giấc ngủ & Nhịp sinh học: Mất ngủ, ngủ trằn trọc, thức giấc nửa đêm, ác mộng, bóng đè, ngáy, điều chỉnh đồng hồ sinh học, ngủ bù cho người làm ca đêm.
2. Sức khỏe thể chất: Đau mỏi cổ vai gáy, đau lưng, mệt mỏi uể oải, nhức đầu, chóng mặt, tụt huyết áp, phục hồi cơ bắp, thư giãn cơ thể.
3. Dinh dưỡng & Ăn uống: Thực đơn bữa tối dễ ngủ, các loại thực phẩm giàu Magie, Tryptophan, vitamin nhóm B, trà hoa cúc/thảo mộc, cách kiểm soát caffeine và nước uống thanh lọc.
4. Tiêu hóa & Bệnh lý phổ biến: Trào ngược dạ dày (GERD), đầy hơi, khó tiêu, đau dạ dày về đêm, tư thế nằm khoa học.
5. Tâm lý & Thư giãn: Giải tỏa stress công việc, lo âu, cãi nhau/buồn phiền, kỹ thuật thở 4-7-8, thiền định buông thư, xả não trước giờ ngủ.
6. Lối sống lành mạnh: Thói quen sinh hoạt, vận động nhẹ tại bàn làm việc, ánh sáng xanh màn hình (Digital Sunset), nhiệt độ phòng ngủ.

THÔNG TIN NGƯỜI ĐANG TRÒ CHUYỆN:
- Tên: {user_name}
- Nghề nghiệp / Lối sống: {user_role}
- Giờ ngủ mục tiêu: {user_bedtime}
- Tình trạng lưu ý: {user_cond_str}
- Khung giờ hiện tại: {current_time_str} ({current_hour}h)

QUY TẮC TRẢ LỜI:
- Luôn xưng hô gần gũi, dịu dàng: "Mavis chào bạn {user_name} / Mavis chúc bạn...", trả lời tự nhiên, nhiệt tình và cụ thể.
- Đưa ra giải pháp rõ ràng, dễ làm theo từng gạch đầu dòng (thực phẩm, bài tập, tư thế nằm, mẹo dân gian an toàn, thói quen).
- Nếu người dùng hỏi về thuốc hoặc việc uống thuốc: Hãy giải thích cơ chế/công dụng/lưu ý một cách khoa học, đồng thời đưa ra các giải pháp tự nhiên bổ trợ và ân cần khuyên: "Nếu các triệu chứng kéo dài hoặc cần dùng thuốc đặc trị, bạn hãy đi khám hoặc tham khảo ý kiến bác sĩ/dược sĩ chuyên khoa để được kê đơn đúng liều lượng an toàn nhé!"
- TUYỆT ĐỐI KHÔNG cứng nhắc từ chối hay dán thông báo lỗi. Hãy luôn trả lời giúp ích cho sức khỏe của người dùng!"""

    prompt = f"{system_instruction}\n\nNgười dùng hỏi: \"{query}\"\nMavis hãy trả lời thật chu đáo, chi tiết, thoải mái và hữu ích cho người dùng nhé:"

    api_key = os.environ.get("GEMINI_API_KEY") or DEFAULT_GEMINI_KEY
    models_to_try = [
        'gemini-3.5-flash-lite',
        'gemini-3.1-flash-lite',
        'gemini-3.5-flash',
        'gemma-4-26b-a4b-it',
        'gemini-flash-latest'
    ]

    for model_name in models_to_try:
        try:
            gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
            payload_data = json.dumps({
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.65, "maxOutputTokens": 2048}
            }).encode('utf-8')

            req = urllib.request.Request(gemini_url, data=payload_data, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=12.0) as resp:
                res_json = json.loads(resp.read().decode('utf-8'))
                raw_text = res_json['candidates'][0]['content']['parts'][0]['text'].strip()
                if raw_text:
                    return {
                        "success": True,
                        "reply": raw_text,
                        "model": model_name
                    }
        except Exception as e:
            print(f"[Chatbot Gemini] Error with {model_name}: {e}", flush=True)
            continue

    return None


# ==============================================================================
# CLINICAL VOICE JOURNAL INTAKE & 5-PILLAR EXTRACTION ENGINE (TALK MODE)
# ==============================================================================

def get_missing_pillars(answers):
    """
    Identifies which of the 5 pillars have no information.
    1: Tâm lý | 2: Môi trường | 3: Lối sống | 4: Sinh lý | 5: Bệnh lý
    """
    ans = answers or {}
    def has_val(key):
        v = ans.get(key)
        if not v:
            return False
        if isinstance(v, list):
            return len(v) > 0 and v[0] not in ["", "none_selected"]
        return str(v).strip() != ""

    missing = []
    if not (has_val("stress_level") or has_val("mood_state")):
        missing.append(1)
    if not (has_val("env_light") or has_val("env_temp") or has_val("env_noise")):
        missing.append(2)
    if not (has_val("caffeine_usage") or has_val("alcohol_nicotine") or has_val("dinner_habit") or has_val("bed_phone")):
        missing.append(3)
    if not (has_val("age_group") or has_val("hormone_state")):
        missing.append(4)
    if not (has_val("physical_pain") or has_val("chronic_condition")):
        missing.append(5)
    return missing


def local_semantic_extract(user_text, current_answers=None):
    """
    Deterministic rule-based parser for Vietnamese sleep journals.
    Runs 100% offline with zero API key requirement.
    """
    ans = dict(current_answers or {})
    extracted = {}
    custom = {}
    lower = user_text.lower()

    # 1. Tâm Lý & Căng Thẳng
    if any(w in lower for w in ['stress', 'áp lực', 'deadline', 'căng thẳng', 'cháy deadline', 'quá tải', 'mệt mỏi']):
        extracted['stress_level'] = ['high']
        extracted['mood_state'] = ['anxious']
    elif any(w in lower for w in ['thư thái', 'thoải mái', 'nhẹ nhõm', 'không stress', 'bình yên', 'êm ả']):
        extracted['stress_level'] = ['low']
        extracted['mood_state'] = ['good']
    elif any(w in lower for w in ['uể oải', 'chán nản', 'lo âu', 'buồn', 'bồn chồn']):
        extracted['mood_state'] = ['brain_fog']

    # 2. Môi Trường Phòng Ngủ
    if any(w in lower for w in ['nóng', 'hầm', 'bí bách', 'nóng bức', 'chảy mồ hôi']):
        extracted['env_temp'] = ['hot']
    elif any(w in lower for w in ['lạnh', 'lạnh buốt', 'rét', 'quá lạnh']):
        extracted['env_temp'] = ['too_cold']
    elif any(w in lower for w in ['mát', 'mát mẻ', 'điều hòa', 'máy lạnh']):
        extracted['env_temp'] = ['ideal']

    if any(w in lower for w in ['ồn', 'tiếng xe', 'xe cộ', 'công trường', 'tiếng ồn', 'ồn ào']):
        extracted['env_noise'] = ['noisy']
    elif any(w in lower for w in ['yên tĩnh', 'cách âm', 'êm ả', 'không ồn']):
        extracted['env_noise'] = ['quiet']

    if any(w in lower for w in ['màn hình', 'ánh sáng xanh', 'đèn sáng', 'chói']):
        extracted['env_light'] = ['screen_heavy']
    elif any(w in lower for w in ['phòng tối', 'tối om', 'kéo rèm']):
        extracted['env_light'] = ['dark']

    # 3. Lối Sống & Chất Kích Thích
    if any(w in lower for w in ['cà phê', 'cafe', 'matcha', 'trà đặc', 'bò húc', 'nước tăng lực', 'trà sữa']):
        if any(w in lower for w in ['chiều', 'tối', 'trưa', 'muộn', '12h', '13h', '14h', '15h', '16h', '17h', '4h', '3h', '2h']):
            extracted['caffeine_usage'] = ['late_high']
        else:
            extracted['caffeine_usage'] = ['morning_only']
    elif any(w in lower for w in ['không uống cafe', 'nước lọc', 'không caffeine']):
        extracted['caffeine_usage'] = ['none']

    if any(w in lower for w in ['rượu', 'bia', 'nhậu', 'say', 'cồn']):
        extracted['alcohol_nicotine'] = ['alcohol_dinner']
    elif any(w in lower for w in ['thuốc lá', 'hút thuốc', 'vape', 'pod']):
        extracted['alcohol_nicotine'] = ['nicotine']

    if any(w in lower for w in ['ăn muộn', 'ăn khuya', 'dầu mỡ', 'no căng', 'đầy bụng', 'ăn tối trễ']):
        extracted['dinner_habit'] = ['heavy_late']
    elif any(w in lower for w in ['uống nhiều nước', 'uống nước trước khi ngủ']):
        extracted['dinner_habit'] = ['drink_lots_water']
    elif any(w in lower for w in ['ăn thanh đạm', 'ăn sớm', 'ăn nhẹ']):
        extracted['dinner_habit'] = ['light_early']

    if any(w in lower for w in ['tiktok', 'facebook', 'lướt điện thoại', 'xem điện thoại trên giường', 'lướt web']):
        extracted['bed_phone'] = ['lướt_tiktok_fb']
    elif any(w in lower for w in ['không dùng điện thoại', 'cất điện thoại', 'không lướt']):
        extracted['bed_phone'] = ['no_phone']

    # 4. Sinh Lý & Nhóm Tuổi
    if any(w in lower for w in ['tiền mãn kinh', 'mãn kinh', 'bốc hỏa', 'vã mồ hôi đêm']):
        extracted['hormone_state'] = ['menopause_hotflash']
        extracted['age_group'] = ['middle_aged']
    elif any(w in lower for w in ['50 tuổi', '60 tuổi', 'lớn tuổi', 'già']):
        extracted['age_group'] = ['middle_aged']
    elif any(w in lower for w in ['thanh niên', '20 tuổi', '30 tuổi', 'trẻ']):
        extracted['age_group'] = ['young_adult']

    # 5. Bệnh Lý & Thể Chất
    if any(w in lower for w in ['cổ', 'vai', 'gáy', 'mỏi cổ', 'đau lưng', 'mỏi lưng']):
        extracted['physical_pain'] = ['neck_back_pain']
    elif any(w in lower for w in ['đau đầu', 'nhức đầu', 'nửa đầu']):
        extracted['physical_pain'] = ['headache']

    if any(w in lower for w in ['trào ngược', 'gerd', 'dạ dày', 'ợ chua', 'ợ nóng']):
        extracted['chronic_condition'] = ['gerd']
    elif any(w in lower for w in ['tiểu đêm', 'đái đêm', 'đi vệ sinh']):
        extracted['chronic_condition'] = ['nocturia']

    # Ghi nhận các chi tiết "THỪA" / độc lạ ngoài schema cố định
    for phrase in ['ca đêm', 'tăng ca', 'deadline', 'cãi nhau', 'matcha', 'trà sữa', 'chia tay', 'mất ngủ']:
        if phrase in lower:
            custom['note_' + phrase] = phrase

    # Merge với đáp án hiện tại
    merged = dict(ans)
    merged.update(extracted)
    missing = get_missing_pillars(merged)

    # Xây dựng phản hồi
    ack_parts = []
    if 'stress_level' in extracted: ack_parts.append("căng thẳng/áp lực")
    if 'env_temp' in extracted: ack_parts.append("nhiệt độ phòng")
    if 'env_noise' in extracted: ack_parts.append("tiếng ồn")
    if 'caffeine_usage' in extracted: ack_parts.append("thời điểm nạp caffeine")
    if 'physical_pain' in extracted: ack_parts.append("tình trạng đau mỏi cổ vai gáy")
    if 'dinner_habit' in extracted: ack_parts.append("thói quen ăn tối")
    if 'bed_phone' in extracted: ack_parts.append("thói quen dùng điện thoại")

    ack_str = f"Mavis đã ghi nhận {', '.join(ack_parts)} của bạn vào hồ sơ!" if ack_parts else "Mavis đã lắng nghe và ghi nhận chia sẻ của bạn!"

    if len(missing) == 0:
        response_text = f"{ack_str} Tuyệt vời! Bạn đã có đủ thông tin của cả 5 trụ cột y khoa. Mời bạn bấm **Hoàn Tất & Phân Tích Chuẩn Y Khoa** bên dưới để nhận phác đồ nhịp sinh học ngay tối nay!"
        chips = [
            {"text": "Phân tích ngay bây giờ", "action": "analyze"}
        ]
    elif 2 in missing:
        response_text = f"{ack_str} Để tối ưu giấc ngủ tối nay, bạn cho Mavis hỏi thêm: **Phòng ngủ tối nay của bạn có thoáng mát (24-26°C), yên tĩnh không và bạn có thói quen lướt điện thoại trên giường không?**"
        chips = [
            {"text": "Phòng mát mẻ, tối và yên tĩnh", "fill": "Phòng mát mẻ, tối và yên tĩnh"},
            {"text": "Phòng hơi nóng và ồn xe cộ", "fill": "Phòng hơi nóng và ồn xe cộ"}
        ]
    elif 3 in missing:
        response_text = f"{ack_str} Mavis hỏi thêm một chút: **Hôm nay bạn có uống cà phê/trà chiều không, và tối nay có ăn muộn nhiều dầu mỡ không?**"
        chips = [
            {"text": "Có lướt điện thoại trên giường", "fill": "Có lướt điện thoại trên giường"},
            {"text": "Không uống cafe muộn, ăn sớm", "fill": "Không uống cafe muộn, ăn thanh đạm"}
        ]
    elif 5 in missing:
        response_text = f"{ack_str} Bạn chia sẻ thêm nhé: **Cơ thể bạn có đang bị đau mỏi cổ vai gáy, trào ngược dạ dày hay tiểu đêm không?**"
        chips = [
            {"text": "Đau mỏi cổ vai gáy nhiều", "fill": "Đau mỏi cổ vai gáy nhiều"},
            {"text": "Cơ thể bình thường không đau mỏi", "fill": "Cơ thể hoàn toàn khỏe khoắn không đau mỏi"}
        ]
    else:
        response_text = f"{ack_str} Bạn thuộc nhóm tuổi thanh niên hay trên 50 tuổi, và có triệu chứng nội tiết bốc hỏa đêm nào không?"
        chips = [
            {"text": "Dưới 50 tuổi, sức khỏe bình thường", "fill": "Dưới 50 tuổi, sức khỏe bình thường"},
            {"text": "Trên 50 tuổi, hay thức giấc đêm", "fill": "Trên 50 tuổi, hay thức giấc đêm"}
        ]

    return {
        "success": True,
        "extracted_answers": extracted,
        "custom_notes": custom,
        "missing_pillars": missing,
        "ai_response_text": response_text,
        "quick_chips": chips,
        "is_complete": len(missing) == 0
    }


def extract_journal_intake(user_text, current_answers=None, history=None, user=None):
    """
    Dedicated Clinical Voice Journal Intake & 5-Pillar Extraction Engine.
    Transforms arbitrary voice logs or free-form user journals into:
    1. Structured 5-pillar values (mapped to 5-pillar schema)
    2. Qualitative custom notes (extra details, irregular schedules, life events)
    3. Missing pillar detection & natural follow-up clinical question
    4. Safe guardrails: Strictly refuses drug/supplement queries with friendly non-pharmacological advice.
    """
    user_text_clean = (user_text or "").strip()
    if not user_text_clean:
        return {
            "success": False,
            "error": "Nội dung nhật ký rỗng"
        }

    # 1. RÀO CẢN AN TOÀN PHÁP LÝ (STRICT GUARDRAILS)
    if check_guardrails(user_text_clean):
        missing = get_missing_pillars(current_answers or {})
        return {
            "success": True,
            "is_guardrail_block": True,
            "extracted_answers": {},
            "custom_notes": {},
            "missing_pillars": missing,
            "ai_response_text": (
                "Chào bạn, Mavis là trợ lý điều hòa nhịp sinh học tự nhiên phi dược lý của Mavis chúc bạn ngủ ngon. "
                "Để đảm bảo an toàn tuyệt đối và tuân thủ quy chuẩn y tế, Mavis không được phép kê đơn, chỉ định hoặc tư vấn các loại thuốc tân dược hay thực phẩm chức năng. "
                "Nếu tình trạng mất ngủ kéo dài cần can thiệp y tế, bạn vui lòng thăm khám bác sĩ chuyên khoa nhé!\n\n"
                "Tối nay, Mavis có thể đồng hành cùng bạn bằng phác đồ ánh sáng, nhiệt độ phòng ngủ, dinh dưỡng tự nhiên giàu Melatonin/Magie và kỹ thuật thở buông thư. "
                "Bạn hãy chia sẻ thêm về cảm giác cơ thể và sinh hoạt hôm nay nhé!"
            ),
            "quick_chips": [
                {"text": "Hôm nay tôi mệt mỏi, áp lực deadline", "fill": "Hôm nay tôi mệt mỏi, áp lực deadline"},
                {"text": "Phòng ngủ hơi nóng, cổ vai gáy bị mỏi", "fill": "Phòng ngủ hơi nóng, cổ vai gáy bị mỏi"},
                {"text": "Chiều có uống ly cà phê lúc 3h", "fill": "Chiều có uống ly cà phê lúc 3h"}
            ],
            "is_complete": False
        }

    # 2. RUN LOCAL NLP EXTRACTOR AS BASELINE
    baseline = local_semantic_extract(user_text_clean, current_answers)

    # 3. CLOUD AI EXTRACTION VIA GEMINI (NẾU CÓ KEY)
    api_key = os.environ.get("GEMINI_API_KEY") or DEFAULT_GEMINI_KEY
    if not api_key:
        return baseline

    system_prompt = """Bạn là Bác Sĩ Tiếp Nhận Bệnh Án Lâm Sàng & Nhịp Sinh Học (Clinical Intake Specialist) của Mavis chúc bạn ngủ ngon.
Nhiệm vụ của bạn là lắng nghe nhật ký giọng nói hoặc tâm sự tự do của người dùng, sau đó:
1. Bóc tách thông tin lâm sàng vào 5 Trụ Cột Y Khoa theo ĐÚNG các mã chuẩn (Schema).
2. Nhận diện các chi tiết "THỪA" (ngữ cảnh riêng: làm ca đêm, cãi nhau, uống trà sữa 16h, chia tay...) để lưu vào custom_notes.
3. Nhận diện các trụ cột "THIẾU" (chưa có thông tin) để đặt 1 câu hỏi dồn tự nhiên, ngắn gọn (chỉ 1 câu duy nhất).
4. QUY TẮC BẤT DI BẤT DỊCH VỀ Y TẾ:
   - TUYỆT ĐỐI KHÔNG hỏi, gợi ý, kê đơn hoặc đề cập đến bất kỳ loại THUỐC, THUỐC NGỦ, THUỐC AN THẦN, hay THỰC PHẨM CHỨC NĂNG (TPCN) nào.
   - Mavis chúc bạn ngủ ngon là hệ thống PHI DƯỢC LÝ (Non-pharmacological chronotherapy). Mọi can thiệp chỉ dựa trên ánh sáng, nhiệt độ phòng, thực phẩm tự nhiên (Tryptophan/Magie trong bữa ăn hàng ngày) và vi-vận động.

SCHEMA 5 TRỤ CỘT (Chỉ gán nếu người dùng nhắc đến hoặc ngụ ý):
- Trụ Cột 1 (Tâm Lý):
  + stress_level: ["low"] (thư thái), ["medium"] (vừa phải), ["high"] (áp lực, deadline, căng thẳng)
  + mood_state: ["good"] (tốt), ["brain_fog"] (uể oải, mệt mỏi), ["anxious"] (lo âu, bồn chồn)
- Trụ Cột 2 (Môi Trường):
  + env_light: ["dark"] (tối tốt), ["screen_heavy"] (nhiều ánh sáng xanh, xem màn hình), ["light_polluted"] (lọt sáng)
  + env_temp: ["ideal"] (mát mẻ 24-26°C), ["hot"] (nóng bức, hầm), ["too_cold"] (lạnh buốt)
  + env_noise: ["quiet"] (yên tĩnh), ["noisy"] (ồn ào, tiếng xe, hàng xóm)
- Trụ Cột 3 (Lối Sống & Chất Kích Thích):
  + caffeine_usage: ["none"] (không dùng), ["morning_only"] (chỉ uống sáng), ["late_high"] (uống chiều/tối/sau 11h trưa, trà đặc, nước tăng lực)
  + alcohol_nicotine: ["none"] (không), ["alcohol_dinner"] (uống bia rượu chiều/tối), ["nicotine"] (hút thuốc)
  + dinner_habit: ["light_early"] (ăn thanh đạm sớm), ["heavy_late"] (ăn muộn, nhiều dầu mỡ), ["drink_lots_water"] (uống nhiều nước tối)
  + bed_phone: ["no_phone"] (không dùng), ["lướt_tiktok_fb"] (lướt điện thoại trên giường)
- Trụ Cột 4 (Sinh Lý & Nhóm Tuổi):
  + age_group: ["young_adult"] (dưới 50 tuổi / thanh niên), ["middle_aged"] (trên 50 tuổi)
  + hormone_state: ["normal"] (bình thường), ["menopause_hotflash"] (tiền mãn kinh, bốc hỏa, vã mồ hôi đêm)
- Trụ Cột 5 (Bệnh Lý & Đau Nhức):
  + physical_pain: ["none"] (khỏe mạnh), ["neck_back_pain"] (đau mỏi cổ vai gáy, đau lưng), ["headache"] (đau đầu)
  + chronic_condition: ["none"] (không có), ["gerd"] (trào ngược dạ dày, ợ chua, đau dạ dày), ["nocturia"] (tiểu đêm)

BẠN PHẢI TRẢ VỀ DUY NHẤT 1 ĐỐI TƯỢNG JSON HỢP LỆ (Không thêm markdown ```json):
{
  "extracted_answers": {
    // Chỉ các key phát hiện được, giá trị là mảng chuỗi e.g. ["high"]
  },
  "custom_notes": {
    // Chi tiết độc lạ người dùng chia sẻ
  },
  "ai_response_text": "Lời nói của Mavis: Ghi nhận ân cần những gì vừa phát hiện + đặt 1 câu hỏi ngắn về thông tin còn thiếu (tuyệt đối không hỏi về thuốc/TPCN).",
  "quick_chips": [
    {"text": "Nội dung nút bấm nhanh 1", "fill": "Văn bản điền 1"},
    {"text": "Nội dung nút bấm nhanh 2", "fill": "Văn bản điền 2"}
  ]
}"""

    prompt = f"""{system_prompt}

ĐÁP ÁN ĐÃ CÓ TỪ TRƯỚC CỦA NGƯỜI DÙNG:
{json.dumps(current_answers or {}, ensure_ascii=False)}

CÂU NÓI NHẬT KÝ MỚI NHẤT CỦA NGƯỜI DÙNG:
"{user_text_clean}"

Hãy bóc tách và phản hồi bằng JSON:"""

    models_to_try = [
        'gemini-3.5-flash-lite',
        'gemini-3.1-flash-lite',
        'gemini-3.5-flash',
        'gemma-4-26b-a4b-it',
        'gemini-flash-latest'
    ]

    for model_name in models_to_try:
        try:
            gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
            payload_data = json.dumps({
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.4, "maxOutputTokens": 1024}
            }).encode('utf-8')

            req = urllib.request.Request(gemini_url, data=payload_data, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=10.0) as resp:
                res_json = json.loads(resp.read().decode('utf-8'))
                raw_text = res_json['candidates'][0]['content']['parts'][0]['text'].strip()

                # Clean markdown blocks
                if raw_text.startswith("```"):
                    raw_text = re.sub(r"^```[a-zA-Z]*\n?", "", raw_text)
                    raw_text = re.sub(r"\n?```$", "", raw_text)
                raw_text = raw_text.strip()

                parsed = json.loads(raw_text)

                # Check guardrails on generated text
                if check_guardrails(raw_text):
                    return baseline

                # Merge extracted into answers to get updated missing pillars
                merged = dict(current_answers or {})
                merged.update(parsed.get("extracted_answers", {}))
                missing = get_missing_pillars(merged)

                return {
                    "success": True,
                    "extracted_answers": parsed.get("extracted_answers", {}),
                    "custom_notes": parsed.get("custom_notes", {}),
                    "missing_pillars": missing,
                    "ai_response_text": parsed.get("ai_response_text") or baseline.get("ai_response_text"),
                    "quick_chips": parsed.get("quick_chips") or baseline.get("quick_chips"),
                    "is_complete": len(missing) == 0,
                    "model": model_name
                }
        except Exception as e:
            print(f"[Voice Intake Gemini] Error with {model_name}: {e}", flush=True)
            continue

    return baseline

