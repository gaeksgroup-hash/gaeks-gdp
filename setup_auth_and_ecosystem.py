import os, re

print("=== 1. Menulis auth.js (Session, Whitelist VIP & User Database) ===")
with open("auth.js", "w") as f:
    f.write('''// GAEKS DIGITAL ECOSYSTEM - AUTH & USER MANAGEMENT CONTROLLER
const VIP_WHITELIST = [
  "gaeks.group@gmail.com",
  "triawan25@gmail.com",
  "ranesath@gmail.com"
];
const SUPER_ADMIN_EMAIL = "gaeks.group@gmail.com";

const AUTH_STORAGE_KEY = 'gaeks_user_session_v2';
const USERS_DB_KEY = 'gaeks_users_db_v2';

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
      this.sendWelcomeEmailNotice(userObj.email, userObj.name);
    }
    this.saveUsersDb(db);
  },

  sendWelcomeEmailNotice(email, name) {
    try {
      fetch('/api/send_welcome_email.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email, name: name })
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

  loginWithEmail(email, password, name = '') {
    const cleanEmail = email.toLowerCase().trim();
    const isVip = VIP_WHITELIST.includes(cleanEmail);
    const displayName = name || cleanEmail.split('@')[0];

    const user = {
      id: 'usr_' + Math.random().toString(36).substr(2, 9),
      email: cleanEmail,
      name: displayName,
      avatar: 'https://api.dicebear.com/7.x/initials/svg?seed=' + encodeURIComponent(displayName),
      provider: 'email',
      isPro: isVip,
      isAdmin: (cleanEmail === SUPER_ADMIN_EMAIL),
      plan: isVip ? 'PRO_VIP' : 'FREE',
      planLabel: isVip ? (cleanEmail === SUPER_ADMIN_EMAIL ? 'SUPER ADMIN' : 'GAEKS PRO VIP') : 'Free Tier',
      loginAt: Date.now()
    };

    this.recordUserRegistration(user);
    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(user));
    window.location.reload();
  },

  loginWithGoogle(emailInput = '') {
    const cleanEmail = (emailInput || prompt("Masukkan Akun Google Anda (contoh: gaeks.group@gmail.com):") || "").toLowerCase().trim();
    if (!cleanEmail) return;

    const isVip = VIP_WHITELIST.includes(cleanEmail);
    const displayName = cleanEmail.split('@')[0].toUpperCase();

    const user = {
      id: 'usr_goog_' + Math.random().toString(36).substr(2, 9),
      email: cleanEmail,
      name: displayName,
      avatar: 'https://api.dicebear.com/7.x/initials/svg?seed=' + encodeURIComponent(displayName),
      provider: 'google',
      isPro: isVip,
      isAdmin: (cleanEmail === SUPER_ADMIN_EMAIL),
      plan: isVip ? 'PRO_VIP' : 'FREE',
      planLabel: isVip ? (cleanEmail === SUPER_ADMIN_EMAIL ? 'SUPER ADMIN' : 'GAEKS PRO VIP') : 'Free Tier',
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
      target.plan = (target.plan === 'PRO' || target.plan === 'PRO_VIP') ? 'FREE' : 'PRO';
      this.saveUsersDb(db);
      return target.plan;
    }
    return null;
  }
};
''')

print("=== 2. Menulis api/send_welcome_email.php (Hostinger Mailer) ===")
os.makedirs("api", exist_ok=True)
with open("api/send_welcome_email.php", "w") as f:
    f.write('''<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

$rawInput = file_get_contents('php://input');
$data = json_decode($rawInput, true);

$toEmail = filter_var($data['email'] ?? '', FILTER_VALIDATE_EMAIL);
$toName  = htmlspecialchars($data['name'] ?? 'Pengguna GAEKS');

if (!$toEmail) {
    echo json_encode(['status' => 'error', 'message' => 'Email tidak valid']);
    exit;
}

$subject = "Selamat Datang di GAEKS Digital Products - Akun Anda Telah Aktif";

$message = "
<html>
<head>
  <title>Selamat Datang di GAEKS Digital</title>
  <style>
    body { font-family: Arial, sans-serif; line-height: 1.6; color: #1e293b; }
    .container { max-width: 600px; margin: auto; padding: 20px; border: 1px solid #e2e8f0; border-radius: 12px; }
    .header { background: #0f172a; color: white; padding: 20px; border-radius: 8px 8px 0 0; text-align: center; }
    .content { padding: 20px; background: #ffffff; }
    .button { display: inline-block; padding: 12px 24px; background: #2563eb; color: #ffffff !important; text-decoration: none; border-radius: 6px; font-weight: bold; margin-top: 15px; }
    .footer { font-size: 11px; color: #64748b; text-align: center; margin-top: 20px; }
  </style>
</head>
<body>
  <div class='container'>
    <div class='header'>
      <h2 style='margin:0;'>GAEKS DIGITAL PRODUCTS</h2>
    </div>
    <div class='content'>
      <h3>Halo, {$toName}!</h3>
      <p>Terima kasih telah mendaftar di <strong>GAEKS Digital Products</strong>. Akun Anda berhasil terdaftar dengan email: <strong>{$toEmail}</strong>.</p>
      <p>Anda sekarang dapat langsung menggunakan <strong>ATS CV Studio</strong> untuk menyusun resume berstandar korporat global dengan 520+ bank profesi terverifikasi.</p>
      <p style='text-align:center;'>
        <a href='https://gdp.gaeks.com/cv.html' class='button'>Buka Studio CV Sekarang</a>
      </p>
      <p>Jika ada pertanyaan atau membutuhkan bantuan seputar akun atau paket PRO, silakan hubungi tim kami via WhatsApp di <a href='https://wa.me/6285608561745'>+62 856-0856-1745</a>.</p>
    </div>
    <div class='footer'>
      &copy; " . date('Y') . " GAEKS Group. All rights reserved.
    </div>
  </div>
</body>
</html>
";

$headers  = "MIME-Version: 1.0\r\n";
$headers .= "Content-type: text/html; charset=UTF-8\r\n";
$headers .= "From: GAEKS Digital <no-reply@gaeks.com>\r\n";
$headers .= "Reply-To: gaeks.group@gmail.com\r\n";
$headers .= "X-Mailer: PHP/" . phpversion();

$mailSent = @mail($toEmail, $subject, $message, $headers);

echo json_encode([
    'status' => $mailSent ? 'success' : 'queued',
    'recipient' => $toEmail,
    'message' => $mailSent ? 'Email selamat datang berhasil dikirim' : 'Email diproses oleh server Hostinger'
]);
''')

print("=== 3. Memperbarui index.html (Navigasi Auth, Hero Gatekeeper & Modal Admin Users) ===")
# Generate complete index.html with authentication and admin user view
with open("index.html", "w") as f:
    f.write('''<!DOCTYPE html>
<html lang="id" class="scroll-smooth">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>GAEKS Digital Products | Corporate ATS Studio & Enterprise SaaS</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <script src="auth.js"></script>
  <style> body { font-family: 'Plus Jakarta Sans', sans-serif; } </style>
</head>
<body class="bg-slate-950 text-slate-100 antialiased min-h-screen flex flex-col justify-between selection:bg-blue-600 selection:text-white">

  <!-- NAVBAR UTAMA -->
  <header class="sticky top-0 z-50 w-full backdrop-blur-md bg-slate-950/90 border-b border-slate-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <a href="index.html" class="flex items-center space-x-2">
          <span class="w-8 h-8 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center font-extrabold text-white text-sm shadow-md shadow-blue-500/30">G</span>
          <span class="font-extrabold text-lg bg-gradient-to-r from-blue-400 via-indigo-300 to-white bg-clip-text text-transparent">
            GAEKS DIGITAL
          </span>
        </a>
      </div>

      <nav class="hidden md:flex items-center space-x-6 text-xs font-semibold text-slate-400">
        <a href="#services" class="hover:text-white transition">Layanan Digital</a>
        <a href="pricing.html" class="hover:text-white transition">Paket & Harga</a>
        <a href="cv.html" class="hover:text-white transition">ATS CV Studio</a>
      </nav>

      <div class="flex items-center space-x-2.5">
        <button id="nav-btn-admin" onclick="openAdminModal()" class="hidden px-2.5 py-1.5 text-[11px] font-bold rounded-lg bg-amber-950/60 border border-amber-600 text-amber-300 hover:bg-amber-900 transition flex items-center gap-1">
          <span>👑 Admin Users</span>
        </button>

        <div id="nav-user-pill" class="hidden flex items-center space-x-2">
          <a href="profile.html" class="flex items-center space-x-2 p-1 pr-3 rounded-full bg-slate-900 border border-slate-700 hover:border-blue-500 transition">
            <img id="nav-user-avatar" class="w-6 h-6 rounded-full object-cover" src="" alt="Avatar" />
            <span id="nav-user-name" class="text-xs font-semibold text-slate-200 max-w-[100px] truncate">User</span>
            <span id="nav-user-badge" class="px-1.5 py-0.2 rounded-full text-[9px] font-extrabold bg-blue-950 text-blue-300 border border-blue-800">FREE</span>
          </a>
        </div>

        <button id="nav-btn-login" onclick="openAuthModal()" class="px-4 py-2 text-xs font-bold rounded-xl bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-500/20 transition flex items-center gap-1.5">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"></path></svg>
          <span>Masuk / Daftar</span>
        </button>
      </div>
    </div>
  </header>

  <!-- HERO -->
  <main class="flex-grow">
    <section class="py-16 sm:py-24 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-5">
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-950/80 border border-blue-800/80 text-[11px] font-bold text-blue-300">
        <span class="w-2 h-2 rounded-full bg-blue-400 animate-pulse"></span>
        <span>Ekosistem Aplikasi Digital GAEKS Group</span>
      </div>
      <h1 class="text-3xl sm:text-5xl font-black text-white tracking-tight leading-tight max-w-3xl mx-auto">
        Bangun Karier Eksekutif & Infrastruktur Bisnis Modern
      </h1>
      <p class="text-sm sm:text-base text-slate-400 max-w-2xl mx-auto leading-relaxed">
        Satu akun terpadu untuk menyusun Resume ATS berstandar global, slide presentasi pitch deck investor, dan arsitektur transformasi proses bisnis.
      </p>
      <div class="pt-4 flex flex-col sm:flex-row items-center justify-center gap-3">
        <button onclick="handleServiceAccess('cv.html')" class="w-full sm:w-auto px-6 py-3.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-extrabold text-xs sm:text-sm shadow-xl shadow-blue-500/25 transition">
          🚀 Buka ATS CV Studio Sekarang
        </button>
        <a href="pricing.html" class="w-full sm:w-auto px-6 py-3.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 font-bold text-xs sm:text-sm transition">
          Lihat 15 Tema Visual & Harga
        </a>
      </div>
      <p class="text-[11px] text-slate-500">*Wajib mendaftar / masuk menggunakan akun Google atau email Anda sebelum mengakses layanan.</p>
    </section>

    <!-- LAYANAN -->
    <section id="services" class="py-12 border-t border-slate-900 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="p-6 bg-slate-900/90 rounded-2xl border border-slate-800 hover:border-blue-500/50 transition shadow-xl flex flex-col justify-between space-y-5">
          <div class="space-y-3">
            <div class="w-10 h-10 rounded-xl bg-blue-950 text-blue-400 flex items-center justify-center font-bold text-lg border border-blue-800/80">📄</div>
            <div class="flex items-center justify-between">
              <h3 class="font-extrabold text-base text-white">GAEKS ATS CV Studio</h3>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800">Aktif & Siap Pakai</span>
            </div>
            <p class="text-xs text-slate-400 leading-relaxed">
              Dilengkapi <strong>520+ bank profesi</strong>, pencarian live search instan, 15 varian tema visual, anti-cut PDF export, dan tanpa watermark buatan AI.
            </p>
          </div>
          <button onclick="handleServiceAccess('cv.html')" class="w-full py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs transition text-center">
            Coba Pembuat CV ATS &rarr;
          </button>
        </div>

        <div class="p-6 bg-slate-900/60 rounded-2xl border border-slate-800/80 transition shadow-xl flex flex-col justify-between space-y-5">
          <div class="space-y-3">
            <div class="w-10 h-10 rounded-xl bg-purple-950 text-purple-400 flex items-center justify-center font-bold text-lg border border-purple-800/80">📊</div>
            <div class="flex items-center justify-between">
              <h3 class="font-extrabold text-base text-white">GAEKS Presentation Maker</h3>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-amber-950 text-amber-300 border border-amber-800">Tahap Pengembangan</span>
            </div>
            <p class="text-xs text-slate-400 leading-relaxed">
              Generator presentasi pitch deck eksekutif untuk pendanaan startup (Trial 3 hari & SaaS bulanan). Otomatisasi struktur alur cerita dan blueprint visual slide.
            </p>
          </div>
          <button onclick="alert('Layanan GAEKS Presentation Maker sedang dalam tahap finalisasi dan akan segera hadir!')" class="w-full py-2.5 rounded-xl bg-slate-800 text-slate-400 font-bold text-xs transition text-center">
            Segera Hadir (Trial 3 Hari)
          </button>
        </div>

        <div class="p-6 bg-slate-900/60 rounded-2xl border border-slate-800/80 transition shadow-xl flex flex-col justify-between space-y-5">
          <div class="space-y-3">
            <div class="w-10 h-10 rounded-xl bg-emerald-950 text-emerald-400 flex items-center justify-center font-bold text-lg border border-emerald-800/80">⚙️</div>
            <div class="flex items-center justify-between">
              <h3 class="font-extrabold text-base text-white">ERP & Business Process</h3>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-950 text-blue-300 border border-blue-800">Konsultasi</span>
            </div>
            <p class="text-xs text-slate-400 leading-relaxed">
              Arsitektur sistem ERP (Odoo & Dolibarr), integrasi supply chain, pemetaan alur proses bisnis ISO 31000, serta otomatisasi operasional logistik ekspor-impor.
            </p>
          </div>
          <a href="https://wa.me/6285608561745?text=Halo%20Admin%20GAEKS%2C%20saya%20tertarik%20konsultasi%20implementasi%20ERP%20dan%20Business%20Process" target="_blank" class="w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-emerald-300 font-bold text-xs transition text-center">
            Konsultasi via WhatsApp &rarr;
          </a>
        </div>
      </div>
    </section>
  </main>

  <!-- AUTH MODAL -->
  <div id="auth-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
    <div class="bg-slate-900 border border-slate-700 rounded-2xl max-w-md w-full p-6 sm:p-7 shadow-2xl space-y-5">
      <div class="flex items-start justify-between">
        <div>
          <h3 class="font-extrabold text-lg text-white">Masuk / Daftar Akun</h3>
          <p class="text-xs text-slate-400 mt-0.5">Daftar gratis untuk mulai membuat resume ATS berstandar internasional.</p>
        </div>
        <button onclick="closeAuthModal()" class="text-slate-400 hover:text-white text-xl font-bold">&times;</button>
      </div>

      <button onclick="loginGoogle()" class="w-full py-2.5 px-4 bg-white hover:bg-slate-100 text-slate-900 font-bold text-xs rounded-xl flex items-center justify-center gap-2.5 transition shadow-md">
        <svg class="w-4 h-4" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>
        <span>Lanjutkan dengan Google (1-Klik)</span>
      </button>

      <div class="flex items-center gap-2 text-slate-600 text-xs">
        <hr class="flex-grow border-slate-800" /><span>atau dengan Email</span><hr class="flex-grow border-slate-800" />
      </div>

      <form onsubmit="handleEmailSubmit(event)" class="space-y-3">
        <div>
          <label class="block text-[11px] text-slate-400 mb-1">Nama Lengkap</label>
          <input type="text" id="auth-name" placeholder="Alexander Pratama" class="w-full px-3 py-2 text-xs bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" />
        </div>
        <div>
          <label class="block text-[11px] text-slate-400 mb-1">Alamat Email</label>
          <input type="email" id="auth-email" required placeholder="nama@email.com" class="w-full px-3 py-2 text-xs bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" />
        </div>
        <div>
          <label class="block text-[11px] text-slate-400 mb-1">Kata Sandi</label>
          <input type="password" id="auth-pass" required placeholder="••••••••" class="w-full px-3 py-2 text-xs bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" />
        </div>
        <button type="submit" class="w-full py-2.5 px-4 bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs rounded-xl transition shadow-lg shadow-blue-500/20">
          Daftar / Masuk Sekarang
        </button>
      </form>

      <div class="p-3 bg-slate-950 rounded-xl border border-slate-800/80 space-y-1.5">
        <span class="text-[10px] text-slate-400 font-bold block">Akses Pengujian Cepat (Admin & VIP):</span>
        <div class="flex flex-wrap gap-1">
          <button type="button" onclick="quickLogin('gaeks.group@gmail.com', 'GAEKS Admin')" class="px-2 py-0.5 rounded text-[10px] bg-amber-950/80 text-amber-300 border border-amber-800 hover:bg-amber-900 transition">👑 gaeks.group@gmail.com (Admin)</button>
          <button type="button" onclick="quickLogin('triawan25@gmail.com', 'Deny Triawan')" class="px-2 py-0.5 rounded text-[10px] bg-blue-950/80 text-blue-300 border border-blue-800 hover:bg-blue-900 transition">⭐ triawan25@gmail.com (VIP)</button>
          <button type="button" onclick="quickLogin('ranesath@gmail.com', 'Ranesath')" class="px-2 py-0.5 rounded text-[10px] bg-blue-950/80 text-blue-300 border border-blue-800 hover:bg-blue-900 transition">⭐ ranesath@gmail.com (VIP)</button>
        </div>
      </div>
    </div>
  </div>

  <!-- ADMIN USERS MODAL -->
  <div id="admin-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/85 backdrop-blur-sm">
    <div class="bg-slate-900 border border-slate-700 rounded-2xl max-w-2xl w-full p-6 shadow-2xl space-y-4 max-h-[85vh] flex flex-col">
      <div class="flex items-start justify-between pb-3 border-b border-slate-800">
        <div>
          <h3 class="font-extrabold text-lg text-white flex items-center gap-2">
            <span>👑 Panel Admin: Daftar Pengguna Terdaftar</span>
            <span id="admin-user-count" class="px-2 py-0.5 text-xs rounded-full bg-blue-950 text-blue-300 border border-blue-800">0 User</span>
          </h3>
          <p class="text-xs text-slate-400">Seluruh akun yang mendaftar atau masuk tercatat di database ini.</p>
        </div>
        <button onclick="closeAdminModal()" class="text-slate-400 hover:text-white text-xl font-bold">&times;</button>
      </div>

      <input type="text" id="admin-search-user" oninput="filterAdminUsers(this.value)" placeholder="🔍 Cari email atau nama pengguna..." class="w-full px-3 py-1.5 text-xs bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" />

      <div class="overflow-y-auto flex-grow border border-slate-800 rounded-xl bg-slate-950/60">
        <table class="w-full text-left text-xs">
          <thead class="bg-slate-900 text-slate-400 text-[11px] sticky top-0 border-b border-slate-800">
            <tr>
              <th class="p-2.5">Nama & Email</th>
              <th class="p-2.5">Metode</th>
              <th class="p-2.5">Tgl Daftar</th>
              <th class="p-2.5">Status Paket</th>
              <th class="p-2.5 text-right">Aksi</th>
            </tr>
          </thead>
          <tbody id="admin-user-table-body" class="divide-y divide-slate-800/80 text-slate-300"></tbody>
        </table>
      </div>

      <div class="pt-2 flex justify-between items-center text-xs text-slate-500">
        <span>Data tersimpan di Database Sistem.</span>
        <button onclick="exportUsersJson()" class="px-3 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded font-semibold text-[11px] transition">
          Ekspor Data (JSON)
        </button>
      </div>
    </div>
  </div>

  <footer class="border-t border-slate-900 bg-slate-950 py-8 text-center text-xs text-slate-500">
    <p>&copy; 2026 GAEKS DIGITAL PRODUCT. All rights reserved.</p>
  </footer>

  <script>
    let pendingRedirect = null;

    function handleServiceAccess(targetUrl) {
      const user = GaeksAuth.getCurrentUser();
      if (user) {
        window.location.href = targetUrl;
      } else {
        pendingRedirect = targetUrl;
        openAuthModal();
      }
    }

    function openAuthModal() {
      document.getElementById('auth-modal').classList.remove('hidden');
    }

    function closeAuthModal() {
      document.getElementById('auth-modal').classList.add('hidden');
    }

    function loginGoogle() {
      GaeksAuth.loginWithGoogle();
      if (pendingRedirect) window.location.href = pendingRedirect;
    }

    function handleEmailSubmit(e) {
      e.preventDefault();
      const email = document.getElementById('auth-email').value;
      const pass = document.getElementById('auth-pass').value;
      const name = document.getElementById('auth-name').value;
      GaeksAuth.loginWithEmail(email, pass, name);
      if (pendingRedirect) window.location.href = pendingRedirect;
    }

    function quickLogin(email, name) {
      GaeksAuth.loginWithEmail(email, 'password123', name);
      if (pendingRedirect) window.location.href = pendingRedirect;
    }

    function updateNavbar() {
      const user = GaeksAuth.getCurrentUser();
      const btnLogin = document.getElementById('nav-btn-login');
      const pill = document.getElementById('nav-user-pill');
      const adminBtn = document.getElementById('nav-btn-admin');

      if (user) {
        btnLogin.classList.add('hidden');
        pill.classList.remove('hidden');
        document.getElementById('nav-user-avatar').src = user.avatar;
        document.getElementById('nav-user-name').innerText = user.name;
        
        const badge = document.getElementById('nav-user-badge');
        if (user.isAdmin) {
          badge.className = "px-1.5 py-0.2 rounded-full text-[9px] font-extrabold bg-amber-950 text-amber-300 border border-amber-800";
          badge.innerText = "ADMIN";
          adminBtn.classList.remove('hidden');
        } else if (user.isPro) {
          badge.className = "px-1.5 py-0.2 rounded-full text-[9px] font-extrabold bg-emerald-950 text-emerald-300 border border-emerald-800";
          badge.innerText = "PRO VIP";
        } else {
          badge.className = "px-1.5 py-0.2 rounded-full text-[9px] font-extrabold bg-blue-950 text-blue-300 border border-blue-800";
          badge.innerText = "FREE";
        }
      } else {
        btnLogin.classList.remove('hidden');
        pill.classList.add('hidden');
        adminBtn.classList.add('hidden');
      }
    }

    function openAdminModal() {
      renderAdminUsersTable();
      document.getElementById('admin-modal').classList.remove('hidden');
    }

    function closeAdminModal() {
      document.getElementById('admin-modal').classList.add('hidden');
    }

    function renderAdminUsersTable(searchKeyword = '') {
      const users = GaeksAuth.getUsersDb();
      const tbody = document.getElementById('admin-user-table-body');
      tbody.innerHTML = '';

      let filtered = users;
      if (searchKeyword.trim()) {
        const kw = searchKeyword.toLowerCase();
        filtered = users.filter(u => u.email.toLowerCase().includes(kw) || (u.name && u.name.toLowerCase().includes(kw)));
      }

      document.getElementById('admin-user-count').innerText = `${filtered.length} Pengguna`;

      if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" class="p-4 text-center text-slate-500 italic">Tidak ada pengguna yang cocok.</td></tr>`;
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

    window.onload = function() {
      updateNavbar();
    };
  </script>
</body>
</html>
''')

print("=== 4. Memverifikasi cv.html (Pre-fill CV Deny Triawan khusus gaeks.group@gmail.com, Gatekeeper & Panel Admin) ===")
with open("cv.html", "r") as f:
    cv_html = f.read()

# Pastikan gaeks.group@gmail.com dan triawan25@gmail.com selalu memuat CV Deny Triawan
cv_html = cv_html.replace(
    "if (user && (user.email.toLowerCase() === 'triawan25@gmail.com' || user.email.toLowerCase() === 'gaeks.group@gmail.com'))",
    "if (user && (user.email.toLowerCase().trim() === 'gaeks.group@gmail.com' || user.email.toLowerCase().trim() === 'triawan25@gmail.com'))"
)

# Tulis kembali cv.html
with open("cv.html", "w") as f:
    f.write(cv_html)

print("Semua file berhasil diperbarui!")
