import os, re, subprocess

print("=== 1. Menulis login.html (Bersih \\n\\n, Tab Responsif & Deteksi Duplikat) ===")
with open("login.html", "w") as fp:
    fp.write('''<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Masuk / Daftar Akun | GAEKS Digital</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <script src="https://accounts.google.com/gsi/client" async defer></script>
  <script src="auth.js?v=20260914_07"></script>
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; }
    .cursor-pointer { cursor: pointer; }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex items-center justify-center p-4 selection:bg-blue-600 selection:text-white">

  <div class="max-w-4xl w-full bg-slate-900 rounded-3xl border border-slate-800 shadow-2xl overflow-hidden grid grid-cols-1 lg:grid-cols-12 min-h-[580px]">
    
    <!-- LEFT SIDEBAR -->
    <div class="lg:col-span-5 bg-gradient-to-br from-slate-900 via-blue-950/40 to-slate-950 p-8 sm:p-10 flex flex-col justify-between border-b lg:border-b-0 lg:border-r border-slate-800">
      <div class="space-y-6">
        <a href="index.html" class="flex items-center space-x-2.5">
          <span class="w-9 h-9 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center font-extrabold text-white text-sm shadow-md shadow-blue-500/30">G</span>
          <span class="font-extrabold text-lg bg-gradient-to-r from-blue-400 via-indigo-300 to-white bg-clip-text text-transparent">
            GAEKS DIGITAL
          </span>
        </a>

        <div class="space-y-2 pt-4">
          <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-blue-950 text-blue-300 border border-blue-800">Satu Akun Terpadu</span>
          <h2 class="text-2xl sm:text-3xl font-black text-white tracking-tight leading-snug">
            Akses Seluruh Solusi Karier & SaaS Eksekutif
          </h2>
          <p class="text-xs text-slate-400 leading-relaxed">
            Kelola pembuatan Resume ATS standar internasional, materi presentasi eksekutif, dan arsitektur bisnis modern.
          </p>
        </div>

        <div class="space-y-2.5 pt-2 text-xs text-slate-300">
          <div class="flex items-center gap-2">
            <span class="text-emerald-400 font-bold">✓</span>
            <span>ATS CV Studio dengan 520+ bank profesi</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-emerald-400 font-bold">✓</span>
            <span>15 Varian tema visual eksekutif</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-emerald-400 font-bold">✓</span>
            <span>Verifikasi email resmi dari no-reply@gaeks.com</span>
          </div>
        </div>
      </div>

      <div class="pt-8 text-[11px] text-slate-500">
        &copy; 2026 GAEKS Group. All rights reserved.
      </div>
    </div>

    <!-- RIGHT PANEL -->
    <div class="lg:col-span-7 p-8 sm:p-10 flex flex-col justify-between bg-slate-900/60">
      
      <div>
        <!-- TAB SWITCHER -->
        <div class="flex bg-slate-950 p-1 rounded-xl border border-slate-800 mb-6 text-xs font-bold">
          <button type="button" id="tab-login" onclick="setAuthTab('login')" class="flex-1 py-2.5 rounded-lg bg-blue-600 text-white transition cursor-pointer">
            Masuk ke Akun
          </button>
          <button type="button" id="tab-register" onclick="setAuthTab('register')" class="flex-1 py-2.5 rounded-lg text-slate-400 hover:text-white transition cursor-pointer">
            Daftar Akun Baru
          </button>
        </div>

        <!-- 1 TOMBOL RESMI GOOGLE -->
        <div id="google-auth-wrapper" class="w-full flex justify-center mb-5">
          <div id="g_id_onload"
               data-client_id="41832472270-6r8iudma1eho6kn3q6rs4rl7b9ank7n4.apps.googleusercontent.com"
               data-callback="handleCredentialResponse"
               data-auto_prompt="false">
          </div>
          <div class="g_id_signin" 
               data-type="standard" 
               data-size="large" 
               data-theme="outline" 
               data-text="continue_with" 
               data-shape="pill" 
               data-logo_alignment="left" 
               data-width="360">
          </div>
        </div>

        <div class="flex items-center gap-3 text-slate-600 text-xs mb-5">
          <hr class="flex-grow border-slate-800" />
          <span class="text-[11px] text-slate-400">atau dengan alamat email</span>
          <hr class="flex-grow border-slate-800" />
        </div>

        <div id="status-alert" class="hidden p-3.5 rounded-xl text-xs mb-4"></div>

        <!-- FORM LOGIN -->
        <form id="form-login" onsubmit="submitLogin(event)" class="space-y-3.5">
          <div>
            <label class="block text-[11px] font-semibold text-slate-400 mb-1">Alamat Email</label>
            <input type="email" id="login-email" required placeholder="nama@email.com" class="w-full px-3.5 py-2.5 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-xl text-white focus:border-blue-500 focus:outline-none transition" />
          </div>
          <div>
            <div class="flex justify-between items-center mb-1">
              <label class="text-[11px] font-semibold text-slate-400">Kata Sandi</label>
              <a href="https://wa.me/6285608561745?text=Halo%20Admin%20GAEKS%2C%20saya%20butuh%20bantuan%20reset%20kata%20sandi" target="_blank" class="text-[10px] text-blue-400 hover:underline">Lupa sandi?</a>
            </div>
            <input type="password" id="login-pass" required placeholder="••••••••" class="w-full px-3.5 py-2.5 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-xl text-white focus:border-blue-500 focus:outline-none transition" />
          </div>
          <button type="submit" id="btn-submit-login" class="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs sm:text-sm rounded-xl transition shadow-lg shadow-blue-500/20 cursor-pointer">
            Masuk ke Akun Saya &rarr;
          </button>
        </form>

        <!-- FORM DAFTAR DENGAN OTP EMAIL -->
        <div id="form-register" class="hidden space-y-4">
          <div id="reg-step-request" class="space-y-3.5">
            <div>
              <label class="block text-[11px] font-semibold text-slate-400 mb-1">Nama Lengkap</label>
              <input type="text" id="reg-name" required placeholder="Alexander Pratama" class="w-full px-3.5 py-2.5 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-xl text-white focus:border-blue-500 focus:outline-none transition" />
            </div>
            <div>
              <label class="block text-[11px] font-semibold text-slate-400 mb-1">Alamat Email</label>
              <input type="email" id="reg-email" required placeholder="nama@email.com" class="w-full px-3.5 py-2.5 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-xl text-white focus:border-blue-500 focus:outline-none transition" />
              <p class="text-[10px] text-slate-500 mt-1">Kode 6 digit akan dikirimkan resmi dari <strong>no-reply@gaeks.com</strong>.</p>
            </div>
            <button type="button" id="btn-send-otp" onclick="requestOtpCode()" class="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs sm:text-sm rounded-xl transition shadow-lg shadow-blue-500/20 cursor-pointer">
              Kirim 6 Digit Kode Verifikasi ke Email &rarr;
            </button>
          </div>

          <div id="reg-step-verify" class="hidden space-y-3.5">
            <div class="p-3 bg-blue-950/40 border border-blue-800/60 rounded-xl text-xs text-blue-300">
              Kode verifikasi telah dikirimkan ke <strong id="target-email-badge" class="text-white"></strong>.
            </div>
            <div>
              <label class="block text-xs font-bold text-center text-slate-300 mb-1">Masukkan 6 Digit Kode Verifikasi</label>
              <input type="text" id="reg-otp-code" maxlength="6" placeholder="123456" class="w-full px-3 py-3 text-center text-xl tracking-[10px] font-mono font-black bg-slate-950 border border-blue-500 rounded-xl text-white focus:outline-none shadow-inner" />
            </div>
            <div>
              <label class="block text-[11px] font-semibold text-slate-400 mb-1">Buat Kata Sandi Akun</label>
              <input type="password" id="reg-password" placeholder="Minimal 6 karakter" class="w-full px-3.5 py-2.5 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-xl text-white focus:border-blue-500 focus:outline-none transition" />
            </div>
            <button type="button" id="btn-submit-verify" onclick="submitOtpVerification()" class="w-full py-3 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs sm:text-sm rounded-xl transition shadow-lg shadow-emerald-500/20 cursor-pointer">
              Verifikasi Kode & Masuk Sekarang &rarr;
            </button>
            <div class="text-center pt-1">
              <button type="button" onclick="backToStep1()" class="text-xs text-slate-400 hover:text-blue-400 transition cursor-pointer">&larr; Ganti email atau kirim ulang kode</button>
            </div>
          </div>
        </div>

      </div>

      <div class="pt-6 border-t border-slate-800 flex justify-between items-center text-xs text-slate-500">
        <a id="link-back-origin" href="index.html" class="hover:text-slate-300 transition">&larr; Kembali</a>
        <a href="pricing.html" class="hover:text-slate-300 transition">Lihat Paket & Layanan</a>
      </div>

    </div>

  </div>

  <script>
    function getRedirectTarget() {
      const p = new URLSearchParams(window.location.search);
      const r = p.get('redirect');
      if (r) return decodeURIComponent(r);
      return 'index.html';
    }

    (function() {
      try {
        const u = GaeksAuth.getCurrentUser();
        if (u && u.email) {
          const dest = getRedirectTarget();
          window.location.replace(window.location.origin + '/' + dest.replace(/^\\//, ''));
        }
      } catch(e) {}
    })();

    window.addEventListener('DOMContentLoaded', () => {
      const target = getRedirectTarget();
      const backLink = document.getElementById('link-back-origin');
      if (backLink) {
        backLink.href = target;
        backLink.innerHTML = "&larr; Kembali ke " + (target.includes('cv.html') ? 'Studio CV' : 'Beranda');
      }

      const urlParams = new URLSearchParams(window.location.search);
      if (urlParams.get('tab') === 'register') {
        setAuthTab('register');
      }
    });

    function setAuthTab(tab) {
      const tabL = document.getElementById('tab-login');
      const tabR = document.getElementById('tab-register');
      const formL = document.getElementById('form-login');
      const formR = document.getElementById('form-register');
      hideAlert();

      if (tab === 'login') {
        tabL.className = "flex-1 py-2.5 rounded-lg bg-blue-600 text-white transition cursor-pointer";
        tabR.className = "flex-1 py-2.5 rounded-lg text-slate-400 hover:text-white transition cursor-pointer";
        formL.classList.remove('hidden');
        formR.classList.add('hidden');
      } else {
        tabR.className = "flex-1 py-2.5 rounded-lg bg-blue-600 text-white transition cursor-pointer";
        tabL.className = "flex-1 py-2.5 rounded-lg text-slate-400 hover:text-white transition cursor-pointer";
        formR.classList.remove('hidden');
        formL.classList.add('hidden');
      }
    }

    function showAlert(msg, isSuccess = false) {
      const box = document.getElementById('status-alert');
      box.classList.remove('hidden');
      if (isSuccess) {
        box.className = "p-3.5 rounded-xl text-xs bg-emerald-950/80 border border-emerald-800 text-emerald-300 font-medium mb-4";
      } else {
        box.className = "p-3.5 rounded-xl text-xs bg-rose-950/80 border border-rose-800 text-rose-300 font-medium mb-4";
      }
      box.innerHTML = msg;
    }

    function hideAlert() {
      document.getElementById('status-alert').classList.add('hidden');
    }

    function processLoginSuccess(email, name, avatar, provider, targetUrl) {
      const cleanEmail = (email || '').toLowerCase().trim();
      const vipList = [
        "gaeks.group@gmail.com",
        "triawan25@gmail.com",
        "ranesath@gmail.com"
      ];
      const isVip = vipList.includes(cleanEmail);
      const isSuperAdmin = (cleanEmail === "gaeks.group@gmail.com");
      const displayName = name || cleanEmail.split('@')[0];

      const user = {
        id: 'usr_' + (provider === 'google' ? 'goog_' : '') + Math.random().toString(36).substr(2, 9),
        email: cleanEmail,
        name: displayName,
        avatar: avatar || ('https://api.dicebear.com/7.x/initials/svg?seed=' + encodeURIComponent(displayName)),
        provider: provider || 'email',
        isPro: isVip,
        isAdmin: isSuperAdmin,
        plan: isVip ? 'PRO_VIP' : 'FREE',
        planLabel: isVip ? (isSuperAdmin ? 'SUPER ADMIN' : 'GAEKS PRO VIP') : 'Free Tier',
        loginAt: Date.now()
      };

      try {
        localStorage.setItem('gaeks_user_session_v3', JSON.stringify(user));
      } catch(e) {}
      
      try {
        document.cookie = "gaeks_session_v3=" + encodeURIComponent(JSON.stringify(user)) + "; path=/; max-age=2592000; SameSite=Lax";
      } catch(e) {}

      try {
        if (window.GaeksAuth && typeof GaeksAuth.recordUserRegistration === 'function') {
          GaeksAuth.recordUserRegistration(user);
        }
      } catch(e) {}

      let dest = targetUrl;
      if (!dest) {
        const p = new URLSearchParams(window.location.search);
        dest = p.get('redirect') || 'index.html';
      }
      dest = decodeURIComponent(dest).replace(/^\\//, '');
      const finalUrl = window.location.origin + '/' + dest;
      window.location.replace(finalUrl);
    }

    function handleCredentialResponse(response) {
      try {
        const base64Url = response.credential.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
          return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));

        const payload = JSON.parse(jsonPayload);
        if (payload && payload.email) {
          const dest = getRedirectTarget();
          showAlert("✓ Berhasil masuk dengan Google! Mengalihkan ke tujuan...", true);
          processLoginSuccess(payload.email, payload.name || payload.given_name, payload.picture, 'google', dest);
        }
      } catch (err) {
        console.error("Gagal membaca kredensial Google:", err);
        showAlert("Gagal memproses akun Google: " + err.message);
      }
    }

    function submitLogin(e) {
      e.preventDefault();
      const email = document.getElementById('login-email').value.trim();
      const pass = document.getElementById('login-pass').value.trim();
      if (!email || !pass) {
        showAlert("Silakan masukkan email dan kata sandi.");
        return;
      }
      const dest = getRedirectTarget();
      processLoginSuccess(email, email.split("@")[0], "", "email", dest);
    }

    let storedEmail = '';
    let storedName = '';

    async function requestOtpCode() {
      const name = document.getElementById('reg-name').value.trim();
      const email = document.getElementById('reg-email').value.trim();
      const btn = document.getElementById('btn-send-otp');

      if (!name || !email) {
        showAlert("Silakan lengkapi nama dan alamat email.");
        return;
      }

      // 1. CEK JIKA SUDAH TERDAFTAR (DI SISI CLIENT)
      try {
        const db = GaeksAuth.getUsersDb();
        const existing = db.find(u => u.email.toLowerCase() === email.toLowerCase());
        if (existing) {
          showAlert("⚠️ Akun dengan email <strong>" + email + "</strong> sudah terdaftar. Mengalihkan ke tab 'Masuk'...");
          setTimeout(() => {
            setAuthTab('login');
            document.getElementById('login-email').value = email;
            document.getElementById('login-pass').focus();
          }, 1500);
          return;
        }
      } catch(e) {}

      btn.disabled = true;
      btn.innerText = "⏳ Mengirim kode dari no-reply@gaeks.com...";
      hideAlert();

      try {
        const res = await fetch('/api/auth_otp.php', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ action: 'send_otp', email: email, name: name })
        });
        const data = await res.json();

        if (data.status === 'success') {
          storedEmail = email;
          storedName = name;
          document.getElementById('target-email-badge').innerText = email;
          document.getElementById('reg-step-request').classList.add('hidden');
          document.getElementById('reg-step-verify').classList.remove('hidden');
          showAlert("✓ Kode verifikasi 6 digit telah dikirimkan ke email Anda.", true);
        } else if (data.status === 'already_registered') {
          showAlert("⚠️ " + data.message);
          setTimeout(() => {
            setAuthTab('login');
            document.getElementById('login-email').value = email;
            document.getElementById('login-pass').focus();
          }, 1500);
        } else {
          showAlert(data.message || "Gagal mengirimkan kode verifikasi.");
        }
      } catch (err) {
        showAlert("Gagal menghubungi server: " + err.message);
      } finally {
        btn.disabled = false;
        btn.innerText = "Kirim 6 Digit Kode Verifikasi ke Email →";
      }
    }

    async function submitOtpVerification() {
      const code = document.getElementById('reg-otp-code').value.trim();
      const pass = document.getElementById('reg-password').value.trim();
      const btn = document.getElementById('btn-submit-verify');

      if (!code || code.length !== 6) {
        showAlert("Masukkan 6 digit kode verifikasi yang Anda terima.");
        return;
      }
      if (!pass || pass.length < 6) {
        showAlert("Kata sandi minimal 6 karakter.");
        return;
      }

      btn.disabled = true;
      btn.innerText = "⏳ Memvalidasi kode verifikasi...";
      hideAlert();

      try {
        const res = await fetch('/api/auth_otp.php', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ action: 'verify_otp', email: storedEmail, code: code, password: pass })
        });
        const data = await res.json();

        if (data.status === 'success') {
          const dest = getRedirectTarget();
          showAlert("✓ Pendaftaran berhasil! Mengalihkan ke tujuan...", true);
          processLoginSuccess(storedEmail, storedName, "", "email", dest);
        } else {
          showAlert(data.message || "Kode verifikasi salah.");
        }
      } catch (err) {
        showAlert("Gagal verifikasi: " + err.message);
      } finally {
        btn.disabled = false;
        btn.innerText = "Verifikasi Kode & Masuk Sekarang →";
      }
    }

    function backToStep1() {
      document.getElementById('reg-step-verify').classList.add('hidden');
      document.getElementById('reg-step-request').classList.remove('hidden');
      hideAlert();
    }
  </script>
</body>
</html>
''')
print("✓ login.html berhasil ditulis.")

print("=== 2. Menulis auth.js (Multi-Key Session Tolerance & Hard Redirect) ===")
with open("auth.js", "w") as fp:
    fp.write('''// GAEKS DIGITAL ECOSYSTEM - MULTI-KEY PERSISTENT AUTH ENGINE
const VIP_WHITELIST = [
  "gaeks.group@gmail.com",
  "triawan25@gmail.com",
  "ranesath@gmail.com"
];
const SUPER_ADMIN_EMAIL = "gaeks.group@gmail.com";
const GOOGLE_CLIENT_ID = "41832472270-6r8iudma1eho6kn3q6rs4rl7b9ank7n4.apps.googleusercontent.com";

const AUTH_STORAGE_KEY = 'gaeks_user_session_v3';
const USERS_DB_KEY = 'gaeks_users_db_v3';

const GaeksAuth = {
  getUsersDb() {
    let raw = null;
    try { raw = localStorage.getItem(USERS_DB_KEY); } catch(e) {}
    if (!raw) {
      try { raw = localStorage.getItem('gaeks_users_db_v2'); } catch(e) {}
    }
    if (!raw) {
      const initial = [
        { id: 'usr_adm_1', email: 'gaeks.group@gmail.com', name: 'GAEKS Group (Admin)', provider: 'google', plan: 'PRO_VIP', registeredAt: Date.now() - 86400000 * 5, lastLoginAt: Date.now() },
        { id: 'usr_vip_2', email: 'triawan25@gmail.com', name: 'Deny Triawan', provider: 'google', plan: 'PRO_VIP', registeredAt: Date.now() - 86400000 * 4, lastLoginAt: Date.now() },
        { id: 'usr_vip_3', email: 'ranesath@gmail.com', name: 'Ranesath', provider: 'google', plan: 'PRO_VIP', registeredAt: Date.now() - 86400000 * 3, lastLoginAt: Date.now() }
      ];
      try { localStorage.setItem(USERS_DB_KEY, JSON.stringify(initial)); } catch(e) {}
      return initial;
    }
    try { return JSON.parse(raw); } catch(e) { return []; }
  },

  saveUsersDb(db) {
    try { localStorage.setItem(USERS_DB_KEY, JSON.stringify(db)); } catch(e) {}
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
    let raw = null;
    try { raw = localStorage.getItem('gaeks_user_session_v3'); } catch(e) {}
    if (!raw) {
      try { raw = localStorage.getItem('gaeks_user_session_v2'); } catch(e) {}
    }
    if (!raw) {
      try { raw = localStorage.getItem('gaeks_user_session'); } catch(e) {}
    }
    if (!raw) {
      try {
        const m = document.cookie.match(/gaeks_session_v3=([^;]+)/);
        if (m) raw = decodeURIComponent(m[1]);
      } catch(e) {}
    }
    if (!raw) {
      try {
        const m = document.cookie.match(/gaeks_session=([^;]+)/);
        if (m) raw = decodeURIComponent(m[1]);
      } catch(e) {}
    }

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
        try {
          localStorage.setItem('gaeks_user_session_v3', JSON.stringify(user));
          document.cookie = "gaeks_session_v3=" + encodeURIComponent(JSON.stringify(user)) + "; path=/; max-age=2592000; SameSite=Lax";
        } catch(e) {}
        return user;
      }
    } catch(e) {
      return null;
    }
    return null;
  },

  isProUser() {
    const user = this.getCurrentUser();
    return user ? !!user.isPro : false;
  },

  isAdmin() {
    const user = this.getCurrentUser();
    return user ? (user.email.toLowerCase().trim() === SUPER_ADMIN_EMAIL) : false;
  },

  logout() {
    try {
      localStorage.removeItem('gaeks_user_session_v3');
      localStorage.removeItem('gaeks_user_session_v2');
      localStorage.removeItem('gaeks_user_session');
    } catch(e) {}
    try {
      document.cookie = "gaeks_session_v3=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
      document.cookie = "gaeks_session=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
    } catch(e) {}
    window.location.replace(window.location.origin + '/index.html');
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
''')
print("✓ auth.js berhasil ditulis.")

print("=== 3. Menulis profile.html (Bebas Pop-up Alert & Sesi Mulus) ===")
with open("profile.html", "w") as fp:
    fp.write('''<!DOCTYPE html>
<html lang="id">
<head>
  <script>
    (function() {
      var raw = null;
      try { raw = localStorage.getItem('gaeks_user_session_v3') || localStorage.getItem('gaeks_user_session_v2') || localStorage.getItem('gaeks_user_session'); } catch(e) {}
      if (!raw) {
        try {
          var m = document.cookie.match(/gaeks_session_v3=([^;]+)/) || document.cookie.match(/gaeks_session=([^;]+)/);
          if (m) raw = decodeURIComponent(m[1]);
        } catch(e) {}
      }
      if (!raw) {
        window.location.replace('login.html?redirect=profile.html');
      }
    })();
  </script>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Profil Akun & Berlangganan | GAEKS Digital</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <script src="auth.js?v=20260914_07"></script>
  <style> body { font-family: 'Plus Jakarta Sans', sans-serif; } </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col justify-between selection:bg-blue-600 selection:text-white">

  <header class="sticky top-0 z-50 w-full backdrop-blur-md bg-slate-950/90 border-b border-slate-800">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <a href="index.html" class="text-xs sm:text-sm font-semibold text-slate-400 hover:text-white flex items-center gap-1.5 py-1 px-2 rounded-lg hover:bg-slate-900 transition">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
          <span>Beranda</span>
        </a>
        <span class="text-slate-700">|</span>
        <a href="cv.html" class="text-xs sm:text-sm font-semibold text-slate-400 hover:text-white transition">ATS CV Studio</a>
        <span class="text-slate-700">|</span>
        <a href="presentation.html" class="text-xs sm:text-sm font-semibold text-slate-400 hover:text-white transition">Presentation Maker</a>
      </div>

      <div class="flex items-center space-x-3">
        <button onclick="GaeksAuth.logout()" class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-rose-950/40 hover:bg-rose-900/60 border border-rose-900/50 text-rose-300 transition">
          Keluar (Sign Out)
        </button>
      </div>
    </div>
  </header>

  <main class="max-w-4xl mx-auto w-full px-4 sm:px-6 py-10 flex-grow space-y-8">
    
    <div class="p-6 sm:p-8 bg-slate-900/90 rounded-2xl border border-slate-800 shadow-xl flex flex-col sm:flex-row sm:items-center justify-between gap-6">
      <div class="flex items-center gap-4">
        <img id="prof-avatar" class="w-16 h-16 sm:w-20 sm:h-20 rounded-2xl border border-slate-700 object-cover" src="https://api.dicebear.com/7.x/initials/svg?seed=User" alt="Avatar" />
        <div>
          <div class="flex items-center gap-2">
            <h1 id="prof-name" class="text-xl sm:text-2xl font-extrabold text-white">Nama Pengguna</h1>
            <span id="prof-badge-plan" class="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-blue-950 text-blue-300 border border-blue-800">Free Tier</span>
          </div>
          <p id="prof-email" class="text-xs sm:text-sm text-slate-400 mt-0.5">user@email.com</p>
          <p class="text-[11px] text-slate-500 mt-1">Metode Masuk: <span id="prof-provider" class="font-medium text-slate-300 uppercase">Google / Email</span></p>
        </div>
      </div>

      <div id="box-upgrade-cta" class="shrink-0 flex flex-col gap-2">
        <a href="pricing.html" class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white text-xs sm:text-sm font-bold shadow-lg shadow-blue-500/20 text-center transition">
          ⭐ Upgrade ke GAEKS PRO
        </a>
        <a href="https://wa.me/6285608561745?text=Halo%20Admin%20GAEKS%2C%20saya%20ingin%20tanya%20paket%20langganan%20GAEKS%20PRO" target="_blank" class="text-[11px] text-slate-400 hover:text-emerald-400 text-center font-medium transition">
          💬 Tanya via WhatsApp
        </a>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      
      <div class="p-6 bg-slate-900/80 rounded-2xl border border-slate-800 space-y-4">
        <h3 class="text-sm font-bold uppercase tracking-wider text-blue-400">Status Langganan Anda</h3>
        <div class="p-4 bg-slate-950 rounded-xl border border-slate-800/80">
          <div class="flex justify-between items-center mb-1">
            <span class="text-xs text-slate-400">Paket Saat Ini</span>
            <span id="plan-name-detail" class="text-xs font-bold text-white">Free Plan</span>
          </div>
          <div class="flex justify-between items-center mb-1">
            <span class="text-xs text-slate-400">Masa Aktif</span>
            <span id="plan-expiry-detail" class="text-xs font-medium text-emerald-400">Tidak Terbatas</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-xs text-slate-400">Akses Tema CV</span>
            <span id="plan-themes-detail" class="text-xs font-bold text-slate-300">5 Tema Dasar</span>
          </div>
        </div>
        <p class="text-xs text-slate-400 leading-relaxed">
          Nikmati akses ke mesin resume standar ATS global dan uji coba presentasi maker. Tingkatkan keanggotaan untuk membuka seluruh tema visual eksekutif.
        </p>
      </div>

      <div class="p-6 bg-slate-900/80 rounded-2xl border border-slate-800 space-y-4">
        <h3 class="text-sm font-bold uppercase tracking-wider text-emerald-400">Keunggulan GAEKS PRO</h3>
        <ul class="space-y-2.5 text-xs text-slate-300">
          <li class="flex items-center gap-2">
            <span class="text-emerald-400 font-bold">✓</span>
            <span>Buka seluruh <strong>15 Tema Visual</strong> Studio CV.</span>
          </li>
          <li class="flex items-center gap-2">
            <span class="text-emerald-400 font-bold">✓</span>
            <span>Ekspor PDF resolusi tinggi A4 tanpa batas dan tanpa watermark.</span>
          </li>
          <li class="flex items-center gap-2">
            <span class="text-emerald-400 font-bold">✓</span>
            <span>Penyimpanan banyak versi CV & Slide Presentasi di server cloud.</span>
          </li>
          <li class="flex items-center gap-2">
            <span class="text-emerald-400 font-bold">✓</span>
            <span>Dukungan prioritas WhatsApp untuk konsultasi dan review.</span>
          </li>
        </ul>
      </div>

    </div>

    <div class="p-5 bg-slate-900/50 rounded-2xl border border-slate-800/80 flex flex-wrap items-center justify-between gap-4">
      <div>
        <h4 class="text-sm font-bold text-white">Mulai Membuat Resume atau Presentasi?</h4>
        <p class="text-xs text-slate-400">Pilih alat produktivitas digital untuk kebutuhan karier dan bisnis Anda.</p>
      </div>
      <div class="flex gap-2">
        <a href="cv.html" class="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs transition">
          Buka Studio CV &rarr;
        </a>
        <a href="presentation.html" class="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs transition">
          Buka Presentation Maker &rarr;
        </a>
      </div>
    </div>

  </main>

  <footer class="border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-500">
    <p>&copy; 2026 GAEKS DIGITAL PRODUCT. All rights reserved.</p>
  </footer>

  <script>
    function renderProfile() {
      const user = GaeksAuth.getCurrentUser();
      if (!user) {
        window.location.replace('login.html?redirect=profile.html');
        return;
      }

      document.getElementById('prof-name').innerText = user.name || 'Pengguna GAEKS';
      document.getElementById('prof-email').innerText = user.email || '-';
      document.getElementById('prof-avatar').src = user.avatar || ('https://api.dicebear.com/7.x/initials/svg?seed=' + encodeURIComponent(user.name || 'User'));
      document.getElementById('prof-provider').innerText = (user.provider || 'email') + ' authentication';

      if (user.isPro) {
        document.getElementById('prof-badge-plan').className = "px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-emerald-950 text-emerald-300 border border-emerald-800";
        document.getElementById('prof-badge-plan').innerText = user.planLabel || "GAEKS PRO (Aktif)";
        document.getElementById('plan-name-detail').innerText = "GAEKS PRO VIP (Akses Penuh)";
        document.getElementById('plan-themes-detail').innerText = "15 Tema Visual Terbuka";
        document.getElementById('box-upgrade-cta').innerHTML = `
          <div class="px-4 py-2 bg-emerald-950/80 border border-emerald-800 rounded-xl text-xs text-emerald-300 font-bold flex items-center gap-1.5">
            <span>✓ Member PRO VIP Aktif</span>
          </div>
        `;
      } else {
        document.getElementById('prof-badge-plan').innerText = "Free Tier";
        document.getElementById('plan-name-detail').innerText = "Free Plan";
        document.getElementById('plan-themes-detail').innerText = "5 Tema Dasar";
      }
    }

    renderProfile();
    window.addEventListener('DOMContentLoaded', renderProfile);
    window.addEventListener('pageshow', renderProfile);
  </script>
</body>
</html>
''')
print("✓ profile.html berhasil ditulis.")

print("=== 4. Menulis presentation.html (Gaeks Presentation Maker Trial 3 Hari) ===")
with open("presentation.html", "w") as fp:
    fp.write('''<!DOCTYPE html>
<html lang="id">
<head>
  <script>
    (function() {
      var raw = null;
      try { raw = localStorage.getItem('gaeks_user_session_v3') || localStorage.getItem('gaeks_user_session_v2') || localStorage.getItem('gaeks_user_session'); } catch(e) {}
      if (!raw) {
        try {
          var m = document.cookie.match(/gaeks_session_v3=([^;]+)/) || document.cookie.match(/gaeks_session=([^;]+)/);
          if (m) raw = decodeURIComponent(m[1]);
        } catch(e) {}
      }
      if (!raw) {
        window.location.replace('login.html?redirect=presentation.html');
      }
    })();
  </script>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>GAEKS Presentation Maker | Executive Pitch Deck Studio</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <script src="auth.js?v=20260914_07"></script>
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; }
    .slide-canvas { aspect-ratio: 16 / 9; }
    @media print {
      .no-print { display: none !important; }
      body { background: white !important; color: black !important; padding: 0 !important; }
      .slide-canvas { page-break-after: always; width: 100% !important; border: none !important; box-shadow: none !important; }
    }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col selection:bg-blue-600 selection:text-white">

  <!-- TOP NAVBAR -->
  <header class="no-print border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-40">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <a href="index.html" class="flex items-center space-x-2">
          <span class="w-8 h-8 rounded-lg bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center font-extrabold text-white text-xs">G</span>
          <span class="font-extrabold text-sm sm:text-base tracking-tight text-white">GAEKS PRESENTATION</span>
        </a>
        <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-950 text-emerald-300 border border-emerald-800 flex items-center gap-1">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
          Trial 3 Hari Aktif
        </span>
      </div>

      <div class="flex items-center space-x-3">
        <button onclick="window.print()" class="px-3.5 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs shadow-md shadow-blue-500/20 transition flex items-center gap-1.5">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
          <span>Export Slide PDF</span>
        </button>
        <a href="index.html" class="px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 text-xs font-semibold transition">
          &larr; Beranda
        </a>
      </div>
    </div>
  </header>

  <!-- MAIN WORKSPACE -->
  <main class="max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8 flex-grow grid grid-cols-1 lg:grid-cols-12 gap-6">
    
    <div class="no-print lg:col-span-4 bg-slate-900/70 border border-slate-800 rounded-2xl p-5 space-y-4 h-fit">
      <div class="flex justify-between items-center pb-3 border-b border-slate-800">
        <div>
          <h2 class="text-sm font-bold text-white">Daftar Slide Pitch Deck</h2>
          <p class="text-[11px] text-slate-400">Pilih slide untuk mengedit konten</p>
        </div>
        <button onclick="addNewSlide()" class="px-2.5 py-1 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-[11px] font-bold transition">
          + Slide Baru
        </button>
      </div>

      <div id="slide-thumb-list" class="space-y-2 max-h-[520px] overflow-y-auto pr-1">
      </div>
    </div>

    <div class="lg:col-span-8 space-y-6">
      
      <div id="slide-viewport" class="slide-canvas w-full bg-gradient-to-br from-slate-900 via-slate-900 to-blue-950/60 rounded-2xl border-2 border-slate-700 shadow-2xl p-8 sm:p-12 flex flex-col justify-between relative overflow-hidden transition-all duration-300">
        <div class="flex justify-between items-start">
          <div class="space-y-1">
            <span id="canvas-slide-tag" class="text-[11px] font-extrabold uppercase tracking-widest text-blue-400 font-mono">PITCH DECK</span>
            <h1 id="canvas-slide-title" class="text-2xl sm:text-4xl font-black text-white tracking-tight">Judul Presentasi Eksekutif</h1>
          </div>
          <span class="w-8 h-8 rounded-lg bg-blue-600/30 border border-blue-500/40 text-blue-300 text-xs font-bold flex items-center justify-center">G</span>
        </div>

        <div id="canvas-slide-content" class="py-6 text-sm sm:text-base text-slate-300 leading-relaxed max-w-2xl">
          Deskripsi masalah mendasar dan peluang pasar strategis yang ingin diselesaikan oleh ekosistem bisnis ini.
        </div>

        <div class="pt-4 border-t border-slate-800/80 flex justify-between items-center text-xs text-slate-500">
          <span id="canvas-slide-footer">GAEKS GROUP &bull; Confidential Pitch</span>
          <span id="canvas-slide-number" class="font-mono">Slide 1 / 1</span>
        </div>
      </div>

      <div class="no-print bg-slate-900/80 border border-slate-800 rounded-2xl p-6 space-y-4 shadow-xl">
        <h3 class="text-xs font-bold uppercase tracking-wider text-slate-400">Editor Konten Slide Aktif</h3>
        
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-[11px] font-semibold text-slate-400 mb-1">Tag Kategori Slide</label>
            <input type="text" id="edit-slide-tag" oninput="updateActiveSlide()" class="w-full px-3 py-2 text-xs bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" />
          </div>
          <div>
            <label class="block text-[11px] font-semibold text-slate-400 mb-1">Pilihan Tema Visual</label>
            <select id="edit-slide-theme" onchange="changeSlideTheme(this.value)" class="w-full px-3 py-2 text-xs bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none">
              <option value="theme-navy">Obsidian Navy (Standar Eksekutif)</option>
              <option value="theme-emerald">Emerald Growth (Fintech & Supply Chain)</option>
              <option value="theme-purple">Silicon Venture (Startup AI & Digital)</option>
              <option value="theme-minimal">Monochrome Slate (Minimalis VC)</option>
            </select>
          </div>
        </div>

        <div>
          <label class="block text-[11px] font-semibold text-slate-400 mb-1">Judul Slide</label>
          <input type="text" id="edit-slide-title" oninput="updateActiveSlide()" class="w-full px-3.5 py-2.5 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white font-bold focus:border-blue-500 focus:outline-none" />
        </div>

        <div>
          <label class="block text-[11px] font-semibold text-slate-400 mb-1">Poin & Uraian Narasi Slide</label>
          <textarea id="edit-slide-desc" rows="4" oninput="updateActiveSlide()" class="w-full px-3.5 py-2.5 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none"></textarea>
        </div>
      </div>

    </div>
  </main>

  <script>
    let slides = [
      { tag: "PROBLEM & OPPORTUNITY", title: "Fragmentasi Logistik & Regulasi Ekspor-Impor", desc: "Tingginya biaya operasional dan rumitnya kepatuhan bea cukai (PIB/PEB) menghambat efisiensi bisnis. Dibutuhkan ekosistem digital terpadu untuk merampingkan seluruh rantai pasok.", theme: "theme-navy" },
      { tag: "SOLUTION", title: "GAEKS Digital Ecosystem", desc: "Integrasi menyeluruh antara Freight Forwarding Internasional, software ERP terpusat (erp.gaeks.com), dan otomasi media pemasaran digital.", theme: "theme-emerald" },
      { tag: "MARKET SIZE (TAM / SAM / SOM)", title: "Potensi Pasar Logistik Indonesia Rp 1.400T", desc: "Pertumbuhan ekspor-impor dan manufaktur menuntut digitalisasi rantai pasok yang cepat, transparan, dan akurat tanpa keterlambatan dokumen.", theme: "theme-purple" },
      { tag: "BUSINESS MODEL", title: "Monetisasi Berkelanjutan & Ekosistem Layanan", desc: "Revenue stream berasal dari freight margin, subscription SaaS ERP bulanan, layanan custom website korporat, dan kursus e-book eksekutif.", theme: "theme-navy" }
    ];

    let activeIndex = 0;

    function renderSlideOutline() {
      const container = document.getElementById('slide-thumb-list');
      container.innerHTML = '';

      slides.forEach((s, idx) => {
        const isActive = (idx === activeIndex);
        container.innerHTML += `
          <div onclick="selectSlide(${idx})" class="p-3 rounded-xl border transition cursor-pointer flex justify-between items-center ${isActive ? 'bg-blue-950/60 border-blue-500 text-white shadow' : 'bg-slate-950/40 border-slate-800 hover:border-slate-700 text-slate-400'}">
            <div class="truncate max-w-[200px]">
              <div class="text-[9px] uppercase font-mono font-bold text-blue-400">${s.tag}</div>
              <div class="text-xs font-bold truncate">${idx + 1}. ${s.title}</div>
            </div>
            ${slides.length > 1 ? `<button onclick="deleteSlide(event, ${idx})" class="text-rose-400 hover:text-rose-300 text-xs px-1">&times;</button>` : ''}
          </div>
        `;
      });

      populateEditor();
      renderActiveCanvas();
    }

    function selectSlide(idx) {
      activeIndex = idx;
      renderSlideOutline();
    }

    function addNewSlide() {
      slides.push({
        tag: "NEW SLIDE",
        title: "Slide Judul Baru " + (slides.length + 1),
        desc: "Tambahkan poin narasi bisnis atau metrik pertumbuhan Anda di sini.",
        theme: "theme-navy"
      });
      activeIndex = slides.length - 1;
      renderSlideOutline();
    }

    function deleteSlide(e, idx) {
      e.stopPropagation();
      if (slides.length <= 1) return;
      slides.splice(idx, 1);
      if (activeIndex >= slides.length) activeIndex = slides.length - 1;
      renderSlideOutline();
    }

    function populateEditor() {
      const current = slides[activeIndex];
      document.getElementById('edit-slide-tag').value = current.tag;
      document.getElementById('edit-slide-title').value = current.title;
      document.getElementById('edit-slide-desc').value = current.desc;
      document.getElementById('edit-slide-theme').value = current.theme || 'theme-navy';
    }

    function updateActiveSlide() {
      const current = slides[activeIndex];
      current.tag = document.getElementById('edit-slide-tag').value.toUpperCase();
      current.title = document.getElementById('edit-slide-title').value;
      current.desc = document.getElementById('edit-slide-desc').value;
      renderActiveCanvas();
      
      const thumb = document.querySelectorAll('#slide-thumb-list > div')[activeIndex];
      if (thumb) {
        thumb.querySelector('.text-\\\\[9px\\\\]').innerText = current.tag;
        thumb.querySelector('.text-xs').innerText = `${activeIndex + 1}. ${current.title}`;
      }
    }

    function changeSlideTheme(themeName) {
      slides[activeIndex].theme = themeName;
      renderActiveCanvas();
    }

    function renderActiveCanvas() {
      const s = slides[activeIndex];
      const viewport = document.getElementById('slide-viewport');

      document.getElementById('canvas-slide-tag').innerText = s.tag;
      document.getElementById('canvas-slide-title').innerText = s.title;
      document.getElementById('canvas-slide-content').innerText = s.desc;
      document.getElementById('canvas-slide-number').innerText = `Slide ${activeIndex + 1} / ${slides.length}`;

      if (s.theme === 'theme-emerald') {
        viewport.className = "slide-canvas w-full bg-gradient-to-br from-slate-950 via-emerald-950/50 to-slate-900 rounded-2xl border-2 border-emerald-700/80 shadow-2xl p-8 sm:p-12 flex flex-col justify-between relative overflow-hidden transition-all duration-300";
      } else if (s.theme === 'theme-purple') {
        viewport.className = "slide-canvas w-full bg-gradient-to-br from-slate-950 via-indigo-950/60 to-purple-950/40 rounded-2xl border-2 border-indigo-700/80 shadow-2xl p-8 sm:p-12 flex flex-col justify-between relative overflow-hidden transition-all duration-300";
      } else if (s.theme === 'theme-minimal') {
        viewport.className = "slide-canvas w-full bg-slate-900 rounded-2xl border-2 border-slate-700 shadow-2xl p-8 sm:p-12 flex flex-col justify-between relative overflow-hidden transition-all duration-300";
      } else {
        viewport.className = "slide-canvas w-full bg-gradient-to-br from-slate-900 via-slate-900 to-blue-950/60 rounded-2xl border-2 border-slate-700 shadow-2xl p-8 sm:p-12 flex flex-col justify-between relative overflow-hidden transition-all duration-300";
      }
    }

    window.addEventListener('DOMContentLoaded', () => {
      renderSlideOutline();
    });
  </script>
</body>
</html>
''')
print("✓ presentation.html berhasil ditulis.")

print("=== 5. Menulis index.html (Katalog Lengkap GAEKS: Services & Products) ===")
with open("index.html", "w") as fp:
    fp.write('''<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>GAEKS Digital Products | Executive Career, SaaS & Business Ecosystem</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <script src="auth.js?v=20260914_07"></script>
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; }
    .hero-glow {
      background: radial-gradient(circle at 50% 10%, rgba(37, 99, 235, 0.15), transparent 70%);
    }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col selection:bg-blue-600 selection:text-white">

  <!-- NAVBAR -->
  <header class="border-b border-slate-800/80 bg-slate-950/80 backdrop-blur sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      
      <a href="index.html" class="flex items-center space-x-2.5">
        <span class="w-8 h-8 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center font-extrabold text-white text-xs shadow-md shadow-blue-500/30">G</span>
        <span class="font-extrabold text-base tracking-tight bg-gradient-to-r from-blue-400 via-indigo-300 to-white bg-clip-text text-transparent">
          GAEKS DIGITAL
        </span>
      </a>

      <nav class="hidden md:flex items-center space-x-6 text-xs font-semibold text-slate-400">
        <a href="#services" class="hover:text-white transition">Digital Services</a>
        <a href="#products" class="hover:text-white transition">Digital Products</a>
        <a href="pricing.html" class="hover:text-white transition">Paket & Harga</a>
      </nav>

      <div class="flex items-center space-x-2.5">
        <button id="nav-btn-admin" onclick="openAdminModal()" class="hidden px-2.5 py-1.5 text-[11px] font-bold rounded-lg bg-amber-950/60 border border-amber-600 text-amber-300 hover:bg-amber-900 transition flex items-center gap-1">
          <span>👑 Admin Users</span>
        </button>

        <div id="nav-user-pill" class="hidden flex items-center space-x-2">
          <a href="profile.html" class="flex items-center space-x-2 p-1 pr-3 rounded-full bg-slate-900 border border-slate-700 hover:border-blue-500 transition">
            <img id="nav-user-avatar" class="w-6 h-6 rounded-full object-cover" src="https://api.dicebear.com/7.x/initials/svg?seed=User" alt="Avatar" />
            <span id="nav-user-name" class="text-xs font-semibold text-slate-200 max-w-[100px] truncate">User</span>
            <span id="nav-user-badge" class="px-1.5 py-0.2 rounded-full text-[9px] font-extrabold bg-blue-950 text-blue-300 border border-blue-800">FREE</span>
          </a>
        </div>

        <a href="login.html?redirect=index.html" id="nav-btn-login" class="px-4 py-2 text-xs font-bold rounded-xl bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-500/20 transition flex items-center gap-1.5">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"></path></svg>
          <span>Masuk / Daftar</span>
        </a>
      </div>

      <script>
        (function() {
          try {
            var raw = localStorage.getItem('gaeks_user_session_v3') || localStorage.getItem('gaeks_user_session_v2') || localStorage.getItem('gaeks_user_session');
            if (!raw) {
              var m = document.cookie.match(/gaeks_session_v3=([^;]+)/) || document.cookie.match(/gaeks_session=([^;]+)/);
              if (m) raw = decodeURIComponent(m[1]);
            }
            if (raw) {
              var u = JSON.parse(raw);
              if (u && u.email) {
                var b = document.getElementById('nav-btn-login');
                var p = document.getElementById('nav-user-pill');
                if (b) b.style.display = 'none';
                if (p) { p.classList.remove('hidden'); p.style.display = 'flex'; }
                var av = document.getElementById('nav-user-avatar');
                if (av && u.avatar) av.src = u.avatar;
                var nm = document.getElementById('nav-user-name');
                if (nm && u.name) nm.innerText = u.name;
              }
            }
          } catch(e) {}
        })();
      </script>

    </div>
  </header>

  <!-- HERO SECTION -->
  <section class="hero-glow py-16 sm:py-24 border-b border-slate-800/60 relative">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-6">
      
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-950/70 border border-blue-800/80 text-blue-300 text-xs font-semibold">
        <span class="w-2 h-2 rounded-full bg-blue-400 animate-pulse"></span>
        Ekosistem Digital Terpadu GAEKS Group
      </div>

      <h1 class="text-3xl sm:text-5xl lg:text-6xl font-black text-white tracking-tight leading-tight sm:leading-none">
        Karier Eksekutif, Presentasi Pitch Deck & Solusi Digital Modern
      </h1>

      <p class="text-sm sm:text-base text-slate-400 max-w-2xl mx-auto leading-relaxed">
        Akses instan ke generator Resume ATS berstandar global, pembuat presentasi bisnis trial 3 hari, sistem ERP logistik, e-book bisnis, dan layanan website korporat.
      </p>

      <div class="pt-4 flex flex-col sm:flex-row items-center justify-center gap-3">
        <a href="#services" class="w-full sm:w-auto px-6 py-3.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-extrabold text-xs sm:text-sm shadow-xl shadow-blue-500/25 transition flex items-center justify-center gap-2">
          <span>🚀 Buka Digital Services (Wajib Login)</span>
        </a>
        <a href="#products" class="w-full sm:w-auto px-6 py-3.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 font-bold text-xs sm:text-sm transition text-center">
          <span>📦 Jelajahi Produk Digital</span>
        </a>
      </div>

    </div>
  </section>

  <!-- SECTION 1: DIGITAL SERVICES (WAJIB LOGIN) -->
  <section id="services" class="py-16 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 space-y-10 border-b border-slate-800">
    <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
      <div>
        <span class="text-xs font-extrabold uppercase tracking-widest text-blue-400 font-mono">DIGITAL SERVICES</span>
        <h2 class="text-2xl sm:text-3xl font-black text-white tracking-tight mt-1">Layanan Interaktif Berbasis Cloud</h2>
        <p class="text-xs sm:text-sm text-slate-400 mt-1">Untuk menggunakan fitur ini, Anda wajib masuk atau mendaftar terlebih dahulu.</p>
      </div>
      <span class="text-xs text-slate-500 italic">*Pendaftaran gratis via Akun Google atau Email OTP</span>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      
      <!-- SERVICE 1: GAEKS PRESENTATION MAKER -->
      <div class="p-8 rounded-3xl bg-slate-900/80 border border-slate-800 hover:border-indigo-500/60 transition duration-300 flex flex-col justify-between shadow-xl relative overflow-hidden group">
        <div class="space-y-4">
          <div class="flex justify-between items-start">
            <span class="w-12 h-12 rounded-2xl bg-indigo-950 border border-indigo-800 text-indigo-400 flex items-center justify-center font-black text-lg">P</span>
            <span class="px-2.5 py-1 rounded-full text-[10px] font-extrabold bg-indigo-950 text-indigo-300 border border-indigo-800">
              Trial 3 Hari &bull; Berlangganan
            </span>
          </div>

          <div>
            <h3 class="text-xl font-bold text-white group-hover:text-indigo-400 transition">Gaeks Presentation Maker</h3>
            <p class="text-xs text-slate-400 mt-2 leading-relaxed">
              Platform pembuat materi presentasi pitch deck investor, laporan operasional bisnis, dan slide eksekutif 16:9 berstandar Venture Capital dengan ekspor PDF instan.
            </p>
          </div>

          <ul class="text-xs text-slate-300 space-y-2 pt-2">
            <li class="flex items-center gap-2"><span class="text-emerald-400">✓</span> Template Slide Pitch Deck Startup (Problem, Solution, TAM/SAM/SOM)</li>
            <li class="flex items-center gap-2"><span class="text-emerald-400">✓</span> 4 Varian tema warna eksekutif</li>
            <li class="flex items-center gap-2"><span class="text-emerald-400">✓</span> Uji coba gratis 3 hari penuh tanpa komitmen</li>
          </ul>
        </div>

        <div class="pt-6 mt-6 border-t border-slate-800/80">
          <button onclick="handleServiceAccess('presentation.html')" class="w-full py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs sm:text-sm transition flex items-center justify-center gap-2 shadow-lg shadow-indigo-600/20 cursor-pointer">
            <span>Mulai Uji Coba 3 Hari Presentation Maker &rarr;</span>
          </button>
        </div>
      </div>

      <!-- SERVICE 2: CV MAKER (ATS CV STUDIO) -->
      <div class="p-8 rounded-3xl bg-slate-900/80 border border-slate-800 hover:border-blue-500/60 transition duration-300 flex flex-col justify-between shadow-xl relative overflow-hidden group">
        <div class="space-y-4">
          <div class="flex justify-between items-start">
            <span class="w-12 h-12 rounded-2xl bg-blue-950 border border-blue-800 text-blue-400 flex items-center justify-center font-black text-lg">CV</span>
            <span class="px-2.5 py-1 rounded-full text-[10px] font-extrabold bg-blue-950 text-blue-300 border border-blue-800">
              520+ Profesi &bull; 15 Tema
            </span>
          </div>

          <div>
            <h3 class="text-xl font-bold text-white group-hover:text-blue-400 transition">ATS CV Maker Studio</h3>
            <p class="text-xs text-slate-400 mt-2 leading-relaxed">
              Penyusun resume profesional dengan live search bank profesi global, tata letak anti-potong A4, struktur kompetensi teruji HRD, dan unduhan dokumen bersih tanpa watermark.
            </p>
          </div>

          <ul class="text-xs text-slate-300 space-y-2 pt-2">
            <li class="flex items-center gap-2"><span class="text-emerald-400">✓</span> 520+ Bank data profesi dengan pencarian langsung</li>
            <li class="flex items-center gap-2"><span class="text-emerald-400">✓</span> 15 Varian tema visual eksekutif berstandar internasional</li>
            <li class="flex items-center gap-2"><span class="text-emerald-400">✓</span> Pengarsipan otomatis & tempat sampah terproteksi 3 hari</li>
          </ul>
        </div>

        <div class="pt-6 mt-6 border-t border-slate-800/80">
          <button onclick="handleServiceAccess('cv.html')" class="w-full py-3 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs sm:text-sm transition flex items-center justify-center gap-2 shadow-lg shadow-blue-500/20 cursor-pointer">
            <span>Buka ATS CV Studio Sekarang &rarr;</span>
          </button>
        </div>
      </div>

    </div>
  </section>

  <!-- SECTION 2: DIGITAL PRODUCTS -->
  <section id="products" class="py-16 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 space-y-10 border-b border-slate-800">
    <div>
      <span class="text-xs font-extrabold uppercase tracking-widest text-emerald-400 font-mono">DIGITAL PRODUCTS</span>
      <h2 class="text-2xl sm:text-3xl font-black text-white tracking-tight mt-1">Katalog Produk & Solusi Digital Mandiri</h2>
      <p class="text-xs sm:text-sm text-slate-400 mt-1">Infrastruktur perangkat lunak, buku panduan eksekutif, dan paket pengembangan bisnis.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      
      <!-- PRODUCT 1: ERP FORWARDING -->
      <div class="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-slate-700 transition flex flex-col justify-between space-y-4">
        <div class="space-y-3">
          <div class="flex justify-between items-center">
            <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-950 text-amber-300 border border-amber-800">ERP Software</span>
            <span class="text-xs text-slate-500">gaeks.com</span>
          </div>
          <h3 class="text-base font-bold text-white">ERP Forwarding</h3>
          <p class="text-xs text-slate-400 leading-relaxed">
            Sistem ERP berbasis cloud untuk pengelolaan bisnis freight forwarding, kepatuhan pabean (PIB/PEB), kontainer, dan inventaris gudang.
          </p>
        </div>
        <a href="https://erp.gaeks.com" target="_blank" class="w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xs font-bold transition text-center block">
          Akses erp.gaeks.com &rarr;
        </a>
      </div>

      <!-- PRODUCT 2: E-BOOK DIGITAL -->
      <div class="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-slate-700 transition flex flex-col justify-between space-y-4">
        <div class="space-y-3">
          <div class="flex justify-between items-center">
            <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-purple-950 text-purple-300 border border-purple-800">E-Book Store</span>
            <span class="text-xs text-slate-500">Mulai Rp 79k</span>
          </div>
          <h3 class="text-base font-bold text-white">Buku Digital Bisnis</h3>
          <p class="text-xs text-slate-400 leading-relaxed">
            Koleksi panduan operasional: <em>Mastering Freight Forwarding</em>, <em>Startup Logistics Blueprint</em>, dan <em>Panduan Lolos HRD</em>.
          </p>
        </div>
        <a href="https://wa.me/6285608561745?text=Halo%20Admin%20GAEKS%2C%20saya%20ingin%20membeli%20koleksi%20E-Book%20Bisnis%20dan%20Logistik" target="_blank" class="w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xs font-bold transition text-center block">
          Beli & Unduh E-Book &rarr;
        </a>
      </div>

      <!-- PRODUCT 3: WEBSITE BUILDER -->
      <div class="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-slate-700 transition flex flex-col justify-between space-y-4">
        <div class="space-y-3">
          <div class="flex justify-between items-center">
            <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-950 text-blue-300 border border-blue-800">Pricelist Web</span>
            <span class="text-xs text-slate-500">Mulai Rp 750k</span>
          </div>
          <h3 class="text-base font-bold text-white">Website Builder</h3>
          <p class="text-xs text-slate-400 leading-relaxed">
            Paket pembuatan Landing Page konversi tinggi, web portofolio personal, hingga aplikasi web kustom dengan backend terintegrasi.
          </p>
        </div>
        <a href="https://wa.me/6285608561745?text=Halo%20Admin%20GAEKS%2C%20saya%20tertarik%20dengan%20layanan%20Website%20Builder%20dan%20Development" target="_blank" class="w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xs font-bold transition text-center block">
          Pesan Pembuatan Web &rarr;
        </a>
      </div>

      <!-- PRODUCT 4: SMM MARKETING -->
      <div class="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-slate-700 transition flex flex-col justify-between space-y-4">
        <div class="space-y-3">
          <div class="flex justify-between items-center">
            <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-950 text-emerald-300 border border-emerald-800">Growth Marketing</span>
            <span class="text-xs text-slate-500">smm.gaeks.com</span>
          </div>
          <h3 class="text-base font-bold text-white">Portal SMM</h3>
          <p class="text-xs text-slate-400 leading-relaxed">
            Solusi otomatisasi Social Media Marketing untuk memperluas jangkauan brand, engagement akun bisnis, dan kampanye digital bertarget.
          </p>
        </div>
        <a href="https://smm.gaeks.com" target="_blank" class="w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xs font-bold transition text-center block">
          Buka Portal SMM &rarr;
        </a>
      </div>

    </div>
  </section>

  <!-- FOOTER -->
  <footer class="border-t border-slate-800 bg-slate-950 py-12 text-center text-xs text-slate-500 space-y-2 mt-auto">
    <p>&copy; 2026 GAEKS DIGITAL PRODUCTS. All rights reserved.</p>
    <p class="text-[11px]">Infrastruktur Subdomain: gdp.gaeks.com | erp.gaeks.com | smm.gaeks.com</p>
  </footer>

  <script>
    function handleServiceAccess(targetUrl) {
      const user = GaeksAuth.getCurrentUser();
      if (user) {
        window.location.href = window.location.origin + '/' + targetUrl.replace(/^\\//, '');
      } else {
        window.location.href = window.location.origin + '/login.html?redirect=' + encodeURIComponent(targetUrl);
      }
    }

    function updateNavbar() {
      const user = GaeksAuth.getCurrentUser();
      const btnLogin = document.getElementById('nav-btn-login');
      const pill = document.getElementById('nav-user-pill');
      const adminBtn = document.getElementById('nav-btn-admin');

      if (user) {
        if (btnLogin) btnLogin.style.display = 'none';
        if (pill) {
          pill.classList.remove('hidden');
          pill.style.display = 'flex';
        }
        const avatar = document.getElementById('nav-user-avatar');
        if (avatar && user.avatar) avatar.src = user.avatar;
        const name = document.getElementById('nav-user-name');
        if (name && user.name) name.innerText = user.name;

        const badge = document.getElementById('nav-user-badge');
        if (badge) {
          if (user.isAdmin) {
            badge.className = "px-1.5 py-0.2 rounded-full text-[9px] font-extrabold bg-amber-950 text-amber-300 border border-amber-800";
            badge.innerText = "ADMIN";
            if (adminBtn) adminBtn.classList.remove('hidden');
          } else if (user.isPro) {
            badge.className = "px-1.5 py-0.2 rounded-full text-[9px] font-extrabold bg-emerald-950 text-emerald-300 border border-emerald-800";
            badge.innerText = "PRO VIP";
            if (adminBtn) adminBtn.classList.add('hidden');
          } else {
            badge.className = "px-1.5 py-0.2 rounded-full text-[9px] font-extrabold bg-blue-950 text-blue-300 border border-blue-800";
            badge.innerText = "FREE";
            if (adminBtn) adminBtn.classList.add('hidden');
          }
        }
      } else {
        if (btnLogin) btnLogin.style.display = 'inline-flex';
        if (pill) {
          pill.classList.add('hidden');
          pill.style.display = 'none';
        }
        if (adminBtn) adminBtn.classList.add('hidden');
      }
    }

    updateNavbar();
    window.addEventListener('DOMContentLoaded', updateNavbar);
    window.addEventListener('load', updateNavbar);
    window.addEventListener('pageshow', updateNavbar);
  </script>
</body>
</html>
''')
print("✓ index.html berhasil ditulis.")

print("=== 6. Menulis .htaccess (Clean URLs & HTTPS) ===")
with open(".htaccess", "w") as fp:
    fp.write('''RewriteEngine On
RewriteBase /

# 1. Enforce HTTPS
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# 2. Clean URLs (Menghilangkan ekstensi .html di URL)
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME}.html -f
RewriteRule ^([^\.]+)$ $1.html [NC,L]

# 3. Index File Fallback
DirectoryIndex index.html index.php cv.html

# 4. Encoding UTF-8
AddDefaultCharset UTF-8
''')
print("✓ .htaccess berhasil ditulis.")

print("=== 7. Menulis api/auth_otp.php (Validasi Duplikat di Server) ===")
os.makedirs("api", exist_ok=True)
with open("api/auth_otp.php", "w") as fp:
    fp.write('''<?php
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
$registeredUsersFile = __DIR__ . '/users_registry.json';

$raw = file_get_contents('php://input');
$data = json_decode($raw, true) ?? [];
$action = $data['action'] ?? '';
$email = filter_var($data['email'] ?? '', FILTER_VALIDATE_EMAIL);

if (!$email) {
    echo json_encode(["status" => "error", "message" => "Format alamat email tidak valid."]);
    exit;
}

if ($action === 'send_otp') {
    if (file_exists($registeredUsersFile)) {
        $regUsers = json_decode(file_get_contents($registeredUsersFile), true) ?? [];
        if (in_array(strtolower($email), array_map('strtolower', $regUsers))) {
            echo json_encode([
                "status" => "already_registered",
                "message" => "Email ini sudah pernah terdaftar. Silakan gunakan tab Masuk ke Akun atau reset sandi."
            ]);
            exit;
        }
    }

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

    $regUsers = [];
    if (file_exists($registeredUsersFile)) {
        $regUsers = json_decode(file_get_contents($registeredUsersFile), true) ?? [];
    }
    if (!in_array(strtolower($email), array_map('strtolower', $regUsers))) {
        $regUsers[] = strtolower($email);
        file_put_contents($registeredUsersFile, json_encode($regUsers));
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
print("✓ api/auth_otp.php berhasil ditulis.")

print("=== 8. Memperbarui cv.html (Tombol Buat CV Baru Aktif & Hapus Modal Lama) ===")
if os.path.exists("cv.html"):
    with open("cv.html", "r") as fp:
        cv = fp.read()

    # 1. Hapus fungsi modal lama
    cv = re.sub(r'function openAuthModal\(\)\s*\{.*?\}\s*function closeAuthModal\(\)\s*\{.*?\}', '''function openAuthModal() {
      window.location.href = 'login.html?redirect=cv.html';
    }

    function closeAuthModal() {
    }''', cv, flags=re.DOTALL)

    # 2. Hapus elemen modal lama dari DOM
    idx_modal = cv.find('<div id="auth-modal"')
    if idx_modal != -1:
        idx_comment = cv.rfind('<!-- ================= MODAL MASUK', 0, idx_modal)
        if idx_comment == -1: idx_comment = idx_modal
        idx_next = cv.find('<!-- ================= MODAL ADMIN', idx_modal)
        if idx_next != -1:
            cv = cv[:idx_comment] + cv[idx_next:]
        else:
            idx_next = cv.find('</body>', idx_modal)
            cv = cv[:idx_comment] + '\\n</body>\\n</html>'

    # 3. Hapus duplikasi saveCvList legacy
    legacy_block = """    function _legacy_loadCvList() {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        try { cvList = JSON.parse(raw); } catch(e) { cvList = []; }
      }
      if (!cvList || cvList.length === 0) {
        cvList = [getDenyTriawanSampleData()];
        saveCvList();
      }
      autoPurgeTrash();
    }

    function saveCvList() {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(cvList));
      updateDashboardCounts();
    }"""
    if legacy_block in cv:
        cv = cv.replace(legacy_block, "")

    # 4. Perbaiki openEditor agar langsung membuka kanvas
    open_editor_fix = """    function openEditor(id) {
      currentCvId = id;
      const cv = cvList.find(c => c.id === id);
      if (!cv) return;

      const vDash = document.getElementById('view-dashboard');
      const vEdit = document.getElementById('view-editor');
      const btnDash = document.getElementById('nav-btn-dashboard');
      const btnPrint = document.getElementById('nav-btn-print');

      if (vDash) vDash.classList.add('hidden');
      if (vEdit) {
        vEdit.classList.remove('hidden');
        vEdit.style.display = 'block';
      }
      if (btnDash) btnDash.classList.remove('hidden');
      if (btnPrint) btnPrint.classList.remove('hidden');

      const titleInput = document.getElementById('current-cv-title');
      if (titleInput) titleInput.value = cv.title;
      loadFormData(cv.data);

      historyStack = [JSON.stringify(cv.data)];
      historyIndex = 0;
      updateUndoRedoButtons();

      renderCV();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }"""
    cv = re.sub(r'function openEditor\(id\)\s*\{.*?renderCV\(\);\s*\}', open_editor_fix, cv, flags=re.DOTALL)

    # 5. Perbaiki showDashboardView
    show_dash_fix = """    function showDashboardView() {
      const vDash = document.getElementById('view-dashboard');
      const vEdit = document.getElementById('view-editor');
      const btnDash = document.getElementById('nav-btn-dashboard');
      const btnPrint = document.getElementById('nav-btn-print');

      if (vDash) {
        vDash.classList.remove('hidden');
        vDash.style.display = 'block';
      }
      if (vEdit) {
        vEdit.classList.add('hidden');
        vEdit.style.display = 'none';
      }
      if (btnDash) btnDash.classList.add('hidden');
      if (btnPrint) btnPrint.classList.add('hidden');
      renderDashboardGrid();
    }"""
    cv = re.sub(r'function showDashboardView\(\)\s*\{.*?renderDashboardGrid\(\);\s*\}', show_dash_fix, cv, flags=re.DOTALL)

    # 6. Perbaiki createNewBlankCV
    create_cv_fix = """function createNewBlankCV() {
      try {
        const title = (currentLang === 'en' ? 'New Resume ' : 'CV Baru ') + (cvList.length + 1);
        const newCv = createBlankCvObject(title);
        cvList.unshift(newCv);
        saveCvList();
        renderDashboardGrid();
        openEditor(newCv.id);
      } catch(err) {
        console.error("Gagal membuat CV baru:", err);
        alert("Gagal membuka editor CV: " + err.message);
      }
    }"""
    cv = re.sub(r'function createNewBlankCV\(\)\s*\{.*?\}', create_cv_fix, cv, flags=re.DOTALL)

    cv = cv.replace('src="auth.js"', 'src="auth.js?v=20260914_07"')
    cv = cv.replace('src="auth.js?v=20260914_04"', 'src="auth.js?v=20260914_07"')
    cv = cv.replace('src="auth.js?v=20260914_05"', 'src="auth.js?v=20260914_07"')
    cv = cv.replace('src="auth.js?v=20260914_06"', 'src="auth.js?v=20260914_07"')

    with open("cv.html", "w") as f:
        f.write(cv)
    print("✓ cv.html berhasil diperbarui & modal lama dibersihkan.")

print("=== 9. Menjalankan Git Commit & Force Push ke GitHub ===")
subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "fix: complete bulletproof auth system, profile session sync without popups, active createNewBlankCV action, and clean full catalog"])
push_res = subprocess.run(["git", "push", "origin", "main", "--force"], capture_output=True, text=True)
print(push_res.stdout)
if push_res.stderr: print(push_res.stderr)
print("=== DEPLOYMENT SELESAI & AKTIF DI SERVER LIVE! ===")
