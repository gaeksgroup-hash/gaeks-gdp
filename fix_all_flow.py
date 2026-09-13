import os, re, subprocess

print("=== 1. Memperbaiki index.html (Pembersihan Syntax Error & Navbar Otomatis) ===")
with open("index.html", "r") as f:
    idx = f.read()

# Perbaiki tombol Masuk/Daftar di navbar agar membawa ?redirect=index.html
idx = re.sub(
    r'<a href="login\.html.*?" id="nav-btn-login".*?</a>',
    '<a href="login.html?redirect=index.html" id="nav-btn-login" class="px-4 py-2 text-xs font-bold rounded-xl bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-500/20 transition flex items-center gap-1.5"><svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"></path></svg><span>Masuk / Daftar</span></a>',
    idx,
    flags=re.DOTALL
)

# Tulis ulang skrip pengendali index.html secara bersih tanpa duplikasi fungsi
script_pos = idx.rfind("<script>")
clean_idx_js = """<script>
    function handleServiceAccess(targetUrl) {
      const user = GaeksAuth.getCurrentUser();
      if (user) {
        window.location.href = targetUrl;
      } else {
        window.location.href = 'login.html?redirect=' + encodeURIComponent(targetUrl);
      }
    }

    function updateNavbar() {
      const user = GaeksAuth.getCurrentUser();
      const btnLogin = document.getElementById('nav-btn-login');
      const pill = document.getElementById('nav-user-pill');
      const adminBtn = document.getElementById('nav-btn-admin');

      if (user) {
        if (btnLogin) btnLogin.classList.add('hidden');
        if (pill) pill.classList.remove('hidden');
        const avatar = document.getElementById('nav-user-avatar');
        if (avatar) avatar.src = user.avatar;
        const name = document.getElementById('nav-user-name');
        if (name) name.innerText = user.name;

        const badge = document.getElementById('nav-user-badge');
        if (badge) {
          if (user.isAdmin) {
            badge.className = "px-1.5 py-0.2 rounded-full text-[9px] font-extrabold bg-amber-950 text-amber-300 border border-amber-800";
            badge.innerText = "ADMIN";
            if (adminBtn) adminBtn.classList.remove('hidden');
          } else if (user.isPro) {
            badge.className = "px-1.5 py-0.2 rounded-full text-[9px] font-extrabold bg-emerald-950 text-emerald-300 border border-emerald-800";
            badge.innerText = "PRO VIP";
          } else {
            badge.className = "px-1.5 py-0.2 rounded-full text-[9px] font-extrabold bg-blue-950 text-blue-300 border border-blue-800";
            badge.innerText = "FREE";
          }
        }
      } else {
        if (btnLogin) btnLogin.classList.remove('hidden');
        if (pill) pill.classList.add('hidden');
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

    // Jalankan segera saat file diparsing browser
    updateNavbar();
    window.addEventListener('DOMContentLoaded', updateNavbar);
    window.addEventListener('load', updateNavbar);
  </script>"""

idx = idx[:script_pos] + clean_idx_js + "\n</body>\n</html>"
with open("index.html", "w") as f:
    f.write(idx)
print("✓ index.html selesai diperbarui.")

print("=== 2. Memperbarui auth.js (Redirect Langsung Tanpa Reload) ===")
with open("auth.js", "r") as f:
    auth_code = f.read()

# Pastikan proses login menggunakan window.location.replace ke target yang diminta
auth_code = re.sub(
    r'processVerifiedGoogleUser\(email, name, avatar.*?\)\s*\{.*?\}',
    '''processVerifiedGoogleUser(email, name, avatar, targetUrl = '') {
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

    const finalDest = targetUrl || new URLSearchParams(window.location.search).get('redirect') || 'index.html';
    window.location.replace(finalDest);
  }''',
    auth_code,
    flags=re.DOTALL
)

auth_code = re.sub(
    r'loginWithEmail\(email, password.*?\)\s*\{.*?\}',
    '''loginWithEmail(email, password, customName = '', targetUrl = '') {
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

    const finalDest = targetUrl || new URLSearchParams(window.location.search).get('redirect') || 'index.html';
    window.location.replace(finalDest);
  }''',
    auth_code,
    flags=re.DOTALL
)

with open("auth.js", "w") as f:
    f.write(auth_code)
print("✓ auth.js selesai diperbarui.")

print("=== 3. Memasang Pelindung Head Guard Ketat di cv.html ===")
if os.path.exists("cv.html"):
    with open("cv.html", "r") as f: cv = f.read()
    if "window.location.replace('login.html?redirect=cv.html')" not in cv:
        guard = """<head>\\n  <script>\\n    (function() {{\\n      var s = localStorage.getItem('gaeks_user_session_v2');\\n      if (!s) {{\\n        window.location.replace('login.html?redirect=cv.html');\\n      }}\\n    }})();\\n  </script>"""
        cv = cv.replace("<head>", guard)
        with open("cv.html", "w") as f: f.write(cv)
    print("✓ cv.html head guard aktif.")

print("=== 4. Mem-push Pembaruan ke GitHub Repository ===")
subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "fix: resolve navbar session update, strict service gatekeeper, and context-aware destination redirects"])
push_res = subprocess.run(["git", "push", "origin", "main", "--force"], capture_output=True, text=True)
print(push_res.stdout)
if push_res.stderr: print(push_res.stderr)

print("=== SELESAI! Silakan uji langsung di peramban Anda ===")
