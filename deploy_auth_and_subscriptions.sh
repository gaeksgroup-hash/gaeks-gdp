#!/bin/bash
set -e

echo "=== 1. Membuat auth.js (Sentral Autentikasi & Whitelist VIP) ==="
cat << 'AUTH_JS' > auth.js
// GAEKS DIGITAL ECOSYSTEM - AUTH & SESSION CONTROLLER
const VIP_WHITELIST = [
  "gaeks.group@gmail.com",
  "triawan25@gmail.com",
  "ranesath@gmail.com"
];

const AUTH_STORAGE_KEY = 'gaeks_user_session_v1';

const GaeksAuth = {
  getCurrentUser() {
    const raw = localStorage.getItem(AUTH_STORAGE_KEY);
    if (!raw) return null;
    try {
      const user = JSON.parse(raw);
      if (user && user.email && VIP_WHITELIST.includes(user.email.toLowerCase().trim())) {
        user.isPro = true;
        user.plan = 'PRO_VIP';
        user.planLabel = 'GAEKS PRO VIP (Akses Penuh)';
      }
      return user;
    } catch(e) {
      return null;
    }
  },

  isProUser() {
    const user = this.getCurrentUser();
    if (!user) return false;
    return !!user.isPro;
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
      plan: isVip ? 'PRO_VIP' : 'FREE',
      planLabel: isVip ? 'GAEKS PRO VIP (Akses Penuh)' : 'Free Tier',
      loginAt: Date.now()
    };

    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(user));
    window.location.reload();
  },

  loginWithGoogle(emailInput = '') {
    const cleanEmail = (emailInput || prompt("Masukkan Akun Google Anda (contoh: triawan25@gmail.com):") || "").toLowerCase().trim();
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
      plan: isVip ? 'PRO_VIP' : 'FREE',
      planLabel: isVip ? 'GAEKS PRO VIP (Akses Penuh)' : 'Free Tier',
      loginAt: Date.now()
    };

    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(user));
    window.location.reload();
  },

  logout() {
    localStorage.removeItem(AUTH_STORAGE_KEY);
    window.location.reload();
  }
};
AUTH_JS

echo "=== 2. Membuat profile.html (Halaman Profil & Status Langganan) ==="
cat << 'PROFILE_HTML' > profile.html
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Profil Akun & Berlangganan | GAEKS Digital</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <script src="auth.js"></script>
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
        <span class="font-extrabold text-base bg-gradient-to-r from-blue-400 to-indigo-300 bg-clip-text text-transparent">Profil & Langganan</span>
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
          Nikmati akses ke mesin resume standar ATS global. Tingkatkan keanggotaan untuk membuka seluruh 15 tema visual eksekutif dan fitur premium lainnya.
        </p>
      </div>

      <div class="p-6 bg-slate-900/80 rounded-2xl border border-slate-800 space-y-4">
        <h3 class="text-sm font-bold uppercase tracking-wider text-emerald-400">Keunggulan GAEKS PRO</h3>
        <ul class="space-y-2.5 text-xs text-slate-300">
          <li class="flex items-center gap-2">
            <span class="text-emerald-400 font-bold">✓</span>
            <span>Buka seluruh <strong>15 Tema Visual</strong> (termasuk tema bermain warna lembar kerja).</span>
          </li>
          <li class="flex items-center gap-2">
            <span class="text-emerald-400 font-bold">✓</span>
            <span>Ekspor PDF resolusi tinggi A4 tanpa batas dan tanpa watermark.</span>
          </li>
          <li class="flex items-center gap-2">
            <span class="text-emerald-400 font-bold">✓</span>
            <span>Penyimpanan banyak versi CV di server cloud per akun.</span>
          </li>
          <li class="flex items-center gap-2">
            <span class="text-emerald-400 font-bold">✓</span>
            <span>Dukungan prioritas WhatsApp untuk review dan saran tata letak ATS.</span>
          </li>
        </ul>
      </div>
    </div>

    <div class="p-5 bg-slate-900/50 rounded-2xl border border-slate-800/80 flex flex-wrap items-center justify-between gap-4">
      <div>
        <h4 class="text-sm font-bold text-white">Mulai Membuat Resume Baru?</h4>
        <p class="text-xs text-slate-400">Buka studio resume ATS untuk menyusun pengalaman kerja Anda.</p>
      </div>
      <a href="cv.html" class="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs transition">
        Buka ATS CV Studio &rarr;
      </a>
    </div>
  </main>

  <footer class="border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-500">
    <p>&copy; 2026 GAEKS DIGITAL PRODUCT. Standard ATS Resume Engine.</p>
  </footer>

  <script>
    window.onload = function() {
      const user = GaeksAuth.getCurrentUser();
      if (!user) {
        alert("Silakan masuk atau daftar akun terlebih dahulu.");
        window.location.href = "cv.html";
        return;
      }

      document.getElementById('prof-name').innerText = user.name || 'Pengguna GAEKS';
      document.getElementById('prof-email').innerText = user.email || '-';
      document.getElementById('prof-avatar').src = user.avatar || 'https://api.dicebear.com/7.x/initials/svg?seed=' + encodeURIComponent(user.name);
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
    };
  </script>
</body>
</html>
PROFILE_HTML

echo "=== 3. Membuat pricing.html (Pilihan Paket & Berlangganan) ==="
cat << 'PRICING_HTML' > pricing.html
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Pilihan Paket & Berlangganan | GAEKS Digital</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <script src="auth.js"></script>
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
      </div>

      <div class="flex items-center space-x-3">
        <a href="profile.html" id="nav-user-profile-btn" class="text-xs font-semibold px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-700 text-slate-300 hover:text-white transition">
          Profil Saya
        </a>
      </div>
    </div>
  </header>

  <main class="max-w-5xl mx-auto w-full px-4 sm:px-6 py-12 flex-grow space-y-12">
    <div class="text-center max-w-2xl mx-auto space-y-3">
      <span class="text-xs font-bold uppercase tracking-widest text-blue-400 bg-blue-950/80 px-3 py-1 rounded-full border border-blue-800/80">Rencana Berlangganan</span>
      <h1 class="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">Investasi Terbaik untuk Karier Impian Anda</h1>
      <p class="text-xs sm:text-sm text-slate-400">Pilih paket yang sesuai dengan kebutuhan persiapan seleksi kerja dan eksekutif Anda.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-stretch max-w-4xl mx-auto">
      <!-- FREE TIER -->
      <div class="p-8 bg-slate-900/80 rounded-2xl border border-slate-800 flex flex-col justify-between shadow-xl">
        <div class="space-y-4">
          <div class="flex justify-between items-center">
            <h3 class="text-lg font-bold text-white">Free Starter</h3>
            <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-slate-800 text-slate-400">Gratis Selamanya</span>
          </div>
          <div class="flex items-baseline gap-1">
            <span class="text-3xl font-extrabold text-white">Rp 0</span>
            <span class="text-xs text-slate-400">/ selamanya</span>
          </div>
          <p class="text-xs text-slate-400">Cocok untuk fresh graduate atau pembuatan 1 resume cepat standar dasar.</p>
          
          <div class="pt-4 border-t border-slate-800 space-y-3 text-xs text-slate-300">
            <div class="flex items-center gap-2"><span>✓</span><span>Akses 5 Tema Visual Terbuka</span></div>
            <div class="flex items-center gap-2"><span>✓</span><span>Pencarian 520+ Profesi ATS</span></div>
            <div class="flex items-center gap-2"><span>✓</span><span>Format A4 Anti-Terpotong</span></div>
            <div class="flex items-center gap-2 text-slate-500"><span>✕</span><span>10 Tema Eksklusif Bermain Warna</span></div>
            <div class="flex items-center gap-2 text-slate-500"><span>✕</span><span>Dukungan Konsultasi Prioritas</span></div>
          </div>
        </div>

        <div class="pt-8">
          <a href="cv.html" class="block w-full py-2.5 text-center text-xs font-bold rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 transition">
            Gunakan Versi Gratis
          </a>
        </div>
      </div>

      <!-- PRO TIER -->
      <div class="p-8 bg-gradient-to-b from-blue-950/40 to-slate-900/90 rounded-2xl border-2 border-blue-500 flex flex-col justify-between shadow-2xl relative">
        <div class="absolute -top-3.5 right-6 px-3 py-0.5 bg-blue-600 rounded-full text-[10px] font-extrabold text-white uppercase tracking-wider">
          Paling Populer
        </div>

        <div class="space-y-4">
          <div class="flex justify-between items-center">
            <h3 class="text-lg font-bold text-white">GAEKS PRO Member</h3>
            <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-950 text-blue-300 border border-blue-800">Akses Penuh</span>
          </div>
          <div class="flex items-baseline gap-1">
            <span class="text-3xl font-extrabold text-white">Rp 49.000</span>
            <span class="text-xs text-slate-400">/ bulan (atau Rp 299.000/thn)</span>
          </div>
          <p class="text-xs text-slate-300">Untuk profesional dan eksekutif yang menginginkan impresi visual berkelas dunia.</p>
          
          <div class="pt-4 border-t border-slate-800 space-y-3 text-xs text-slate-200 font-medium">
            <div class="flex items-center gap-2 text-emerald-400"><span>✓</span><span>Buka Seluruh 15 Tema Visual Eksekutif</span></div>
            <div class="flex items-center gap-2 text-emerald-400"><span>✓</span><span>Desain Bermain Warna (Ivory, Emerald, Linen, Azure)</span></div>
            <div class="flex items-center gap-2 text-emerald-400"><span>✓</span><span>Kartu Identitas Dua Warna (Two-Tone Header Card)</span></div>
            <div class="flex items-center gap-2 text-emerald-400"><span>✓</span><span>Simpan Banyak Resume di Cloud Storage Per Akun</span></div>
            <div class="flex items-center gap-2 text-emerald-400"><span>✓</span><span>Dukungan WhatsApp Prioritas untuk Konsultasi</span></div>
          </div>
        </div>

        <div class="pt-8 space-y-2">
          <a href="https://wa.me/6285608561745?text=Halo%20Admin%20GAEKS%2C%20saya%20ingin%20upgrade%20ke%20GAEKS%20PRO%20Rp49.000%2Fbulan" target="_blank" class="block w-full py-3 text-center text-xs font-bold rounded-xl bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-500/30 transition">
            💬 Upgrade ke GAEKS PRO Sekarang
          </a>
        </div>
      </div>
    </div>
  </main>

  <footer class="border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-500">
    <p>&copy; 2026 GAEKS DIGITAL PRODUCT. Standard ATS Resume Engine.</p>
  </footer>
</body>
</html>
PRICING_HTML

echo "=== 4. Mem-push pembaruan sistem ke GitHub ==="
git add auth.js profile.html pricing.html cv.html
git commit -m "feat: complete auth module, sanitized generic hints, profile and subscription pages with VIP PRO unlock" || true
git push origin main

echo "=== Selesai! Buka https://gdp.gaeks.com/cv.html untuk melihat hasilnya ==="
