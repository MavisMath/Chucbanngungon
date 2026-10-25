/**
 * SLEEPSYNC AI - RAG KNOWLEDGE BASE & AI CHATBOT ENGINE
 * 
 * Features:
 * 1. Retrieval-Augmented Generation (RAG) using verified chronobiology & sleep hygiene chunks.
 * 2. Strict Safety Guardrail: ABSOLUTELY REFUSES advice on medicines, sleeping pills, 
 *    or dietary supplements (TPCN) to protect users and platform founders from liability.
 * 3. Personalized integration with active user profile from SleepSyncDB.
 * 4. Draggable Floating FAB controller (Mouse + Touch) across the entire viewport.
 */

const SleepRAG = (function() {
  // ==========================================
  // 1. VERIFIED CLINICAL & LIFESTYLE KNOWLEDGE BASE (CHUNKS)
  // ==========================================
  const KNOWLEDGE_BASE = [
    {
      id: 'circadian_basics',
      tags: ['nhịp sinh học', 'melatonin', 'ánh sáng', 'điện thoại', 'màn hình', 'phòng ngủ', 'nhiệt độ'],
      title: 'Nhịp Sinh Học & Cơ Chế Tiết Melatonin Tự Nhiên',
      content: `• Nhịp sinh học được điều hòa bởi nhân trên chéo thị giác (SCN) trong não.
• Tuyến tùng chỉ tiết Melatonin tự nhiên khi môi trường thiếu ánh sáng xanh (bước sóng 450-480nm phát ra từ smartphone, laptop, TV).
• Kích hoạt "Digital Sunset": Tắt hoặc chuyển màn hình sang chế độ Night Shift / ánh sáng ấm trước giờ ngủ ít nhất 60 phút.
• Nhiệt độ phòng ngủ lý tưởng cho giấc ngủ sâu NREM là từ 24°C đến 26°C. Thân nhiệt trung tâm cần hạ từ 1 - 1.5°C để não bộ chuyển sang trạng thái ngủ sâu.`
    },
    {
      id: 'caffeine_lifestyle',
      tags: ['cà phê', 'caffeine', 'trà', 'nước tăng lực', 'tỉnh táo', 'adenosine'],
      title: 'Cơ Chế Adenosine & Thời Điểm Chốt Cà Phê',
      content: `• Cảm giác buồn ngủ tự nhiên tích tụ thông qua phân tử Adenosine trong não suốt cả ngày.
• Caffeine là chất đối kháng cạnh tranh gắn vào thụ thể Adenosine, tạm thời ngăn não cảm nhận sự mệt mỏi nhưng không làm mất đi mệt mỏi thực sự.
• Chu kỳ bán rã của Caffeine kéo dài từ 5 đến 7 tiếng (và mất tới 10-12 tiếng để đào thải hoàn toàn khỏi gan).
• NGUYÊN TẮC VÀNG: Hãy uống cữ cà phê cuối cùng trước 11:00 trưa. Sau 12:00 trưa, chỉ nên dùng nước lọc, nước ấm hoặc trà hoa cúc loãng không chứa caffeine.`
    },
    {
      id: 'alcohol_night_wake',
      tags: ['thức giấc', 'nửa đêm', 'rượu', 'bia', 'giật mình', 'rem', 'ngủ chập chờn'],
      title: 'Nguyên Nhân Thức Giấc Nửa Đêm & Phân Mảnh Giấc Ngủ REM',
      content: `• Nhiều người lầm tưởng uống rượu bia giúp dễ ngủ, nhưng cồn gây "an thần giả" (ức chế vỏ não tạm thời).
• Ở nửa sau của đêm khi gan chuyển hóa cồn thành Acetaldehyde, giấc ngủ sẽ bị phân mảnh nghiêm trọng, ức chế hoàn toàn pha ngủ mơ (REM Sleep).
• Hậu quả: Thức giấc lúc 2h - 4h sáng với tim đập nhanh, bồn chồn, khát nước và uể oải sương mù não (Brain Fog) vào sáng hôm sau.
• GIẢI PHÁP: Không dùng đồ uống có cồn sát giờ ngủ; nếu có tiệc tối, uống nhiều nước lọc bù khoáng và kết thúc trước 19:30.`
    },
    {
      id: 'physical_desk_pain',
      tags: ['cổ vai gáy', 'đau lưng', 'mỏi cổ', 'ngồi máy tính', 'dân it', 'văn phòng', 'căng cơ'],
      title: 'Khắc Phục Đau Mỏi Cổ Vai Gáy Do Ngồi Máy Tính Nhiều',
      content: `• Ngồi máy tính liên tục gây co thắt nhóm cơ nâng vai (Levator Scapulae) và cơ hình thang (Trapezius), chèn ép tuần hoàn máu lên não.
• VI-VẬN ĐỘNG 3 PHÚT TẠI BÀN LÀM VIỆC:
  1. Động tác Chin-Tuck (Thu cằm): Ngồi thẳng lưng, dùng 2 ngón tay đẩy nhẹ cằm về phía sau như tạo cằm đôi, giữ 5 giây, lặp lại 10 lần.
  2. Mở ngực & Xoay bả vai: Đan hai tay sau gáy, mở rộng khuỷu tay hết cỡ, hít sâu nâng ngực lên trần, giữ 10 giây.
• Tư thế nằm ngủ: Dùng gối công thái học nâng đỡ đường cong sinh lý cổ, tránh gối quá cao hoặc quá xẹp.`
    },
    {
      id: 'natural_nutrition_wholefood',
      tags: ['ăn gì', 'thực đơn', 'bữa tối', 'dinh dưỡng', 'tryptophan', 'magie', 'chuối', 'kiwi', 'trứng'],
      title: 'Dinh Dưỡng Tự Nhiên Từ Bữa Ăn Thường Ngày Giúp Ngủ Ngon (Không Dùng Thuốc/TPCN)',
      content: `• Thực phẩm giàu Axit Amin Tryptophan (tiền chất tổng hợp Serotonin và Melatonin nội sinh): 
  - 1-2 quả trứng gà luộc lòng đào vào bữa tối.
  - Thịt ức gà áp chảo, hạt mè, yến mạch.
• Thực phẩm giàu Magie tự nhiên (giúp thả lỏng hệ thần kinh và cơ bắp):
  - Canh rau bina (rau chân vịt) luộc, hạt bí đỏ, chuối chín.
• Quả Kiwi: Nghiên cứu tại Đại học Y Taipei cho thấy ăn 1-2 quả Kiwi trước khi ngủ 1 giờ giúp tăng 13.4% thời lượng ngủ sâu nhờ giàu chất chống oxy hóa và serotonin tự nhiên.
• LƯU Ý UỐNG NƯỚC: Uống đủ nước ban ngày, nhưng hạn chế uống nhiều sau 20:00 và áp dụng kỹ thuật "Double Voiding" (đi tiểu 2 lần cách nhau 15 phút trước khi lên giường) để tránh thức giấc tiểu đêm.`
    },
    {
      id: 'gerd_reflux',
      tags: ['trào ngược', 'dạ dày', 'gerd', 'nóng rát', 'ợ chua', 'đầy bụng'],
      title: 'Ngăn Ngừa Trào Ngược Dạ Dày Thực Quản (GERD) Khi Ngủ',
      content: `• Trào ngược axit dạ dày gây rát ngực, ngạt thở, ho đêm và làm gián đoạn chu kỳ giấc ngủ.
• NGUYÊN TẮC 3 TIẾNG: Tuyệt đối không nằm ngay sau khi ăn. Bữa tối phải kết thúc trước giờ đi ngủ ít nhất 3 tiếng.
• TƯ THẾ NẰM KHOA HỌC: Nằm nghiêng bên trái (Left Lateral Decubitus) giúp góc tiếp giáp giữa dạ dày và thực quản nằm cao hơn mực axit dịch vị, ngăn dịch vị trào ngược hiệu quả.
• Kê cao phần đầu giường hoặc dùng gối chống trào ngược dốc 15-20 độ.`
    },
    {
      id: 'stress_anxiety_technique',
      tags: ['stress', 'căng thẳng', 'deadline', 'lo âu', 'thở', '478', 'suy nghĩ'],
      title: 'Hạ Mức Độ Cortisol & Thả Lỏng Hệ Thần Kinh Thực Vật Bằng Hơi Thở 4-7-8',
      content: `• Khi stress công việc hoặc áp lực deadline kích hoạt trục HPA, nồng độ Adrenaline và Cortisol tăng vọt khiến tim đập nhanh và não bộ luôn trong trạng thái cảnh giác.
• KỸ THUẬT THỞ 4-7-8 (Tiến sĩ Andrew Weil, Harvard):
  1. Thở hết hơi ra bằng miệng.
  2. Hít vào chậm rãi bằng mũi trong 4 giây.
  3. Nín thở giữ hơi trong 7 giây (tăng bão hòa oxy và ổn định nhịp tim).
  4. Thở ra từ từ bằng miệng tạo âm thanh "phù" êm dịu trong 8 giây.
  • Thực hiện 4 chu kỳ liên tục ngay trên giường giúp kích hoạt hệ thần kinh phó giao cảm (Parasympathetic), hạ nhịp tim và đưa não vào trạng thái sẵn sàng ngủ trong vài phút.`
    },
    {
      id: 'soundscape_frequency',
      tags: ['âm thanh', 'sóng não', 'delta', 'tiếng mưa', 'pink noise', 'chuông', 'thư giãn'],
      title: 'Cơ Chế Ru Ngủ Của Sóng Não Delta 4Hz & Âm Thanh Pink Noise',
      content: `• Sóng não Delta (tần số 0.5 - 4Hz) là sóng não chủ đạo trong giai đoạn ngủ sâu nhất (NREM Stage 3 & 4) - thời điểm não bộ quét sạch độc tố beta-amyloid và tái tạo tế bào.
• Kỹ thuật Binaural Beats: Sử dụng tai nghe với độ chênh lệch tần số 4Hz giữa hai tai giúp vỏ não tự động đồng pha (Brainwave Entrainment) và giảm số lần thức giấc.
• Tiếng mưa rào (Pink Noise) có dải tần số suy giảm đều đặn, giúp tạo tấm chắn âm học (acoustic camouflage) che phủ các tiếng ồn giao thông hoặc tiếng động đột ngột.`
    }
  ];

  // ==========================================
  // 2. STRICT MEDICINE & SUPPLEMENT GUARDRAILS
  // ==========================================
  // Patterns matching pharmaceuticals, sleeping pills, supplements (TPCN), prescription drugs
  const FORBIDDEN_MEDICINE_PATTERNS = [
    /\b(thu[ố][c|k]|thuoc)\b/i,
    /\b(thu[ố]c ng[ủu]|thuoc ngu)\b/i,
    /\b(thu[ố]c an th[ầ]n|thuoc an than)\b/i,
    /\b(th[ự]c ph[ẩ]m ch[ứ]c n[ắ]ng|thuc pham chuc nang|tpcn)\b/i,
    /\b(vi[ê]n u[ố]ng|vien uong|kẹo ng[ủu]|keo ngu)\b/i,
    /\b(b[ổ] n[ã]o|bo nao|b[ổ] m[ắ]t|collagen)\b/i,
    /\b(seduxen|stilnox|rotunda|valium|lexomil|ambien|olanzapine|diazepam|bromazepam)\b/i,
    /\b(melatonin vi[ê]n|vi[ê]n melatonin|gaba vi[ê]n|5-htp|ashwagandha vi[ê]n)\b/i,
    /\b(paracetamol|panadol|efferalgan|kh[á]ng sinh|gi[ả]m đau vi[ê]n)\b/i,
    /\b(thu[ố]c b[ắ]c|thu[ố]c nam|[đd][ô]ng y|k[ê] [đd]on)\b/i,
    /\b(mua thu[ố]c g[ì]|u[ố]ng thu[ố]c g[ì]|lo[ạ]i thu[ố]c n[à]o)\b/i,
    /\b(u[ố]ng vi[ê]n g[ì]|b[ổ] sung vi[ê]n g[ì]|th[ứ]c u[ố]ng b[ổ] sung n[à]o)\b/i
  ];

  // Standard Strict Refusal Response for liability protection
  const GUARDRAIL_REFUSAL_MESSAGE = `⚠️ **TUYÊN BỐ AN TOÀN Y TẾ & CHÍNH SÁCH MIỄN TRỪ TRÁCH NHIỆM:**

Để đảm bảo an toàn sức khỏe tối đa cho bạn và tuân thủ các quy định pháp lý y tế, **SleepSync AI được lập trình với nguyên tắc nghiêm ngặt: TUYỆT ĐỐI KHÔNG TƯ VẤN, KHÔNG CHỈ ĐỊNH VÀ KHÔNG ĐỀ XUẤT BẤT KỲ LOẠI THUỐC HAY THỰC PHẨM CHỨC NĂNG (TPCN) NÀO** dưới mọi hình thức.

🩺 **Lý do y khoa quan trọng:**
1. Việc tự ý sử dụng thuốc ngủ, thuốc an thần hoặc các viên uống bổ sung (kể cả thực phẩm chức năng) có nguy cơ gây **lệch pha thụ thể thần kinh, phụ thuộc thuốc, suy giảm khả năng tự tiết Melatonin nội sinh** hoặc gây tương tác nguy hiểm đến gan, thận và tim mạch nếu không có chẩn đoán trực tiếp từ **Bác sĩ chuyên khoa Thần kinh - Giấc ngủ**.
2. **Hướng tiếp cận phi dược lý của SleepSync AI:**
Chúng tôi chỉ tập trung vào các **giải pháp lối sống tự nhiên thuần khiết đã được khoa học chứng minh**:
   • **Điều chỉnh nhịp sinh học (Circadian Rhythm):** Đón nắng ban mai, chốt cữ cà phê trước 11:00, tắm nước ấm trước ngủ.
   • **Dinh dưỡng tự nhiên từ thức ăn thường ngày:** Trứng luộc, chuối, quả kiwi, rau bina luộc (cung cấp Tryptophan & Magie tự nhiên mà không cần viên uống).
   • **Vi-vận động thả lỏng:** Kỹ thuật thở 4-7-8 kích hoạt phó giao cảm và bài tập xoay cổ vai gáy Chin-Tuck 3 phút.

*(Nếu bạn đang gặp tình trạng mất ngủ mãn tính hoặc suy nhược nghiêm trọng, vui lòng thăm khám trực tiếp tại bệnh viện chuyên khoa để được bác sĩ kê đơn an toàn).*`;

  // Function to detect if query violates supplement/medicine guardrails
  // ==========================================
  // GOOGLE GEMINI API CONFIGURATION
  // ==========================================
  const GEMINI_CONFIG = {
    apiKey: (typeof window !== 'undefined' && window.GEMINI_API_KEY) || (typeof localStorage !== 'undefined' ? localStorage.getItem('sleepsync_gemini_key') || '' : ''),
    model: 'gemini-1.5-flash',
    altModel: 'gemini-flash-latest'
  };

  // Function to detect if query violates supplement/medicine guardrails
  function violatesSafetyGuardrail(query) {
    if (!query) return false;
    const lower = query.toLowerCase().trim();
    return FORBIDDEN_MEDICINE_PATTERNS.some(regex => regex.test(lower));
  }

  // ==========================================
  // 3. RAG SEMANTIC RETRIEVAL & RESPONSE GENERATION (GEMINI API + VERIFIED CHUNKS)
  // ==========================================
  async function generateRAGResponse(userQuery) {
    // Step 1: Strict Safety Guardrail Check (Medicine / Supplement refusal)
    if (violatesSafetyGuardrail(userQuery)) {
      if (window.SleepSyncDB) {
        SleepSyncDB.logServiceUsage(
          'GUARDRAIL_INTERCEPT',
          'Kích hoạt bộ lọc an toàn y tế (Chặn thuốc/TPCN)',
          `Truy vấn: "${userQuery.slice(0, 40)}..." đã được chuyển hướng an toàn.`
        );
      }
      return GUARDRAIL_REFUSAL_MESSAGE;
    }

    // Step 2: Retrieve Active User Profile from Database
    let activeUser = null;
    let isAuth = false;
    if (window.SleepSyncDB) {
      activeUser = SleepSyncDB.getCurrentUser();
      isAuth = SleepSyncDB.isAuthenticated && SleepSyncDB.isAuthenticated();
    }

    const userName = (isAuth && activeUser) ? activeUser.fullName : 'bạn';
    const userRole = (isAuth && activeUser) ? (activeUser.role || activeUser.occupation || 'thành viên') : 'người dùng tự do';
    const userBedtime = (isAuth && activeUser) ? (activeUser.targetBedtime || '23:00') : '23:00';
    const userWaketime = (isAuth && activeUser) ? (activeUser.wakeTime || '06:30') : '06:30';
    const userConditions = (isAuth && activeUser && Array.isArray(activeUser.healthConditions)) 
      ? activeUser.healthConditions.join(', ') 
      : 'Không có hạn chế đặc biệt';
    const userStreak = (isAuth && activeUser) ? (activeUser.streakDays || 1) : 0;

    // Step 3: Semantic Retrieval from Knowledge Base (RAG Chunks)
    const matchedChunks = retrieveRelevantChunks(userQuery);
    let ragKnowledgeContext = '';
    matchedChunks.forEach(c => {
      ragKnowledgeContext += `\n[Tài liệu Y khoa: ${c.title}]\n${c.content}\n`;
    });

    // Step 4: Call Google Gemini API (gemini-3.5-flash) with Personalized Clinical RAG
    if (GEMINI_CONFIG.apiKey) {
      try {
        let userContextPrompt = '';
        if (isAuth && activeUser) {
          userContextPrompt = `
THÔNG TIN HỒ SƠ NGƯỜI DÙNG ĐANG ĐỒNG BỘ:
- Họ tên: ${userName}
- Nghề nghiệp / Lối sống: ${userRole}
- Tuổi tác: ${activeUser.age || 'Chưa cập nhật'}
- Giờ ngủ mục tiêu: ${userBedtime} (Giờ thức dậy: ${userWaketime})
- Thể lực nền: ${activeUser.fitnessLevel || 'Trung bình'}
- Tiền sử sức khỏe & thói quen cần lưu ý: ${userConditions}
- Chuỗi ngày streak chăm sóc giấc ngủ: 🔥 ${userStreak} ngày
- Ghi chú mục tiêu cá nhân (Bio): ${activeUser.bio || 'Cải thiện giấc ngủ sâu'}`;
        } else {
          userContextPrompt = `
THÔNG TIN NGƯỜI DÙNG: Đang trò chuyện ở Chế độ Tự Do (Khách). Xưng hô thân thiện, ấm áp: "Chào bạn, Mavis chúc bạn ngủ ngon! 🌙"`;
        }

        const systemPrompt = `Bạn là Mavis - Trợ lý AI Giấc ngủ SleepSync chuyên sâu về Khoa học thần kinh và Nhịp sinh học.
${userContextPrompt}

CƠ SỞ TRI THỨC KHOA HỌC:
${ragKnowledgeContext || 'Khoa học về vệ sinh giấc ngủ, nhịp sinh học và giải pháp phi dược lý.'}

HƯỚNG DẪN TRẢ LỜI & ĐỒNG BỘ CÁ NHÂN HÓA (BẮT BUỘC TUÂN THỦ):
1. ĐỒNG BỘ THEO HỒ SƠ: Nếu người dùng đã đăng nhập (${userName}), hãy xưng hô thân mật trực tiếp với tên họ (ví dụ: "Chào bạn ${userName}"), liên kết giải pháp trực tiếp với công việc (${userRole}), tiền sử sức khỏe (${userConditions}) và mốc giờ ngủ mục tiêu (${userBedtime}).
2. NỘI DUNG THỰC TẾ, ĐI THẲNG VÀO TRỌNG TÂM: Trả lời trong 3 - 5 gạch đầu dòng có hành động cụ thể, khoa học.
3. VÍ DỤ CỤ THỂ:
   - Khi hỏi về ăn/uống: Nêu rõ tên thực phẩm tự nhiên + chất dinh dưỡng chính + thời điểm ăn sát với giờ ngủ ${userBedtime}.
   - Khi hỏi về cổ vai gáy: Nhấn mạnh vi-vận động Chin-tuck, nghỉ giải lao màn hình xanh sau mỗi giờ làm việc.
   - Khi hỏi về trào ngược/GERD: Nhắc bữa tối kết thúc trước 3 tiếng so với ${userBedtime} và nằm nghiêng bên trái.
4. NGUYÊN TẮC BẢO VỆ PHÁP LÝ TUYỆT ĐỐI: TUYỆT ĐỐI KHÔNG kê đơn, tư vấn hay gợi ý bất kỳ loại thuốc ngủ hay thực phẩm chức năng (TPCN, viên uống) nào!`;

        const fullPrompt = `${systemPrompt}\n\nNgười dùng hỏi: "${userQuery}"\nHãy trả lời bằng tiếng Việt cực kỳ chu đáo, đồng bộ theo hồ sơ và đưa ra giải pháp thiết thực:`;

        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 9500);

        const geminiUrl = `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_CONFIG.model}:generateContent?key=${GEMINI_CONFIG.apiKey}`;

        const res = await fetch(geminiUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          signal: controller.signal,
          body: JSON.stringify({
            contents: [{
              parts: [{ text: fullPrompt }]
            }]
          })
        });

        clearTimeout(timeoutId);

        if (res.ok) {
          const data = await res.json();
          const candidateText = data.candidates?.[0]?.content?.parts?.[0]?.text;
          if (candidateText) {
            // Post-Generation Safety Guardrail Check
            if (violatesSafetyGuardrail(candidateText)) {
              return GUARDRAIL_REFUSAL_MESSAGE;
            }

            if (window.SleepSyncDB) {
              SleepSyncDB.logServiceUsage(
                'AI_CHATBOT_GEMINI',
                'Hỏi đáp Trợ lý AI Gemini 3.5 Flash (Đồng bộ hồ sơ)',
                `Câu hỏi: "${userQuery.slice(0, 35)}..." - AI trả lời cá nhân hóa theo ${userName}.`
              );
            }
            return candidateText.trim();
          }
        } else {
          console.warn('[SleepSync Gemini API Error]', res.status);
        }
      } catch (err) {
        console.warn('[SleepSync Gemini Network/Timeout Error, fallback to Local RAG]', err);
      }
    }

    // Step 5: Fallback to Local Verified RAG Synthesis (Offline or API rate-limit)
    return generateLocalRAGResponse(userQuery, matchedChunks);
  }

  // Local RAG fallback generator - Personalized with active user profile
  function generateLocalRAGResponse(userQuery, matchedChunks) {
    const qLower = (userQuery || '').toLowerCase();
    let activeUser = null;
    let isAuth = false;
    if (window.SleepSyncDB) {
      activeUser = SleepSyncDB.getCurrentUser();
      isAuth = SleepSyncDB.isAuthenticated && SleepSyncDB.isAuthenticated();
    }

    const userName = (isAuth && activeUser) ? activeUser.fullName : '';
    const userRole = (isAuth && activeUser) ? (activeUser.role || activeUser.occupation || '') : '';
    const userBedtime = (isAuth && activeUser) ? (activeUser.targetBedtime || '23:00') : '23:00';
    const userConditions = (isAuth && activeUser && Array.isArray(activeUser.healthConditions))
      ? activeUser.healthConditions.join(', ')
      : '';

    let intro = '';
    if (userName) {
      intro = `Chào **${userName}**! Mavis đã đối chiếu câu hỏi của bạn với hồ sơ nhịp sinh học (Giờ ngủ đích: **${userBedtime}**):\n\n`;
    } else {
      intro = `Chào bạn! Mavis chúc bạn ngủ ngon! Dưới đây là giải pháp nhịp sinh học tối ưu:\n\n`;
    }

    let response = '';

    // Direct answer based on question topic
    if (qLower.includes('ăn') || qLower.includes('uống') || qLower.includes('thực phẩm') || qLower.includes('món') || qLower.includes('dinh dưỡng')) {
      const dinnerHour = parseInt(userBedtime.split(':')[0], 10) || 23;
      const dinnerCutoff = `${(dinnerHour - 3 + 24) % 24}:00`;
      response = intro +
        `• **Trứng gà luộc / Ức gà / Yến mạch**: Giàu Tryptophan (tổng hợp Melatonin tự nhiên giúp gây buồn ngủ).\n` +
        `• **Rau bina / Chuối chín / Hạt bí**: Giàu Magie tự nhiên (giúp thả lỏng cơ bắp và làm dịu hệ thần kinh).\n` +
        `• **1-2 quả Kiwi**: Ăn trước khi ngủ 1 giờ giúp tăng thời lượng ngủ sâu NREM.\n` +
        `• **Mốc giờ tối ưu cho bạn**: Bữa tối nên kết thúc trước **${dinnerCutoff}** (ít nhất 3 tiếng trước giờ ngủ ${userBedtime}); sau 20:00 hạn chế uống nhiều nước để tránh tiểu đêm.`;
    } else if (qLower.includes('cổ') || qLower.includes('vai') || qLower.includes('gáy') || qLower.includes('lưng') || qLower.includes('đau') || qLower.includes('mỏi')) {
      response = intro +
        `• **Động tác Chin-Tuck (1 phút)**: Rất phù hợp nếu bạn ${userRole ? 'làm ' + userRole : 'ngồi máy tính nhiều'}. Ngồi thẳng, dùng 2 ngón tay đẩy cằm về sau tạo cằm đôi, giữ 5 giây, lặp lại 10 lần.\n` +
        `• **Mở ngực & Xoay bả vai**: Đan hai tay sau gáy, mở rộng khuỷu tay hết cỡ, hít sâu giữ 10 giây để giải phóng nhóm cơ nâng vai.\n` +
        `• **Gối ngủ công thái học**: Nâng đỡ đúng độ cong đốt sống cổ C1-C7, tránh dùng gối quá cao gây gập cổ chèn ép tuần hoàn máu não.`;
    } else if (qLower.includes('stress') || qLower.includes('căng thẳng') || qLower.includes('lo') || qLower.includes('suy nghĩ') || qLower.includes('deadline')) {
      response = intro +
        `• **Kỹ thuật thở 4-7-8 (3 phút)**: Hít mũi 4s -> Nín thở 7s -> Thở miệng 8s (lặp lại 4 chu kỳ trên giường để kích hoạt hệ phó giao cảm).\n` +
        `• **Nghe sóng não Delta 4Hz**: Bấm biểu tượng 🎧 trên thanh công cụ để đưa sóng não từ Beta tỉnh táo về Delta ngủ sâu.\n` +
        `• **Viết xả suy nghĩ (Brain Dump)**: Viết nhanh 3 điều cần làm ngày mai ra sổ giấy trước ${userBedtime} 30 phút để não bộ yên tâm nghỉ ngơi.`;
    } else if (qLower.includes('cà phê') || qLower.includes('cafe') || qLower.includes('caffeine') || qLower.includes('trà')) {
      response = intro +
        `• **Chốt cữ trước 11:00 trưa**: Caffeine có chu kỳ bán rã 5-7 tiếng và mất 10-12 tiếng để gan đào thải hoàn toàn. Uống muộn sẽ chặn thụ thể Adenosine, gây mất ngủ vào mốc ${userBedtime}.\n` +
        `• **Buổi chiều**: Đổi sang nước lọc, nước ấm hoặc trà hoa cúc loãng không chứa caffeine.`;
    } else if (qLower.includes('trào ngược') || qLower.includes('dạ dày') || qLower.includes('gerd') || qLower.includes('ợ')) {
      response = intro +
        `• **Nằm nghiêng bên TRÁI**: Tư thế khoa học nhất giúp dạ dày thấp hơn cuống thực quản, ngăn dịch vị axit trào ngược.\n` +
        `• **Ăn tối trước ngủ 3 tiếng**: Bữa tối kết thúc trước 20:00 nếu bạn ngủ lúc ${userBedtime}; không ăn đồ cay nóng hoặc nhiều dầu mỡ vào bữa tối.\n` +
        `• **Kê cao đầu giường**: Dùng gối dốc nhẹ 15-20 độ để trọng lực giữ axit trong dạ dày.`;
    } else {
      response = intro +
        `• **Digital Sunset**: Cất điện thoại hoặc bật Night Shift trước giờ ngủ **${userBedtime}** ít nhất 45 phút để tuyến tùng tiết Melatonin.\n` +
        `• **Nhiệt độ phòng**: Cài đặt máy lạnh 24°C - 26°C giúp hạ nhiệt độ trung tâm cơ thể.\n` +
        `• **Bật âm thanh ru ngủ**: Nghe sóng não Delta hoặc tiếng mưa rào trong ứng dụng để đi vào giấc ngủ nhanh hơn.`;
    }

    if (window.SleepSyncDB) {
      SleepSyncDB.logServiceUsage(
        'AI_CHATBOT_RAG',
        'Hỏi đáp Trợ lý AI Giấc ngủ (Đồng bộ hồ sơ)',
        `Câu hỏi: "${userQuery.slice(0, 35)}..." - Đã đồng bộ hồ sơ ${userName || 'Khách'}.`
      );
    }

    return response;
  }

  // Tokenize and calculate relevance score
  function retrieveRelevantChunks(query) {
    const qLower = query.toLowerCase();
    const queryTokens = qLower.split(/\s+/).filter(t => t.length > 1);

    const scored = KNOWLEDGE_BASE.map(chunk => {
      let score = 0;

      // Tag matching (High weight)
      chunk.tags.forEach(tag => {
        if (qLower.includes(tag.toLowerCase())) {
          score += 6;
        }
      });

      // Title matching
      queryTokens.forEach(token => {
        if (chunk.title.toLowerCase().includes(token)) {
          score += 3;
        }
        if (chunk.content.toLowerCase().includes(token)) {
          score += 1;
        }
      });

      return { chunk, score };
    });

    // Filter and sort
    const matched = scored
      .filter(item => item.score > 2)
      .sort((a, b) => b.score - a.score)
      .slice(0, 2)
      .map(item => item.chunk);

    // If query mentions pain/neck
    if (matched.length === 0 && (qLower.includes('đau') || qLower.includes('mỏi') || qLower.includes('cổ'))) {
      const painChunk = KNOWLEDGE_BASE.find(c => c.id === 'physical_desk_pain');
      if (painChunk) matched.push(painChunk);
    }

    // If query mentions food/eat
    if (matched.length === 0 && (qLower.includes('ăn') || qLower.includes('thức ăn') || qLower.includes('món'))) {
      const foodChunk = KNOWLEDGE_BASE.find(c => c.id === 'natural_nutrition_wholefood');
      if (foodChunk) matched.push(foodChunk);
    }

    return matched;
  }

  // ==========================================
  // 4. DRAGGABLE FLOATING FAB CONTROLLER
  // ==========================================
  function initDraggableFAB() {
    const fab = document.getElementById('floating-profile-fab');
    if (!fab) return;

    // Load saved position from localStorage
    try {
      const savedPos = localStorage.getItem('sleepsync_fab_pos');
      if (savedPos) {
        const { top, left } = JSON.parse(savedPos);
        const maxLeft = window.innerWidth - 68;
        const maxTop = window.innerHeight - 68;
        const safeLeft = Math.max(8, Math.min(left, maxLeft));
        const safeTop = Math.max(8, Math.min(top, maxTop));
        fab.style.top = safeTop + 'px';
        fab.style.left = safeLeft + 'px';
        fab.style.bottom = 'auto';
        fab.style.right = 'auto';
      }
    } catch (e) {}

    let isDragging = false;
    let startX = 0;
    let startY = 0;
    let initialLeft = 0;
    let initialTop = 0;
    let hasMoved = false;

    // Mouse Events
    fab.addEventListener('mousedown', onPointerDown);
    // Touch Events
    fab.addEventListener('touchstart', onPointerDown, { passive: false });

    function onPointerDown(e) {
      // Prevent default on touch to stop scrolling while dragging
      if (e.type === 'touchstart') {
        const touch = e.touches[0];
        startX = touch.clientX;
        startY = touch.clientY;
      } else {
        if (e.button !== 0) return; // Only left click
        startX = e.clientX;
        startY = e.clientY;
      }

      const rect = fab.getBoundingClientRect();
      initialLeft = rect.left;
      initialTop = rect.top;
      hasMoved = false;
      isDragging = true;

      fab.style.cursor = 'grabbing';
      fab.classList.add('is-dragging');

      document.addEventListener('mousemove', onPointerMove);
      document.addEventListener('mouseup', onPointerUp);
      document.addEventListener('touchmove', onPointerMove, { passive: false });
      document.addEventListener('touchend', onPointerUp);
    }

    function onPointerMove(e) {
      if (!isDragging) return;

      let clientX = 0;
      let clientY = 0;

      if (e.type === 'touchmove') {
        const touch = e.touches[0];
        clientX = touch.clientX;
        clientY = touch.clientY;
        e.preventDefault(); // Stop page scrolling
      } else {
        clientX = e.clientX;
        clientY = e.clientY;
      }

      const deltaX = clientX - startX;
      const deltaY = clientY - startY;

      if (Math.hypot(deltaX, deltaY) > 5) {
        hasMoved = true;
      }

      let newLeft = initialLeft + deltaX;
      let newTop = initialTop + deltaY;

      // Clamp within screen boundaries with 8px margin
      const fabWidth = fab.offsetWidth || 58;
      const fabHeight = fab.offsetHeight || 58;
      const maxLeft = window.innerWidth - fabWidth - 8;
      const maxTop = window.innerHeight - fabHeight - 8;

      newLeft = Math.max(8, Math.min(newLeft, maxLeft));
      newTop = Math.max(8, Math.min(newTop, maxTop));

      fab.style.left = newLeft + 'px';
      fab.style.top = newTop + 'px';
      fab.style.bottom = 'auto';
      fab.style.right = 'auto';

      // Keep chatbot docked directly to the star in real-time as it moves!
      const chatWindow = document.getElementById('ai-chatbot-window');
      if (chatWindow && chatWindow.style.display !== 'none') {
        positionChatbotNearFAB();
      }
    }

    function onPointerUp(e) {
      if (!isDragging) return;
      isDragging = false;
      fab.style.cursor = 'pointer';
      fab.classList.remove('is-dragging');

      document.removeEventListener('mousemove', onPointerMove);
      document.removeEventListener('mouseup', onPointerUp);
      document.removeEventListener('touchmove', onPointerMove);
      document.removeEventListener('touchend', onPointerUp);

      if (hasMoved) {
        // Save new position
        const rect = fab.getBoundingClientRect();
        try {
          localStorage.setItem('sleepsync_fab_pos', JSON.stringify({
            top: rect.top,
            left: rect.left
          }));
        } catch (err) {}
        positionChatbotNearFAB();
      } else {
        // If it was a tap/click without dragging, toggle Chatbot!
        toggleChatbot();
      }
    }
  }

  // ==========================================
  // DYNAMIC ANCHORING: CHATBOT ATTACHES DIRECTLY TO THE STAR FAB
  // ==========================================
  function positionChatbotNearFAB() {
    const fab = document.getElementById('floating-profile-fab');
    const chatWindow = document.getElementById('ai-chatbot-window');
    if (!fab || !chatWindow) return;

    // Mobile screens: use full-width bottom sheet
    if (window.innerWidth <= 480) {
      chatWindow.style.left = '0px';
      chatWindow.style.right = '0px';
      chatWindow.style.bottom = '0px';
      chatWindow.style.top = 'auto';
      chatWindow.style.width = '100vw';
      return;
    }

    const fabRect = fab.getBoundingClientRect();
    const chatWidth = 420;
    const chatHeight = 590;
    const margin = 14;
    const gap = 12;

    let left = 0;
    let top = 0;

    // Horizontal placement:
    // If star is in right half of screen, align right edge of chatbot with star
    if (fabRect.left > window.innerWidth / 2) {
      left = fabRect.right - chatWidth;
    } else {
      // Star is in left half, align left edge of chatbot with star
      left = fabRect.left;
    }

    // Vertical placement:
    // If star is in bottom half, open ABOVE the star
    if (fabRect.top > window.innerHeight / 2) {
      top = fabRect.top - chatHeight - gap;
      if (top < margin) {
        if (window.innerHeight - fabRect.bottom - gap > chatHeight) {
          top = fabRect.bottom + gap;
        } else {
          top = margin;
        }
      }
    } else {
      // Star is in top half, open BELOW the star
      top = fabRect.bottom + gap;
      if (top + chatHeight > window.innerHeight - margin) {
        top = Math.max(margin, window.innerHeight - chatHeight - margin);
      }
    }

    // Safety boundary clamping within viewport
    left = Math.max(margin, Math.min(left, window.innerWidth - chatWidth - margin));
    top = Math.max(margin, Math.min(top, window.innerHeight - chatHeight - margin));

    chatWindow.style.position = 'fixed';
    chatWindow.style.left = left + 'px';
    chatWindow.style.top = top + 'px';
    chatWindow.style.right = 'auto';
    chatWindow.style.bottom = 'auto';
  }

  // ==========================================
  // 5. CHATBOT WINDOW CONTROLLER
  // ==========================================
  function updateChatbotUserContext() {
    const badgeEl = document.getElementById('chatbot-user-sync-badge');
    if (!badgeEl) return;
    const isAuth = window.SleepSyncDB && SleepSyncDB.isAuthenticated && SleepSyncDB.isAuthenticated();
    const user = window.SleepSyncDB ? SleepSyncDB.getCurrentUser() : null;

    if (isAuth && user) {
      badgeEl.innerHTML = `<span class="sync-dot online"></span> Đồng bộ: <strong>${escapeHTML(user.fullName || user.username)}</strong> (${user.targetBedtime || '23:00'})`;
      badgeEl.title = `Đã đồng bộ hồ sơ: ${user.fullName} (${user.role || 'Người dùng'}) | Chuỗi: ${user.streak || 0} ngày`;
    } else {
      badgeEl.innerHTML = `<span class="sync-dot free"></span> Trực tuyến 24/7 • Chế độ mở`;
      badgeEl.title = `Mavis luôn sẵn sàng hỗ trợ bất kỳ lúc nào`;
    }
  }

  function initChatbot() {
    initDraggableFAB();

    const closeBtn = document.getElementById('close-chatbot-btn');
    const clearBtn = document.getElementById('clear-chat-btn');
    const form = document.getElementById('chatbot-input-form');
    const input = document.getElementById('chatbot-text-input');
    const micBtn = document.getElementById('chatbot-mic-btn');
    const quickChips = document.querySelectorAll('.quick-chip');

    if (closeBtn) {
      closeBtn.addEventListener('click', (e) => {
        if (e) {
          e.preventDefault();
          e.stopPropagation();
        }
        closeChatbot();
      });
    }
    if (clearBtn) clearBtn.addEventListener('click', resetChat);
    if (form) {
      form.addEventListener('submit', (e) => {
        e.preventDefault();
        const text = input.value.trim();
        if (text) {
          // Botchat always active 24/7 - no auth gate block!
          sendUserMessage(text);
          input.value = '';
        }
      });
    }

    // Quick prompt chips
    quickChips.forEach(chip => {
      chip.addEventListener('click', () => {
        const query = chip.dataset.query;
        if (query) {
          // Botchat always active 24/7 - no auth gate block!
          sendUserMessage(query);
        }
      });
    });

    // Voice Input via Web Speech API
    if (micBtn && ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const recognizer = new SpeechRecognition();
      recognizer.lang = 'vi-VN';
      recognizer.continuous = false;
      recognizer.interimResults = false;

      recognizer.onstart = () => {
        micBtn.classList.add('recording');
        micBtn.innerHTML = '<i class="fa-solid fa-microphone-lines"></i>';
      };

      recognizer.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        if (transcript) {
          input.value = transcript;
          sendUserMessage(transcript);
          input.value = '';
        }
      };

      recognizer.onerror = () => {
        micBtn.classList.remove('recording');
        micBtn.innerHTML = '<i class="fa-solid fa-microphone"></i>';
      };

      recognizer.onend = () => {
        micBtn.classList.remove('recording');
        micBtn.innerHTML = '<i class="fa-solid fa-microphone"></i>';
      };

      micBtn.addEventListener('click', () => {
        try {
          recognizer.start();
        } catch (e) {
          recognizer.stop();
        }
      });
    }

    // Responsive resize handler to keep chatbot attached to star
    window.addEventListener('resize', positionChatbotNearFAB);

    // Sync context on user change / update
    window.addEventListener('sleepsync:user-changed', () => {
      updateChatbotUserContext();
      resetChat();
    });

    window.addEventListener('sleepsync:user-updated', () => {
      updateChatbotUserContext();
    });

    // Initial Welcome Message & Sync Badge
    updateChatbotUserContext();
    renderWelcomeMessage();
  }

  function toggleChatbot() {
    const chatWindow = document.getElementById('ai-chatbot-window');
    if (!chatWindow) return;

    if (chatWindow.style.display === 'none' || !chatWindow.classList.contains('active')) {
      openChatbot();
    } else {
      closeChatbot();
    }
  }

  function openChatbot() {
    const chatWindow = document.getElementById('ai-chatbot-window');
    if (!chatWindow) return;

    // Anchor chatbot right next to the star position!
    positionChatbotNearFAB();

    chatWindow.style.display = 'flex';
    setTimeout(() => chatWindow.classList.add('active'), 10);

    const input = document.getElementById('chatbot-text-input');
    if (input) setTimeout(() => input.focus(), 150);

    updateChatbotUserContext();
    scrollToBottom();
  }

  function closeChatbot() {
    const chatWindow = document.getElementById('ai-chatbot-window');
    if (!chatWindow) return;
    chatWindow.classList.remove('active');
    setTimeout(() => {
      chatWindow.style.display = 'none';
    }, 250);
  }

  function resetChat() {
    const container = document.getElementById('chatbot-messages');
    if (container) container.innerHTML = '';
    renderWelcomeMessage();
  }

  function renderWelcomeMessage() {
    updateChatbotUserContext();
    const isAuth = window.SleepSyncDB && SleepSyncDB.isAuthenticated && SleepSyncDB.isAuthenticated();
    const user = window.SleepSyncDB ? SleepSyncDB.getCurrentUser() : null;

    if (isAuth && user) {
      appendBotMessage(`Xin chào **${user.fullName}**! Tôi là **Mavis - Trợ Lý Giấc Ngủ**. Mavis chúc bạn ngủ ngon! 🌙✨

*"Bạn ngủ ngon, Mavis hạnh phúc."*

✨ **Hồ sơ của bạn đã kết nối thành công:**
• Nghề nghiệp / Lối sống: **${user.role || 'Chưa cập nhật'}**
• Mục tiêu ngủ: **${user.targetBedtime || '23:00'}** | Thức dậy: **${user.wakeTime || '06:30'}**
• Chuỗi ngủ ngon: **🔥 ${user.streak || 1} ngày liên tiếp**
${user.healthConditions && user.healthConditions.length ? `• Tình trạng cần lưu ý: *${user.healthConditions.join(', ')}*` : ''}

Mavis đã sẵn sàng phân tích và đồng hành cùng bạn để cải thiện nhịp sinh học, ngủ sâu giấc và tràn đầy năng lượng mỗi ngày.

*(Lưu ý an toàn: Mavis tư vấn giải pháp phi dược lý lành tính, **tuyệt đối không kê đơn thuốc hay TPCN**)*. Bạn cần Mavis hỗ trợ gì hôm nay?`);
    } else {
      appendBotMessage(`Xin chào bạn! Tôi là **Mavis - Trợ Lý Giấc Ngủ Thông Minh**. Mavis chúc bạn ngủ ngon! 🌙✨

*"Bạn ngủ ngon, Mavis hạnh phúc."*

Mavis luôn hoạt động **24/7 hoàn toàn mở** để hỗ trợ bạn bất kỳ lúc nào — không cần đăng nhập hay điều kiện phức tạp!

💡 **Mavis có thể hỗ trợ bạn ngay:**
• Khắc phục thức giấc lúc 3h sáng & khó vào giấc
• Giãn cơ cổ vai gáy 3 phút cho dân văn phòng
• Món ăn giàu Magie & Tryptophan từ bữa cơm gia đình
• Bài tập thở 4-7-8 giúp thư giãn thần kinh cấp tốc

*(Lưu ý y tế: Mavis chỉ tư vấn giải pháp phi dược lý lành tính, **tuyệt đối không kê đơn thuốc hay TPCN**)*. Bạn có thể hỏi Mavis bất cứ câu hỏi nào ngay bên dưới nhé!`);
    }
  }

  async function sendUserMessage(text) {
    appendUserMessage(text);
    scrollToBottom();

    // Show AI typing indicator
    const typingId = showTypingIndicator();

    try {
      const answer = await generateRAGResponse(text);
      removeTypingIndicator(typingId);
      appendBotMessage(answer);
      scrollToBottom();
    } catch (err) {
      removeTypingIndicator(typingId);
      appendBotMessage("Xin lỗi bạn, kết nối AI tạm thời bị gián đoạn. Bạn vui lòng thử lại sau giây lát nhé!");
      scrollToBottom();
    }
  }

  function appendUserMessage(text) {
    const container = document.getElementById('chatbot-messages');
    if (!container) return;

    const div = document.createElement('div');
    div.className = 'chat-msg msg-user';
    div.innerHTML = `
      <div class="msg-bubble">${escapeHTML(text)}</div>
      <div class="msg-avatar"><i class="fa-solid fa-user"></i></div>
    `;
    container.appendChild(div);
  }

  function appendBotMessage(markdownText) {
    const container = document.getElementById('chatbot-messages');
    if (!container) return;

    const div = document.createElement('div');
    div.className = 'chat-msg msg-bot';
    div.innerHTML = `
      <div class="msg-avatar bot-avatar-wrap"><i class="fa-solid fa-wand-magic-sparkles"></i></div>
      <div class="msg-bubble">${formatMarkdownToHTML(markdownText)}</div>
    `;
    container.appendChild(div);
  }

  function showTypingIndicator() {
    const container = document.getElementById('chatbot-messages');
    if (!container) return null;

    const id = 'typing-' + Date.now();
    const div = document.createElement('div');
    div.id = id;
    div.className = 'chat-msg msg-bot msg-typing';
    div.innerHTML = `
      <div class="msg-avatar bot-avatar-wrap"><i class="fa-solid fa-wand-magic-sparkles"></i></div>
      <div class="msg-bubble typing-dots">
        <span></span><span></span><span></span>
      </div>
    `;
    container.appendChild(div);
    scrollToBottom();
    return id;
  }

  function removeTypingIndicator(id) {
    if (!id) return;
    const el = document.getElementById(id);
    if (el) el.remove();
  }

  function scrollToBottom() {
    const container = document.getElementById('chatbot-messages');
    if (container) {
      container.scrollTop = container.scrollHeight;
    }
  }

  function escapeHTML(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function formatMarkdownToHTML(md) {
    if (!md) return '';
    let html = md;
    
    // Headings
    html = html.replace(/^### (.*$)/gim, '<h5 class="chat-md-h5">$1</h5>');
    html = html.replace(/^## (.*$)/gim, '<h4 class="chat-md-h4">$1</h4>');

    // Bold
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Italic
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');

    // Bullet points
    html = html.replace(/^[•\-] (.*$)/gim, '<li class="chat-bullet">$1</li>');

    // Paragraphs / line breaks
    html = html.replace(/\n\n/g, '<div class="chat-space"></div>');
    html = html.replace(/\n/g, '<br>');

    return html;
  }

  return {
    initChatbot,
    toggleChatbot,
    openChatbot,
    closeChatbot,
    updateChatbotUserContext,
    generateRAGResponse,
    violatesSafetyGuardrail
  };
})();

// Global window helpers for direct inline onclick and external modules
window.SleepRAG = SleepRAG;
window.closeChatbot = () => SleepRAG.closeChatbot();
window.openChatbot = () => SleepRAG.openChatbot();
window.toggleChatbot = () => SleepRAG.toggleChatbot();

// Auto initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  SleepRAG.initChatbot();
});
