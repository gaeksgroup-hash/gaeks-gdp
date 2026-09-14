# GDP Security Audit

## Evidence Scan
The following files contain references related to auth/session/privilege logic. Secret values are intentionally not printed.
```text
./upgrade_pro_cv.sh:180:                <p class="text-[10px] text-slate-500 mt-1">Disimpan di peramban (akan otomatis tersinkron ke server setelah fitur login aktif).</p>
./upgrade_pro_cv.sh:335:            <!-- SECTION: PROFESSIONAL SUMMARY -->
./upgrade_pro_cv.sh:391:    <p>&copy; 2026 GAEKS DIGITAL PRODUCT. Format CV dioptimalkan secara ketat untuk Applicant Tracking System (ATS).</p>
./upgrade_pro_cv.sh:412:    // Catatan: Jika sistem login telah aktif, fungsi ini dapat mengirimkan file langsung ke endpoint backend server
./upgrade_pro_cv.sh:415:        // Placeholder untuk request POST ke endpoint backend saat login aktif:
./upgrade_pro_cv.sh:416:        // fetch('/api/upload_media.php', { method: 'POST', body: JSON.stringify({ image: base64Data, token: userToken }) });
./update_modern_ats_cv.sh:211:          <!-- FORM 1: PROFIL & KONTAK -->
./update_modern_ats_cv.sh:355:    <p>&copy; 2026 GAEKS DIGITAL PRODUCT. Modern Executive ATS Engine.</p>
./index.html:11:  <script src="auth.js?v=20260914_07"></script>
./index.html:39:        <button id="nav-btn-admin" onclick="openAdminModal()" class="hidden px-2.5 py-1.5 text-[11px] font-bold rounded-lg bg-amber-950/60 border border-amber-600 text-amber-300 hover:bg-amber-900 transition flex items-center gap-1">
./index.html:51:        <a href="login.html?redirect=index.html" id="nav-btn-login" class="px-4 py-2 text-xs font-bold rounded-xl bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-500/20 transition flex items-center gap-1.5">
./index.html:60:            var raw = localStorage.getItem('gaeks_user_session_v3') || localStorage.getItem('gaeks_user_session_v2') || localStorage.getItem('gaeks_user_session');
./index.html:62:              var m = document.cookie.match(/gaeks_session_v3=([^;]+)/) || document.cookie.match(/gaeks_session=([^;]+)/);
./index.html:68:                var b = document.getElementById('nav-btn-login');
./index.html:192:  <!-- SECTION 2: DIGITAL PRODUCTS -->
./index.html:195:      <span class="text-xs font-extrabold uppercase tracking-widest text-emerald-400 font-mono">DIGITAL PRODUCTS</span>
./index.html:202:      <!-- PRODUCT 1: ERP FORWARDING -->
./index.html:219:      <!-- PRODUCT 2: E-BOOK DIGITAL -->
./index.html:236:      <!-- PRODUCT 3: WEBSITE BUILDER -->
./index.html:253:      <!-- PRODUCT 4: SMM MARKETING -->
./index.html:275:    <p>&copy; 2026 GAEKS DIGITAL PRODUCTS. All rights reserved.</p>
./index.html:285:        window.location.href = window.location.origin + '/login.html?redirect=' + encodeURIComponent(targetUrl);
./index.html:291:      const btnLogin = document.getElementById('nav-btn-login');
./index.html:293:      const adminBtn = document.getElementById('nav-btn-admin');
./index.html:311:            if (adminBtn) adminBtn.classList.remove('hidden');
./index.html:314:            badge.innerText = "PRO VIP";
./index.html:315:            if (adminBtn) adminBtn.classList.add('hidden');
./index.html:319:            if (adminBtn) adminBtn.classList.add('hidden');
./index.html:328:        if (adminBtn) adminBtn.classList.add('hidden');
./update_ats_cv_ultimate.sh:180:        <!-- FORM 1: PROFIL -->
./update_ats_cv_ultimate.sh:311:              <!-- BARIS KONTAK BERIKON RINGKAS & PROFESIONAL -->
./update_ats_cv_ultimate.sh:393:    <p>&copy; 2026 GAEKS DIGITAL PRODUCT. Standard ATS Resume Engine.</p>
./fix_mime_and_render.sh:20:        <h2 style='color:#ffffff;margin:0;'>GAEKS DIGITAL PRODUCTS</h2>
./fix_mime_and_render.sh:48:        $authRes = $read($socket);
./fix_mime_and_render.sh:50:        if (substr($authRes, 0, 3) != "235") {
./fix_mime_and_render.sh:52:            $result = ["status" => "error", "message" => "Autentikasi SMTP Gagal: $authRes. Periksa kata sandi."];
./cv-dashboard.html:11:  <script src="auth.js?v=20260914_08"></script>
./presentation.html:17:    <script src="auth.js?v=20260914_08"></script>
./presentation.html:189:        <section id="adminView" class="hidden p-6 max-w-6xl mx-auto w-full relative z-20">
./presentation.html:344:                const raw = localStorage.getItem('gaeks_user_session_v3') || localStorage.getItem('gaeks_user_session_v2') || localStorage.getItem('gaeks_user_session');
./presentation.html:430:                authorName: "Deny Triawan",
./presentation.html:718:                switchView('admin'); 
./presentation.html:844:                let rawData = { id: null, meetingName: "Presentasi Baru", meetingDate: new Date().toISOString().split('T')[0], authorName: "", companyName: "", logoUrl: "", slides: [{ title: "Pendahuluan", points: [{title: "Poin Pembuka", desc: "Keterangan poin..."}], layout: "standard", momNote: "", images: [{url:"", caption:""},{url:"", caption:""},{url:"", caption:""},{url:"", caption:""}], chartType: "bar", chartData: "", tableData: "" }] };
./presentation.html:925:                const elmAuthor = document.getElementById('inputAuthor'); if(elmAuthor) elmAuthor.value = activeMeeting.authorName || ""; 
./presentation.html:1017:                switchView('admin');
./presentation.html:1042:                const elmAuthor = document.getElementById('inputAuthor'); if(elmAuthor) activeMeeting.authorName = elmAuthor.value; 
./presentation.html:1277:                    if (activeMeeting.authorName) metaHtml += `<div class="w-1.5 h-1.5 rounded-full bg-slate-400"></div><span class="text-slate-200 font-medium">${activeMeeting.authorName}</span>`;
./presentation.html:1420:            const vAdmin = document.getElementById('adminView');
./presentation.html:1434:            else if (view === 'admin') { 
./presentation.html:1516:                if(activeMeeting.authorName) metaText += `   •   ${activeMeeting.authorName}`;
./presentation.html:1601:                window.exportJob.active = false; document.documentElement.classList.remove('exporting-mode'); document.body.classList.remove('exporting-mode'); document.getElementById('presentationView').classList.add('hidden'); document.getElementById('presentationView').classList.remove('pdf-background-render'); switchView('admin');
./presentation.html:1651:                if (activeMeeting.authorName) metaText += `   •   ${activeMeeting.authorName}`;
./presentation.html:1785:                window.exportJob.active = false; document.documentElement.classList.remove('exporting-mode'); document.body.classList.remove('exporting-mode'); document.getElementById('presentationView').classList.add('hidden'); document.getElementById('presentationView').classList.remove('pdf-background-render'); switchView('admin');
./update_15_themes_and_clean_sample.sh:4:echo "=== Memperbarui cv.html: Hapus Sampel Deny Triawan & Terapkan 15 Tema (5 Free + 10 PRO Locked) ==="
./update_15_themes_and_clean_sample.sh:54:    /* 6. Emerald Horizon (PRO) */
./update_15_themes_and_clean_sample.sh:60:    /* 7. Crimson Elegance (PRO) */
./update_15_themes_and_clean_sample.sh:66:    /* 8. Obsidian Minimal (PRO) */
./update_15_themes_and_clean_sample.sh:72:    /* 9. Oxford Two-Tone (PRO) */
./update_15_themes_and_clean_sample.sh:78:    /* 10. Swiss Editorial (PRO) */
./update_15_themes_and_clean_sample.sh:84:    /* 11. Imperial Gold (PRO) */
./update_15_themes_and_clean_sample.sh:90:    /* 12. Azure Blue (PRO) */
./update_15_themes_and_clean_sample.sh:96:    /* 13. Metropolitan Boxed (PRO) */
./update_15_themes_and_clean_sample.sh:102:    /* 14. Boutique Creative (PRO) */
./update_15_themes_and_clean_sample.sh:108:    /* 15. Apex Monolith (PRO) */
./update_15_themes_and_clean_sample.sh:268:            <optgroup label="10 Tema Berbayar (GAEKS PRO 🔒)">
./update_15_themes_and_clean_sample.sh:269:              <option value="emerald-horizon">6. Emerald Horizon (PRO 🔒)</option>
./update_15_themes_and_clean_sample.sh:270:              <option value="crimson-elegance">7. Crimson Elegance (PRO 🔒)</option>
./update_15_themes_and_clean_sample.sh:271:              <option value="obsidian-minimal">8. Obsidian Minimal (PRO 🔒)</option>
./update_15_themes_and_clean_sample.sh:272:              <option value="oxford-navy">9. Oxford Two-Tone (PRO 🔒)</option>
./update_15_themes_and_clean_sample.sh:273:              <option value="swiss-editorial">10. Swiss Editorial (PRO 🔒)</option>
./update_15_themes_and_clean_sample.sh:274:              <option value="imperial-gold">11. Imperial Gold (PRO 🔒)</option>
./update_15_themes_and_clean_sample.sh:275:              <option value="azure-sky">12. Azure Blue (PRO 🔒)</option>
./update_15_themes_and_clean_sample.sh:276:              <option value="metro-corporate">13. Metropolitan Boxed (PRO 🔒)</option>
./update_15_themes_and_clean_sample.sh:277:              <option value="boutique-creative">14. Boutique Creative (PRO 🔒)</option>
./update_15_themes_and_clean_sample.sh:278:              <option value="apex-monolith">15. Apex Monolith (PRO 🔒)</option>
./update_15_themes_and_clean_sample.sh:302:          <!-- FORM 1: PROFIL & KONTAK -->
./update_15_themes_and_clean_sample.sh:326:            <!-- TARGET ROLES (520+ PROFESI DENGAN LIVE SEARCH & DRAG/DROP) -->
./update_15_themes_and_clean_sample.sh:503:  <!-- ================= MODAL GAEKS PRO (UPGRADE MEMBER BERBAYAR) ================= -->
./update_15_themes_and_clean_sample.sh:510:            <h3 class="font-extrabold text-lg text-white" id="modal-pro-title">Tema Premium (GAEKS PRO)</h3>
./update_15_themes_and_clean_sample.sh:519:          <span>✨ Keunggulan Tema Visual PRO:</span>
./update_15_themes_and_clean_sample.sh:541:    <p>&copy; 2026 GAEKS DIGITAL PRODUCT. Standard ATS Resume Engine.</p>
./update_15_themes_and_clean_sample.sh:550:    // DEFINISI 15 TEMA (5 FREE + 10 PRO LOCKED)
./update_15_themes_and_clean_sample.sh:557:      { id: 'emerald-horizon', name: 'Emerald Horizon (PRO)', free: false },
./update_15_themes_and_clean_sample.sh:558:      { id: 'crimson-elegance', name: 'Crimson Elegance (PRO)', free: false },
./update_15_themes_and_clean_sample.sh:559:      { id: 'obsidian-minimal', name: 'Obsidian Minimal (PRO)', free: false },
./update_15_themes_and_clean_sample.sh:560:      { id: 'oxford-navy', name: 'Oxford Two-Tone (PRO)', free: false },
./update_15_themes_and_clean_sample.sh:561:      { id: 'swiss-editorial', name: 'Swiss Editorial (PRO)', free: false },
./update_15_themes_and_clean_sample.sh:562:      { id: 'imperial-gold', name: 'Imperial Gold (PRO)', free: false },
./update_15_themes_and_clean_sample.sh:563:      { id: 'azure-sky', name: 'Azure Blue (PRO)', free: false },
./update_15_themes_and_clean_sample.sh:564:      { id: 'metro-corporate', name: 'Metropolitan Boxed (PRO)', free: false },
./update_15_themes_and_clean_sample.sh:565:      { id: 'boutique-creative', name: 'Boutique Creative (PRO)', free: false },
./update_15_themes_and_clean_sample.sh:566:      { id: 'apex-monolith', name: 'Apex Monolith (PRO)', free: false }
./update_15_themes_and_clean_sample.sh:569:    // BANK DATA LENGKAP 526+ PROFESI
./update_15_themes_and_clean_sample.sh:779:        sheetSummary: "PROFIL PROFESIONAL",
./update_15_themes_and_clean_sample.sh:780:        sheetExperience: "PENGALAMAN PROFESIONAL",
./update_15_themes_and_clean_sample.sh:841:        sheetSummary: "PROFESSIONAL SUMMARY",
./update_15_themes_and_clean_sample.sh:842:        sheetExperience: "PROFESSIONAL EXPERIENCE",
./update_15_themes_and_clean_sample.sh:853:        emptyEducation: "No education credentials added yet.",
./update_15_themes_and_clean_sample.sh:1364:          credentialId: el.querySelector('.cert-id').value
./update_15_themes_and_clean_sample.sh:1608:    function addCertificationItem(item = { name: '', issuer: '', period: '', credentialId: '' }) {
./update_15_themes_and_clean_sample.sh:1631:            <input type="text" placeholder="ID: ORCL-78901 / Nilai: Mastery" value="${item.credentialId || ''}" oninput="handleInputChange()" class="cert-id w-full px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded text-white focus:border-blue-500 focus:outline-none" />
./update_15_themes_and_clean_sample.sh:1718:    // ================= 15 TEMA HANDLER (FREE VS PRO LOCKED) =================
./update_15_themes_and_clean_sample.sh:1733:      document.getElementById('modal-pro-title').innerText = `Tema ${theme.name} (GAEKS PRO 🔒)`;
./update_15_themes_and_clean_sample.sh:2181:git commit -m "feat: clean sample data and implement 15 visual themes with 5 free and 10 PRO locked variants" || true
./update_executive_density_cv.sh:215:          <!-- FORM 1: PROFIL & KONTAK -->
./update_executive_density_cv.sh:359:    <p>&copy; 2026 GAEKS DIGITAL PRODUCT. Standard ATS Resume Engine.</p>
./update_executive_density_cv.sh:472:        sheetExperience: "PROFESSIONAL EXPERIENCE",
./update_executive_density_cv.sh:482:        emptyEducation: "No education credentials added yet.",
./update_executive_density_cv.sh:1516:git commit -m "feat: complete overhaul to high-density authentic executive resume standard without AI fluff"
./update_cv_dashboard.sh:193:        <!-- FORM: PROFIL -->
./update_cv_dashboard.sh:384:    <p>&copy; 2026 GAEKS DIGITAL PRODUCT. Standard ATS Resume Engine.</p>
./setup_cv_page.sh:12:  <title>ATS CV Maker | GAEKS DIGITAL PRODUCT</title>
./setup_cv_page.sh:205:    <p>&copy; 2026 GAEKS DIGITAL PRODUCT. Standar Format ATS.</p>
./setup_cv_page.sh:390:  <title>GAEKS DIGITAL PRODUCT | Solusi Layanan & Produk Digital</title>
./setup_cv_page.sh:404:          GAEKS DIGITAL PRODUCT
./setup_cv_page.sh:449:      <p class="text-slate-400 mt-1">Gunakan langsung tanpa hambatan login.</p>
./setup_cv_page.sh:465:            Format ATS profesional dengan live preview dan ekspor PDF langsung ukuran A4. Tanpa syarat login, langsung pakai sekarang.
./setup_cv_page.sh:499:  <!-- PRODUCTS SECTION -->
./setup_cv_page.sh:523:    <p>&copy; 2026 GAEKS DIGITAL PRODUCT. Seluruh hak cipta dilindungi.</p>
./setup_cv_page.sh:531:git commit -m "feat: separate dedicated cv.html page and remove login completely"
./fix_ajax_test_mail.sh:26:        <h2 style='color:#ffffff;margin:0;'>GAEKS DIGITAL PRODUCTS</h2>
./fix_ajax_test_mail.sh:56:    $authRes = $read($socket);
./fix_ajax_test_mail.sh:58:    if (substr($authRes, 0, 3) != "235") {
./fix_ajax_test_mail.sh:60:        echo json_encode(["status" => "error", "message" => "Autentikasi SMTP Gagal: $authRes. Periksa kata sandi."]);
./safe_deploy.sh:8:# 1. Update auth.js
./safe_deploy.sh:9:with open("auth.js", "w") as f:
./safe_deploy.sh:11:const VIP_WHITELIST = [
./safe_deploy.sh:16:const SUPER_ADMIN_EMAIL = "gaeks.group@gmail.com";
./safe_deploy.sh:19:const AUTH_STORAGE_KEY = 'gaeks_user_session_v2';
./safe_deploy.sh:27:        { id: 'usr_adm_1', email: 'gaeks.group@gmail.com', name: 'GAEKS Group (Admin)', provider: 'google', plan: 'PRO_VIP', registeredAt: Date.now() - 86400000 * 5, lastLoginAt: Date.now() },
./safe_deploy.sh:28:        { id: 'usr_vip_2', email: 'triawan25@gmail.com', name: 'Deny Triawan', provider: 'google', plan: 'PRO_VIP', registeredAt: Date.now() - 86400000 * 4, lastLoginAt: Date.now() },
./safe_deploy.sh:29:        { id: 'usr_vip_3', email: 'ranesath@gmail.com', name: 'Ranesath', provider: 'google', plan: 'PRO_VIP', registeredAt: Date.now() - 86400000 * 3, lastLoginAt: Date.now() }
./safe_deploy.sh:84:        user.isAdmin = (clean === SUPER_ADMIN_EMAIL);
./safe_deploy.sh:85:        if (VIP_WHITELIST.includes(clean)) {
./safe_deploy.sh:87:          user.plan = 'PRO_VIP';
./safe_deploy.sh:88:          user.planLabel = (clean === SUPER_ADMIN_EMAIL) ? 'SUPER ADMIN (Akses Penuh)' : 'GAEKS PRO VIP (Akses Penuh)';
./safe_deploy.sh:104:    return user ? (user.email.toLowerCase().trim() === SUPER_ADMIN_EMAIL) : false;
./safe_deploy.sh:109:    const isVip = VIP_WHITELIST.includes(cleanEmail);
./safe_deploy.sh:110:    const isSuperAdmin = (cleanEmail === SUPER_ADMIN_EMAIL);
./safe_deploy.sh:121:      plan: isVip ? 'PRO_VIP' : 'FREE',
./safe_deploy.sh:122:      planLabel: isVip ? (isSuperAdmin ? 'SUPER ADMIN' : 'GAEKS PRO VIP') : 'Free Tier',
./safe_deploy.sh:123:      loginAt: Date.now()
./safe_deploy.sh:133:  loginWithEmail(email, password, customName = '', targetUrl = '') {
./safe_deploy.sh:135:    const isVip = VIP_WHITELIST.includes(cleanEmail);
./safe_deploy.sh:136:    const isSuperAdmin = (cleanEmail === SUPER_ADMIN_EMAIL);
./safe_deploy.sh:147:      plan: isVip ? 'PRO_VIP' : 'FREE',
./safe_deploy.sh:148:      planLabel: isVip ? (isSuperAdmin ? 'SUPER ADMIN' : 'GAEKS PRO VIP') : 'Free Tier',
./safe_deploy.sh:149:      loginAt: Date.now()
./safe_deploy.sh:159:  logout() {
./safe_deploy.sh:168:      const willBePro = (target.plan !== 'PRO' && target.plan !== 'PRO_VIP');
./safe_deploy.sh:169:      target.plan = willBePro ? 'PRO' : 'FREE';
./safe_deploy.sh:172:        this.sendEmailNotification('purchase', target.email, target.name, { plan_name: 'GAEKS PRO Member' });
./safe_deploy.sh:180:print("1. auth.js updated.")
./safe_deploy.sh:182:# 2. Update login.html (1 Google Button & Clean OTP Verification)
./safe_deploy.sh:183:with open("login.html", "w") as f:
./safe_deploy.sh:195:  <script src="auth.js"></script>
./safe_deploy.sh:248:          <button id="tab-login" onclick="setAuthTab('login')" class="flex-1 py-2 rounded-lg bg-blue-600 text-white transition">
./safe_deploy.sh:257:        <div id="google-auth-wrapper" class="w-full flex justify-center mb-5">
./safe_deploy.sh:283:        <form id="form-login" onsubmit="submitLogin(event)" class="space-y-3.5">
./safe_deploy.sh:286:            <input type="email" id="login-email" required placeholder="nama@email.com" class="w-full px-3.5 py-2.5 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-xl text-white focus:border-blue-500 focus:outline-none transition" />
./safe_deploy.sh:293:            <input type="password" id="login-pass" required placeholder="••••••••" class="w-full px-3.5 py-2.5 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-xl text-white focus:border-blue-500 focus:outline-none transition" />
./safe_deploy.sh:295:          <button type="submit" id="btn-submit-login" class="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs sm:text-sm rounded-xl transition shadow-lg shadow-blue-500/20">
./safe_deploy.sh:372:      const tabL = document.getElementById('tab-login');
./safe_deploy.sh:374:      const formL = document.getElementById('form-login');
./safe_deploy.sh:378:      if (tab === 'login') {
./safe_deploy.sh:408:        const base64Url = response.credential.split('.')[1];
./safe_deploy.sh:430:      const email = document.getElementById('login-email').value.trim();
./safe_deploy.sh:431:      const pass = document.getElementById('login-pass').value.trim();
./safe_deploy.sh:437:      GaeksAuth.loginWithEmail(email, pass, '', dest);
./safe_deploy.sh:458:        const res = await fetch('/api/auth_otp.php', {
./safe_deploy.sh:502:        const res = await fetch('/api/auth_otp.php', {
./safe_deploy.sh:513:            GaeksAuth.loginWithEmail(storedEmail, pass, storedName, dest);
./safe_deploy.sh:535:print("2. login.html updated.")
./safe_deploy.sh:544:        window.location.href = 'login.html?redirect=' + encodeURIComponent(targetUrl);
./safe_deploy.sh:547:idx = idx.replace('href="login.html"', 'href="login.html?redirect=index.html"')
./safe_deploy.sh:556:      var s = localStorage.getItem('gaeks_user_session_v2');
./safe_deploy.sh:558:        window.location.replace('login.html?redirect=cv.html');
./safe_deploy.sh:563:if "window.location.replace('login.html?redirect=cv.html')" not in cv:
./profile.html:7:      try { raw = localStorage.getItem('gaeks_user_session_v3') || localStorage.getItem('gaeks_user_session_v2') || localStorage.getItem('gaeks_user_session'); } catch(e) {}
./profile.html:10:          var m = document.cookie.match(/gaeks_session_v3=([^;]+)/) || document.cookie.match(/gaeks_session=([^;]+)/);
./profile.html:15:        window.location.replace('login.html?redirect=profile.html');
./profile.html:24:  <script src="auth.js?v=20260914_07"></script>
./profile.html:43:        <button onclick="GaeksAuth.logout()" class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-rose-950/40 hover:bg-rose-900/60 border border-rose-900/50 text-rose-300 transition">
./profile.html:67:          ⭐ Upgrade ke GAEKS PRO
./profile.html:69:        <a href="https://wa.me/6285608561745?text=Halo%20Admin%20GAEKS%2C%20saya%20ingin%20tanya%20paket%20langganan%20GAEKS%20PRO" target="_blank" class="text-[11px] text-slate-400 hover:text-emerald-400 text-center font-medium transition">
./profile.html:99:        <h3 class="text-sm font-bold uppercase tracking-wider text-emerald-400">Keunggulan GAEKS PRO</h3>
./profile.html:140:    <p>&copy; 2026 GAEKS DIGITAL PRODUCT. All rights reserved.</p>
./profile.html:147:        window.location.replace('login.html?redirect=profile.html');
./profile.html:154:      document.getElementById('prof-provider').innerText = (user.provider || 'email') + ' authentication';
./profile.html:158:        document.getElementById('prof-badge-plan').innerText = user.planLabel || "GAEKS PRO (Aktif)";
./profile.html:159:        document.getElementById('plan-name-detail').innerText = "GAEKS PRO VIP (Akses Penuh)";
./profile.html:163:            <span>✓ Member PRO VIP Aktif</span>
./run_deploy_fix.py:15:base_cv = re.sub(r"if\s*\(!GaeksAuth\.getCurrentUser\(\)\)\s*\{[^}]*login\.html[^}]*\}", "// Guest mode enabled", base_cv)
./run_deploy_fix.py:85:    // ================= 520+ BANK PROFESI GLOBAL & NASIONAL =================
./run_deploy_fix.py:86:    const BANK_PROFESI_520 = """ + professions_json_escaped + """;
./run_deploy_fix.py:91:        datalist.innerHTML = BANK_PROFESI_520.map(p => '<option value="' + p + '">').join('');
./run_deploy_fix.py:103:      const matches = BANK_PROFESI_520.filter(p => p.toLowerCase().includes(q)).slice(0, 10);
./run_deploy_fix.py:140:      const filtered = BANK_PROFESI_520.filter(p => p.toLowerCase().includes(q));
./run_deploy_fix.py:164:  <!-- MODAL KATALOG 520+ PROFESI -->
./run_deploy_fix.py:351:print("=== SEMUA APLIKASI TELAH DIPERBAIKI & AKTIF DI SERVER PRODUKSI! ===")
./update_500_professions_cv.sh:214:          <!-- FORM 1: PROFIL & KONTAK -->
./update_500_professions_cv.sh:238:            <!-- MULTIPLE CHOICE TARGET ROLES (520+ PROFESI DENGAN LIVE SEARCH & DRAG/DROP) -->
./update_500_professions_cv.sh:259:              <!-- LIVE SEARCH & BANK DATA PROFESI (520+ ITEMS) -->
./update_500_professions_cv.sh:406:    <p>&copy; 2026 GAEKS DIGITAL PRODUCT. Standard ATS Resume Engine.</p>
./update_500_professions_cv.sh:414:    // BANK DATA LENGKAP 526+ PROFESI TERVERIFIKASI
./update_500_professions_cv.sh:683:        sheetExperience: "PROFESSIONAL EXPERIENCE",
./update_500_professions_cv.sh:693:        emptyEducation: "No education credentials added yet.",
./update_500_professions_cv.sh:777:    // GET ALL PROFESSIONS IN FLAT ARRAY
./deploy_auth_and_subscriptions.sh:4:echo "=== 1. Membuat auth.js (Sentral Autentikasi & Whitelist VIP) ==="
./deploy_auth_and_subscriptions.sh:5:cat << 'AUTH_JS' > auth.js
./deploy_auth_and_subscriptions.sh:7:const VIP_WHITELIST = [
./deploy_auth_and_subscriptions.sh:13:const AUTH_STORAGE_KEY = 'gaeks_user_session_v1';
./deploy_auth_and_subscriptions.sh:21:      if (user && user.email && VIP_WHITELIST.includes(user.email.toLowerCase().trim())) {
./deploy_auth_and_subscriptions.sh:23:        user.plan = 'PRO_VIP';
./deploy_auth_and_subscriptions.sh:24:        user.planLabel = 'GAEKS PRO VIP (Akses Penuh)';
./deploy_auth_and_subscriptions.sh:38:  loginWithEmail(email, password, name = '') {
./deploy_auth_and_subscriptions.sh:40:    const isVip = VIP_WHITELIST.includes(cleanEmail);
./deploy_auth_and_subscriptions.sh:50:      plan: isVip ? 'PRO_VIP' : 'FREE',
./deploy_auth_and_subscriptions.sh:51:      planLabel: isVip ? 'GAEKS PRO VIP (Akses Penuh)' : 'Free Tier',
./deploy_auth_and_subscriptions.sh:52:      loginAt: Date.now()
./deploy_auth_and_subscriptions.sh:59:  loginWithGoogle(emailInput = '') {
./deploy_auth_and_subscriptions.sh:63:    const isVip = VIP_WHITELIST.includes(cleanEmail);
./deploy_auth_and_subscriptions.sh:73:      plan: isVip ? 'PRO_VIP' : 'FREE',
./deploy_auth_and_subscriptions.sh:74:      planLabel: isVip ? 'GAEKS PRO VIP (Akses Penuh)' : 'Free Tier',
./deploy_auth_and_subscriptions.sh:75:      loginAt: Date.now()
./deploy_auth_and_subscriptions.sh:82:  logout() {
./deploy_auth_and_subscriptions.sh:90:cat << 'PROFILE_HTML' > profile.html
./deploy_auth_and_subscriptions.sh:99:  <script src="auth.js"></script>
./deploy_auth_and_subscriptions.sh:118:        <button onclick="GaeksAuth.logout()" class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-rose-950/40 hover:bg-rose-900/60 border border-rose-900/50 text-rose-300 transition">
./deploy_auth_and_subscriptions.sh:141:          ⭐ Upgrade ke GAEKS PRO
./deploy_auth_and_subscriptions.sh:143:        <a href="https://wa.me/6285608561745?text=Halo%20Admin%20GAEKS%2C%20saya%20ingin%20tanya%20paket%20langganan%20GAEKS%20PRO" target="_blank" class="text-[11px] text-slate-400 hover:text-emerald-400 text-center font-medium transition">
./deploy_auth_and_subscriptions.sh:172:        <h3 class="text-sm font-bold uppercase tracking-wider text-emerald-400">Keunggulan GAEKS PRO</h3>
./deploy_auth_and_subscriptions.sh:206:    <p>&copy; 2026 GAEKS DIGITAL PRODUCT. Standard ATS Resume Engine.</p>
./deploy_auth_and_subscriptions.sh:221:      document.getElementById('prof-provider').innerText = (user.provider || 'email') + ' authentication';
./deploy_auth_and_subscriptions.sh:225:        document.getElementById('prof-badge-plan').innerText = user.planLabel || "GAEKS PRO (Aktif)";
./deploy_auth_and_subscriptions.sh:226:        document.getElementById('plan-name-detail').innerText = "GAEKS PRO VIP (Akses Penuh)";
./deploy_auth_and_subscriptions.sh:230:            <span>✓ Member PRO VIP Aktif</span>
./deploy_auth_and_subscriptions.sh:242:PROFILE_HTML
./deploy_auth_and_subscriptions.sh:254:  <script src="auth.js"></script>
./deploy_auth_and_subscriptions.sh:315:      <!-- PRO TIER -->
./deploy_auth_and_subscriptions.sh:323:            <h3 class="text-lg font-bold text-white">GAEKS PRO Member</h3>
./deploy_auth_and_subscriptions.sh:342:          <a href="https://wa.me/6285608561745?text=Halo%20Admin%20GAEKS%2C%20saya%20ingin%20upgrade%20ke%20GAEKS%20PRO%20Rp49.000%2Fbulan" target="_blank" class="block w-full py-3 text-center text-xs font-bold rounded-xl bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-500/30 transition">
./deploy_auth_and_subscriptions.sh:343:            💬 Upgrade ke GAEKS PRO Sekarang
./deploy_auth_and_subscriptions.sh:351:    <p>&copy; 2026 GAEKS DIGITAL PRODUCT. Standard ATS Resume Engine.</p>
./deploy_auth_and_subscriptions.sh:358:git add auth.js profile.html pricing.html cv.html
./deploy_auth_and_subscriptions.sh:359:git commit -m "feat: complete auth module, sanitized generic hints, profile and subscription pages with VIP PRO unlock" || true
./update_deny_triawan_full_cv.sh:204:        <!-- FORM 1: PROFIL -->
./update_deny_triawan_full_cv.sh:336:    <p>&copy; 2026 GAEKS DIGITAL PRODUCT. Standard ATS Resume Engine.</p>
./update_deny_triawan_full_cv.sh:1195:            <!-- CONTACT STRIP DENGAN IKON PROFESIONAL -->
./update_deny_triawan_full_cv.sh:1277:git commit -m "feat: adopt 100% authentic Deny Triawan Europass data with 4 distinct ATS layout architectures"
./update_cv_pdf_fix.sh:223:          <!-- FORM 1: PROFIL & KONTAK -->
./update_cv_pdf_fix.sh:367:    <p>&copy; 2026 GAEKS DIGITAL PRODUCT. Standard ATS Resume Engine.</p>
./update_cv_pdf_fix.sh:480:        sheetExperience: "PROFESSIONAL EXPERIENCE & TRACK RECORD",
./update_cv_pdf_fix.sh:490:        emptyEducation: "No education credentials added yet.",
./fix_mail_test.sh:41:    $authRes = $read($socket);
./fix_mail_test.sh:43:    if (substr($authRes, 0, 3) != "235") {
./fix_mail_test.sh:45:        return ["status" => "error", "message" => "Autentikasi SMTP Gagal: $authRes"];
./fix_mail_test.sh:90:            <h2 style='color:#ffffff;margin:0;font-size:20px;'>GAEKS DIGITAL PRODUCTS</h2>
./editor.html:49:    /* 6. Emerald Horizon (PRO) */
./editor.html:55:    /* 7. Crimson Elegance (PRO) */
./editor.html:61:    /* 8. Obsidian Minimal (PRO) */
./editor.html:67:    /* 9. Oxford Two-Tone (PRO) */
./editor.html:73:    /* 10. Swiss Editorial (PRO) */
./editor.html:79:    /* 11. Imperial Gold (PRO) */
./editor.html:85:    /* 12. Azure Blue (PRO) */
./editor.html:91:    /* 13. Metropolitan Boxed (PRO) */
./editor.html:97:    /* 14. Boutique Creative (PRO) */
./editor.html:103:    /* 15. Apex Monolith (PRO) */
./editor.html:183:        <div id="nav-auth-container" class="flex items-center">
./editor.html:184:          <a href="login.html" id="btn-open-login" class="px-3.5 py-1.5 text-xs font-bold rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-200 transition flex items-center gap-1.5">
./editor.html:240:            <optgroup label="10 Tema Berbayar (GAEKS PRO 🔒)">
./editor.html:241:              <option value="emerald-horizon">6. Emerald Horizon (PRO 🔒)</option>
./editor.html:242:              <option value="crimson-elegance">7. Crimson Elegance (PRO 🔒)</option>
./editor.html:243:              <option value="obsidian-minimal">8. Obsidian Minimal (PRO 🔒)</option>
./editor.html:244:              <option value="oxford-navy">9. Oxford Two-Tone (PRO 🔒)</option>
./editor.html:245:              <option value="swiss-editorial">10. Swiss Editorial (PRO 🔒)</option>
./editor.html:246:              <option value="imperial-gold">11. Imperial Gold (PRO 🔒)</option>
./editor.html:247:              <option value="azure-sky">12. Azure Blue (PRO 🔒)</option>
./editor.html:248:              <option value="metro-corporate">13. Metropolitan Boxed (PRO 🔒)</option>
./editor.html:249:              <option value="boutique-creative">14. Boutique Creative (PRO 🔒)</option>
./editor.html:250:              <option value="apex-monolith">15. Apex Monolith (PRO 🔒)</option>
./editor.html:274:          <!-- FORM 1: PROFIL & KONTAK -->
./editor.html:298:            <!-- TARGET ROLES (520+ PROFESI DENGAN LIVE SEARCH & DRAG/DROP) -->
./login.html:12:  <script src="auth.js?v=20260914_07"></script>
./login.html:69:          <button type="button" id="tab-login" onclick="setAuthTab('login')" class="flex-1 py-2.5 rounded-lg bg-blue-600 text-white transition cursor-pointer">
./login.html:78:        <div id="google-auth-wrapper" class="w-full flex justify-center mb-5">
./login.html:104:        <form id="form-login" onsubmit="submitLogin(event)" class="space-y-3.5">
./login.html:107:            <input type="email" id="login-email" required placeholder="nama@email.com" class="w-full px-3.5 py-2.5 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-xl text-white focus:border-blue-500 focus:outline-none transition" />
./login.html:114:            <input type="password" id="login-pass" required placeholder="••••••••" class="w-full px-3.5 py-2.5 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-xl text-white focus:border-blue-500 focus:outline-none transition" />
./login.html:116:          <button type="submit" id="btn-submit-login" class="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs sm:text-sm rounded-xl transition shadow-lg shadow-blue-500/20 cursor-pointer">
./login.html:203:      const tabL = document.getElementById('tab-login');
./login.html:205:      const formL = document.getElementById('form-login');
./login.html:209:      if (tab === 'login') {
./login.html:256:        plan: isVip ? 'PRO_VIP' : 'FREE',
./login.html:257:        planLabel: isVip ? (isSuperAdmin ? 'SUPER ADMIN' : 'GAEKS PRO VIP') : 'Free Tier',
./login.html:258:        loginAt: Date.now()
./login.html:262:        localStorage.setItem('gaeks_user_session_v3', JSON.stringify(user));
./login.html:266:        document.cookie = "gaeks_session_v3=" + encodeURIComponent(JSON.stringify(user)) + "; path=/; max-age=2592000; SameSite=Lax";
./login.html:287:        const base64Url = response.credential.split('.')[1];
./login.html:307:      const email = document.getElementById('login-email').value.trim();
./login.html:308:      const pass = document.getElementById('login-pass').value.trim();
./login.html:337:            setAuthTab('login');
./login.html:338:            document.getElementById('login-email').value = email;
./login.html:339:            document.getElementById('login-pass').focus();
./login.html:350:        const res = await fetch('/api/auth_otp.php', {
./login.html:367:            setAuthTab('login');
./login.html:368:            document.getElementById('login-email').value = email;
./login.html:369:            document.getElementById('login-pass').focus();
./login.html:401:        const res = await fetch('/api/auth_otp.php', {
./api/presentation.php:15:    echo json_encode(["status" => "error", "message" => "Unauthorized: Sesi tidak valid atau telah berakhir."]);
./api/presentation.php:19:$authUserId = $user['id'];
./api/presentation.php:29:        $stmt->execute([':uid' => $authUserId]);
./api/presentation.php:39:        foreach ($store[$authUserId] ?? [] as $p) {
./api/presentation.php:62:            if ($ownerRow['user_id'] !== $authUserId) {
./api/presentation.php:68:            $stmt->execute([':id' => $id, ':uid' => $authUserId]);
./api/presentation.php:81:            if ($otherUid !== $authUserId) {
./api/presentation.php:91:        foreach ($store[$authUserId] ?? [] as $p) {
./api/presentation.php:114:        if ($existing && $existing['user_id'] !== $authUserId) {
./api/presentation.php:121:            $updateStmt->execute([':name' => $name, ':date' => $date, ':status' => $status, ':data' => $dataJson, ':now' => $now, ':id' => $id, ':uid' => $authUserId]);
./api/presentation.php:124:            $insertStmt->execute([':id' => $id, ':uid' => $authUserId, ':name' => $name, ':date' => $date, ':status' => $status, ':data' => $dataJson, ':created' => $now, ':updated' => $now]);
./api/presentation.php:129:            if ($otherUid !== $authUserId) {
./api/presentation.php:139:        if (!isset($store[$authUserId])) $store[$authUserId] = [];
./api/presentation.php:141:        foreach ($store[$authUserId] as $i => $p) { if ($p['id'] === $id) { $idx = $i; break; } }
./api/presentation.php:143:        if ($idx >= 0) $store[$authUserId][$idx] = $pres;
./api/presentation.php:144:        else array_unshift($store[$authUserId], $pres);
./api/presentation.php:159:        if ($existing && $existing['user_id'] !== $authUserId) {
./api/presentation.php:166:            $stmt->execute([':id' => $id, ':uid' => $authUserId]);
./api/presentation.php:170:            $stmt->execute([':status' => $status, ':del' => $delAt, ':now' => $now, ':id' => $id, ':uid' => $authUserId]);
./api/presentation.php:174:        if (isset($store[$authUserId])) {
./api/presentation.php:176:                $store[$authUserId] = array_values(array_filter($store[$authUserId], fn($p) => $p['id'] !== $id));
./api/presentation.php:178:                foreach ($store[$authUserId] as &$p) {
./api/mailer.php:36:    $authRes = $read($socket);
./api/mailer.php:38:    if (substr($authRes, 0, 3) != "235") {
./api/mailer.php:40:        return ["status" => "error", "message" => "Autentikasi SMTP Gagal: $authRes"];
./api/mailer.php:85:            <h2 style='color:#ffffff;margin:0;font-size:20px;'>GAEKS DIGITAL PRODUCTS</h2>
./api/test_mail.php:20:        <h2 style='color:#ffffff;margin:0;'>GAEKS DIGITAL PRODUCTS</h2>
./api/test_mail.php:50:    $authRes = $read($socket);
./api/test_mail.php:52:    if (substr($authRes, 0, 3) != "235") {
./api/test_mail.php:54:        echo json_encode(["status" => "error", "message" => "Autentikasi SMTP Gagal: $authRes. Periksa kata sandi."]);
./api/cv.php:15:    echo json_encode(["status" => "error", "message" => "Unauthorized: Sesi tidak valid atau telah berakhir."]);
./api/cv.php:19:$authUserId = $user['id'];
./api/cv.php:35:        $stmt->execute([':uid' => $authUserId]);
./api/cv.php:49:        $userCvs = $store[$authUserId] ?? [];
./api/cv.php:70:            if ($ownerRow['user_id'] !== $authUserId) {
./api/cv.php:76:            $stmt->execute([':id' => $id, ':uid' => $authUserId]);
./api/cv.php:91:            if ($otherUid !== $authUserId) {
./api/cv.php:101:        foreach ($store[$authUserId] ?? [] as $c) {
./api/cv.php:128:        if ($existing && $existing['user_id'] !== $authUserId) {
./api/cv.php:135:            $updateStmt->execute([':title' => $title, ':draft' => $isDraft, ':comp' => $completeness, ':data' => $dataJson, ':now' => $now, ':id' => $id, ':uid' => $authUserId]);
./api/cv.php:138:            $insertStmt->execute([':id' => $id, ':uid' => $authUserId, ':title' => $title, ':draft' => $isDraft, ':comp' => $completeness, ':data' => $dataJson, ':created' => $now, ':updated' => $now]);
./api/cv.php:143:            if ($otherUid !== $authUserId) {
./api/cv.php:153:        if (!isset($store[$authUserId])) $store[$authUserId] = [];
./api/cv.php:155:        foreach ($store[$authUserId] as $i => $c) { if ($c['id'] === $id) { $idx = $i; break; } }
./api/cv.php:157:        if ($idx >= 0) $store[$authUserId][$idx] = $savedObj;
./api/cv.php:158:        else array_unshift($store[$authUserId], $savedObj);
./api/cv.php:174:        if ($existing && $existing['user_id'] !== $authUserId) {
./api/cv.php:180:        $stmt->execute([':del' => $now, ':now' => $now, ':id' => $id, ':uid' => $authUserId]);
./api/cv.php:183:        if (isset($store[$authUserId])) {
./api/cv.php:184:            foreach ($store[$authUserId] as &$c) { if ($c['id'] === $id) { $c['deletedAt'] = $now; break; } }
./api/cv.php:199:        if ($existing && $existing['user_id'] !== $authUserId) {
./api/cv.php:205:        $stmt->execute([':now' => $now, ':id' => $id, ':uid' => $authUserId]);
./api/cv.php:208:        if (isset($store[$authUserId])) {
./api/cv.php:209:            foreach ($store[$authUserId] as &$c) { if ($c['id'] === $id) { $c['deletedAt'] = null; break; } }
./api/cv.php:223:        if ($existing && $existing['user_id'] !== $authUserId) {
./api/cv.php:229:        $stmt->execute([':id' => $id, ':uid' => $authUserId]);
./api/cv.php:232:        if (isset($store[$authUserId])) {
./api/cv.php:233:            $store[$authUserId] = array_values(array_filter($store[$authUserId], fn($c) => $c['id'] !== $id));
./api/send_welcome_email.php:41:      <h2 style='margin:0;'>GAEKS DIGITAL PRODUCTS</h2>
./api/send_welcome_email.php:50:      <p>Jika ada pertanyaan atau membutuhkan bantuan seputar akun atau paket PRO, silakan hubungi tim kami via WhatsApp di <a href='https://wa.me/6285608561745'>+62 856-0856-1745</a>.</p>
./api/db.php:37:    elseif (!empty($_COOKIE['gaeks_session_v3'])) $uJson = $_COOKIE['gaeks_session_v3'];
./api/db.php:38:    elseif (!empty($_COOKIE['gaeks_session'])) $uJson = $_COOKIE['gaeks_session'];
./update_prestige_perfect_cv.sh:224:          <!-- FORM 1: PROFIL & KONTAK -->
./update_prestige_perfect_cv.sh:369:    <p>&copy; 2026 GAEKS DIGITAL PRODUCT. Standard ATS Resume Engine.</p>
./update_prestige_perfect_cv.sh:481:        sheetExperience: "PROFESSIONAL EXPERIENCE",
./update_prestige_perfect_cv.sh:491:        emptyEducation: "No education credentials added yet.",
./setup_auth_and_ecosystem.py:3:print("=== 1. Menulis auth.js (Session, Whitelist VIP & User Database) ===")
./setup_auth_and_ecosystem.py:4:with open("auth.js", "w") as f:
./setup_auth_and_ecosystem.py:6:const VIP_WHITELIST = [
./setup_auth_and_ecosystem.py:11:const SUPER_ADMIN_EMAIL = "gaeks.group@gmail.com";
./setup_auth_and_ecosystem.py:13:const AUTH_STORAGE_KEY = 'gaeks_user_session_v2';
./setup_auth_and_ecosystem.py:21:        { id: 'usr_adm_1', email: 'gaeks.group@gmail.com', name: 'GAEKS Group (Admin)', provider: 'google', plan: 'PRO_VIP', registeredAt: Date.now() - 86400000 * 5, lastLoginAt: Date.now() },
./setup_auth_and_ecosystem.py:22:        { id: 'usr_vip_2', email: 'triawan25@gmail.com', name: 'Deny Triawan', provider: 'google', plan: 'PRO_VIP', registeredAt: Date.now() - 86400000 * 4, lastLoginAt: Date.now() },
./setup_auth_and_ecosystem.py:23:        { id: 'usr_vip_3', email: 'ranesath@gmail.com', name: 'Ranesath', provider: 'google', plan: 'PRO_VIP', registeredAt: Date.now() - 86400000 * 3, lastLoginAt: Date.now() }
./setup_auth_and_ecosystem.py:73:        user.isAdmin = (clean === SUPER_ADMIN_EMAIL);
./setup_auth_and_ecosystem.py:74:        if (VIP_WHITELIST.includes(clean)) {
./setup_auth_and_ecosystem.py:76:          user.plan = 'PRO_VIP';
./setup_auth_and_ecosystem.py:77:          user.planLabel = (clean === SUPER_ADMIN_EMAIL) ? 'SUPER ADMIN (Akses Penuh)' : 'GAEKS PRO VIP (Akses Penuh)';
./setup_auth_and_ecosystem.py:93:    return user ? (user.email.toLowerCase().trim() === SUPER_ADMIN_EMAIL) : false;
./setup_auth_and_ecosystem.py:96:  loginWithEmail(email, password, name = '') {
./setup_auth_and_ecosystem.py:98:    const isVip = VIP_WHITELIST.includes(cleanEmail);
./setup_auth_and_ecosystem.py:108:      isAdmin: (cleanEmail === SUPER_ADMIN_EMAIL),
./setup_auth_and_ecosystem.py:109:      plan: isVip ? 'PRO_VIP' : 'FREE',
./setup_auth_and_ecosystem.py:110:      planLabel: isVip ? (cleanEmail === SUPER_ADMIN_EMAIL ? 'SUPER ADMIN' : 'GAEKS PRO VIP') : 'Free Tier',
./setup_auth_and_ecosystem.py:111:      loginAt: Date.now()
./setup_auth_and_ecosystem.py:119:  loginWithGoogle(emailInput = '') {
./setup_auth_and_ecosystem.py:123:    const isVip = VIP_WHITELIST.includes(cleanEmail);
./setup_auth_and_ecosystem.py:133:      isAdmin: (cleanEmail === SUPER_ADMIN_EMAIL),
./setup_auth_and_ecosystem.py:134:      plan: isVip ? 'PRO_VIP' : 'FREE',
./setup_auth_and_ecosystem.py:135:      planLabel: isVip ? (cleanEmail === SUPER_ADMIN_EMAIL ? 'SUPER ADMIN' : 'GAEKS PRO VIP') : 'Free Tier',
./setup_auth_and_ecosystem.py:136:      loginAt: Date.now()
./setup_auth_and_ecosystem.py:144:  logout() {
./setup_auth_and_ecosystem.py:153:      target.plan = (target.plan === 'PRO' || target.plan === 'PRO_VIP') ? 'FREE' : 'PRO';
./setup_auth_and_ecosystem.py:205:      <h2 style='margin:0;'>GAEKS DIGITAL PRODUCTS</h2>
./setup_auth_and_ecosystem.py:214:      <p>Jika ada pertanyaan atau membutuhkan bantuan seputar akun atau paket PRO, silakan hubungi tim kami via WhatsApp di <a href='https://wa.me/6285608561745'>+62 856-0856-1745</a>.</p>
./setup_auth_and_ecosystem.py:240:# Generate complete index.html with authentication and admin user view
./setup_auth_and_ecosystem.py:252:  <script src="auth.js"></script>
./setup_auth_and_ecosystem.py:276:        <button id="nav-btn-admin" onclick="openAdminModal()" class="hidden px-2.5 py-1.5 text-[11px] font-bold rounded-lg bg-amber-950/60 border border-amber-600 text-amber-300 hover:bg-amber-900 transition flex items-center gap-1">
./setup_auth_and_ecosystem.py:288:        <button id="nav-btn-login" onclick="openAuthModal()" class="px-4 py-2 text-xs font-bold rounded-xl bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-500/20 transition flex items-center gap-1.5">
./setup_auth_and_ecosystem.py:375:  <div id="auth-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
./setup_auth_and_ecosystem.py:385:      <button onclick="loginGoogle()" class="w-full py-2.5 px-4 bg-white hover:bg-slate-100 text-slate-900 font-bold text-xs rounded-xl flex items-center justify-center gap-2.5 transition shadow-md">
./setup_auth_and_ecosystem.py:397:          <input type="text" id="auth-name" placeholder="Alexander Pratama" class="w-full px-3 py-2 text-xs bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" />
./setup_auth_and_ecosystem.py:401:          <input type="email" id="auth-email" required placeholder="nama@email.com" class="w-full px-3 py-2 text-xs bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" />
./setup_auth_and_ecosystem.py:405:          <input type="password" id="auth-pass" required placeholder="••••••••" class="w-full px-3 py-2 text-xs bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" />
./setup_auth_and_ecosystem.py:413:        <span class="text-[10px] text-slate-400 font-bold block">Akses Pengujian Cepat (Admin & VIP):</span>
./setup_auth_and_ecosystem.py:416:          <button type="button" onclick="quickLogin('triawan25@gmail.com', 'Deny Triawan')" class="px-2 py-0.5 rounded text-[10px] bg-blue-950/80 text-blue-300 border border-blue-800 hover:bg-blue-900 transition">⭐ triawan25@gmail.com (VIP)</button>
./setup_auth_and_ecosystem.py:417:          <button type="button" onclick="quickLogin('ranesath@gmail.com', 'Ranesath')" class="px-2 py-0.5 rounded text-[10px] bg-blue-950/80 text-blue-300 border border-blue-800 hover:bg-blue-900 transition">⭐ ranesath@gmail.com (VIP)</button>
./setup_auth_and_ecosystem.py:424:  <div id="admin-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/85 backdrop-blur-sm">
./setup_auth_and_ecosystem.py:430:            <span id="admin-user-count" class="px-2 py-0.5 text-xs rounded-full bg-blue-950 text-blue-300 border border-blue-800">0 User</span>
./setup_auth_and_ecosystem.py:437:      <input type="text" id="admin-search-user" oninput="filterAdminUsers(this.value)" placeholder="🔍 Cari email atau nama pengguna..." class="w-full px-3 py-1.5 text-xs bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" />
./setup_auth_and_ecosystem.py:450:          <tbody id="admin-user-table-body" class="divide-y divide-slate-800/80 text-slate-300"></tbody>
./setup_auth_and_ecosystem.py:464:    <p>&copy; 2026 GAEKS DIGITAL PRODUCT. All rights reserved.</p>
./setup_auth_and_ecosystem.py:481:      document.getElementById('auth-modal').classList.remove('hidden');
./setup_auth_and_ecosystem.py:485:      document.getElementById('auth-modal').classList.add('hidden');
./setup_auth_and_ecosystem.py:488:    function loginGoogle() {
./setup_auth_and_ecosystem.py:489:      GaeksAuth.loginWithGoogle();
./setup_auth_and_ecosystem.py:495:      const email = document.getElementById('auth-email').value;
./setup_auth_and_ecosystem.py:496:      const pass = document.getElementById('auth-pass').value;
./setup_auth_and_ecosystem.py:497:      const name = document.getElementById('auth-name').value;
./setup_auth_and_ecosystem.py:498:      GaeksAuth.loginWithEmail(email, pass, name);
./setup_auth_and_ecosystem.py:503:      GaeksAuth.loginWithEmail(email, 'password123', name);
./setup_auth_and_ecosystem.py:509:      const btnLogin = document.getElementById('nav-btn-login');
./setup_auth_and_ecosystem.py:511:      const adminBtn = document.getElementById('nav-btn-admin');
./setup_auth_and_ecosystem.py:523:          adminBtn.classList.remove('hidden');
./setup_auth_and_ecosystem.py:526:          badge.innerText = "PRO VIP";
./setup_auth_and_ecosystem.py:534:        adminBtn.classList.add('hidden');
./setup_auth_and_ecosystem.py:540:      document.getElementById('admin-modal').classList.remove('hidden');
./setup_auth_and_ecosystem.py:544:      document.getElementById('admin-modal').classList.add('hidden');
./setup_auth_and_ecosystem.py:549:      const tbody = document.getElementById('admin-user-table-body');
./setup_auth_and_ecosystem.py:558:      document.getElementById('admin-user-count').innerText = `${filtered.length} Pengguna`;
./setup_auth_and_ecosystem.py:567:        const isPro = (u.plan === 'PRO' || u.plan === 'PRO_VIP');
./setup_auth_and_ecosystem.py:584:                ${isPro ? 'Ubah ke Free' : 'Jadikan PRO'}
./update_ats_cv_pro.sh:142:          <span>Burgundy</span> <span class="text-[9px] text-amber-400">PRO 🔒</span>
./update_ats_cv_pro.sh:145:          <span>Nordic Teal</span> <span class="text-[9px] text-amber-400">PRO 🔒</span>
./update_ats_cv_pro.sh:172:        <!-- TAB 1: PROFIL & KONTAK -->
./update_ats_cv_pro.sh:396:  <!-- MODAL UPGRADE PRO -->
./update_ats_cv_pro.sh:402:      <h3 class="text-xl font-bold text-white tracking-tight">Tema Eksklusif PRO</h3>
./update_ats_cv_pro.sh:404:        Buka akses ke tema premium ini dengan paket langganan PRO GAEKS Digital Product.
./update_ats_cv_pro.sh:410:        <a href="https://wa.me/?text=Halo%20Admin%20Gaeks,%20saya%20ingin%20upgrade%20ke%20paket%20PRO" target="_blank" class="w-1/2 py-2.5 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 text-xs font-bold transition flex items-center justify-center">
./update_ats_cv_pro.sh:418:    <p>&copy; 2026 GAEKS DIGITAL PRODUCT. Standar Format ATS Internasional.</p>
./update_ats_cv_pro.sh:555:      document.getElementById('proModalDesc').innerText = `Tema "${name}" terkunci. Dapatkan akses ke semua tema eksekutif dengan langganan PRO GAEKS.`;
./update_cv_themes.sh:4:echo "=== Memperbarui cv.html dengan Desain Modern, Pemilih Tema & Lock PRO ==="
./update_cv_themes.sh:129:        <!-- TEMA TERKUNCI (PRO) -->
./update_cv_themes.sh:133:          <span class="text-[10px] bg-amber-500/20 text-amber-400 px-1.5 py-0.2 rounded font-bold">PRO 🔒</span>
./update_cv_themes.sh:138:          <span class="text-[10px] bg-amber-500/20 text-amber-400 px-1.5 py-0.2 rounded font-bold">PRO 🔒</span>
./update_cv_themes.sh:143:          <span class="text-[10px] bg-amber-500/20 text-amber-400 px-1.5 py-0.2 rounded font-bold">PRO 🔒</span>
./update_cv_themes.sh:366:  <!-- MODAL PRO / LOCK UPGRADE -->
./update_cv_themes.sh:372:      <h3 class="text-xl font-bold text-white tracking-tight">Fitur Eksklusif PRO</h3>
./update_cv_themes.sh:393:        <a href="https://wa.me/?text=Halo%20Admin%20Gaeks,%20saya%20ingin%20berlangganan%20paket%20PRO%20GAEKS%20Digital%20Product" target="_blank" class="w-1/2 py-2.5 rounded-lg bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 text-xs font-bold transition flex items-center justify-center">
./update_cv_themes.sh:394:          Upgrade ke PRO
./update_cv_themes.sh:401:    <p>&copy; 2026 GAEKS DIGITAL PRODUCT. Standar Format ATS Internasional.</p>
./update_cv_themes.sh:700:git commit -m "feat: implement stable photo layout, distinctive badges, 3 free themes and PRO lock modal"
./deploy_redirect_fix.sh:4:echo "=== 1. Memperbarui login.html (Satu Tombol Google & Pengalihan Cerdas) ==="
./deploy_redirect_fix.sh:5:cat << 'EOF_LOGIN' > login.html
./deploy_redirect_fix.sh:17:  <script src="auth.js"></script>
./deploy_redirect_fix.sh:70:          <button id="tab-login" onclick="setAuthTab('login')" class="flex-1 py-2 rounded-lg bg-blue-600 text-white transition">
./deploy_redirect_fix.sh:79:        <div id="google-auth-wrapper" class="w-full flex justify-center mb-5">
./deploy_redirect_fix.sh:105:        <form id="form-login" onsubmit="submitLogin(event)" class="space-y-3.5">
./deploy_redirect_fix.sh:108:            <input type="email" id="login-email" required placeholder="nama@email.com" class="w-full px-3.5 py-2.5 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-xl text-white focus:border-blue-500 focus:outline-none transition" />
./deploy_redirect_fix.sh:115:            <input type="password" id="login-pass" required placeholder="••••••••" class="w-full px-3.5 py-2.5 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-xl text-white focus:border-blue-500 focus:outline-none transition" />
./deploy_redirect_fix.sh:117:          <button type="submit" id="btn-submit-login" class="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs sm:text-sm rounded-xl transition shadow-lg shadow-blue-500/20">
./deploy_redirect_fix.sh:194:      const tabL = document.getElementById('tab-login');
./deploy_redirect_fix.sh:196:      const formL = document.getElementById('form-login');
./deploy_redirect_fix.sh:200:      if (tab === 'login') {
./deploy_redirect_fix.sh:231:        const base64Url = response.credential.split('.')[1];
./deploy_redirect_fix.sh:253:      const email = document.getElementById('login-email').value.trim();
./deploy_redirect_fix.sh:254:      const pass = document.getElementById('login-pass').value.trim();
./deploy_redirect_fix.sh:260:      GaeksAuth.loginWithEmail(email, pass, '', dest);
./deploy_redirect_fix.sh:281:        const res = await fetch('/api/auth_otp.php', {
./deploy_redirect_fix.sh:325:        const res = await fetch('/api/auth_otp.php', {
./deploy_redirect_fix.sh:336:            GaeksAuth.loginWithEmail(storedEmail, pass, storedName, dest);
./deploy_redirect_fix.sh:359:echo "=== 2. Memperbarui auth.js dengan Parameter Pengalihan Dinamis ==="
./deploy_redirect_fix.sh:360:cat << 'EOF_AUTH' > auth.js
./deploy_redirect_fix.sh:362:const VIP_WHITELIST = [
./deploy_redirect_fix.sh:367:const SUPER_ADMIN_EMAIL = "gaeks.group@gmail.com";
./deploy_redirect_fix.sh:370:const AUTH_STORAGE_KEY = 'gaeks_user_session_v2';
./deploy_redirect_fix.sh:378:        { id: 'usr_adm_1', email: 'gaeks.group@gmail.com', name: 'GAEKS Group (Admin)', provider: 'google', plan: 'PRO_VIP', registeredAt: Date.now() - 86400000 * 5, lastLoginAt: Date.now() },
./deploy_redirect_fix.sh:379:        { id: 'usr_vip_2', email: 'triawan25@gmail.com', name: 'Deny Triawan', provider: 'google', plan: 'PRO_VIP', registeredAt: Date.now() - 86400000 * 4, lastLoginAt: Date.now() },
./deploy_redirect_fix.sh:380:        { id: 'usr_vip_3', email: 'ranesath@gmail.com', name: 'Ranesath', provider: 'google', plan: 'PRO_VIP', registeredAt: Date.now() - 86400000 * 3, lastLoginAt: Date.now() }
./deploy_redirect_fix.sh:435:        user.isAdmin = (clean === SUPER_ADMIN_EMAIL);
./deploy_redirect_fix.sh:436:        if (VIP_WHITELIST.includes(clean)) {
./deploy_redirect_fix.sh:438:          user.plan = 'PRO_VIP';
./deploy_redirect_fix.sh:439:          user.planLabel = (clean === SUPER_ADMIN_EMAIL) ? 'SUPER ADMIN (Akses Penuh)' : 'GAEKS PRO VIP (Akses Penuh)';
./deploy_redirect_fix.sh:455:    return user ? (user.email.toLowerCase().trim() === SUPER_ADMIN_EMAIL) : false;
./deploy_redirect_fix.sh:460:    const isVip = VIP_WHITELIST.includes(cleanEmail);
./deploy_redirect_fix.sh:461:    const isSuperAdmin = (cleanEmail === SUPER_ADMIN_EMAIL);
./deploy_redirect_fix.sh:472:      plan: isVip ? 'PRO_VIP' : 'FREE',
./deploy_redirect_fix.sh:473:      planLabel: isVip ? (isSuperAdmin ? 'SUPER ADMIN' : 'GAEKS PRO VIP') : 'Free Tier',
./deploy_redirect_fix.sh:474:      loginAt: Date.now()
./deploy_redirect_fix.sh:480:    const dest = targetUrl || new URLSearchParams(window.location.search).get('redirect') || (window.location.pathname.includes('login.html') ? 'cv.html' : '');
./deploy_redirect_fix.sh:488:  loginWithEmail(email, password, customName = '', targetUrl = '') {
```

## Storage Evidence
```text
./auth.js
./cv-dashboard.html
./cv.html
./deploy_auth_and_subscriptions.sh
./deploy_codespaces.py
./deploy_login_and_otp.sh
./deploy_redirect_fix.sh
./index.html
./login.html
./presentation.html
./profile.html
./safe_deploy.sh
./setup_auth_and_ecosystem.py
./update_15_themes_and_clean_sample.sh
./update_500_professions_cv.sh
./update_ats_cv_ultimate.sh
./update_blank_cv_and_clean_contact.sh
./update_credentials_and_push.sh
./update_cv_dashboard.sh
./update_cv_pdf_fix.sh
./update_cv_sample_deny.sh
./update_deny_triawan_full_cv.sh
./update_executive_density_cv.sh
./update_full_architecture_cv.sh
./update_modern_ats_cv.sh
./update_prestige_perfect_cv.sh
./update_standardized_cv.sh
./update_target_roles_and_clean_cv.sh
./update_universal_ats_cv.sh
./upgrade_pro_cv.sh
```

## Initial Risk Categories
- Critical/High candidates must be verified against actual implementation before remediation.
- Client-side identity or privilege decisions must not be treated as authoritative.
- User-owned CV/Presentation records require server-side ownership checks.
- Uploads require server-side validation and safe storage.
- Cookies/sessions require secure production attributes.
- Never log or expose secrets.

## Remediation Order
1. Authentication/session authority
2. Server-side authorization
3. Document ownership
4. Upload validation
5. XSS/CSRF/injection hardening
6. Security regression testing
