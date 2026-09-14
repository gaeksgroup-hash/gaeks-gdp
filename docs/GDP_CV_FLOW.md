# GDP CV Maker Flow

## Detected CV Files
```text
./api/cv.php
./cv-dashboard.html
./cv.html
./docs/GDP_CV_FLOW.md
./fix_cv_now.py
./setup_cv_page.sh
./update_500_professions_cv.sh
./update_ats_cv_pro.sh
./update_ats_cv_ultimate.sh
./update_blank_cv_and_clean_contact.sh
./update_cv_dashboard.sh
./update_cv_maker.sh
./update_cv_pdf_fix.sh
./update_cv_sample_deny.sh
./update_cv_themes.sh
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

## Storage / API Evidence
```text
cv.html:113:    .cv-sheet-themed-bg { background-color: var(--sheet-bg) !important; }
cv.html:173:            15 Visual Themes
cv.html:188:        <button id="nav-btn-print" onclick="window.print()" class="hidden px-3.5 py-1.5 text-xs font-bold rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white transition shadow-sm flex items-center gap-1.5 cursor-pointer">
cv.html:190:          <span id="ui-btn-download-pdf">Download PDF</span>
cv.html:277:          <select id="theme-selector-dropdown" onchange="handleThemeSelect(this.value)" class="px-2 py-1 text-xs bg-slate-950 border border-slate-800 rounded font-bold text-blue-300 focus:border-blue-500 focus:outline-none cursor-pointer">
cv.html:417:                <label id="lbl-f-summary" class="text-[11px] text-slate-400">Profil Profesional (Professional Summary)</label>
cv.html:506:          <button onclick="window.print()" class="font-bold text-blue-400 hover:text-blue-300 flex items-center gap-1 cursor-pointer">
cv.html:507:            <span id="ui-btn-sheet-download">Download PDF</span> &rarr;
cv.html:512:        <div id="cv-preview-sheet" class="font-cv-body cv-sheet-themed-bg w-full max-w-[780px] text-slate-800 shadow-2xl rounded-sm p-8 sm:p-11 min-h-[1050px] border border-slate-200">
cv.html:521:  <div id="pro-theme-modal" class="no-print hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
cv.html:550:        <button onclick="previewProThemeTemporarily()" class="w-full py-2 px-4 bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs rounded-xl transition cursor-pointer">
cv.html:567:          const raw = localStorage.getItem('gaeks_user_session_v3') || localStorage.getItem('gaeks_user_session_v2');
cv.html:577:    let pendingProTheme = null;
cv.html:580:    const themesConfig = [
cv.html:599:    const professionBank = {
cv.html:654:        "Project Management Professional (PMP)", "Agile Coach / Scrum Master", "Program Manager", "Portfolio Manager",
cv.html:766:        btnDownloadPdf: "Download PDF",
cv.html:775:        btnSheetDownload: "Download PDF",
cv.html:828:        btnDownloadPdf: "Export PDF",
cv.html:829:        dashTitle: "Professional Resume & CV Manager",
cv.html:837:        btnSheetDownload: "Download PDF",
cv.html:857:        lblSummary: "Professional Summary",
cv.html:858:        lblExpTitle: "Professional Experience",
cv.html:870:        sheetSummary: "PROFESSIONAL SUMMARY",
cv.html:871:        sheetExperience: "PROFESSIONAL EXPERIENCE",
cv.html:1018:    function getAllProfessions() {
cv.html:1020:      Object.values(professionBank).forEach(arr => {
cv.html:1037:        list = getAllProfessions();
cv.html:1039:        list = professionBank[cat] || [];
cv.html:1139:    function getRoleSeparatorForTheme() {
cv.html:1183:      const raw = localStorage.getItem(currentKey);
cv.html:1192:        const guestRaw = localStorage.getItem('gaeks_cv_master_list_v17');
cv.html:1212:      localStorage.setItem(currentKey, JSON.stringify(cvList));
cv.html:1473:      document.getElementById('theme-selector-dropdown').value = targetLyt;
cv.html:1474:      setThemeLayout(targetLyt);
cv.html:1877:    function handleThemeSelect(themeId) {
cv.html:1878:      const target = themesConfig.find(t => t.id === themeId);
cv.html:1882:        pendingProTheme = target;
cv.html:1887:      setThemeLayout(themeId);
cv.html:1890:    function showProModal(theme) {
cv.html:1891:      document.getElementById('modal-pro-title').innerText = `Tema ${theme.name} (GAEKS PRO 🔒)`;
cv.html:1892:      const waLink = `https://wa.me/6285608561745?text=Halo%20Admin%20GAEKS%2C%20saya%20tertarik%20upgrade%20ke%20Member%20Berbayar%20untuk%20membuka%2015%20Tema%20CV%20Premium%20(Tema%3A%20${encodeURIComponent(theme.name)})`;
cv.html:1894:      document.getElementById('pro-theme-modal').classList.remove('hidden');
cv.html:1898:      document.getElementById('pro-theme-modal').classList.add('hidden');
cv.html:1899:      document.getElementById('theme-selector-dropdown').value = activeLayout;
cv.html:1900:      pendingProTheme = null;
cv.html:1903:    function previewProThemeTemporarily() {
cv.html:1904:      if (pendingProTheme) {
cv.html:1905:        setThemeLayout(pendingProTheme.id);
cv.html:1906:        document.getElementById('theme-selector-dropdown').value = pendingProTheme.id;
cv.html:1911:    function setThemeLayout(name) {
cv.html:1916:      const current = themesConfig.find(t => t.id === name);
cv.html:1948:      document.getElementById('ui-btn-download-pdf').innerText = dict.btnDownloadPdf;
cv.html:2028:      const sep = getRoleSeparatorForTheme();
cv.html:2033:        rolesString = currentLang === 'en' ? 'Target Position / Professional Roles' : 'Target Posisi / Profesi';
cv-dashboard.html:149:    function getSessionStorageKey() {
cv-dashboard.html:157:      const sKey = getSessionStorageKey();
cv-dashboard.html:158:      const raw = localStorage.getItem(sKey);
cv-dashboard.html:178:      const sKey = getSessionStorageKey();
cv-dashboard.html:179:      localStorage.setItem(sKey, JSON.stringify(cvList));
cv-dashboard.html:356:          const sKey = (typeof getSessionStorageKey === 'function') ? getSessionStorageKey() : 'gaeks_cv_guest_v18';
cv-dashboard.html:357:          localStorage.setItem(sKey, JSON.stringify(cvList));
auth.js:26:    try { raw = localStorage.getItem(USERS_DB_KEY); } catch(e) {}
auth.js:28:      try { raw = localStorage.getItem('gaeks_users_db_v2'); } catch(e) {}
auth.js:36:      try { localStorage.setItem(USERS_DB_KEY, JSON.stringify(initial)); } catch(e) {}
auth.js:43:    try { localStorage.setItem(USERS_DB_KEY, JSON.stringify(db)); } catch(e) {}
auth.js:69:      fetch('/api/mailer.php', {
auth.js:84:    try { raw = localStorage.getItem('gaeks_user_session_v3'); } catch(e) {}
auth.js:86:      try { raw = localStorage.getItem('gaeks_user_session_v2'); } catch(e) {}
auth.js:89:      try { raw = localStorage.getItem('gaeks_user_session'); } catch(e) {}
auth.js:117:          localStorage.setItem('gaeks_user_session_v3', JSON.stringify(user));
auth.js:140:      localStorage.removeItem('gaeks_user_session_v3');
auth.js:141:      localStorage.removeItem('gaeks_user_session_v2');
auth.js:142:      localStorage.removeItem('gaeks_user_session');
auth.js:143:      sessionStorage.clear();
```

## Target Flow
User → authenticated session → CV record owned by user → editor/autosave → dashboard → A4 PDF export

## Main Risks To Verify
- Browser-only persistence
- Cross-device consistency
- Cross-user access
- PDF pagination/clipping
- Internal sample data appearing as user data
