import os, re, subprocess

print("=== 1. Memperbarui login.html (Prosesor Mandiri Bebas Cache) ===")
with open("login.html", "r") as fp:
    login = fp.read()

# Jadikan pemroses sesi mandiri langsung di dalam login.html
inline_proc = """
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

      // 1. Dual Persistence: LocalStorage + Cookie
      try {
        localStorage.setItem('gaeks_user_session_v2', JSON.stringify(user));
      } catch(e) {}
      try {
        document.cookie = "gaeks_session=" + encodeURIComponent(JSON.stringify(user)) + "; path=/; max-age=2592000; SameSite=Lax";
      } catch(e) {}

      // 2. Record User Registration
      try {
        if (window.GaeksAuth && typeof GaeksAuth.recordUserRegistration === 'function') {
          GaeksAuth.recordUserRegistration(user);
        }
      } catch(e) {}

      // 3. HARD ABSOLUTE REDIRECT (URL Mutlak Langsung)
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
"""

login = re.sub(r'function handleCredentialResponse\(response\)\s*\{.*?\}\s*\}', inline_proc, login, flags=re.DOTALL)
login = re.sub(r'GaeksAuth\.loginWithEmail\(email, pass, \'\'\, dest\);', 'processLoginSuccess(email, email.split("@")[0], "", "email", dest);', login)
login = re.sub(r'GaeksAuth\.loginWithEmail\(storedEmail, pass, storedName, dest\);', 'processLoginSuccess(storedEmail, storedName, "", "email", dest);', login)
login = login.replace('src="auth.js"', 'src="auth.js?v=20260914_04"')
login = login.replace('src="auth.js?v=20260914_03"', 'src="auth.js?v=20260914_04"')

with open("login.html", "w") as fp:
    fp.write(login)
print("✓ login.html selesai diperbarui.")

print("=== 2. Memperbaiki cv.html (Tombol Buat CV Baru & Anti-Cache) ===")
if os.path.exists("cv.html"):
    with open("cv.html", "r") as fp:
        cv = fp.read()
    
    # Hapus duplikasi saveCvList legacy yang menimpa kunci penyimpanan
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

    # Perbaiki createNewBlankCV agar langsung membuka editor secara instan
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

    cv = cv.replace('src="auth.js"', 'src="auth.js?v=20260914_04"')
    cv = cv.replace('src="auth.js?v=20260914_03"', 'src="auth.js?v=20260914_04"')

    with open("cv.html", "w") as fp:
        fp.write(cv)
    print("✓ cv.html tombol Buat CV Baru aktif & responsif.")

print("=== 3. Memperbarui index.html (Anti-Cache) ===")
if os.path.exists("index.html"):
    with open("index.html", "r") as fp:
        idx = fp.read()
    idx = idx.replace('src="auth.js"', 'src="auth.js?v=20260914_04"')
    idx = idx.replace('src="auth.js?v=20260914_03"', 'src="auth.js?v=20260914_04"')
    with open("index.html", "w") as fp:
        fp.write(idx)
    print("✓ index.html anti-cache diperbarui.")

print("=== 4. Menjalankan Git Force Push ke GitHub ===")
subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "fix: self-contained auth processor in login.html and fix createNewBlankCV editor trigger"])
push_res = subprocess.run(["git", "push", "origin", "main", "--force"], capture_output=True, text=True)
print(push_res.stdout)
if push_res.stderr: print(push_res.stderr)
print("=== DEPLOYMENT SELESAI! ===")
