#!/bin/bash
set -e

echo "=== Memperbarui cv.html dengan Fitur Eksekutif ATS CV Studio ==="

cat << 'HTML_CV' > cv.html
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>GAEKS ATS CV Studio | Professional Resume Builder</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; }
    .cv-font { font-family: 'Inter', sans-serif; }
    
    /* PREVIEW SCROLLBAR */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #090d16; }
    ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #334155; }

    /* CSS CETAK A4 PRESISI KHUSUS ATS */
    @media print {
      body * {
        visibility: hidden !important;
      }
      #cv-preview-wrapper, #cv-preview-wrapper * {
        visibility: visible !important;
      }
      #cv-preview-wrapper {
        position: absolute !important;
        left: 0 !important;
        top: 0 !important;
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        background: transparent !important;
      }
      #cv-sheet {
        box-shadow: none !important;
        border: none !important;
        width: 100% !important;
        min-height: 100% !important;
        padding: 16mm 18mm !important;
        margin: 0 !important;
        background: white !important;
        color: #0f172a !important;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
      }
      .no-print {
        display: none !important;
      }
      @page {
        size: A4 portrait;
        margin: 0;
      }
    }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 antialiased min-h-screen flex flex-col justify-between selection:bg-blue-600 selection:text-white">

  <!-- NAVBAR UTAMA -->
  <header class="no-print sticky top-0 z-40 w-full backdrop-blur-md bg-slate-950/90 border-b border-slate-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <a href="index.html" class="text-xs sm:text-sm font-semibold text-slate-400 hover:text-white flex items-center gap-1.5 transition py-1 px-2 rounded-lg hover:bg-slate-900">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
          <span>Beranda</span>
        </a>
        <span class="text-slate-700">|</span>
        <div class="flex items-center space-x-2">
          <span class="font-extrabold text-base sm:text-lg bg-gradient-to-r from-blue-400 to-indigo-300 bg-clip-text text-transparent">
            GAEKS ATS Studio
          </span>
          <span class="hidden md:inline-flex text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-blue-950 text-blue-300 border border-blue-800/60">
            Pro ATS Builder
          </span>
        </div>
      </div>

      <!-- AKSI NAVBAR CEPAT -->
      <div class="flex items-center space-x-2 sm:space-x-3">
        <button onclick="exportJSON()" title="Cadangkan Data" class="hidden sm:inline-flex items-center px-3 py-1.5 text-xs font-medium rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 transition">
          Export JSON
        </button>
        <button onclick="document.getElementById('import-file').click()" title="Buka Data Tersimpan" class="hidden sm:inline-flex items-center px-3 py-1.5 text-xs font-medium rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 transition">
          Import JSON
        </button>
        <input type="file" id="import-file" onchange="importJSON(event)" class="hidden" accept=".json" />
        
        <button onclick="window.print()" class="px-4 py-2 text-xs sm:text-sm font-bold rounded-lg bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white transition shadow-lg shadow-blue-500/20 flex items-center space-x-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
          <span>Download PDF</span>
        </button>
      </div>
    </div>
  </header>

  <!-- WORKSPACE -->
  <main class="max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-6 flex-grow">
    
    <!-- SUBHEADER / TOOLBAR -->
    <div class="no-print flex flex-col md:flex-row md:items-center justify-between pb-6 mb-6 border-b border-slate-800/80 gap-4">
      <div>
        <h1 class="text-xl sm:text-2xl font-extrabold text-white tracking-tight">Perancang CV & Resume Eksekutif</h1>
        <p class="text-xs sm:text-sm text-slate-400 mt-0.5">Dirancang khusus untuk menembus seleksi Applicant Tracking System (ATS) dan menarik perhatian HRD.</p>
      </div>
      
      <!-- CONTROLS & THEME PICKER -->
      <div class="flex flex-wrap items-center gap-3">
        <!-- THEME SELECTION -->
        <div class="flex items-center space-x-1.5 bg-slate-900/90 p-1.5 rounded-lg border border-slate-800">
          <span class="text-[11px] text-slate-400 px-2 font-medium">Tema:</span>
          <button onclick="setTheme('navy')" title="Executive Navy" class="w-5 h-5 rounded-full bg-blue-900 border-2 border-white/80 transition hover:scale-110"></button>
          <button onclick="setTheme('slate')" title="Slate Charcoal" class="w-5 h-5 rounded-full bg-slate-800 border border-slate-600 transition hover:scale-110"></button>
          <button onclick="setTheme('emerald')" title="Emerald Corporate" class="w-5 h-5 rounded-full bg-emerald-800 border border-slate-600 transition hover:scale-110"></button>
          <button onclick="setTheme('burgundy')" title="Burgundy Executive" class="w-5 h-5 rounded-full bg-rose-950 border border-slate-600 transition hover:scale-110"></button>
        </div>

        <button onclick="loadSampleData()" class="px-3 py-2 text-xs font-semibold rounded-lg bg-indigo-950 text-indigo-300 hover:bg-indigo-900 border border-indigo-700/60 transition">
          Muat Sampel Eksekutif
        </button>
        <button onclick="resetForm()" class="px-3 py-2 text-xs font-semibold rounded-lg bg-slate-900 text-slate-400 hover:text-white border border-slate-800 transition">
          Reset
        </button>
      </div>
    </div>

    <!-- MAIN TWO COLUMN LAYOUT -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
      
      <!-- FORM INPUT COLUMN (5 KOLOM) -->
      <div class="no-print lg:col-span-5 space-y-6 bg-slate-900/80 p-5 sm:p-6 rounded-2xl border border-slate-800/90 max-h-[85vh] overflow-y-auto">
        
        <!-- WIDGET ATS SCORE CHECKER -->
        <div class="p-4 rounded-xl bg-slate-950 border border-blue-900/50 relative overflow-hidden">
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs font-bold uppercase tracking-wider text-blue-400 flex items-center gap-1.5">
              <span class="inline-block w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              ATS Health Score
            </span>
            <span id="ats-score-badge" class="text-xs font-extrabold px-2 py-0.5 rounded bg-blue-950 text-blue-300 border border-blue-800">
              0%
            </span>
          </div>
          <div class="w-full bg-slate-900 h-1.5 rounded-full overflow-hidden">
            <div id="ats-progress" class="bg-gradient-to-r from-blue-500 to-emerald-400 h-full w-[0%] transition-all duration-500"></div>
          </div>
          <p id="ats-tip" class="text-[11px] text-slate-400 mt-2 italic leading-tight">
            Lengkapi data kontak dan pengalaman kerja untuk mencapai skor maksimal.
          </p>
        </div>

        <!-- 1. DATA PRIBADI, KONTAK & FOTO -->
        <div>
          <div class="flex items-center justify-between mb-3">
            <h2 class="text-xs font-bold uppercase tracking-wider text-blue-400">1. Data Pribadi & Kontak</h2>
            <div class="flex items-center space-x-2">
              <label class="text-[11px] text-slate-400 cursor-pointer flex items-center space-x-1.5">
                <input type="checkbox" id="toggle-photo" onchange="togglePhotoVisibility()" class="rounded bg-slate-950 border-slate-700 text-blue-600 focus:ring-0" />
                <span>Pakai Foto</span>
              </label>
            </div>
          </div>

          <div class="space-y-3">
            <!-- PHOTO UPLOAD BOX -->
            <div id="photo-upload-area" class="hidden p-3 bg-slate-950/60 rounded-xl border border-slate-800 flex items-center space-x-4">
              <img id="preview-photo-thumb" class="w-14 h-14 rounded-full object-cover border-2 border-slate-700 bg-slate-900" src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80" alt="Avatar" />
              <div class="flex-grow text-xs">
                <label class="block text-slate-300 font-medium mb-1">Unggah Foto Formal</label>
                <input type="file" id="input-photo" onchange="handlePhotoUpload(event)" accept="image/*" class="text-[11px] text-slate-400 file:mr-2 file:py-1 file:px-2.5 file:rounded-md file:border-0 file:text-xs file:font-semibold file:bg-blue-950 file:text-blue-300 hover:file:bg-blue-900 cursor-pointer" />
                <p class="text-[10px] text-slate-500 mt-1">Disimpan di peramban (akan otomatis tersinkron ke server setelah fitur login aktif).</p>
              </div>
            </div>

            <div>
              <label class="block text-[11px] text-slate-400 mb-1">Nama Lengkap & Gelar</label>
              <input type="text" id="input-name" oninput="triggerUpdate()" placeholder="contoh: Denyt Yudhanusa, S.T." class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" />
            </div>

            <div>
              <label class="block text-[11px] text-slate-400 mb-1">Target Posisi / Profesi</label>
              <input type="text" id="input-title" oninput="triggerUpdate()" placeholder="contoh: VP of Logistics & Supply Chain" class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" />
            </div>

            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="block text-[11px] text-slate-400 mb-1">Email Profesional</label>
                <input type="email" id="input-email" oninput="triggerUpdate()" placeholder="nama@email.com" class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" />
              </div>
              <div>
                <label class="block text-[11px] text-slate-400 mb-1">No. WhatsApp / HP</label>
                <input type="text" id="input-phone" oninput="triggerUpdate()" placeholder="+62 812-xxxx-xxxx" class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="block text-[11px] text-slate-400 mb-1">Kota & Negara Domisili</label>
                <input type="text" id="input-location" oninput="triggerUpdate()" placeholder="Jakarta, Indonesia" class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" />
              </div>
              <div>
                <label class="block text-[11px] text-slate-400 mb-1">LinkedIn URL</label>
                <input type="text" id="input-linkedin" oninput="triggerUpdate()" placeholder="linkedin.com/in/username" class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" />
              </div>
            </div>

            <div>
              <label class="block text-[11px] text-slate-400 mb-1">Portfolio / Personal Website</label>
              <input type="text" id="input-portfolio" oninput="triggerUpdate()" placeholder="gaeks.com" class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" />
            </div>
          </div>
        </div>

        <hr class="border-slate-800" />

        <!-- 2. SUMMARY -->
        <div>
          <h2 class="text-xs font-bold uppercase tracking-wider text-blue-400 mb-1">2. Ringkasan Profesional (Executive Summary)</h2>
          <p class="text-[11px] text-slate-500 mb-2">Tuliskan 3-4 kalimat padat yang merangkum masa kerja, keahlian utama, dan metrik dampak bisnis.</p>
          <textarea id="input-summary" rows="3" oninput="triggerUpdate()" class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" placeholder="Praktisi berpengalaman dengan rekam jejak dalam mengelola..."></textarea>
        </div>

        <hr class="border-slate-800" />

        <!-- 3. WORK EXPERIENCE -->
        <div>
          <div class="flex items-center justify-between mb-2">
            <h2 class="text-xs font-bold uppercase tracking-wider text-blue-400">3. Pengalaman Kerja</h2>
            <button onclick="addExperience()" class="text-xs px-2.5 py-1 bg-blue-950 text-blue-300 hover:bg-blue-900 rounded-lg border border-blue-800 transition">
              + Tambah Posisi
            </button>
          </div>
          <div id="experience-list" class="space-y-3"></div>
        </div>

        <hr class="border-slate-800" />

        <!-- 4. EDUCATION -->
        <div>
          <div class="flex items-center justify-between mb-2">
            <h2 class="text-xs font-bold uppercase tracking-wider text-blue-400">4. Riwayat Pendidikan</h2>
            <button onclick="addEducation()" class="text-xs px-2.5 py-1 bg-blue-950 text-blue-300 hover:bg-blue-900 rounded-lg border border-blue-800 transition">
              + Tambah Pendidikan
            </button>
          </div>
          <div id="education-list" class="space-y-3"></div>
        </div>

        <hr class="border-slate-800" />

        <!-- 5. SKILLS & EXPERTISE -->
        <div>
          <h2 class="text-xs font-bold uppercase tracking-wider text-blue-400 mb-1">5. Keahlian, Tools, & Bahasa</h2>
          <div class="space-y-3">
            <div>
              <label class="block text-[11px] text-slate-400 mb-1">Keahlian Teknis & Industri (Pisahkan koma)</label>
              <textarea id="input-skills" rows="2" oninput="triggerUpdate()" placeholder="Supply Chain, Customs Clearance, Freight Forwarding, ERP..." class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none"></textarea>
            </div>
            <div>
              <label class="block text-[11px] text-slate-400 mb-1">Tools & Software (Pisahkan koma)</label>
              <input type="text" id="input-tools" oninput="triggerUpdate()" placeholder="Dolibarr ERP, Excel Advanced, SAP, PowerBI, Git" class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" />
            </div>
            <div>
              <label class="block text-[11px] text-slate-400 mb-1">Bahasa (Pisahkan koma)</label>
              <input type="text" id="input-languages" oninput="triggerUpdate()" placeholder="Bahasa Indonesia (Native), English (Professional Working)" class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" />
            </div>
          </div>
        </div>

        <hr class="border-slate-800" />

        <!-- 6. SERTIFIKASI & PENCAPAIAN (OPSIONAL) -->
        <div>
          <h2 class="text-xs font-bold uppercase tracking-wider text-blue-400 mb-1">6. Sertifikasi & Lisensi Resmi</h2>
          <textarea id="input-certifications" rows="2" oninput="triggerUpdate()" placeholder="Sertifikasi Ahli Kepabeanan (PPJK), Supply Chain Professional..." class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none"></textarea>
        </div>

      </div>

      <!-- LIVE PREVIEW COLUMN (7 KOLOM) -->
      <div class="lg:col-span-7 flex flex-col items-center sticky top-20">
        <div class="no-print w-full flex justify-between items-center mb-2 px-2">
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-blue-500"></span>
            Pratinjau Lembar A4 ATS
          </span>
          <button onclick="window.print()" class="text-xs font-bold text-blue-400 hover:text-blue-300 flex items-center gap-1">
            <span>Cetak / Simpan PDF</span> &rarr;
          </button>
        </div>

        <!-- CANVAS PREVIEW CONTAINER -->
        <div id="cv-preview-wrapper" class="w-full flex justify-center overflow-x-auto pb-6">
          <div id="cv-sheet" class="cv-font w-full max-w-[780px] bg-white text-slate-900 shadow-2xl rounded-sm p-8 sm:p-12 min-h-[1050px] border border-slate-200">
            
            <!-- CV HEADER -->
            <div id="cv-header-container" class="border-b pb-4 flex items-start justify-between gap-4 border-slate-800">
              <div class="flex-grow text-center" id="header-text-block">
                <h1 id="view-name" class="text-2xl sm:text-3xl font-extrabold uppercase tracking-tight text-slate-950">
                  NAMA LENGKAP ANDA
                </h1>
                <p id="view-title" class="text-sm sm:text-base font-semibold text-slate-700 mt-0.5 tracking-wide">
                  Target Posisi / Profesi
                </p>
                
                <!-- CONTACT STRIP -->
                <div id="view-contact-strip" class="flex flex-wrap justify-center items-center gap-x-2.5 gap-y-1 text-xs text-slate-600 mt-2 font-medium">
                  <span id="view-email">email@anda.com</span>
                  <span>•</span>
                  <span id="view-phone">+62 8xx</span>
                  <span>•</span>
                  <span id="view-location">Kota, Negara</span>
                  <span id="sep-linkedin">•</span>
                  <span id="view-linkedin">linkedin.com/in/...</span>
                  <span id="sep-portfolio">•</span>
                  <span id="view-portfolio">website.com</span>
                </div>
              </div>

              <!-- OPTIONAL PHOTO ELEMENT -->
              <div id="view-photo-container" class="hidden flex-shrink-0">
                <img id="view-photo" class="w-24 h-24 rounded-full object-cover border-2 border-slate-800" src="" alt="Profile" />
              </div>
            </div>

            <!-- SECTION: PROFESSIONAL SUMMARY -->
            <div id="cv-section-summary" class="mt-4">
              <h2 class="cv-section-title text-xs font-bold uppercase tracking-wider text-slate-900 border-b border-slate-300 pb-1 mb-1.5">
                Ringkasan Profesional
              </h2>
              <p id="view-summary" class="text-[12px] leading-relaxed text-slate-800 text-justify">
                Ringkasan pengalaman eksekutif Anda.
              </p>
            </div>

            <!-- SECTION: WORK EXPERIENCE -->
            <div id="cv-section-experience" class="mt-4">
              <h2 class="cv-section-title text-xs font-bold uppercase tracking-wider text-slate-900 border-b border-slate-300 pb-1 mb-2">
                Pengalaman Kerja & Rekam Jejak
              </h2>
              <div id="view-experience" class="space-y-3"></div>
            </div>

            <!-- SECTION: EDUCATION -->
            <div id="cv-section-education" class="mt-4">
              <h2 class="cv-section-title text-xs font-bold uppercase tracking-wider text-slate-900 border-b border-slate-300 pb-1 mb-1.5">
                Pendidikan Formal
              </h2>
              <div id="view-education" class="space-y-1.5"></div>
            </div>

            <!-- SECTION: SKILLS & COMPETENCIES -->
            <div id="cv-section-skills" class="mt-4">
              <h2 class="cv-section-title text-xs font-bold uppercase tracking-wider text-slate-900 border-b border-slate-300 pb-1 mb-1.5">
                Keahlian & Penguasaan Teknologi
              </h2>
              <div class="text-[12px] leading-relaxed text-slate-800 space-y-1">
                <div id="view-skills-line"></div>
                <div id="view-tools-line"></div>
                <div id="view-languages-line"></div>
              </div>
            </div>

            <!-- SECTION: CERTIFICATIONS (CONDITIONAL) -->
            <div id="cv-section-certifications" class="mt-4">
              <h2 class="cv-section-title text-xs font-bold uppercase tracking-wider text-slate-900 border-b border-slate-300 pb-1 mb-1.5">
                Sertifikasi & Lisensi
              </h2>
              <div id="view-certifications" class="text-[12px] leading-relaxed text-slate-800"></div>
            </div>

          </div>
        </div>

      </div>

    </div>
  </main>

  <!-- FOOTER -->
  <footer class="no-print border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-500">
    <p>&copy; 2026 GAEKS DIGITAL PRODUCT. Format CV dioptimalkan secara ketat untuk Applicant Tracking System (ATS).</p>
  </footer>

  <!-- SCRIPT LOGIKA ATS ENGINE & MEDIA STORAGE -->
  <script>
    // Theme Colors
    const themes = {
      navy: { accent: '#1e3a8a', border: '#1e293b' },
      slate: { accent: '#0f172a', border: '#334155' },
      emerald: { accent: '#065f46', border: '#064e3b' },
      burgundy: { accent: '#881337', border: '#4c0519' }
    };
    let currentTheme = 'navy';

    // State Data
    let experiences = [];
    let educations = [];
    let userPhotoData = "";
    let isPhotoEnabled = false;

    // STORAGE & SERVER MEDIA ADAPTER
    // Catatan: Jika sistem login telah aktif, fungsi ini dapat mengirimkan file langsung ke endpoint backend server
    function uploadMediaToServer(base64Data, userToken = null) {
      if (userToken) {
        // Placeholder untuk request POST ke endpoint backend saat login aktif:
        // fetch('/api/upload_media.php', { method: 'POST', body: JSON.stringify({ image: base64Data, token: userToken }) });
      } else {
        // Mode Tamu: simpan lokal di peramban
        localStorage.setItem('gaeks_cv_photo', base64Data);
      }
    }

    function handlePhotoUpload(event) {
      const file = event.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = function(e) {
        userPhotoData = e.target.result;
        document.getElementById('preview-photo-thumb').src = userPhotoData;
        document.getElementById('view-photo').src = userPhotoData;
        uploadMediaToServer(userPhotoData);
        triggerUpdate();
      };
      reader.readAsDataURL(file);
    }

    function togglePhotoVisibility() {
      isPhotoEnabled = document.getElementById('toggle-photo').checked;
      const photoArea = document.getElementById('photo-upload-area');
      const viewPhotoContainer = document.getElementById('view-photo-container');
      const headerTextBlock = document.getElementById('header-text-block');

      if (isPhotoEnabled) {
        photoArea.classList.remove('hidden');
        viewPhotoContainer.classList.remove('hidden');
        headerTextBlock.classList.remove('text-center');
        headerTextBlock.classList.add('text-left');
      } else {
        photoArea.classList.add('hidden');
        viewPhotoContainer.classList.add('hidden');
        headerTextBlock.classList.remove('text-left');
        headerTextBlock.classList.add('text-center');
      }
      triggerUpdate();
    }

    function setTheme(name) {
      currentTheme = name;
      const theme = themes[name] || themes.navy;
      document.querySelectorAll('.cv-section-title').forEach(el => {
        el.style.color = theme.accent;
        el.style.borderColor = theme.accent;
      });
      document.getElementById('view-name').style.color = theme.accent;
      triggerUpdate();
    }

    // Dynamic Experience List
    function addExperience(data = { role: '', company: '', period: '', location: '', desc: '' }) {
      experiences.push(data);
      renderFormLists();
      triggerUpdate();
    }

    function removeExperience(index) {
      experiences.splice(index, 1);
      renderFormLists();
      triggerUpdate();
    }

    // Dynamic Education List
    function addEducation(data = { degree: '', school: '', period: '', details: '' }) {
      educations.push(data);
      renderFormLists();
      triggerUpdate();
    }

    function removeEducation(index) {
      educations.splice(index, 1);
      renderFormLists();
      triggerUpdate();
    }

    function renderFormLists() {
      const expContainer = document.getElementById('experience-list');
      expContainer.innerHTML = '';
      experiences.forEach((exp, i) => {
        expContainer.innerHTML += `
          <div class="p-3 bg-slate-950 rounded-xl border border-slate-800 relative space-y-2">
            <button onclick="removeExperience(${i})" class="absolute top-2 right-2 text-xs text-rose-400 hover:text-rose-300">✕ Hapus</button>
            <div class="grid grid-cols-2 gap-2">
              <input type="text" placeholder="Jabatan / Posisi" value="${exp.role}" oninput="experiences[${i}].role = this.value; triggerUpdate()" class="px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded-lg text-white" />
              <input type="text" placeholder="Nama Perusahaan" value="${exp.company}" oninput="experiences[${i}].company = this.value; triggerUpdate()" class="px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded-lg text-white" />
            </div>
            <div class="grid grid-cols-2 gap-2">
              <input type="text" placeholder="Periode (misal: 2022 - Sekarang)" value="${exp.period}" oninput="experiences[${i}].period = this.value; triggerUpdate()" class="px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded-lg text-white" />
              <input type="text" placeholder="Lokasi (misal: Jakarta)" value="${exp.location}" oninput="experiences[${i}].location = this.value; triggerUpdate()" class="px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded-lg text-white" />
            </div>
            <textarea rows="3" placeholder="Deskripsi pencapaian (Gunakan enter untuk setiap poin, sebutkan metrik/angka)" oninput="experiences[${i}].desc = this.value; triggerUpdate()" class="w-full px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded-lg text-white">${exp.desc}</textarea>
          </div>
        `;
      });

      const eduContainer = document.getElementById('education-list');
      eduContainer.innerHTML = '';
      educations.forEach((edu, i) => {
        eduContainer.innerHTML += `
          <div class="p-3 bg-slate-950 rounded-xl border border-slate-800 relative space-y-2">
            <button onclick="removeEducation(${i})" class="absolute top-2 right-2 text-xs text-rose-400 hover:text-rose-300">✕ Hapus</button>
            <div class="grid grid-cols-2 gap-2">
              <input type="text" placeholder="Gelar / Jurusan" value="${edu.degree}" oninput="educations[${i}].degree = this.value; triggerUpdate()" class="px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded-lg text-white" />
              <input type="text" placeholder="Kampus / Universitas" value="${edu.school}" oninput="educations[${i}].school = this.value; triggerUpdate()" class="px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded-lg text-white" />
            </div>
            <div class="grid grid-cols-2 gap-2">
              <input type="text" placeholder="Tahun (misal: 2017 - 2021)" value="${edu.period}" oninput="educations[${i}].period = this.value; triggerUpdate()" class="px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded-lg text-white" />
              <input type="text" placeholder="Keterangan / IPK (misal: IPK 3.85)" value="${edu.details}" oninput="educations[${i}].details = this.value; triggerUpdate()" class="px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded-lg text-white" />
            </div>
          </div>
        `;
      });
    }

    // Highlight metrics & numbers automatically for ATS visibility
    function highlightMetrics(text) {
      if (!text) return '';
      // Menemukan persentase (15%), angka dengan currency (Rp 2 Miliar, $100K), kelipatan (2x, 5x)
      return text.replace(/(\b\d+(\.\d+)?%\b|\b(Rp|USD|\$)\s?[\d.,]+(\s?(juta|miliar|k|m))?|\b\d+x\b|\b\d{2,}\b)/gi, '<strong class="text-slate-950 font-semibold">$1</strong>');
    }

    function renderCV() {
      // 1. Personal Details
      document.getElementById('view-name').innerText = document.getElementById('input-name').value || 'NAMA LENGKAP ANDA';
      document.getElementById('view-title').innerText = document.getElementById('input-title').value || 'Target Posisi / Profesi';
      document.getElementById('view-email').innerText = document.getElementById('input-email').value || 'email@anda.com';
      document.getElementById('view-phone').innerText = document.getElementById('input-phone').value || '+62 8xx';
      document.getElementById('view-location').innerText = document.getElementById('input-location').value || 'Kota, Negara';

      const linkedin = document.getElementById('input-linkedin').value;
      const elLinkedin = document.getElementById('view-linkedin');
      const sepLinkedin = document.getElementById('sep-linkedin');
      elLinkedin.innerText = linkedin;
      elLinkedin.style.display = linkedin ? 'inline' : 'none';
      sepLinkedin.style.display = linkedin ? 'inline' : 'none';

      const portfolio = document.getElementById('input-portfolio').value;
      const elPort = document.getElementById('view-portfolio');
      const sepPort = document.getElementById('sep-portfolio');
      elPort.innerText = portfolio;
      elPort.style.display = portfolio ? 'inline' : 'none';
      sepPort.style.display = portfolio ? 'inline' : 'none';

      // 2. Summary
      const summaryVal = document.getElementById('input-summary').value;
      document.getElementById('view-summary').innerHTML = highlightMetrics(summaryVal) || 'Ringkasan profesional Anda akan ditampilkan di sini.';

      // 3. Experiences
      const expView = document.getElementById('view-experience');
      expView.innerHTML = '';
      if (experiences.length === 0) {
        expView.innerHTML = '<p class="text-xs text-slate-400 italic">Belum ada pengalaman kerja yang ditambahkan.</p>';
      } else {
        experiences.forEach(exp => {
          const bulletList = exp.desc
            .split('\n')
            .filter(l => l.trim().length > 0)
            .map(l => `<li class="ml-4 list-disc">${highlightMetrics(l.replace(/^[*-]\s*/, ''))}</li>`)
            .join('');

          expView.innerHTML += `
            <div class="mb-3">
              <div class="flex justify-between items-baseline text-xs font-bold text-slate-900">
                <span>${exp.role || 'Jabatan'} <span class="font-semibold text-slate-700">| ${exp.company || 'Perusahaan'}</span></span>
                <span class="font-normal text-slate-600">${exp.period || ''}</span>
              </div>
              <div class="text-[11px] text-slate-500 italic mb-1">${exp.location || ''}</div>
              <ul class="text-[12px] leading-relaxed text-slate-800 space-y-0.5">${bulletList || '<li>Tugas dan pencapaian...</li>'}</ul>
            </div>
          `;
        });
      }

      // 4. Educations
      const eduView = document.getElementById('view-education');
      eduView.innerHTML = '';
      if (educations.length === 0) {
        eduView.innerHTML = '<p class="text-xs text-slate-400 italic">Belum ada riwayat pendidikan.</p>';
      } else {
        educations.forEach(edu => {
          eduView.innerHTML += `
            <div class="flex justify-between text-xs mb-1">
              <div>
                <span class="font-bold text-slate-900">${edu.school || 'Institusi'}</span> — <span>${edu.degree || 'Gelar'}</span>
                ${edu.details ? `<div class="text-[11px] text-slate-600">${edu.details}</div>` : ''}
              </div>
              <span class="text-slate-600 font-medium">${edu.period || ''}</span>
            </div>
          `;
        });
      }

      // 5. Skills
      const skillsRaw = document.getElementById('input-skills').value;
      const toolsRaw = document.getElementById('input-tools').value;
      const langRaw = document.getElementById('input-languages').value;

      document.getElementById('view-skills-line').innerHTML = skillsRaw.trim() 
        ? `<strong>Keahlian Inti:</strong> ` + skillsRaw.split(',').map(s => s.trim()).filter(Boolean).join(' • ')
        : 'Keahlian teknis dan kompetensi.';
      
      document.getElementById('view-tools-line').innerHTML = toolsRaw.trim() 
        ? `<strong>Tools & Software:</strong> ` + toolsRaw.split(',').map(s => s.trim()).filter(Boolean).join(' • ')
        : '';
      
      document.getElementById('view-languages-line').innerHTML = langRaw.trim() 
        ? `<strong>Kemampuan Bahasa:</strong> ` + langRaw.split(',').map(s => s.trim()).filter(Boolean).join(' • ')
        : '';

      // 6. Certifications
      const certRaw = document.getElementById('input-certifications').value;
      const certSection = document.getElementById('cv-section-certifications');
      if (certRaw.trim()) {
        certSection.style.display = 'block';
        document.getElementById('view-certifications').innerHTML = certRaw.split('\n').filter(l => l.trim()).map(l => `• ${l.trim()}`).join('<br>');
      } else {
        certSection.style.display = 'none';
      }
    }

    // ATS Audit Algorithm
    function evaluateATSScore() {
      let score = 0;
      let tips = [];

      if (document.getElementById('input-name').value.trim()) score += 10;
      if (document.getElementById('input-title').value.trim()) score += 10;
      if (document.getElementById('input-email').value.includes('@')) score += 10;
      if (document.getElementById('input-phone').value.trim()) score += 10;

      const summary = document.getElementById('input-summary').value.trim();
      if (summary.length > 50) {
        score += 15;
      } else {
        tips.push("Perpanjang ringkasan profesional Anda (minimal 2-3 kalimat).");
      }

      if (experiences.length > 0) {
        score += 20;
        const totalDesc = experiences.map(e => e.desc).join(' ');
        if (/(\d+%|\b(Rp|\$)\b|\d+x|\b\d{2,}\b)/.test(totalDesc)) {
          score += 10;
        } else {
          tips.push("Tambahkan angka atau metrik persentase pada deskripsi pekerjaan.");
        }
      } else {
        tips.push("Tambahkan minimal 1 pengalaman kerja.");
      }

      if (educations.length > 0) score += 10;
      if (document.getElementById('input-skills').value.trim().length > 10) score += 5;

      // Update UI
      document.getElementById('ats-score-badge').innerText = `${score}%`;
      document.getElementById('ats-progress').style.width = `${score}%`;

      if (score >= 90) {
        document.getElementById('ats-tip').innerText = "Skor Sangat Baik! CV Anda siap menembus pemindai ATS.";
      } else if (tips.length > 0) {
        document.getElementById('ats-tip').innerText = tips[0];
      }
    }

    function triggerUpdate() {
      renderCV();
      evaluateATSScore();
      saveToLocalStorage();
    }

    function saveToLocalStorage() {
      const data = {
        name: document.getElementById('input-name').value,
        title: document.getElementById('input-title').value,
        email: document.getElementById('input-email').value,
        phone: document.getElementById('input-phone').value,
        location: document.getElementById('input-location').value,
        linkedin: document.getElementById('input-linkedin').value,
        portfolio: document.getElementById('input-portfolio').value,
        summary: document.getElementById('input-summary').value,
        skills: document.getElementById('input-skills').value,
        tools: document.getElementById('input-tools').value,
        languages: document.getElementById('input-languages').value,
        certifications: document.getElementById('input-certifications').value,
        experiences: experiences,
        educations: educations,
        isPhotoEnabled: isPhotoEnabled,
        theme: currentTheme
      };
      localStorage.setItem('gaeks_cv_data', JSON.stringify(data));
    }

    function exportJSON() {
      const data = localStorage.getItem('gaeks_cv_data');
      if (!data) return alert("Belum ada data untuk diekspor.");
      const blob = new Blob([data], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `CV_${(document.getElementById('input-name').value || 'Resume').replace(/\s+/g, '_')}.json`;
      a.click();
    }

    function importJSON(e) {
      const file = e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = function(evt) {
        try {
          const data = JSON.parse(evt.target.result);
          populateFromData(data);
          triggerUpdate();
          alert("Data CV berhasil dimuat!");
        } catch(err) {
          alert("Format file JSON tidak valid.");
        }
      };
      reader.readAsText(file);
    }

    function populateFromData(d) {
      document.getElementById('input-name').value = d.name || '';
      document.getElementById('input-title').value = d.title || '';
      document.getElementById('input-email').value = d.email || '';
      document.getElementById('input-phone').value = d.phone || '';
      document.getElementById('input-location').value = d.location || '';
      document.getElementById('input-linkedin').value = d.linkedin || '';
      document.getElementById('input-portfolio').value = d.portfolio || '';
      document.getElementById('input-summary').value = d.summary || '';
      document.getElementById('input-skills').value = d.skills || '';
      document.getElementById('input-tools').value = d.tools || '';
      document.getElementById('input-languages').value = d.languages || '';
      document.getElementById('input-certifications').value = d.certifications || '';
      experiences = d.experiences || [];
      educations = d.educations || [];
      isPhotoEnabled = d.isPhotoEnabled || false;
      document.getElementById('toggle-photo').checked = isPhotoEnabled;
      togglePhotoVisibility();
      renderFormLists();
    }

    function loadSampleData() {
      const sample = {
        name: "Denyt Yudhanusa, S.T.",
        title: "VP of Operations & Logistics Ecosystem",
        email: "contact@gaeks.com",
        phone: "+62 812-3456-7890",
        location: "Jakarta, Indonesia",
        linkedin: "linkedin.com/in/gaeks-executive",
        portfolio: "gdp.gaeks.com",
        summary: "Praktisi senior dengan 7+ tahun pengalaman dalam operasional freight forwarding internasional, kepabeanan terintegrasi, dan digitalisasi ERP rantai pasok. Terbukti berhasil memangkas biaya logistik operasional sebesar 18% per tahun, meningkatkan SLA fulfillment hingga 98.6%, serta mengelola transaksi kargo ekspor-impor senilai lebih dari Rp 45 Miliar.",
        skills: "Freight Forwarding, Supply Chain Optimization, Customs Clearance (PPJK), Strategic Vendor Sourcing, Operational Risk Management, Multimodal Logistics",
        tools: "Dolibarr ERP, Odoo, SAP S/4HANA, Advanced Excel / VBA, Google Cloud Workspace, SQL",
        languages: "Bahasa Indonesia (Native), English (Full Professional Working Proficiency)",
        certifications: "Sertifikasi Ahli Kepabeanan (PPJK) — Badan Pendidikan dan Pelatihan Keuangan\nCertified Supply Chain Manager (CSCM) — Global Logistics Institute",
        isPhotoEnabled: false,
        experiences: [
          {
            role: "Head of Freight Forwarding Operations",
            company: "GAEKS FREIGHT INTERNATIONAL",
            period: "2022 - Sekarang",
            location: "Jakarta, Indonesia",
            desc: "Memimpin divisi kepabeanan dan operasional ekspor-impor laut (FCL/LCL) serta udara dengan volume lebih dari 850 TEUs per kuartal.\nMenegosiasikan kontrak tarif langsung dengan 5 shipping lines global, menghemat biaya pengiriman kargo tahunan sebesar 18% (setara Rp 1.4 Miliar).\nMengurangi waktu proses dwell time kepabeanan dari 4.2 hari menjadi 2.1 hari melalui digitalisasi alur dokumen kepabeanan."
          },
          {
            role: "Senior Logistics Coordinator",
            company: "PT Yudhanusa Ekspresindo",
            period: "2019 - 2022",
            location: "Tangerang, Banten",
            desc: "Mengelola pergerakan armada trucking antarpulau dan audit pergudangan terpadu untuk 40+ klien korporat.\nMeningkatkan on-time delivery rate dari 91% menjadi 98.6% dengan menerapkan kontrol GPS real-time.\nMengawasi kepatuhan dokumen ekspor impor dengan tingkat ketepatan laporan audit 99.8%."
          }
        ],
        educations: [
          {
            degree: "Sarjana Teknik Industri (S.T.)",
            school: "Universitas Indonesia",
            period: "2015 - 2019",
            details: "IPK 3.84 / 4.00 (Cum Laude) • Fokus Manajemen Rantai Pasok & Rekayasa Kualitas"
          }
        ]
      };
      populateFromData(sample);
      triggerUpdate();
    }

    function resetForm() {
      document.querySelectorAll('input, textarea').forEach(el => el.value = '');
      experiences = [];
      educations = [];
      isPhotoEnabled = false;
      document.getElementById('toggle-photo').checked = false;
      togglePhotoVisibility();
      renderFormLists();
      triggerUpdate();
    }

    window.onload = function() {
      const saved = localStorage.getItem('gaeks_cv_data');
      if (saved) {
        try {
          populateFromData(JSON.parse(saved));
        } catch(e) {
          loadSampleData();
        }
      } else {
        loadSampleData();
      }
      triggerUpdate();
    };
  </script>
</body>
</html>
HTML_CV

echo "=== 2. Push Perubahan ke GitHub ==="
git add cv.html
git commit -m "feat: complete overhaul of ATS CV Studio with live audit score and media handling"
git push origin main

echo "=== Berhasil di-deploy! Silakan akses https://gdp.gaeks.com/cv.html ==="
