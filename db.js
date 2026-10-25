/**
 * SLEEPSYNC AI - CLIENT DATABASE ENGINE
 * Persistent storage for user profiles, authentication sessions, and service usage logs.
 * Backed by HTML5 IndexedDB with automated LocalStorage sync & fallback.
 */

const SleepSyncDB = (function() {
  const DB_NAME = 'SleepSyncAI_DB';
  const DB_VERSION = 1;
  const STORAGE_KEY_MIRROR = 'sleepsync_db_mirror';
  const STORAGE_KEY_ACTIVE_USER = 'sleepsync_active_user_id';

  let idb = null;
  let inMemoryData = null;

  // Initial Seed Data with Nguyễn Văn Hùng as primary verified user
  const DEFAULT_SEED_DATA = {
    users: [
      {
        id: 'user_hungnv',
        fullName: 'Nguyễn Văn Hùng',
        verified: true,
        role: 'Kỹ Sư IT & Công Trình',
        bio: 'Thức khuya & mê cà phê • Đang cải thiện giấc ngủ sâu NREM 💤',
        age: '30 tuổi (Nam)',
        gender: 'Nam',
        occupation: 'Kỹ Sư IT & Công Trình',
        phone: '0981 234 567',
        password: '123456',
        targetBedtime: '23:00',
        wakeTime: '06:30',
        fitnessLevel: 'Trung bình',
        healthConditions: [
          'Đau mỏi cổ vai gáy',
          'Căng thẳng deadline',
          'Ngồi nhiều máy tính'
        ],
        avatarType: 'programmer_laptop',
        streakDays: 5,
        createdAt: '2026-10-20T08:00:00.000Z',
        lastLoginAt: new Date().toISOString()
      },
      {
        id: 'user_maitt',
        fullName: 'Trần Thị Mai',
        verified: true,
        role: 'Trưởng Phòng Nhân Sự',
        bio: 'Dễ thức giấc nửa đêm • Mục tiêu ngủ thẳng giấc 7 tiếng 🌸',
        age: '38 tuổi (Nữ)',
        gender: 'Nữ',
        occupation: 'Trưởng Phòng Nhân Sự',
        phone: '0912 345 678',
        password: '123456',
        targetBedtime: '22:00',
        wakeTime: '06:00',
        fitnessLevel: 'Khá',
        healthConditions: [
          'Khó ngủ sau 1h sáng',
          'Áp lực công việc',
          'Bốc hỏa tiền mãn kinh nhẹ'
        ],
        avatarType: 'woman_professional',
        streakDays: 8,
        createdAt: '2026-10-21T09:30:00.000Z',
        lastLoginAt: '2026-10-24T18:15:00.000Z'
      },
      {
        id: 'user_hoanglm',
        fullName: 'Lê Minh Hoàng',
        verified: true,
        role: 'Bác Sĩ Nội Trú Y Khoa',
        bio: 'Trực cấp cứu đêm • Cần ngủ bù khoa học và phục hồi trí não 🩺',
        age: '34 tuổi (Nam)',
        gender: 'Nam',
        occupation: 'Bác Sĩ Nội Trú Y Khoa',
        phone: '0988 999 111',
        password: '123456',
        targetBedtime: '22:30',
        wakeTime: '06:00',
        fitnessLevel: 'Rất tốt',
        healthConditions: [
          'Trực đêm bệnh viện',
          'Áp lực tinh thần cao'
        ],
        avatarType: 'doctor_health',
        streakDays: 12,
        createdAt: '2026-10-22T10:00:00.000Z',
        lastLoginAt: '2026-10-24T21:00:00.000Z'
      }
    ],
    activeUserId: null,
    serviceUsage: [
      {
        id: 1,
        userId: 'user_hungnv',
        serviceType: 'AUTH_LOGIN',
        title: 'Đăng nhập hệ thống',
        detail: 'Tài khoản Nguyễn Văn Hùng đã đăng nhập an toàn vào SleepSync AI.',
        timestamp: new Date(Date.now() - 3600000 * 2).toISOString(),
        icon: 'fa-solid fa-arrow-right-to-bracket',
        badgeColor: 'emerald'
      },
      {
        id: 2,
        userId: 'user_hungnv',
        serviceType: 'DIAGNOSIS_5PILLARS',
        title: 'Chẩn đoán 5 Trụ Cột Y Khoa',
        detail: 'Đánh giá điểm nhịp sinh học đạt 68%. Hệ thống phát hiện stress công việc và tư thế ngồi lâu.',
        timestamp: new Date(Date.now() - 3600000 * 1.5).toISOString(),
        icon: 'fa-solid fa-heart-pulse',
        badgeColor: 'indigo'
      },
      {
        id: 3,
        userId: 'user_hungnv',
        serviceType: 'SOUNDSCAPE_AUDIO',
        title: 'Trị liệu âm thanh sóng não',
        detail: 'Kích hoạt phiên Sóng Não Delta 4Hz ru ngủ nhanh và Tiếng Mưa Rào Pink Noise (30 phút).',
        timestamp: new Date(Date.now() - 3600000 * 0.8).toISOString(),
        icon: 'fa-solid fa-headphones',
        badgeColor: 'cyan'
      },
      {
        id: 4,
        userId: 'user_hungnv',
        serviceType: 'CALENDAR_SCAN',
        title: 'Quét lịch công việc & Xuất .ics',
        detail: 'Phát hiện 3 khe trống trong ngày, xếp lịch 3 vi-hành động 2-5 phút đồng bộ Google Calendar.',
        timestamp: new Date(Date.now() - 1800000).toISOString(),
        icon: 'fa-solid fa-calendar-check',
        badgeColor: 'amber'
      }
    ],
    diagnoses: []
  };

  // Helper to load mirror from localStorage
  function loadLocalStorageMirror() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY_MIRROR);
      if (raw) {
        return JSON.parse(raw);
      }
    } catch (e) {
      console.warn('[SleepSyncDB] LocalStorage mirror parse error:', e);
    }
    return null;
  }

  // Helper to save mirror to localStorage
  function saveLocalStorageMirror(data) {
    try {
      localStorage.setItem(STORAGE_KEY_MIRROR, JSON.stringify(data));
      if (data.activeUserId) {
        localStorage.setItem(STORAGE_KEY_ACTIVE_USER, data.activeUserId);
      } else {
        localStorage.removeItem(STORAGE_KEY_ACTIVE_USER);
      }
    } catch (e) {
      console.warn('[SleepSyncDB] LocalStorage save error:', e);
    }
  }

  // Open / Init IndexedDB
  function openIndexedDB() {
    return new Promise((resolve) => {
      if (!window.indexedDB) {
        console.warn('[SleepSyncDB] IndexedDB not available, using LocalStorage mirror.');
        resolve(null);
        return;
      }

      try {
        const req = indexedDB.open(DB_NAME, DB_VERSION);

        req.onupgradeneeded = function(e) {
          const db = e.target.result;

          if (!db.objectStoreNames.contains('users')) {
            const userStore = db.createObjectStore('users', { keyPath: 'id' });
            userStore.createIndex('phone', 'phone', { unique: false });
          }

          if (!db.objectStoreNames.contains('service_usage')) {
            const usageStore = db.createObjectStore('service_usage', { keyPath: 'id', autoIncrement: true });
            usageStore.createIndex('userId', 'userId', { unique: false });
            usageStore.createIndex('timestamp', 'timestamp', { unique: false });
          }

          if (!db.objectStoreNames.contains('diagnoses')) {
            const diagStore = db.createObjectStore('diagnoses', { keyPath: 'id' });
            diagStore.createIndex('userId', 'userId', { unique: false });
          }

          if (!db.objectStoreNames.contains('meta')) {
            db.createObjectStore('meta', { keyPath: 'key' });
          }
        };

        req.onsuccess = function(e) {
          idb = e.target.result;
          resolve(idb);
        };

        req.onerror = function(e) {
          console.warn('[SleepSyncDB] IndexedDB open failed:', e);
          resolve(null);
        };
      } catch (err) {
        console.warn('[SleepSyncDB] IndexedDB init error:', err);
        resolve(null);
      }
    });
  }

  // Initialize DB instance
  async function init() {
    let mirror = loadLocalStorageMirror();
    if (!mirror || !mirror.users || mirror.users.length === 0) {
      mirror = JSON.parse(JSON.stringify(DEFAULT_SEED_DATA));
      saveLocalStorageMirror(mirror);
    }

    inMemoryData = mirror;

    // Connect to IndexedDB
    try {
      await openIndexedDB();
      if (idb) {
        // Sync in-memory to IndexedDB if needed
        syncMemoryToIndexedDB();
      }
    } catch (err) {
      console.warn('[SleepSyncDB] IndexedDB sync skipped:', err);
    }

    // Check if user previously logged in
    const savedActiveUserId = localStorage.getItem(STORAGE_KEY_ACTIVE_USER);
    const hasExplicitLogout = localStorage.getItem('sleepsync_explicit_logout') === 'true';
    if (savedActiveUserId && inMemoryData.users.some(u => u.id === savedActiveUserId)) {
      inMemoryData.activeUserId = savedActiveUserId;
    } else if (!hasExplicitLogout && inMemoryData.users.length > 0) {
      // Default to initial verified user (Nguyễn Văn Hùng) for full interactive experience
      inMemoryData.activeUserId = inMemoryData.activeUserId || inMemoryData.users[0].id;
    } else {
      inMemoryData.activeUserId = null;
    }

    console.log('[SleepSyncDB] Database initialized. Current user:', getCurrentUser()?.fullName || 'Khách (Chưa đăng nhập)');
    
    // Auto-sync with cloud server initially and continuously in realtime
    setTimeout(() => {
      syncWithCloudServer();
    }, 100);

    // Continuous Realtime Cloud Sync every 12 seconds
    setInterval(() => {
      syncWithCloudServer();
    }, 12000);

    return inMemoryData;
  }

  function syncMemoryToIndexedDB() {
    if (!idb) return;
    try {
      const tx = idb.transaction(['users', 'service_usage', 'meta'], 'readwrite');
      const userStore = tx.objectStore('users');
      const metaStore = tx.objectStore('meta');

      inMemoryData.users.forEach(u => userStore.put(u));
      metaStore.put({ key: 'activeUserId', value: inMemoryData.activeUserId });
    } catch (e) {
      console.warn('[SleepSyncDB] Error syncing to IndexedDB:', e);
    }
  }

  // Get current active user (returns null if Guest / Not logged in)
  function getCurrentUser() {
    if (!inMemoryData || !inMemoryData.users || !inMemoryData.activeUserId) return null;
    const active = inMemoryData.users.find(u => u.id === inMemoryData.activeUserId);
    return active || null;
  }

  // Check if authenticated
  function isAuthenticated() {
    return !!getCurrentUser();
  }

  // Get all users
  function getAllUsers() {
    if (!inMemoryData || !inMemoryData.users) return [];
    return [...inMemoryData.users];
  }

  // Switch active user
  function setCurrentUser(userId) {
    const user = inMemoryData.users.find(u => u.id === userId);
    if (!user) return false;

    inMemoryData.activeUserId = userId;
    user.lastLoginAt = new Date().toISOString();
    try {
      localStorage.setItem(STORAGE_KEY_ACTIVE_USER, userId);
      localStorage.removeItem('sleepsync_explicit_logout');
    } catch(e) {}
    saveLocalStorageMirror(inMemoryData);

    // Log the switch/login event
    logServiceUsage(
      'AUTH_LOGIN',
      'Đổi tài khoản đăng nhập',
      `Đã chuyển sang tài khoản ${user.fullName} (${user.role}).`
    );

    // Notify listeners
    window.dispatchEvent(new CustomEvent('sleepsync:user-changed', { detail: user }));
    return user;
  }

  // Update profile
  function updateUserProfile(userId, updatedFields) {
    const idx = inMemoryData.users.findIndex(u => u.id === userId);
    if (idx === -1) return null;

    const user = inMemoryData.users[idx];
    const updated = {
      ...user,
      ...updatedFields,
      updatedAt: new Date().toISOString()
    };

    inMemoryData.users[idx] = updated;
    saveLocalStorageMirror(inMemoryData);

    if (idb) {
      try {
        const tx = idb.transaction(['users'], 'readwrite');
        tx.objectStore('users').put(updated);
      } catch (e) {}
    }

    logServiceUsage(
      'PROFILE_UPDATE',
      'Cập nhật hồ sơ cá nhân',
      `Người dùng ${updated.fullName} đã cập nhật thông tin hồ sơ.`
    );

    window.dispatchEvent(new CustomEvent('sleepsync:user-updated', { detail: updated }));
    syncWithCloudServer();
    return updated;
  }

  // Create new user
  function createUser(userData) {
    const newId = 'user_' + Date.now().toString(36);
    const newUser = {
      id: newId,
      fullName: userData.fullName || 'Người Dùng Mới',
      verified: false,
      role: userData.role || 'Khách Hàng',
      bio: userData.bio || 'Chưa cập nhật mục tiêu giấc ngủ',
      age: userData.age || '28 tuổi',
      gender: userData.gender || 'Nam',
      occupation: userData.occupation || 'Chưa cập nhật',
      phone: userData.phone || '0900 000 000',
      targetBedtime: userData.targetBedtime || '23:00',
      wakeTime: userData.wakeTime || '06:30',
      fitnessLevel: userData.fitnessLevel || 'Trung bình',
      healthConditions: Array.isArray(userData.healthConditions) ? userData.healthConditions : ['Chưa có thông tin'],
      avatarType: userData.avatarType || 'programmer_laptop',
      createdAt: new Date().toISOString(),
      lastLoginAt: new Date().toISOString()
    };

    inMemoryData.users.push(newUser);
    setCurrentUser(newId);

    if (idb) {
      try {
        const tx = idb.transaction(['users'], 'readwrite');
        tx.objectStore('users').put(newUser);
      } catch (e) {}
    }

    logServiceUsage(
      'AUTH_REGISTER',
      'Đăng ký hồ sơ tài khoản mới',
      `Tạo thành công hồ sơ cho ${newUser.fullName} trên thiết bị.`
    );

    window.dispatchEvent(new CustomEvent('sleepsync:user-changed', { detail: newUser }));
    syncWithCloudServer();
    return newUser;
  }

  // Log service usage
  function logServiceUsage(serviceType, title, detail, metadata = {}) {
    if (!inMemoryData) return;

    let icon = 'fa-solid fa-circle-check';
    let badgeColor = 'indigo';

    if (serviceType.includes('AUTH')) {
      icon = 'fa-solid fa-user-shield';
      badgeColor = 'emerald';
    } else if (serviceType.includes('DIAGNOSIS')) {
      icon = 'fa-solid fa-heart-pulse';
      badgeColor = 'indigo';
    } else if (serviceType.includes('SOUND')) {
      icon = 'fa-solid fa-headphones';
      badgeColor = 'cyan';
    } else if (serviceType.includes('CALENDAR')) {
      icon = 'fa-solid fa-calendar-check';
      badgeColor = 'amber';
    } else if (serviceType.includes('PROFILE')) {
      icon = 'fa-solid fa-id-card';
      badgeColor = 'purple';
    }

    const logEntry = {
      id: Date.now() + Math.floor(Math.random() * 1000),
      userId: inMemoryData.activeUserId,
      serviceType,
      title,
      detail,
      metadata,
      icon,
      badgeColor,
      timestamp: new Date().toISOString()
    };

    if (!Array.isArray(inMemoryData.serviceUsage)) {
      inMemoryData.serviceUsage = [];
    }

    inMemoryData.serviceUsage.unshift(logEntry);
    if (inMemoryData.serviceUsage.length > 50) {
      inMemoryData.serviceUsage.pop();
    }

    saveLocalStorageMirror(inMemoryData);

    if (idb) {
      try {
        const tx = idb.transaction(['service_usage'], 'readwrite');
        tx.objectStore('service_usage').add(logEntry);
      } catch (e) {}
    }

    window.dispatchEvent(new CustomEvent('sleepsync:usage-logged', { detail: logEntry }));
    if (serviceType.includes('GUARDRAIL') || serviceType.includes('AUTH')) {
      syncWithCloudServer();
    }
    return logEntry;
  }

  // Get service usage logs for a user
  function getServiceUsage(userId = null, limit = 20) {
    if (!inMemoryData || !inMemoryData.serviceUsage) return [];
    const targetUserId = userId || inMemoryData.activeUserId;
    const filtered = inMemoryData.serviceUsage.filter(entry => entry.userId === targetUserId);
    return filtered.slice(0, limit);
  }

  // Save diagnosis result
  function saveDiagnosis(diagnosisResult) {
    if (!inMemoryData) return;
    const currentUser = getCurrentUser();
    const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);

    const diag = {
      id: Date.now(),
      userId: inMemoryData.activeUserId,
      userName: currentUser ? currentUser.fullName : 'Người dùng',
      score: diagnosisResult.predictedScore,
      pillars: diagnosisResult.pillars,
      summary: diagnosisResult.summary,
      answers: diagnosisResult.answers || (typeof AppState !== 'undefined' ? AppState.answers : null),
      customAnswers: diagnosisResult.customAnswers || (typeof AppState !== 'undefined' ? AppState.customAnswers : null),
      device: isMobile ? 'Mobile App (PWA)' : 'Web Browser',
      timestamp: new Date().toISOString()
    };

    if (!Array.isArray(inMemoryData.diagnoses)) {
      inMemoryData.diagnoses = [];
    }

    inMemoryData.diagnoses.unshift(diag);
    saveLocalStorageMirror(inMemoryData);

    logServiceUsage(
      'DIAGNOSIS_5PILLARS',
      'Hoàn thành chẩn đoán 5 trụ cột y khoa',
      `Điểm số giấc ngủ dự báo: ${diag.score}%. Lịch vi-hành động đã sẵn sàng.`
    );

    // Synchronize to cloud server immediately
    syncWithCloudServer();

    return diag;
  }

  // Export full JSON database backup
  function exportDatabaseBackup() {
    const jsonStr = JSON.stringify(inMemoryData, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `SleepSync_Database_Backup_${new Date().toISOString().slice(0,10)}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  // Restore from JSON
  function importDatabaseBackup(jsonString) {
    try {
      const parsed = JSON.parse(jsonString);
      if (parsed && Array.isArray(parsed.users) && parsed.users.length > 0) {
        inMemoryData = parsed;
        saveLocalStorageMirror(inMemoryData);
        syncMemoryToIndexedDB();
        window.dispatchEvent(new CustomEvent('sleepsync:user-changed', { detail: getCurrentUser() }));
        return true;
      }
    } catch (e) {
      console.error('[SleepSyncDB] Import failed:', e);
    }
    return false;
  }

  // Reset to default seed
  function resetToDefaults() {
    inMemoryData = JSON.parse(JSON.stringify(DEFAULT_SEED_DATA));
    saveLocalStorageMirror(inMemoryData);
    syncMemoryToIndexedDB();
    window.dispatchEvent(new CustomEvent('sleepsync:user-changed', { detail: getCurrentUser() }));
    return inMemoryData;
  }

  // Cloud Synchronizer between Web and Mobile App
  async function syncWithCloudServer() {
    try {
      const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
      const payload = {
        users: inMemoryData.users || [],
        serviceUsage: inMemoryData.serviceUsage || [],
        diagnoses: inMemoryData.diagnoses || [],
        deviceType: isMobile ? 'Mobile App (PWA)' : 'Web Browser'
      };

      const res = await fetch('/api/sync', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        const result = await res.json();
        if (result.success && result.data) {
          const serverData = result.data;
          if (Array.isArray(serverData.users) && serverData.users.length > 0) {
            inMemoryData.users = serverData.users;
          }
          if (Array.isArray(serverData.serviceUsage)) {
            inMemoryData.serviceUsage = serverData.serviceUsage;
          }
          if (Array.isArray(serverData.diagnoses)) {
            inMemoryData.diagnoses = serverData.diagnoses;
          }
          saveLocalStorageMirror(inMemoryData);
          syncMemoryToIndexedDB();
          console.log('[SleepSyncDB] Cloud sync complete. Total users:', inMemoryData.users.length);
          window.dispatchEvent(new CustomEvent('sleepsync:cloud-synced', { detail: result }));
          return true;
        }
      }
    } catch (err) {
      console.warn('[SleepSyncDB] Cloud sync skipped (offline or server unreachable):', err);
    }
    return false;
  }

  // Login with Cloud Account (Synchronize account to this device)
  async function loginWithCloudAccount(phoneOrId, password = '') {
    if (!phoneOrId) return { success: false, message: 'Vui lòng nhập số điện thoại hoặc ID tài khoản' };

    const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          phoneOrId,
          password: password || undefined,
          device: isMobile ? 'Mobile App (PWA)' : 'Web Browser'
        })
      });

      const data = await res.json();
      if (data.success && data.user) {
        const user = data.user;
        const existingIdx = inMemoryData.users.findIndex(u => u.id === user.id);
        if (existingIdx !== -1) {
          inMemoryData.users[existingIdx] = user;
        } else {
          inMemoryData.users.push(user);
        }

        inMemoryData.activeUserId = user.id;

        // If server returned user's diagnoses, merge them
        if (Array.isArray(data.diagnoses) && data.diagnoses.length > 0) {
          const currentDiagIds = new Set((inMemoryData.diagnoses || []).map(d => d.id));
          data.diagnoses.forEach(sd => {
            if (!currentDiagIds.has(sd.id)) {
              inMemoryData.diagnoses.unshift(sd);
            }
          });
        }

        saveLocalStorageMirror(inMemoryData);
        syncMemoryToIndexedDB();

        logServiceUsage(
          'AUTH_LOGIN',
          'Đăng nhập đồng bộ tài khoản',
          `Tài khoản ${user.fullName} đã đăng nhập và đồng bộ thành công sang thiết bị này.`
        );

        window.dispatchEvent(new CustomEvent('sleepsync:user-changed', { detail: user }));
        syncWithCloudServer();
        return { success: true, user, message: data.message || 'Đăng nhập thành công!' };
      } else {
        return { success: false, message: data.message || 'Không tìm thấy tài khoản.' };
      }
    } catch (err) {
      console.warn('[SleepSyncDB] Login cloud fallback search locally:', err);
      const cleanInput = phoneOrId.replace(/\s+/g, '').toLowerCase();
      const localUser = inMemoryData.users.find(u => {
        const uId = (u.id || '').toLowerCase();
        const uUsername = (u.username || '').toLowerCase();
        const uPhone = (u.phone || '').replace(/\s+/g, '');
        const uEmail = (u.email || '').toLowerCase();
        const uName = (u.fullName || '').toLowerCase();
        return (
          uId === cleanInput ||
          uId.replace('user_', '') === cleanInput ||
          ('user_' + cleanInput) === uId ||
          uUsername === cleanInput ||
          uPhone === cleanInput ||
          uEmail === cleanInput ||
          uName === phoneOrId.toLowerCase()
        );
      });

      if (localUser) {
        if (password && localUser.password && localUser.password !== password) {
          return { success: false, message: 'Mật khẩu không chính xác. Vui lòng kiểm tra lại!' };
        }
        setCurrentUser(localUser.id);
        return { success: true, user: localUser, message: 'Đăng nhập thành công!' };
      }
      return { success: false, message: 'Không tìm thấy tài khoản với thông tin đã nhập.' };
    }
  }

  // Register with Cloud Account
  async function registerWithCloudAccount(userData) {
    if (!userData.fullName || !userData.phone) {
      return { success: false, message: 'Vui lòng nhập họ tên và số điện thoại!' };
    }

    const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
    const payload = {
      ...userData,
      device: isMobile ? 'Mobile App (PWA)' : 'Web Browser'
    };

    try {
      const res = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await res.json();
      if (data.success && data.user) {
        const newUser = data.user;
        const existingIdx = inMemoryData.users.findIndex(u => u.id === newUser.id);
        if (existingIdx !== -1) {
          inMemoryData.users[existingIdx] = newUser;
        } else {
          inMemoryData.users.push(newUser);
        }

        setCurrentUser(newUser.id);
        syncMemoryToIndexedDB();

        logServiceUsage(
          'AUTH_REGISTER',
          'Đăng ký tài khoản thành viên mới',
          `Tài khoản ${newUser.fullName} (${newUser.phone}) đã được tạo thành công.`
        );

        window.dispatchEvent(new CustomEvent('sleepsync:user-changed', { detail: newUser }));
        return { success: true, user: newUser, message: data.message || 'Đăng ký thành công!' };
      } else {
        return { success: false, message: data.message || 'Không thể tạo tài khoản.' };
      }
    } catch (err) {
      console.warn('[SleepSyncDB] Register cloud fallback to local creation:', err);
      const newUser = createUser(userData);
      return { success: true, user: newUser, message: 'Tạo tài khoản cục bộ thành công (Máy chủ ngoại tuyến).' };
    }
  }

  // Logout Current User
  function logoutCurrentUser() {
    const currentUser = getCurrentUser();
    inMemoryData.activeUserId = null;
    try {
      localStorage.removeItem(STORAGE_KEY_ACTIVE_USER);
      localStorage.setItem('sleepsync_explicit_logout', 'true');
    } catch(e) {}
    saveLocalStorageMirror(inMemoryData);

    if (idb) {
      try {
        const tx = idb.transaction(['meta'], 'readwrite');
        tx.objectStore('meta').put({ key: 'activeUserId', value: null });
      } catch (e) {}
    }
    
    logServiceUsage(
      'AUTH_LOGOUT',
      'Đăng xuất tài khoản',
      `Người dùng ${currentUser?.fullName || 'Khách'} đã đăng xuất khỏi thiết bị.`
    );

    window.dispatchEvent(new CustomEvent('sleepsync:user-logged-out', { detail: currentUser }));
    window.dispatchEvent(new CustomEvent('sleepsync:user-changed', { detail: null }));
    return true;
  }

  // 1-Click Social Account Login (Google, Facebook, Apple)
  async function loginWithSocialAccount(provider = 'google') {
    const providerProfiles = {
      google: { name: 'Người Dùng Google', phone: 'google.account@gmail.com', avatar: 'sleep_owl', role: 'Thành viên Google Sync' },
      facebook: { name: 'Người Dùng Facebook', phone: 'fb.user@facebook.com', avatar: 'zen_meditator', role: 'Thành viên Facebook Connect' },
      apple: { name: 'Người Dùng Apple ID', phone: 'apple.id@icloud.com', avatar: 'nature_moon', role: 'Thành viên Apple ID' }
    };

    const p = providerProfiles[provider] || providerProfiles.google;
    const socialId = `user_${provider}_demo`;

    let user = inMemoryData.users.find(u => u.id === socialId || u.socialProvider === provider);
    if (!user) {
      user = {
        id: socialId,
        fullName: p.name,
        verified: true,
        role: p.role,
        bio: `Tài khoản kết nối qua ${provider.toUpperCase()} • Đồng bộ hóa nhịp sinh học tự động 🌙`,
        age: '29 tuổi',
        gender: 'Khác',
        occupation: p.role,
        phone: p.phone,
        password: '',
        targetBedtime: '23:00',
        wakeTime: '06:30',
        fitnessLevel: 'Khá',
        healthConditions: ['Đồng bộ thói quen sinh học'],
        avatarType: p.avatar,
        socialProvider: provider,
        streakDays: 3,
        createdAt: new Date().toISOString(),
        lastLoginAt: new Date().toISOString()
      };
      inMemoryData.users.push(user);
    } else {
      user.lastLoginAt = new Date().toISOString();
    }

    setCurrentUser(user.id);
    logServiceUsage(
      'AUTH_LOGIN',
      `Đăng nhập ${provider.toUpperCase()}`,
      `Người dùng ${user.fullName} đã đăng nhập 1-chạm thành công qua ${provider.toUpperCase()}.`
    );
    syncWithCloudServer();
    return { success: true, user, message: `Chào mừng ${user.fullName} đã kết nối thành công qua ${provider.toUpperCase()}!` };
  }

  return {
    init,
    getCurrentUser,
    isAuthenticated,
    getAllUsers,
    setCurrentUser,
    updateUserProfile,
    createUser,
    logServiceUsage,
    getServiceUsage,
    saveDiagnosis,
    exportDatabaseBackup,
    importDatabaseBackup,
    resetToDefaults,
    syncWithCloudServer,
    loginWithCloudAccount,
    registerWithCloudAccount,
    logoutCurrentUser,
    loginWithSocialAccount
  };
})();

// Auto initialize on load
if (typeof window !== 'undefined') {
  window.SleepSyncDB = SleepSyncDB;
}
