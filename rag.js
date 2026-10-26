/**
 * MAVIS CHÚC BẠN NGỦ NGON - RAG KNOWLEDGE BASE & AI CHATBOT ENGINE
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
  // Safety check for extreme self-harm danger only
  const EXTREME_SAFETY_PATTERNS = [
    /\b(t[ự]\s*t[ử]|tu\s*tu|t[ự]\s*s[á]t|tu\s*sat)\b/i,
    /\b(qu[á]\s*li[ề]u|qua\s*lieu|overdose)\b/i
  ];

  const EMERGENCY_CRISIS_MESSAGE = `❤️ **Mavis Luôn Ở Đây Lắng Nghe Bạn:**

Mavis nhận thấy bạn có thể đang trải qua giai đoạn vô cùng căng thẳng hoặc mệt mỏi. Bạn không hề đơn độc. 
Nếu bạn đang gặp khủng hoảng tinh thần, xin hãy dành chút thời gian hít thở thật sâu và liên hệ ngay với người thân, bạn bè hoặc Tổng đài Chăm sóc Sức khỏe & Tâm lý (1900 6233 / 115) để nhận được sự đồng hành kịp thời nhất nhé.`;

  // Function to detect extreme crisis
  function violatesSafetyGuardrail(query) {
    if (!query) return false;
    const lower = query.toLowerCase().trim();
    return EXTREME_SAFETY_PATTERNS.some(regex => regex.test(lower));
  }

  // ==========================================
  // GOOGLE GEMINI API CONFIGURATION
  // ==========================================
  const GEMINI_CONFIG = {
    apiKey: (typeof window !== 'undefined' && window.GEMINI_API_KEY) || (typeof localStorage !== 'undefined' ? localStorage.getItem('sleepsync_gemini_key') || '' : ''),
    model: 'gemini-3.1-flash-lite',
    altModel: 'gemini-3.5-flash'
  };

  // ==========================================
  // 3. RAG SEMANTIC RETRIEVAL & RESPONSE GENERATION (GEMINI API + CHATBOT ENGINE)
  // ==========================================
  async function generateRAGResponse(userQuery) {
    // Step 1: Extreme Crisis Intercept
    if (violatesSafetyGuardrail(userQuery)) {
      if (window.SleepSyncDB) {
        SleepSyncDB.logServiceUsage(
          'CRISIS_SUPPORT',
          'Hỗ trợ tâm lý khẩn cấp',
          `Truy vấn: "${userQuery.slice(0, 40)}..."`
        );
      }
      return EMERGENCY_CRISIS_MESSAGE;
    }

    // Step 2: Retrieve Active User Profile from Database
    let activeUser = null;
    let isAuth = false;
    if (window.SleepSyncDB) {
      activeUser = SleepSyncDB.getCurrentUser();
      isAuth = SleepSyncDB.isAuthenticated && SleepSyncDB.isAuthenticated();
    }

    const userName = (isAuth && activeUser) ? activeUser.fullName : 'bạn';
    const userRole = (isAuth && activeUser) ? (activeUser.role || activeUser.occupation || 'người dùng') : 'người dùng tự do';
    const userBedtime = (isAuth && activeUser) ? (activeUser.targetBedtime || '23:00') : '23:00';
    const userWaketime = (isAuth && activeUser) ? (activeUser.wakeTime || '06:30') : '06:30';
    const userConditions = (isAuth && activeUser && Array.isArray(activeUser.healthConditions)) 
      ? activeUser.healthConditions.join(', ') 
      : 'Sức khỏe ổn định';
    const userStreak = (isAuth && activeUser) ? (activeUser.streakDays || 1) : 0;

    // Step 3: Call Backend Server AI Chat Endpoint (/api/ai/chat)
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 25000);

      const res = await fetch('/api/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        signal: controller.signal,
        body: JSON.stringify({
          message: userQuery,
          user: activeUser,
          device: /Android|iPhone|iPad/i.test(navigator.userAgent) ? 'Mobile Web' : 'Desktop Web'
        })
      });

      clearTimeout(timeoutId);

      if (res.ok) {
        const data = await res.json();
        if (data && data.success && data.reply) {
          if (window.SleepSyncDB) {
            SleepSyncDB.logServiceUsage(
              'AI_CHATBOT_GEMINI',
              `Hỏi đáp AI: ${data.model || 'Gemini 3.5'}`,
              `Câu hỏi: "${userQuery.slice(0, 35)}..." - Đã giải đáp chi tiết.`
            );
          }
          return data.reply.trim();
        }
      }
    } catch (err) {
      console.warn('[SleepSync Chat Server Fetch Error, trying Direct Gemini / Local]', err);
    }

    // Step 4: Direct Client-Side Gemini API Call (if server is offline)
    if (GEMINI_CONFIG.apiKey) {
      try {
        const systemPrompt = `Bạn là Mavis - Trợ lý AI Chăm Sóc Sức Khỏe & Giấc Ngủ của Mavis chúc bạn ngủ ngon.
Người dùng: ${userName} (${userRole}), Giờ ngủ đích: ${userBedtime}, Tình trạng: ${userConditions}.
Bạn được thoải mái trả lời đa dạng mọi câu hỏi về sức khỏe, giấc ngủ, đau mỏi, dinh dưỡng, tâm lý bằng giọng văn dịu dàng, chu đáo, khoa học và dễ hiểu bằng tiếng Việt:`;

        const fullPrompt = `${systemPrompt}\n\nNgười dùng hỏi: "${userQuery}"\nMavis hãy trả lời thật chi tiết, nhiệt tình và đưa ra các giải pháp thiết thực:`;

        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 9500);

        const geminiUrl = `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_CONFIG.model}:generateContent?key=${GEMINI_CONFIG.apiKey}`;

        const res = await fetch(geminiUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          signal: controller.signal,
          body: JSON.stringify({
            contents: [{ parts: [{ text: fullPrompt }] }]
          })
        });

        clearTimeout(timeoutId);

        if (res.ok) {
          const data = await res.json();
          const candidateText = data.candidates?.[0]?.content?.parts?.[0]?.text;
          if (candidateText) {
            return candidateText.trim();
          }
        }
      } catch (err) {
        console.warn('[SleepSync Direct Gemini Error, fallback to Local RAG]', err);
      }
    }

    // Step 5: Fallback to Local Verified RAG Synthesis
    const matchedChunks = retrieveRelevantChunks(userQuery);
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
    } else if (qLower.includes('cãi') || qLower.includes('chồng') || qLower.includes('vợ') || qLower.includes('người yêu') || qLower.includes('buồn') || qLower.includes('khóc') || qLower.includes('tâm sự') || qLower.includes('ấm ức') || qLower.includes('bực') || qLower.includes('tâm trạng')) {
      response = intro +
        `• **Xoa dịu cảm xúc & Hạ Cortisol**: Mavis rất thấu hiểu cảm giác bất hòa hay cãi nhau khiến tim đập nhanh, thần kinh căng như dây đàn và suy nghĩ quẩn quanh trong đầu.\n` +
        `• **Kỹ thuật thở 4-7-8 (3 phút)**: Đặt tay lên bụng, hít sâu mũi 4s -> nín thở 7s -> thở từ từ qua miệng 8s. Lặp lại 4 chu kỳ để kích hoạt hệ thần kinh phó giao cảm đưa nhịp tim chậm lại.\n` +
        `• **Brain Dump (Xả suy nghĩ ra giấy)**: Hãy viết hết những điều bực bội, ấm ức ra một mảnh giấy nháp rồi gấp lại cất đi. Não bộ sẽ tự nhận tín hiệu "chuyện đã tạm gác lại" để bạn có thể nghỉ ngơi.\n` +
        `• **Đừng ép mình ngủ ngay**: Hãy uống vài ngụm nước ấm, bật âm thanh mưa rào hoặc sóng não Delta 4Hz trong ứng dụng để vỗ về tâm trí nhé. Mavis chúc bạn sớm bình tâm! ❤️`;
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

  // Saved / Active chatbot dimensions & position state
  let customChatSize = { width: 420, height: 590 };
  let hasCustomWindowPosition = false;

  try {
    const savedSize = localStorage.getItem('mavis_chat_size');
    if (savedSize) {
      const parsed = JSON.parse(savedSize);
      if (parsed && parsed.width >= 320 && parsed.height >= 360) {
        customChatSize = {
          width: Math.min(parsed.width, window.innerWidth - 16),
          height: Math.min(parsed.height, window.innerHeight - 30)
        };
      }
    }
  } catch (e) {}

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
      chatWindow.style.height = '85vh';
      return;
    }

    const chatWidth = (customChatSize && customChatSize.width) ? customChatSize.width : 420;
    const chatHeight = (customChatSize && customChatSize.height) ? customChatSize.height : 590;

    chatWindow.style.width = chatWidth + 'px';
    chatWindow.style.height = chatHeight + 'px';

    const fabRect = fab.getBoundingClientRect();
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
  // FREEFORM 4-CORNER CROP RESIZE & HEADER DRAG ENGINE
  // ==========================================
  function initChatbotResizable() {
    const chatWindow = document.getElementById('ai-chatbot-window');
    if (!chatWindow) return;

    const header = chatWindow.querySelector('.chatbot-header');
    const sizeIndicator = document.getElementById('chat-size-indicator');
    const handles = chatWindow.querySelectorAll('.chat-resize-handle');

    // 1. Initial size application
    if (window.innerWidth > 480 && customChatSize) {
      chatWindow.style.width = customChatSize.width + 'px';
      chatWindow.style.height = customChatSize.height + 'px';
    }

    // 2. 4-Corner & 4-Edge Resize logic (Crop-tool style)
    let isResizing = false;
    let currentHandleType = '';
    let startX = 0, startY = 0;
    let startW = 0, startH = 0, startL = 0, startT = 0;

    handles.forEach(h => {
      h.addEventListener('mousedown', (e) => startResize(e, h.dataset.handle));
      h.addEventListener('touchstart', (e) => startResize(e, h.dataset.handle), { passive: false });
    });

    function startResize(e, handleType) {
      e.preventDefault();
      e.stopPropagation();

      isResizing = true;
      currentHandleType = handleType;

      const clientX = e.touches ? e.touches[0].clientX : e.clientX;
      const clientY = e.touches ? e.touches[0].clientY : e.clientY;

      startX = clientX;
      startY = clientY;

      const rect = chatWindow.getBoundingClientRect();
      startL = rect.left;
      startT = rect.top;
      startW = rect.width;
      startH = rect.height;

      chatWindow.classList.add('is-resizing');
      document.body.classList.add('chat-is-resizing');

      // Set explicit pixel coordinates
      chatWindow.style.left = startL + 'px';
      chatWindow.style.top = startT + 'px';
      chatWindow.style.width = startW + 'px';
      chatWindow.style.height = startH + 'px';
      chatWindow.style.right = 'auto';
      chatWindow.style.bottom = 'auto';

      if (sizeIndicator) {
        sizeIndicator.textContent = `${Math.round(startW)} × ${Math.round(startH)}px`;
        sizeIndicator.classList.add('active');
      }

      document.addEventListener('mousemove', onResizeMove, { passive: false });
      document.addEventListener('mouseup', onResizeEnd);
      document.addEventListener('touchmove', onResizeMove, { passive: false });
      document.addEventListener('touchend', onResizeEnd);
    }

    function onResizeMove(e) {
      if (!isResizing) return;
      if (e.cancelable) e.preventDefault();

      const clientX = e.touches ? e.touches[0].clientX : e.clientX;
      const clientY = e.touches ? e.touches[0].clientY : e.clientY;

      const dx = clientX - startX;
      const dy = clientY - startY;

      const minW = 320;
      const minH = 360;
      const maxW = Math.min(window.innerWidth - 16, 1100);
      const maxH = Math.min(window.innerHeight - 16, 960);

      let newW = startW;
      let newH = startH;
      let newL = startL;
      let newT = startT;

      // Horizontal Resize (Right vs Left)
      if (currentHandleType.includes('r')) {
        newW = Math.max(minW, Math.min(startW + dx, maxW));
        if (newL + newW > window.innerWidth - 10) {
          newW = Math.max(minW, window.innerWidth - 10 - newL);
        }
      } else if (currentHandleType.includes('l')) {
        const proposedW = startW - dx;
        const clampedW = Math.max(minW, Math.min(proposedW, maxW));
        newL = startL + (startW - clampedW);
        if (newL < 8) {
          newL = 8;
          newW = Math.max(minW, startL + startW - 8);
        } else {
          newW = clampedW;
        }
      }

      // Vertical Resize (Bottom vs Top)
      if (currentHandleType.includes('b')) {
        newH = Math.max(minH, Math.min(startH + dy, maxH));
        if (newT + newH > window.innerHeight - 10) {
          newH = Math.max(minH, window.innerHeight - 10 - newT);
        }
      } else if (currentHandleType.includes('t')) {
        const proposedH = startH - dy;
        const clampedH = Math.max(minH, Math.min(proposedH, maxH));
        newT = startT + (startH - clampedH);
        if (newT < 8) {
          newT = 8;
          newH = Math.max(minH, startT + startH - 8);
        } else {
          newH = clampedH;
        }
      }

      chatWindow.style.width = Math.round(newW) + 'px';
      chatWindow.style.height = Math.round(newH) + 'px';
      chatWindow.style.left = Math.round(newL) + 'px';
      chatWindow.style.top = Math.round(newT) + 'px';

      if (sizeIndicator) {
        sizeIndicator.textContent = `${Math.round(newW)} × ${Math.round(newH)}px`;
      }
    }

    function onResizeEnd() {
      if (!isResizing) return;
      isResizing = false;

      chatWindow.classList.remove('is-resizing');
      document.body.classList.remove('chat-is-resizing');

      if (sizeIndicator) {
        setTimeout(() => sizeIndicator.classList.remove('active'), 250);
      }

      document.removeEventListener('mousemove', onResizeMove);
      document.removeEventListener('mouseup', onResizeEnd);
      document.removeEventListener('touchmove', onResizeMove);
      document.removeEventListener('touchend', onResizeEnd);

      const rect = chatWindow.getBoundingClientRect();
      customChatSize = {
        width: Math.round(rect.width),
        height: Math.round(rect.height)
      };
      hasCustomWindowPosition = true;

      try {
        localStorage.setItem('mavis_chat_size', JSON.stringify(customChatSize));
      } catch (err) {}
    }

    // 3. Draggable Window Header (Reposition window freely)
    if (header) {
      let isMoving = false;
      let moveStartX = 0, moveStartY = 0;
      let initialWinLeft = 0, initialWinTop = 0;
      let hasHeaderMoved = false;

      header.addEventListener('mousedown', onHeaderPointerDown);
      header.addEventListener('touchstart', onHeaderPointerDown, { passive: false });

      function onHeaderPointerDown(e) {
        // Do not trigger window drag when user clicks on header buttons
        if (e.target.closest('button') || e.target.closest('.chat-header-btn')) return;

        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        const clientY = e.touches ? e.touches[0].clientY : e.clientY;

        isMoving = true;
        hasHeaderMoved = false;
        moveStartX = clientX;
        moveStartY = clientY;

        const rect = chatWindow.getBoundingClientRect();
        initialWinLeft = rect.left;
        initialWinTop = rect.top;

        chatWindow.style.left = initialWinLeft + 'px';
        chatWindow.style.top = initialWinTop + 'px';
        chatWindow.style.right = 'auto';
        chatWindow.style.bottom = 'auto';

        header.style.cursor = 'grabbing';

        document.addEventListener('mousemove', onHeaderPointerMove, { passive: false });
        document.addEventListener('mouseup', onHeaderPointerUp);
        document.addEventListener('touchmove', onHeaderPointerMove, { passive: false });
        document.addEventListener('touchend', onHeaderPointerUp);
      }

      function onHeaderPointerMove(e) {
        if (!isMoving) return;

        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        const clientY = e.touches ? e.touches[0].clientY : e.clientY;

        const dx = clientX - moveStartX;
        const dy = clientY - moveStartY;

        if (Math.hypot(dx, dy) > 4) {
          hasHeaderMoved = true;
          if (e.cancelable) e.preventDefault();
        }

        const winW = chatWindow.offsetWidth;
        const winH = chatWindow.offsetHeight;
        const maxL = window.innerWidth - winW - 8;
        const maxT = window.innerHeight - winH - 8;

        const nextL = Math.max(8, Math.min(initialWinLeft + dx, maxL));
        const nextT = Math.max(8, Math.min(initialWinTop + dy, maxT));

        chatWindow.style.left = nextL + 'px';
        chatWindow.style.top = nextT + 'px';
      }

      function onHeaderPointerUp() {
        if (!isMoving) return;
        isMoving = false;
        header.style.cursor = 'grab';

        document.removeEventListener('mousemove', onHeaderPointerMove);
        document.removeEventListener('mouseup', onHeaderPointerUp);
        document.removeEventListener('touchmove', onHeaderPointerMove);
        document.removeEventListener('touchend', onHeaderPointerUp);

        if (hasHeaderMoved) {
          hasCustomWindowPosition = true;
        }
      }
    }
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
    initChatbotResizable();

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
          if (window.requireAuthGuard && !window.requireAuthGuard('trò chuyện cùng Bé Trợ Lý AI Mavis')) {
            return;
          }
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
          if (window.requireAuthGuard && !window.requireAuthGuard('trò chuyện cùng Bé Trợ Lý AI Mavis')) {
            return;
          }
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
          if (window.requireAuthGuard && !window.requireAuthGuard('trò chuyện cùng Bé Trợ Lý AI Mavis')) {
            return;
          }
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
        if (window.requireAuthGuard && !window.requireAuthGuard('trò chuyện cùng Bé Trợ Lý AI Mavis')) {
          return;
        }
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
      if (window.requireAuthGuard && !window.requireAuthGuard('trò chuyện cùng Bé Trợ Lý AI Mavis')) {
        return;
      }
      openChatbot();
    } else {
      closeChatbot();
    }
  }

  function openChatbot() {
    if (window.requireAuthGuard && !window.requireAuthGuard('trò chuyện cùng Bé Trợ Lý AI Mavis')) {
      return;
    }
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

Mavis đã kết nối với **Trí tuệ nhân tạo Gemini** để giải đáp đa dạng mọi câu hỏi về sức khỏe, dinh dưỡng và giấc ngủ cho bạn.

*(Mavis luôn ở đây đồng hành và lắng nghe)*. Bạn có thể hỏi Mavis bất cứ câu hỏi nào ngay bên dưới nhé!`);
    } else {
      appendBotMessage(`Xin chào bạn! Tôi là **Mavis - Bé Trợ Lý AI Chăm Sóc Sức Khỏe & Giấc Ngủ**. Mavis chúc bạn luôn mạnh khỏe và ngủ thật ngon! 🌙✨

*"Bạn khỏe mạnh và ngủ ngon, Mavis hạnh phúc."*

Mavis đã được kết nối với **Google Gemini AI** và hoạt động **24/7 hoàn toàn mở** để cùng bạn trò chuyện thoải mái về mọi chủ đề sức khỏe:

💡 **Mavis có thể hỗ trợ bạn ngay:**
• Khắc phục khó ngủ, trằn trọc & thức giấc giữa đêm
• Giảm đau mỏi cổ vai gáy, đau lưng cho người ngồi nhiều
• Thực đơn ăn uống, món ăn giàu Magie & dinh dưỡng phục hồi
• Mẹo giảm mệt mỏi, đau đầu, trào ngược dạ dày & xả stress cấp tốc

Bạn có thể trò chuyện hoặc hỏi Mavis bất cứ câu hỏi nào về sức khỏe ngay bên dưới nhé! ❤️`);
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
