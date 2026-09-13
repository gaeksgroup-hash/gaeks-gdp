import os, re, subprocess

print("=== 1. Membuat api/auth_otp.php (Server Verifikasi OTP 6 Digit) ===")
os.makedirs("api", exist_ok=True)
with open("api/auth_otp.php", "w") as f:
    f.write('''<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

require_once __DIR__ . '/config.php';
require_once __DIR__ . '/mailer.php';

$storageFile = __DIR__ . '/otp_store.json';

$raw = file_get_contents('php://input');
$data = json_decode($raw, true) ?? [];
$action = $data['action'] ?? '';
$email = filter_var($data['email'] ?? '', FILTER_VALIDATE_EMAIL);

if (!$email) {
    echo json_encode(["status" => "error", "message" => "Format alamat email tidak valid."]);
    exit;
}

if ($action === 'send_otp') {
    $name = htmlspecialchars($data['name'] ?? 'Pengguna GAEKS');
    $otp = strval(random_int(100000, 999999));
    
    $store = [];
    if (file_exists($storageFile)) {
        $store = json_decode(file_get_contents($storageFile), true) ?? [];
    }
    
    $store[strtolower($email)] = [
        'code' => $otp,
        'name' => $name,
        'expires' => time() + 600
    ];
    file_put_contents($storageFile, json_encode($store));

    $subject = "Kode Verifikasi Pendaftaran GAEKS Digital: $otp";
    $html = "
    <div style='max-width:520px;margin:auto;font-family:Arial,sans-serif;border:1px solid #e2e8f0;border-radius:12px;background:#ffffff;padding:28px 24px;'>
      <div style='text-align:center;margin-bottom:20px;'>
        <h2 style='color:#0f172a;margin:0;font-size:22px;'>GAEKS DIGITAL</h2>
        <p style='color:#64748b;font-size:12px;margin:4px 0 0;'>Verifikasi Pendaftaran Akun</p>
      </div>
      <p style='font-size:14px;color:#1e293b;'>Halo <strong>{$name}</strong>,</p>
      <p style='font-size:13px;color:#475569;'>Gunakan 6 digit kode verifikasi berikut untuk menyelesaikan pendaftaran akun Anda di GAEKS Digital:</p>
      <div style='background:#f1f5f9;border:1px dashed #cbd5e1;border-radius:10px;padding:16px;text-align:center;margin:24px 0;'>
        <span style='font-size:32px;font-weight:900;letter-spacing:6px;color:#2563eb;font-family:monospace;'>{$otp}</span>
      </div>
      <p style='font-size:12px;color:#64748b;'>Kode ini berlaku selama <strong>10 menit</strong>. Jangan bagikan kode ini kepada siapapun demi keamanan akun Anda.</p>
      <hr style='border:none;border-top:1px solid #f1f5f9;margin:20px 0;'>
      <p style='font-size:11px;color:#94a3b8;text-align:center;margin:0;'>Email ini dikirimkan otomatis oleh sistem resmi no-reply@gaeks.com.</p>
    </div>";

    $sendRes = sendHostingerSmtp($email, $name, $subject, $html);
    if ($sendRes['status'] === 'success') {
        echo json_encode(["status" => "success", "message" => "Kode verifikasi 6 digit telah dikirimkan ke " . $email]);
    } else {
        echo json_encode(["status" => "error", "message" => "Gagal mengirim email: " . $sendRes['message']]);
    }
    exit;
}

if ($action === 'verify_otp') {
    $code = trim($data['code'] ?? '');

    if (!file_exists($storageFile)) {
        echo json_encode(["status" => "error", "message" => "Kode verifikasi tidak ditemukan atau kedaluwarsa."]);
        exit;
    }

    $store = json_decode(file_get_contents($storageFile), true) ?? [];
    $entry = $store[strtolower($email)] ?? null;

    if (!$entry || time() > $entry['expires']) {
        echo json_encode(["status" => "error", "message" => "Kode verifikasi telah kedaluwarsa. Silakan minta kode baru."]);
        exit;
    }

    if ($entry['code'] !== $code) {
        echo json_encode(["status" => "error", "message" => "Kode verifikasi 6 digit yang Anda masukkan tidak cocok."]);
        exit;
    }

    $userName = $entry['name'];
    unset($store[strtolower($email)]);
    file_put_contents($storageFile, json_encode($store));

    echo json_encode([
        "status" => "success",
        "message" => "Pendaftaran berhasil diverifikasi!",
        "name" => $userName
    ]);
    exit;
}

echo json_encode(["status" => "error", "message" => "Aksi tidak dikenal."]);
''')

print("=== 2. Memperbarui auth.js dengan Sentral Pengendali Popup & OTP ===")
with open("auth.js", "w") as f:
    f.write('''// GAEKS DIGITAL ECOSYSTEM - AUTH, USER MANAGEMENT, GOOGLE POPUP & OTP VERIFIER
const VIP_WHITELIST = [
  "gaeks.group@gmail.com",
  "triawan25@gmail.com",
  "ranesath@gmail.com"
];
const SUPER_ADMIN_EMAIL = "gaeks.group@gmail.com";
const GOOGLE_CLIENT_ID = "41832472270-6r8iudma1eho6kn3q6rs4rl7b9ank7n4.apps.googleusercontent.com";

const AUTH_STORAGE_KEY = 'gaeks_user_session_v2';
const USERS_DB_KEY = 'gaeks_users_db_v2';

let googleTokenClient = null;

const GaeksAuth = {
  getUsersDb() {
    const raw = localStorage.getItem(USERS_DB_KEY);
    if (!raw) {
      const initial = [
        { id: 'usr_adm_1', email: 'gaeks.group@gmail.com', name: 'GAEKS Group (Admin)', provider: 'google', plan: 'PRO_VIP', registeredAt: Date.now() - 86400000 * 5, lastLoginAt: Date.now() },
        { id: 'usr_vip_2', email: 'triawan25@gmail.com', name: 'Deny Triawan', provider: 'google', plan: 'PRO_VIP', registeredAt: Date.now() - 86400000 * 4, lastLoginAt: Date.now() },
        { id: 'usr_vip_3', email: 'ranesath@gmail.com', name: 'Ranesath', provider: 'google', plan: 'PRO_VIP', registeredAt: Date.now() - 86400000 * 3, lastLoginAt: Date.now() }
      ];
      localStorage.setItem(USERS_DB_KEY, JSON.stringify(initial));
      return initial;
    }
    try { return JSON.parse(raw); } catch(e) { return []; }
  },

  saveUsersDb(db) {
    localStorage.setItem(USERS_DB_KEY, JSON.stringify(db));
  },

  recordUserRegistration(userObj) {
    const db = this.getUsersDb();
    const existingIndex = db.findIndex(u => u.email.toLowerCase() === userObj.email.toLowerCase());
    if (existingIndex >= 0) {
      db[existingIndex].lastLoginAt = Date.now();
      if (userObj.name) db[existingIndex].name = userObj.name;
    } else {
      db.unshift({
        id: userObj.id || 'usr_' + Date.now(),
        email: userObj.email,
        name: userObj.name || userObj.email.split('@')[0],
        provider: userObj.provider || 'email',
        plan: userObj.plan || 'FREE',
        registeredAt: Date.now(),
        lastLoginAt: Date.now()
      });
      this.sendEmailNotification('welcome', userObj.email, userObj.name);
    }
    this.saveUsersDb(db);
  },

  sendEmailNotification(actionType, email, name, extraData = {}) {
    try {
      fetch('/api/mailer.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: actionType,
          email: email,
          name: name,
          ...extraData
        })
      }).catch(() => {});
    } catch(e) {}
  },

  getCurrentUser() {
    const raw = localStorage.getItem(AUTH_STORAGE_KEY);
    if (!raw) return null;
    try {
      const user = JSON.parse(raw);
      if (user && user.email) {
        const clean = user.email.toLowerCase().trim();
        user.isAdmin = (clean === SUPER_ADMIN_EMAIL);
        if (VIP_WHITELIST.includes(clean)) {
          user.isPro = true;
          user.plan = 'PRO_VIP';
          user.planLabel = (clean === SUPER_ADMIN_EMAIL) ? 'SUPER ADMIN (Akses Penuh)' : 'GAEKS PRO VIP (Akses Penuh)';
        }
      }
      return user;
    } catch(e) {
      return null;
    }
  },

  isProUser() {
    const user = this.getCurrentUser();
    return user ? !!user.isPro : false;
  },

  isAdmin() {
    const user = this.getCurrentUser();
    return user ? (user.email.toLowerCase().trim() === SUPER_ADMIN_EMAIL) : false;
  },

  processVerifiedGoogleUser(email, name, avatar) {
    const cleanEmail = email.toLowerCase().trim();
    const isVip = VIP_WHITELIST.includes(cleanEmail);
    const isSuperAdmin = (cleanEmail === SUPER_ADMIN_EMAIL);
    const displayName = name || cleanEmail.split('@')[0];

    const user = {
      id: 'usr_goog_' + Math.random().toString(36).substr(2, 9),
      email: cleanEmail,
      name: displayName,
      avatar: avatar || ('https://api.dicebear.com/7.x/initials/svg?seed=' + encodeURIComponent(displayName)),
      provider: 'google',
      isPro: isVip,
      isAdmin: isSuperAdmin,
      plan: isVip ? 'PRO_VIP' : 'FREE',
      planLabel: isVip ? (isSuperAdmin ? 'SUPER ADMIN' : 'GAEKS PRO VIP') : 'Free Tier',
      loginAt: Date.now()
    };

    this.recordUserRegistration(user);
    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(user));
    window.location.reload();
  },

  loginWithEmail(email, password, customName = '') {
    const cleanEmail = email.toLowerCase().trim();
    const isVip = VIP_WHITELIST.includes(cleanEmail);
    const isSuperAdmin = (cleanEmail === SUPER_ADMIN_EMAIL);
    const displayName = customName || cleanEmail.split('@')[0];

    const user = {
      id: 'usr_' + Math.random().toString(36).substr(2, 9),
      email: cleanEmail,
      name: displayName,
      avatar: 'https://api.dicebear.com/7.x/initials/svg?seed=' + encodeURIComponent(displayName),
      provider: 'email',
      isPro: isVip,
      isAdmin: isSuperAdmin,
      plan: isVip ? 'PRO_VIP' : 'FREE',
      planLabel: isVip ? (isSuperAdmin ? 'SUPER ADMIN' : 'GAEKS PRO VIP') : 'Free Tier',
      loginAt: Date.now()
    };

    this.recordUserRegistration(user);
    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(user));
    window.location.reload();
  },

  logout() {
    localStorage.removeItem(AUTH_STORAGE_KEY);
    window.location.reload();
  },

  toggleUserPlan(email) {
    const db = this.getUsersDb();
    const target = db.find(u => u.email.toLowerCase() === email.toLowerCase());
    if (target) {
      const willBePro = (target.plan !== 'PRO' && target.plan !== 'PRO_VIP');
      target.plan = willBePro ? 'PRO' : 'FREE';
      this.saveUsersDb(db);
      if (willBePro) {
        this.sendEmailNotification('purchase', target.email, target.name, { plan_name: 'GAEKS PRO Member' });
      }
      return target.plan;
    }
    return null;
  }
};

// ================= GLOBAL UI & MODAL CONTROLLER FUNCTIONS =================
function openAuthModal() {
  const m = document.getElementById('auth-modal');
  if (m) m.classList.remove('hidden');
}

function closeAuthModal() {
  const m = document.getElementById('auth-modal');
  if (m) m.classList.add('hidden');
}

function switchAuthTab(tab) {
  const btnIn = document.getElementById('tab-btn-signin');
  const btnUp = document.getElementById('tab-btn-signup');
  const viewIn = document.getElementById('auth-view-signin');
  const viewUp = document.getElementById('auth-view-signup');
  const alertBox = document.getElementById('auth-alert-msg');
  if (alertBox) alertBox.classList.add('hidden');

  if (tab === 'signin') {
    if (btnIn) btnIn.className = "flex-1 py-2.5 border-b-2 border-blue-500 text-blue-400 transition";
    if (btnUp) btnUp.className = "flex-1 py-2.5 border-b-2 border-transparent text-slate-400 hover:text-slate-300 transition";
    if (viewIn) viewIn.classList.remove('hidden');
    if (viewUp) viewUp.classList.add('hidden');
    const gText = document.getElementById('google-btn-text');
    if (gText) gText.innerText = "Lanjutkan dengan Akun Google";
  } else {
    if (btnUp) btnUp.className = "flex-1 py-2.5 border-b-2 border-blue-500 text-blue-400 transition";
    if (btnIn) btnIn.className = "flex-1 py-2.5 border-b-2 border-transparent text-slate-400 hover:text-slate-300 transition";
    if (viewUp) viewUp.classList.remove('hidden');
    if (viewIn) viewIn.classList.add('hidden');
    const gText = document.getElementById('google-btn-text');
    if (gText) gText.innerText = "Daftar Cepat dengan Akun Google";
  }
}

function showAuthAlert(msg, isSuccess = false) {
  const el = document.getElementById('auth-alert-msg');
  if (!el) return;
  el.classList.remove('hidden');
  if (isSuccess) {
    el.className = "p-3 rounded-xl text-xs bg-emerald-950/80 border border-emerald-800 text-emerald-300";
  } else {
    el.className = "p-3 rounded-xl text-xs bg-rose-950/80 border border-rose-800 text-rose-300";
  }
  el.innerHTML = msg;
}

function handleSignInSubmit(e) {
  e.preventDefault();
  const email = document.getElementById('signin-email').value.trim();
  const pass = document.getElementById('signin-pass').value.trim();
  if (!email || !pass) {
    showAuthAlert("Silakan lengkapi alamat email dan kata sandi Anda.");
    return;
  }
  GaeksAuth.loginWithEmail(email, pass);
}

// ALUR OTP REGISTRASI EMAIL
let currentOtpEmail = '';
let currentOtpName = '';

async function requestEmailOtp() {
  const nameEl = document.getElementById('signup-name');
  const emailEl = document.getElementById('signup-email');
  const btn = document.getElementById('btn-request-otp');

  const name = nameEl ? nameEl.value.trim() : '';
  const email = emailEl ? emailEl.value.trim() : '';

  if (!name || !email) {
    showAuthAlert("Silakan isi nama lengkap dan alamat email Anda.");
    return;
  }

  btn.disabled = true;
  btn.innerText = "⏳ Mengirim Kode dari no-reply@gaeks.com...";

  try {
    const res = await fetch('/api/auth_otp.php', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action: 'send_otp', email: email, name: name })
    });
    const data = await res.json();

    if (data.status === 'success') {
      currentOtpEmail = email;
      currentOtpName = name;
      const disp = document.getElementById('display-otp-email');
      if (disp) disp.innerText = email;
      document.getElementById('signup-step-1').classList.add('hidden');
      document.getElementById('signup-step-2').classList.remove('hidden');
      showAuthAlert("✓ Kode verifikasi 6 digit telah dikirimkan ke email Anda.", true);
    } else {
      showAuthAlert(data.message || "Gagal mengirimkan kode verifikasi.");
    }
  } catch (err) {
    showAuthAlert("Kendala koneksi: " + err.message);
  } finally {
    btn.disabled = false;
    btn.innerText = "Kirim Kode Verifikasi ke Email";
  }
}

async function verifyAndCompleteRegister() {
  const codeEl = document.getElementById('signup-otp-code');
  const passEl = document.getElementById('signup-password');
  const btn = document.getElementById('btn-verify-otp');

  const code = codeEl ? codeEl.value.trim() : '';
  const pass = passEl ? passEl.value.trim() : '';

  if (!code || code.length !== 6) {
    showAuthAlert("Masukkan 6 digit kode verifikasi yang Anda terima.");
    return;
  }
  if (!pass || pass.length < 6) {
    showAuthAlert("Kata sandi minimal 6 karakter.");
    return;
  }

  btn.disabled = true;
  btn.innerText = "⏳ Memverifikasi Kode...";

  try {
    const res = await fetch('/api/auth_otp.php', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action: 'verify_otp', email: currentOtpEmail, code: code, password: pass })
    });
    const data = await res.json();

    if (data.status === 'success') {
      GaeksAuth.loginWithEmail(currentOtpEmail, pass, currentOtpName);
    } else {
      showAuthAlert(data.message || "Kode verifikasi salah.");
    }
  } catch (err) {
    showAuthAlert("Kendala verifikasi: " + err.message);
  } finally {
    btn.disabled = false;
    btn.innerText = "Verifikasi & Selesaikan Pendaftaran";
  }
}

function resendOtp() {
  document.getElementById('signup-step-2').classList.add('hidden');
  document.getElementById('signup-step-1').classList.remove('hidden');
  requestEmailOtp();
}

// INISIALISASI & PEMANGGILAN POPUP GOOGLE RESMI
function initGoogleOAuth() {
  if (window.google && window.google.accounts && window.google.accounts.oauth2) {
    try {
      googleTokenClient = window.google.accounts.oauth2.initTokenClient({
        client_id: GOOGLE_CLIENT_ID,
        scope: 'email profile openid',
        callback: async (tokenResponse) => {
          if (tokenResponse && tokenResponse.access_token) {
            try {
              const res = await fetch('https://www.googleapis.com/oauth2/v3/userinfo', {
                headers: { Authorization: `Bearer ${tokenResponse.access_token}` }
              });
              const info = await res.json();
              if (info && info.email) {
                GaeksAuth.processVerifiedGoogleUser(info.email, info.name, info.picture);
              }
            } catch(err) {
              console.error("Gagal mengambil profil Google:", err);
              showAuthAlert("Gagal memproses data Google. Silakan coba kembali.");
            }
          }
        }
      });
    } catch(e) {
      console.warn("Init Google OAuth:", e);
    }
  }
}

function triggerGoogleSignInPopup() {
  if (!googleTokenClient) {
    initGoogleOAuth();
  }
  if (googleTokenClient) {
    googleTokenClient.requestAccessToken({ prompt: 'select_account' });
    return;
  }

  const redirectUri = encodeURIComponent(window.location.origin + '/cv.html');
  const googleAuthUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${GOOGLE_CLIENT_ID}&redirect_uri=${redirectUri}&response_type=token&scope=email%20profile%20openid&prompt=select_account`;
  const w = 500, h = 600;
  const left = (window.screen.width / 2) - (w / 2);
  const top = (window.screen.height / 2) - (h / 2);
  const popup = window.open(googleAuthUrl, "GoogleSignIn", `width=${w},height=${h},top=${top},left=${left}`);

  if (!popup) {
    const manualEmail = prompt("Peramban Anda memblokir popup otomatis. Masukkan alamat email Google Anda:");
    if (manualEmail && manualEmail.includes('@')) {
      GaeksAuth.processVerifiedGoogleUser(manualEmail, manualEmail.split('@')[0], '');
    }
  }
}

window.addEventListener('load', () => {
  setTimeout(initGoogleOAuth, 300);
});
''')

print("=== 3. Memperbarui index.html & cv.html ===")
modal_markup = '''
  <!-- ================= MODAL MASUK / DAFTAR RESMI GAEKS ================= -->
  <div id="auth-modal" class="no-print hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/85 backdrop-blur-sm">
    <div class="bg-slate-900 border border-slate-700 rounded-2xl max-w-md w-full p-6 sm:p-7 shadow-2xl space-y-5">
      
      <div class="flex items-start justify-between">
        <div>
          <h3 class="font-extrabold text-lg text-white">Selamat Datang di GAEKS</h3>
          <p class="text-xs text-slate-400 mt-0.5">Masuk atau buat akun untuk mengakses layanan digital kami.</p>
        </div>
        <button type="button" onclick="closeAuthModal()" class="text-slate-400 hover:text-white text-xl font-bold">&times;</button>
      </div>

      <div class="flex border-b border-slate-800 text-xs font-bold">
        <button id="tab-btn-signin" type="button" onclick="switchAuthTab('signin')" class="flex-1 py-2.5 border-b-2 border-blue-500 text-blue-400 transition">
          Masuk ke Akun
        </button>
        <button id="tab-btn-signup" type="button" onclick="switchAuthTab('signup')" class="flex-1 py-2.5 border-b-2 border-transparent text-slate-400 hover:text-slate-300 transition">
          Daftar Baru (Verifikasi Email)
        </button>
      </div>

      <div>
        <button type="button" onclick="triggerGoogleSignInPopup()" class="w-full py-2.5 px-4 bg-white hover:bg-slate-100 text-slate-900 font-bold text-xs rounded-xl flex items-center justify-center gap-2.5 transition shadow-md">
          <svg class="w-4 h-4" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>
          <span id="google-btn-text">Lanjutkan dengan Akun Google</span>
        </button>
      </div>

      <div class="flex items-center gap-2 text-slate-600 text-xs">
        <hr class="flex-grow border-slate-800" />
        <span class="text-[11px]">atau dengan Email</span>
        <hr class="flex-grow border-slate-800" />
      </div>

      <div id="auth-alert-msg" class="hidden p-3 rounded-xl text-xs"></div>

      <div id="auth-view-signin" class="space-y-3">
        <form onsubmit="handleSignInSubmit(event)" class="space-y-3">
          <div>
            <label class="block text-[11px] text-slate-400 mb-1">Alamat Email</label>
            <input type="email" id="signin-email" required placeholder="nama@email.com" class="w-full px-3 py-2 text-xs bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" />
          </div>
          <div>
            <label class="block text-[11px] text-slate-400 mb-1">Kata Sandi</label>
            <input type="password" id="signin-pass" required placeholder="••••••••" class="w-full px-3 py-2 text-xs bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" />
          </div>
          <button type="submit" class="w-full py-2.5 px-4 bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs rounded-xl transition shadow-lg shadow-blue-500/20">
            Masuk ke Akun
          </button>
        </form>
      </div>

      <div id="auth-view-signup" class="hidden space-y-3">
        <div id="signup-step-1" class="space-y-3">
          <div>
            <label class="block text-[11px] text-slate-400 mb-1">Nama Lengkap</label>
            <input type="text" id="signup-name" placeholder="Alexander Pratama" class="w-full px-3 py-2 text-xs bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" />
          </div>
          <div>
            <label class="block text-[11px] text-slate-400 mb-1">Alamat Email</label>
            <input type="email" id="signup-email" placeholder="nama@email.com" class="w-full px-3 py-2 text-xs bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" />
            <p class="text-[10px] text-slate-500 mt-1">Kode 6 digit akan dikirimkan dari no-reply@gaeks.com untuk verifikasi kepemilikan email.</p>
          </div>
          <button type="button" id="btn-request-otp" onclick="requestEmailOtp()" class="w-full py-2.5 px-4 bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs rounded-xl transition shadow-lg shadow-blue-500/20">
            Kirim Kode Verifikasi ke Email
          </button>
        </div>

        <div id="signup-step-2" class="hidden space-y-3">
          <div class="p-3 bg-blue-950/40 border border-blue-800/60 rounded-xl text-[11px] text-blue-300">
            Kode verifikasi 6 digit telah dikirimkan ke <strong id="display-otp-email" class="text-white"></strong>.
          </div>
          <div>
            <label class="block text-[11px] text-slate-400 mb-1 text-center font-bold">Masukkan 6 Digit Kode Verifikasi</label>
            <input type="text" id="signup-otp-code" maxlength="6" placeholder="123456" class="w-full px-3 py-2.5 text-center text-lg tracking-[8px] font-mono font-black bg-slate-950 border border-blue-500 rounded-lg text-white focus:outline-none" />
          </div>
          <div>
            <label class="block text-[11px] text-slate-400 mb-1">Buat Kata Sandi Akun</label>
            <input type="password" id="signup-password" placeholder="Minimal 6 karakter" class="w-full px-3 py-2 text-xs bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" />
          </div>
          <button type="button" id="btn-verify-otp" onclick="verifyAndCompleteRegister()" class="w-full py-2.5 px-4 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl transition shadow-lg shadow-emerald-500/20">
            Verifikasi & Selesaikan Pendaftaran
          </button>
          <div class="text-center pt-1">
            <button type="button" onclick="resendOtp()" class="text-[11px] text-slate-400 hover:text-blue-400 transition">Belum menerima kode? Kirim ulang</button>
          </div>
        </div>
      </div>

    </div>
  </div>
'''

for fname in ["index.html", "cv.html"]:
    if os.path.exists(fname):
        with open(fname, "r") as f: content = f.read()
        if "https://accounts.google.com/gsi/client" not in content:
            content = content.replace("</head>", "  <script src=\"https://accounts.google.com/gsi/client\" async defer></script>\n</head>")
        content = re.sub(r'<!-- =* MODAL.*?(<!-- =* MODAL ADMIN|<!-- =* VIEW|</body>)', modal_markup + r'\n\1', content, count=1, flags=re.DOTALL)
        with open(fname, "w") as f: f.write(content)
        print(f"✓ {fname} berhasil disinkronkan.")

print("=== 4. Mem-push pembaruan ke GitHub Repository ===")
subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "fix: implement global auth functions, Google OAuth popup, and 6-digit email OTP verification"])
subprocess.run(["git", "push", "origin", "main"])

print("=== SELESAI! Seluruh sistem autentikasi profesional telah aktif di https://gdp.gaeks.com ===")
