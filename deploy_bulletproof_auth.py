import os, re, subprocess

print("=== 1. Memperbarui auth.js (Dual-Layer Session: LocalStorage + Cookie & Absolute Redirect) ===")
with open("auth.js", "w") as f:
    f.write('''// GAEKS DIGITAL ECOSYSTEM - AUTH, DUAL PERSISTENCE & HARD REDIRECT
const VIP_WHITELIST = [
  "gaeks.group@gmail.com",
  "triawan25@gmail.com",
  "ranesath@gmail.com"
];
const SUPER_ADMIN_EMAIL = "gaeks.group@gmail.com";
const GOOGLE_CLIENT_ID = "41832472270-6r8iudma1eho6kn3q6rs4rl7b9ank7n4.apps.googleusercontent.com";

const AUTH_STORAGE_KEY = 'gaeks_user_session_v2';
const USERS_DB_KEY = 'gaeks_users_db_v2';

const GaeksAuth = {
  getUsersDb() {
    let raw = null;
    try { raw = localStorage.getItem(USERS_DB_KEY); } catch(e) {}
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
    try { raw = localStorage.getItem(AUTH_STORAGE_KEY); } catch(e) {}
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

  saveSessionDual(user) {
    try {
      localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(user));
    } catch(e) {}
    try {
      document.cookie = "gaeks_session=" + encodeURIComponent(JSON.stringify(user)) + "; path=/; max-age=2592000; SameSite=Lax";
    } catch(e) {}
  },

  processVerifiedGoogleUser(email, name, avatar, targetUrl = '') {
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

    this.saveSessionDual(user);
    this.recordUserRegistration(user);

    let dest = targetUrl;
    if (!dest) {
      const p = new URLSearchParams(window.location.search);
      dest = p.get('redirect') || 'index.html';
    }
    dest = decodeURIComponent(dest).replace(/^\//, '');
    const finalUrl = window.location.origin + '/' + dest;
    window.location.replace(finalUrl);
  },

  loginWithEmail(email, password, customName = '', targetUrl = '') {
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

    this.saveSessionDual(user);
    this.recordUserRegistration(user);

    let dest = targetUrl;
    if (!dest) {
      const p = new URLSearchParams(window.location.search);
      dest = p.get('redirect') || 'index.html';
    }
    dest = decodeURIComponent(dest).replace(/^\//, '');
    const finalUrl = window.location.origin + '/' + dest;
    window.location.replace(finalUrl);
  },

  logout() {
    try { localStorage.removeItem(AUTH_STORAGE_KEY); } catch(e) {}
    try { document.cookie = "gaeks_session=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT"; } catch(e) {}
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
print("✓ auth.js berhasil diperbarui.")

print("=== 2. Memperbarui login.html (Hard Absolute Redirection) ===")
with open("login.html", "w") as f:
    f.write('''<!DOCTYPE html>
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
  <script src="auth.js"></script>
  <style> body { font-family: 'Plus Jakarta Sans', sans-serif; } </style>
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
        <div class="flex bg-slate-950 p-1 rounded-xl border border-slate-800 mb-6 text-xs font-bold">
          <button id="tab-login" onclick="setAuthTab('login')" class="flex-1 py-2 rounded-lg bg-blue-600 text-white transition">
            Masuk ke Akun
          </button>
          <button id="tab-register" onclick="setAuthTab('register')" class="flex-1 py-2 rounded-lg text-slate-400 hover:text-white transition">
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
          <button type="submit" id="btn-submit-login" class="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs sm:text-sm rounded-xl transition shadow-lg shadow-blue-500/20">
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
              <p class="text-[10px] text-slate-500 mt-1">Kami akan mengirimkan 6 digit kode verifikasi resmi dari <strong>no-reply@gaeks.com</strong>.</p>
            </div>
            <button type="button" id="btn-send-otp" onclick="requestOtpCode()" class="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs sm:text-sm rounded-xl transition shadow-lg shadow-blue-500/20">
              Kirim 6 Digit Kode Verifikasi ke Email &rarr;
            </button>
          </div>

          <div id="reg-step-verify" class="hidden space-y-3.5">
            <div class="p-3 bg-blue-950/40 border border-blue-800/60 rounded-xl text-xs text-blue-300">
              Kode verifikasi telah dikirimkan ke <strong id="target-email-badge" class="text-white"></strong>. Periksa kotak masuk atau spam email Anda.
            </div>
            <div>
              <label class="block text-xs font-bold text-center text-slate-300 mb-1">Masukkan 6 Digit Kode Verifikasi</label>
              <input type="text" id="reg-otp-code" maxlength="6" placeholder="123456" class="w-full px-3 py-3 text-center text-xl tracking-[10px] font-mono font-black bg-slate-950 border border-blue-500 rounded-xl text-white focus:outline-none shadow-inner" />
            </div>
            <div>
              <label class="block text-[11px] font-semibold text-slate-400 mb-1">Buat Kata Sandi Akun</label>
              <input type="password" id="reg-password" placeholder="Minimal 6 karakter" class="w-full px-3.5 py-2.5 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-xl text-white focus:border-blue-500 focus:outline-none transition" />
            </div>
            <button type="button" id="btn-submit-verify" onclick="submitOtpVerification()" class="w-full py-3 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs sm:text-sm rounded-xl transition shadow-lg shadow-emerald-500/20">
              Verifikasi Kode & Masuk Sekarang &rarr;
            </button>
            <div class="text-center pt-1">
              <button type="button" onclick="backToStep1()" class="text-xs text-slate-400 hover:text-blue-400 transition">← Ganti email atau kirim ulang kode</button>
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

    // Jika sudah ada sesi, langsung forward tanpa render form
    (function() {
      try {
        const u = GaeksAuth.getCurrentUser();
        if (u && u.email) {
          const dest = getRedirectTarget();
          window.location.replace(window.location.origin + '/' + dest.replace(/^\//, ''));
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
        tabL.className = "flex-1 py-2 rounded-lg bg-blue-600 text-white transition";
        tabR.className = "flex-1 py-2 rounded-lg text-slate-400 hover:text-white transition";
        formL.classList.remove('hidden');
        formR.classList.add('hidden');
      } else {
        tabR.className = "flex-1 py-2 rounded-lg bg-blue-600 text-white transition";
        tabL.className = "flex-1 py-2 rounded-lg text-slate-400 hover:text-white transition";
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
          GaeksAuth.processVerifiedGoogleUser(payload.email, payload.name || payload.given_name, payload.picture, dest);
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
      GaeksAuth.loginWithEmail(email, pass, '', dest);
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
          showAlert("✓ Verifikasi berhasil! Mengalihkan...", true);
          GaeksAuth.loginWithEmail(storedEmail, pass, storedName, dest);
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
print("✓ login.html berhasil diperbarui.")

print("=== 3. Memperbarui index.html (Sinkronisasi Navbar 0ms & pageshow BFCache) ===")
with open("index.html", "r") as f:
    idx = f.read()

# Inline script sinkronisasi langsung di DOM navbar
inline_nav_sync = """
        <!-- USER PILL -->
        <div id="nav-user-pill" class="hidden flex items-center space-x-2">
          <a href="profile.html" class="flex items-center space-x-2 p-1 pr-3 rounded-full bg-slate-900 border border-slate-700 hover:border-blue-500 transition">
            <img id="nav-user-avatar" class="w-6 h-6 rounded-full object-cover" src="https://api.dicebear.com/7.x/initials/svg?seed=User" alt="Avatar" />
            <span id="nav-user-name" class="text-xs font-semibold text-slate-200 max-w-[100px] truncate">User</span>
            <span id="nav-user-badge" class="px-1.5 py-0.2 rounded-full text-[9px] font-extrabold bg-blue-950 text-blue-300 border border-blue-800">FREE</span>
          </a>
        </div>

        <!-- LOGIN / SIGN UP BUTTON -->
        <a href="login.html?redirect=index.html" id="nav-btn-login" class="px-4 py-2 text-xs font-bold rounded-xl bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-500/20 transition flex items-center gap-1.5"><svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"></path></svg><span>Masuk / Daftar</span></a>
      </div>

      <script>
        (function() {
          try {
            var raw = localStorage.getItem('gaeks_user_session_v2');
            if (!raw) {
              var m = document.cookie.match(/gaeks_session=([^;]+)/);
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
"""

idx = re.sub(r'<!-- USER PILL -->.*?<!-- LOGIN / SIGN UP BUTTON -->.*?</a>\s*</div>', inline_nav_sync, idx, flags=re.DOTALL)

script_pos = idx.rfind("<script>")
clean_idx_js = """<script>
    function handleServiceAccess(targetUrl) {
      const user = GaeksAuth.getCurrentUser();
      if (user) {
        window.location.href = window.location.origin + '/' + targetUrl.replace(/^\//, '');
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

    function openAdminModal() {
      renderAdminUsersTable();
      const m = document.getElementById('admin-modal');
      if (m) m.classList.remove('hidden');
    }

    function closeAdminModal() {
      const m = document.getElementById('admin-modal');
      if (m) m.classList.add('hidden');
    }

    function renderAdminUsersTable(searchKeyword = '') {
      const users = GaeksAuth.getUsersDb();
      const tbody = document.getElementById('admin-user-table-body');
      if (!tbody) return;
      tbody.innerHTML = '';

      let filtered = users;
      if (searchKeyword.trim()) {
        const kw = searchKeyword.toLowerCase();
        filtered = users.filter(u => u.email.toLowerCase().includes(kw) || (u.name && u.name.toLowerCase().includes(kw)));
      }

      const countEl = document.getElementById('admin-user-count');
      if (countEl) countEl.innerText = `${filtered.length} Pengguna`;

      if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" class="p-4 text-center text-slate-500 italic">Tidak ada pengguna.</td></tr>`;
        return;
      }

      filtered.forEach(u => {
        const regDate = new Date(u.registeredAt || Date.now()).toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' });
        const isPro = (u.plan === 'PRO' || u.plan === 'PRO_VIP');

        tbody.innerHTML += `
          <tr class="hover:bg-slate-900/60 transition">
            <td class="p-2.5">
              <div class="font-bold text-white">${u.name || 'User'}</div>
              <div class="text-[11px] text-slate-400 font-mono">${u.email}</div>
            </td>
            <td class="p-2.5 uppercase font-medium text-[10px] text-slate-400">${u.provider || 'email'}</td>
            <td class="p-2.5 text-slate-400">${regDate}</td>
            <td class="p-2.5">
              <span class="px-2 py-0.5 rounded text-[10px] font-bold ${isPro ? 'bg-emerald-950 text-emerald-300 border border-emerald-800' : 'bg-slate-900 text-slate-400 border border-slate-800'}">
                ${u.plan || 'FREE'}
              </span>
            </td>
            <td class="p-2.5 text-right">
              <button onclick="togglePlan('${u.email}')" class="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 text-[10px] font-semibold transition">
                ${isPro ? 'Ubah ke Free' : 'Jadikan PRO'}
              </button>
            </td>
          </tr>
        `;
      });
    }

    function togglePlan(email) {
      GaeksAuth.toggleUserPlan(email);
      renderAdminUsersTable();
    }

    function filterAdminUsers(val) {
      renderAdminUsersTable(val);
    }

    function exportUsersJson() {
      const data = JSON.stringify(GaeksAuth.getUsersDb(), null, 2);
      const blob = new Blob([data], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `gaeks_users_export_${Date.now()}.json`;
      a.click();
    }

    // Jalankan segera dan tangani Back-Forward Cache (pageshow)
    updateNavbar();
    window.addEventListener('DOMContentLoaded', updateNavbar);
    window.addEventListener('load', updateNavbar);
    window.addEventListener('pageshow', updateNavbar);
  </script>"""

idx = idx[:script_pos] + clean_idx_js + "\n</body>\n</html>"
with open("index.html", "w") as f: f.write(idx)
print("✓ index.html selesai disinkronkan.")

print("=== 4. Memperbarui cv.html dengan Pengecekan Sesi Ganda ===")
with open("cv.html", "r") as f: cv = f.read()

cv = re.sub(
    r'<head>.*?<meta charset="UTF-8"',
    '''<head>
  <script>
    (function() {
      var raw = null;
      try { raw = localStorage.getItem('gaeks_user_session_v2'); } catch(e) {}
      if (!raw) {
        try {
          var m = document.cookie.match(/gaeks_session=([^;]+)/);
          if (m) raw = decodeURIComponent(m[1]);
        } catch(e) {}
      }
      if (!raw) {
        window.location.replace(window.location.origin + '/login.html?redirect=cv.html');
      }
    })();
  </script>
  <meta charset="UTF-8"''',
    cv,
    flags=re.DOTALL
)
with open("cv.html", "w") as f: f.write(cv)
print("✓ cv.html selesai diperbarui.")

print("=== 5. Menjalankan Git Commit & Force Push ke GitHub ===")
subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "fix: implement dual-layer cookie and localStorage session, BFCache pageshow navbar sync, and absolute URL redirects"])
push_res = subprocess.run(["git", "push", "origin", "main", "--force"], capture_output=True, text=True)
print(push_res.stdout)
if push_res.stderr: print(push_res.stderr)
print("=== SEMUA SELESAI & SUDAH AKTIF DI SERVER LIVE! ===")
