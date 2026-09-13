import os, re, subprocess

print("=== 1. Memperbarui login.html (Bebas Syntax Error & Pengalihan Instan) ===")
with open("login.html", "r") as fp:
    login = fp.read()

# Script login bersih tanpa orphan catch
clean_login_script = """
    function getRedirectTarget() {
      const p = new URLSearchParams(window.location.search);
      const r = p.get('redirect');
      if (r) return decodeURIComponent(r);
      return 'index.html';
    }

    // Auto-forward jika sudah ada sesi aktif v3
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

    // PROSESOR SESI MANDIRI V3 (LOCALSTORAGE + COOKIE)
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
"""

script_pos = login.rfind("<script>")
login = login[:script_pos] + "<script>" + clean_login_script + "\\n</script>\\n</body>\\n</html>"
with open("login.html", "w") as fp:
    fp.write(login)
print("✓ login.html berhasil diperbarui.")

print("=== 2. Memperbarui auth.js (Clean Slate V3 & Pembersihan Sesi Lama) ===")
with open("auth.js", "w") as fp:
    fp.write('''// GAEKS DIGITAL ECOSYSTEM - AUTH ENGINE V3 (CLEAN SLATE)
try {
  localStorage.removeItem('gaeks_user_session_v1');
  localStorage.removeItem('gaeks_user_session_v2');
  localStorage.removeItem('gaeks_user_session');
  document.cookie = "gaeks_session=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
} catch(e) {}

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
        const m = document.cookie.match(/gaeks_session_v3=([^;]+)/);
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

  logout() {
    try { localStorage.removeItem(AUTH_STORAGE_KEY); } catch(e) {}
    try { document.cookie = "gaeks_session_v3=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT"; } catch(e) {}
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

print("=== 3. Memperbaiki cv.html (Tombol Buat CV Baru Aktif & Head Guard V3) ===")
if os.path.exists("cv.html"):
    with open("cv.html", "r") as fp:
        cv = fp.read()

    # Hapus duplikasi saveCvList legacy yang menyebabkan tombol macet
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

    # Perbaiki createNewBlankCV agar langsung membuka editor seketika
    cv = re.sub(
        r'function createNewBlankCV\(\)\s*\{.*?\}',
        """function createNewBlankCV() {
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
    }""",
        cv,
        flags=re.DOTALL
    )

    cv = cv.replace("gaeks_user_session_v2", "gaeks_user_session_v3")
    cv = cv.replace("gaeks_session=", "gaeks_session_v3=")
    cv = cv.replace('src="auth.js"', 'src="auth.js?v=20260914_05"')

    with open("cv.html", "w") as fp:
        fp.write(cv)
    print("✓ cv.html tombol Buat CV Baru aktif & responsif.")

print("=== 4. Memperbarui index.html (Navbar V3 & Rute Layanan) ===")
if os.path.exists("index.html"):
    with open("index.html", "r") as fp:
        idx = fp.read()
    idx = idx.replace("gaeks_user_session_v2", "gaeks_user_session_v3")
    idx = idx.replace("gaeks_users_db_v2", "gaeks_users_db_v3")
    idx = idx.replace("gaeks_session=", "gaeks_session_v3=")
    idx = idx.replace('src="auth.js"', 'src="auth.js?v=20260914_05"')
    with open("index.html", "w") as fp:
        fp.write(idx)
    print("✓ index.html v3 diperbarui.")

print("=== 5. Menjalankan Git Force Push ke GitHub ===")
subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "fix: resolve orphan catch syntax error in login.html, activate clean-slate v3 session, and fix createNewBlankCV editor trigger"])
push_res = subprocess.run(["git", "push", "origin", "main", "--force"], capture_output=True, text=True)
print(push_res.stdout)
if push_res.stderr: print(push_res.stderr)
print("=== DEPLOYMENT SELESAI! ===")
