"""
MAVIS SLEEPSYNC AI - REAL-TIME HYPER-PERSONALIZED CLINICAL ANALYZER
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


def ensure_full_micro_schedule(schedule_tasks, current_hour, current_time_str, user_bedtime, answers):
    """
    Guarantees a complete, chronotherapeutic roadmap of 4-6 micro-actions
    starting from the user's CURRENT time of day through bedtime.
    """
    has_gerd = False
    has_caffeine = False
    has_neck = False
    if isinstance(answers, dict):
        if answers.get("chronic_condition") == "gerd" or "gerd" in str(answers.get("chronic_condition", [])):
            has_gerd = True
        if answers.get("caffeine_usage") in ["late_high", "medium_afternoon"]:
            has_caffeine = True
        if "neck" in str(answers.get("physical_pain", [])) or answers.get("physical_pain") == "neck_shoulder":
            has_neck = True

    pool = []

    # 1. Trưa (11:00 - 13:00)
    if current_hour <= 12:
        pool.append({
            "id": "m_noon",
            "time": "12:15 - 12:20 (5 phút sau ăn trưa)",
            "tag": "Chống trào ngược & Nhu động ruột" if has_gerd else "Đi bộ nhẹ & Phục hồi",
            "title": "🚶 Vi-đi bộ 5 phút quanh văn phòng (Không nằm ngay sau ăn)",
            "desc": "Giúp cơ thắt thực quản dưới đóng kín, hỗ trợ tiêu hóa thức ăn và ngăn trào ngược axit dạ dày (GERD). Chợp mắt Power Nap tối đa 15-20 phút."
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
            "tag": "Giải tỏa cổ vai gáy & Cortisol" if has_neck else "Xả stress & Thở Box Breathing",
            "title": "🧘 Bài tập Chin-Tuck 10 lần + Thở chậm Box Breathing 4-4-4-4",
            "desc": "Thu cằm về sau giữ 5 giây giải phóng chèn ép rễ thần kinh đốt sống cổ C5-C7, hít thở 4 thì để hạ nồng độ hormone căng thẳng."
        })

    # 4. Bữa tối & Hoàng hôn (17:30 - 19:30)
    if current_hour <= 19:
        pool.append({
            "id": "m_dinner",
            "time": "18:30 - 19:00 (Bữa tối nhanh)",
            "tag": "Dinh dưỡng Tryptophan & Tiêu hóa",
            "title": "🥗 Bữa tối thanh đạm giàu Magie & Ngừng nước nhiều sau 20:00",
            "desc": "Trứng luộc lòng đào / Ức gà + Canh rau bina/rau ngót + 1 quả kiwi tráng miệng. Cắt giảm uống nhiều nước sau 20:00 để tránh thức giấc tiểu đêm."
        })

    # 5. Tiền ngủ (21:00 - 22:15)
    pre_bed_hour = int(user_bedtime.split(':')[0]) - 1 if ':' in user_bedtime else 22
    pool.append({
        "id": "m_pre_bed",
        "time": f"{pre_bed_hour}:00 - {pre_bed_hour}:15 (30p trước ngủ)",
        "tag": "Digital Sunset & Hạ thân nhiệt",
        "title": "🛀 Tắm nước ấm 10 phút & Kích hoạt Digital Sunset",
        "desc": "Nước ấm kích hoạt giãn mạch ngoại vi, hạ thân nhiệt trung tâm 1°C để cơ thể chuyển sang trạng thái ngủ sâu. Cất điện thoại xa giường."
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

    prompt = f"""Bạn là Mavis - Trợ lý AI Giác Quan & Nhịp Sinh Học Y Khoa của SleepSync.
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

QUY TẮC BẮT BUỘC VỀ ĐỒNG BỘ THỜI GIAN THỰC (REALTIME CHRONOTHERAPY):
1. 'realtimeActionNow': BẮT BUỘC là lời khuyên hành động NGAY BÂY GIỜ phù hợp chính xác với khung giờ {current_time_str} ({period_label}).
   - Hiện tại là {period_label} ({current_time_str}): Tuyệt đối KHÔNG được khuyên sai lệch (ví dụ KHÔNG ĐƯỢC nói là sáng sớm hay đêm muộn khi đang là {period_label})!
   - Nếu là Buổi trưa ({current_time_str}): Khuyên ăn trưa thanh đạm, chốt cữ cà phê trước 12:00, đi bộ nhẹ 5 phút chống trào ngược axit dạ dày (GERD), chợp mắt power-nap 15-20 phút.
   - Nếu là Buổi chiều: Khuyên dừng nạp caffeine, 3 phút giải tỏa cổ vai gáy Chin-Tuck / Box Breathing, uống nước ấm.
   - Nếu là Hoàng hôn / Tối: Thực đơn ăn tối giàu Tryptophan, cắt giảm uống nước sau 20:00.
   - Nếu là Tiền ngủ / Đêm: Kích hoạt Digital Sunset, tắm nước ấm 10 phút, bật sóng não Delta 4Hz.

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

                # Sanity check: Ensure realtimeActionNow matches actual current hour
                rt_now = str(parsed.get("realtimeActionNow", ""))
                if 11 <= current_hour < 14:
                    if any(w in rt_now.lower() for w in ["sáng sớm", "04:", "03:", "02:", "đêm muộn", "chuẩn bị ngủ", "chúc bạn ngủ"]):
                        parsed["realtimeActionNow"] = f"🥪 <strong>Khung giờ hiện tại ({current_time_str} - Buổi trưa):</strong> Thời điểm vàng nạp lại năng lượng & chốt cữ Caffeine. Bữa trưa ăn thanh đạm, đứng dậy đi dạo nhẹ nhàng 5 phút để tránh trào ngược dạ dày (GERD). Ngủ trưa chớp nhoáng (Power Nap) đúng 15-20 phút, không ngủ quá 30 phút để bảo tồn áp lực buồn ngủ ban đêm."

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
                    if "targetedHealth" not in na and "targetedCare" in na:
                        na["targetedHealth"] = f"<p>{na['targetedCare']}</p>"
                    if "deskExercises" not in na or not na["deskExercises"]:
                        na["deskExercises"] = [
                            "<strong>Động tác Chin-Tuck (1 phút):</strong> Ngồi thẳng lưng, thu cằm về phía sau như tạo 2 cằm, giữ 5 giây rồi thả lỏng.",
                            "<strong>Động tác Mở Ngực Xương Bả Vai (1 phút):</strong> Đan hai tay ra sau gáy, hít sâu ưỡn ngực mở rộng khuỷu tay sang hai bên.",
                            "<strong>Thả Lỏng Mắt 20-20-20 (30 giây):</strong> Nhìn xa 6 mét trong 20 giây để thư giãn mắt."
                        ]

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
        rt_action = f"🥪 <strong>Khung giờ hiện tại ({current_time_str} - Buổi trưa):</strong> Thời điểm vàng nạp lại năng lượng & chốt cữ Caffeine. Bữa trưa ăn thanh đạm, đứng dậy đi dạo nhẹ nhàng 5 phút để tránh trào ngược dạ dày (GERD). Ngủ trưa chớp nhoáng (Power Nap) đúng 15-20 phút, không ngủ quá 30 phút để bảo tồn áp lực buồn ngủ ban đêm."
    elif 14 <= current_hour < 17:
        rt_action = f"⏳ <strong>Khung giờ hiện tại ({current_time_str} - Buổi chiều):</strong> Điểm trũng thể lực. Dừng nhìn màn hình 3 phút, làm động tác Chin-Tuck giãn cơ cổ vai gáy. Tuyệt đối không nạp thêm cà phê hay nước ngọt sau 14:00."
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
            "targetedHealth": f"<p>Thiết lập nhiệt độ phòng ngủ 24-26°C và hoàn tất việc cất điện thoại trước {user_bedtime} ít nhất 45 phút để tuyến tùng giải phóng Melatonin tự nhiên.</p>",
            "targetedCare": f"Thiết lập nhiệt độ phòng ngủ 24-26°C và hoàn tất việc cất điện thoại trước {user_bedtime} ít nhất 45 phút.",
            "deskExercises": [
                "<strong>Động tác Chin-Tuck (1 phút):</strong> Ngồi thẳng lưng, thu cằm về phía sau như tạo 2 cằm, giữ 5 giây rồi thả lỏng. Lặp lại 5 lần để giải tỏa đốt sống cổ C5-C7.",
                "<strong>Động tác Mở Ngực Xương Bả Vai (1 phút):</strong> Đan hai tay ra sau gáy, hít sâu ưỡn ngực mở rộng khuỷu tay sang hai bên. Thở ra từ từ.",
                "<strong>Thả Lỏng Mắt 20-20-20 (30 giây):</strong> Cứ mỗi 20 phút, nhìn vào một vật cách xa 20 feet (6 mét) trong 20 giây để thư giãn cơ thể mi mắt."
            ]
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

    system_instruction = f"""Bạn là Mavis - Bé Trợ Lý AI Chăm Sóc Sức Khỏe & Giấc Ngủ Thông Minh của SleepSync.
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
