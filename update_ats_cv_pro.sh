#!/bin/bash
set -e

echo "=== Memperbarui cv.html dengan Tipografi Lembut, Dual Bahasa & Tabbed UI ==="

cat << 'HTML_CV' > cv.html
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>GAEKS ATS CV Studio | Executive Resume Builder</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; }
    .cv-sheet-font { font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    
    :root {
      --primary-color: #1e3a8a;
      --primary-light: #eff6ff;
      --primary-border: #dbeafe;
    }

    .theme-accent-text { color: var(--primary-color) !important; }
    .theme-accent-border { border-color: var(--primary-color) !important; }
    .theme-badge {
      background-color: var(--primary-light) !important;
      color: var(--primary-color) !important;
      border: 1px solid var(--primary-border) !important;
    }

    /* PREVIEW SCROLLBAR */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: #0b0f19; }
    ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 4px; }

    /* CSS CETAK A4 PRESISI KHUSUS PDF & ATS */
    @media print {
      body * {
        visibility: hidden !important;
      }
      #cv-preview-sheet, #cv-preview-sheet * {
        visibility: visible !important;
      }
      #cv-preview-sheet {
        position: absolute !important;
        left: 0 !important;
        top: 0 !important;
        width: 100% !important;
        margin: 0 !important;
        padding: 14mm 16mm !important;
        box-shadow: none !important;
        border: none !important;
        background: #ffffff !important;
        color: #1e293b !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
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
  <header class="no-print sticky top-0 z-40 w-full backdrop-blur-md bg-slate-950/90 border-b border-slate-800/80">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <a href="index.html" class="text-xs font-semibold text-slate-400 hover:text-white flex items-center gap-1.5 py-1 px-2 rounded-lg hover:bg-slate-900 transition">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
          <span class="hidden sm:inline">Kembali</span>
        </a>
        <span class="text-slate-700">|</span>
        <div class="flex items-center space-x-2">
          <span class="font-extrabold text-base sm:text-lg bg-gradient-to-r from-blue-400 to-indigo-300 bg-clip-text text-transparent">
            GAEKS ATS Studio
          </span>
          <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-950 text-blue-300 border border-blue-800">
            v2.4 Pro
          </span>
        </div>
      </div>

      <!-- AKSI KANAN: DUAL LANGUAGE & PRINT -->
      <div class="flex items-center space-x-2 sm:space-x-3">
        <!-- TOGGLE BAHASA -->
        <div class="bg-slate-900 p-1 rounded-lg border border-slate-800 flex items-center text-xs font-bold">
          <button onclick="setLanguage('id')" id="btn-lang-id" class="px-2.5 py-1 rounded bg-blue-600 text-white transition">
            ID 🇮🇩
          </button>
          <button onclick="setLanguage('en')" id="btn-lang-en" class="px-2.5 py-1 rounded text-slate-400 hover:text-white transition">
            EN 🇬🇧
          </button>
        </div>

        <!-- DOWNLOAD BUTTON -->
        <button onclick="window.print()" class="px-4 py-2 text-xs sm:text-sm font-bold rounded-lg bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white transition shadow-lg shadow-blue-500/20 flex items-center space-x-1.5">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
          <span>Download PDF</span>
        </button>
      </div>
    </div>
  </header>

  <!-- WORKSPACE UTAMA -->
  <main class="max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-6 flex-grow">
    
    <!-- SUB-BAR / THEME CONTROLLER -->
    <div class="no-print flex flex-col md:flex-row md:items-center justify-between pb-5 mb-6 border-b border-slate-800/80 gap-4">
      <div>
        <h1 class="text-xl sm:text-2xl font-extrabold text-white tracking-tight">Executive Resume Builder</h1>
        <p class="text-xs text-slate-400 mt-0.5">Tipografi lembut, posisi kategori teruji ATS, dan dukungan terjemahan otomatis ID/EN.</p>
      </div>

      <!-- TEMA WARNA & CONTROLLER -->
      <div class="flex flex-wrap items-center gap-2 bg-slate-900/90 p-1.5 rounded-xl border border-slate-800">
        <span class="text-[11px] text-slate-400 font-semibold px-2">Tema:</span>
        
        <!-- 3 TEMA GRATIS -->
        <button onclick="setTheme('navy')" id="btn-theme-navy" class="px-2.5 py-1 text-xs font-semibold rounded-md bg-blue-950 text-blue-300 border border-blue-600 transition">
          Executive Navy
        </button>
        <button onclick="setTheme('emerald')" id="btn-theme-emerald" class="px-2.5 py-1 text-xs font-semibold rounded-md bg-slate-950 text-slate-400 border border-slate-800 hover:border-slate-700 transition">
          Emerald Modern
        </button>
        <button onclick="setTheme('slate')" id="btn-theme-slate" class="px-2.5 py-1 text-xs font-semibold rounded-md bg-slate-950 text-slate-400 border border-slate-800 hover:border-slate-700 transition">
          Slate Minimal
        </button>

        <!-- TEMA TERKUNCI -->
        <button onclick="openProModal('Burgundy Luxury')" class="px-2.5 py-1 text-xs font-semibold rounded-md bg-slate-950 text-slate-500 border border-slate-800 hover:border-amber-500/50 hover:text-amber-400 transition flex items-center gap-1">
          <span>Burgundy</span> <span class="text-[9px] text-amber-400">PRO 🔒</span>
        </button>
        <button onclick="openProModal('Nordic Teal')" class="px-2.5 py-1 text-xs font-semibold rounded-md bg-slate-950 text-slate-500 border border-slate-800 hover:border-amber-500/50 hover:text-amber-400 transition flex items-center gap-1">
          <span>Nordic Teal</span> <span class="text-[9px] text-amber-400">PRO 🔒</span>
        </button>
      </div>
    </div>

    <!-- WORKSPACE 2 KOLOM -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
      
      <!-- KOLOM FORMULIR (5 KOLOM) DENGAN TABS INTERAKTIF -->
      <div class="no-print lg:col-span-5 bg-slate-900/90 rounded-2xl border border-slate-800 p-4 sm:p-5 max-h-[85vh] overflow-y-auto">
        
        <!-- TAB SELECTOR -->
        <div class="flex border-b border-slate-800 mb-5 overflow-x-auto space-x-1 pb-1">
          <button onclick="switchTab('profile')" id="tab-btn-profile" class="px-3 py-1.5 text-xs font-bold rounded-lg bg-blue-600 text-white transition whitespace-nowrap">
            1. Profil & Kontak
          </button>
          <button onclick="switchTab('experience')" id="tab-btn-experience" class="px-3 py-1.5 text-xs font-semibold rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition whitespace-nowrap">
            2. Pengalaman
          </button>
          <button onclick="switchTab('education')" id="tab-btn-education" class="px-3 py-1.5 text-xs font-semibold rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition whitespace-nowrap">
            3. Pendidikan
          </button>
          <button onclick="switchTab('skills')" id="tab-btn-skills" class="px-3 py-1.5 text-xs font-semibold rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition whitespace-nowrap">
            4. Keahlian
          </button>
        </div>

        <!-- TAB 1: PROFIL & KONTAK -->
        <div id="tab-content-profile" class="space-y-4">
          <div class="flex items-center justify-between pb-2 border-b border-slate-800/80">
            <span class="text-xs font-bold uppercase tracking-wider text-blue-400">Informasi Pribadi</span>
            <label class="flex items-center space-x-2 text-xs text-slate-300 cursor-pointer">
              <input type="checkbox" id="toggle-photo" onchange="togglePhoto()" class="rounded bg-slate-950 border-slate-700 text-blue-600 focus:ring-0" />
              <span>Gunakan Pas Foto</span>
            </label>
          </div>

          <!-- INPUT FOTO -->
          <div id="photo-box-input" class="hidden p-3 bg-slate-950 rounded-xl border border-slate-800 flex items-center gap-3">
            <img id="thumb-photo" class="w-12 h-12 rounded-lg object-cover border border-slate-700" src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80" alt="Preview" />
            <div class="text-xs flex-grow">
              <span class="block text-slate-300 font-medium mb-1">Unggah Foto Formal</span>
              <input type="file" id="input-photo-file" accept="image/*" onchange="uploadPhoto(event)" class="text-[11px] text-slate-400 file:mr-2 file:py-1 file:px-2 file:rounded file:border-0 file:bg-blue-950 file:text-blue-300 hover:file:bg-blue-900 cursor-pointer" />
            </div>
          </div>

          <div class="space-y-3">
            <div>
              <label class="block text-[11px] text-slate-400 mb-1">Nama Lengkap & Gelar</label>
              <input type="text" id="input-name" oninput="renderCV()" placeholder="Denyt Yudhanusa, S.T." class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" />
            </div>
            <div>
              <label class="block text-[11px] text-slate-400 mb-1">Target Posisi / Profesi</label>
              <input type="text" id="input-title" oninput="renderCV()" placeholder="VP of Logistics Operations" class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" />
            </div>
            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="block text-[11px] text-slate-400 mb-1">Email Profesional</label>
                <input type="email" id="input-email" oninput="renderCV()" class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" />
              </div>
              <div>
                <label class="block text-[11px] text-slate-400 mb-1">No. WhatsApp / HP</label>
                <input type="text" id="input-phone" oninput="renderCV()" class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" />
              </div>
            </div>
            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="block text-[11px] text-slate-400 mb-1">Domisili (Kota, Negara)</label>
                <input type="text" id="input-location" oninput="renderCV()" class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" />
              </div>
              <div>
                <label class="block text-[11px] text-slate-400 mb-1">LinkedIn Username/URL</label>
                <input type="text" id="input-linkedin" oninput="renderCV()" class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" />
              </div>
            </div>
            <div>
              <label class="block text-[11px] text-slate-400 mb-1">Portfolio / Website</label>
              <input type="text" id="input-portfolio" oninput="renderCV()" class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" />
            </div>
            <div>
              <label class="block text-[11px] text-slate-400 mb-1">Ringkasan Profesional (Summary)</label>
              <textarea id="input-summary" rows="4" oninput="renderCV()" class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none"></textarea>
            </div>
          </div>
        </div>

        <!-- TAB 2: PENGALAMAN KERJA -->
        <div id="tab-content-experience" class="hidden space-y-4">
          <div class="flex items-center justify-between pb-2 border-b border-slate-800/80">
            <span class="text-xs font-bold uppercase tracking-wider text-blue-400">Riwayat Karir</span>
            <button onclick="addExperience()" class="text-xs px-2.5 py-1 bg-blue-950 text-blue-300 hover:bg-blue-900 rounded-lg border border-blue-800 transition">
              + Tambah Posisi
            </button>
          </div>
          <div id="experience-list" class="space-y-3"></div>
        </div>

        <!-- TAB 3: PENDIDIKAN -->
        <div id="tab-content-education" class="hidden space-y-4">
          <div class="flex items-center justify-between pb-2 border-b border-slate-800/80">
            <span class="text-xs font-bold uppercase tracking-wider text-blue-400">Pendidikan Formal</span>
            <button onclick="addEducation()" class="text-xs px-2.5 py-1 bg-blue-950 text-blue-300 hover:bg-blue-900 rounded-lg border border-blue-800 transition">
              + Tambah Gelar
            </button>
          </div>
          <div id="education-list" class="space-y-3"></div>
        </div>

        <!-- TAB 4: KEAHLIAN & TOOLS -->
        <div id="tab-content-skills" class="hidden space-y-4">
          <div class="pb-2 border-b border-slate-800/80">
            <span class="text-xs font-bold uppercase tracking-wider text-blue-400">Kompetensi & Sertifikasi</span>
          </div>
          <div class="space-y-3">
            <div>
              <label class="block text-[11px] text-slate-400 mb-1">Keahlian Utama (Pisahkan dengan koma)</label>
              <textarea id="input-skills" rows="3" oninput="renderCV()" class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none"></textarea>
            </div>
            <div>
              <label class="block text-[11px] text-slate-400 mb-1">Tools & Software (Pisahkan dengan koma)</label>
              <input type="text" id="input-tools" oninput="renderCV()" class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none" />
            </div>
            <div>
              <label class="block text-[11px] text-slate-400 mb-1">Sertifikasi Resmi (Tiap baris 1 sertifikasi)</label>
              <textarea id="input-certifications" rows="2" oninput="renderCV()" class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:border-blue-500 focus:outline-none"></textarea>
            </div>
          </div>
        </div>

      </div>

      <!-- KOLOM PRATINJAU DOKUMEN ATS (7 KOLOM) -->
      <div class="lg:col-span-7 flex flex-col items-center">
        
        <!-- STATUS BAR PRATINJAU -->
        <div class="no-print w-full flex justify-between items-center mb-2 px-2 text-xs text-slate-400">
          <div class="flex items-center space-x-2">
            <span class="inline-block w-2 h-2 rounded-full bg-emerald-400"></span>
            <span class="font-bold text-slate-300">Format Lembar A4 ATS</span>
            <span id="label-active-lang" class="px-1.5 py-0.2 rounded text-[10px] font-bold bg-blue-950 text-blue-300 border border-blue-800">Bahasa Indonesia</span>
          </div>
          <button onclick="window.print()" class="font-bold text-blue-400 hover:text-blue-300 flex items-center gap-1">
            <span>Cetak PDF</span> &rarr;
          </button>
        </div>

        <!-- LEMBAR A4 RESUME (WARNA SOFT DAN TIPOGRAFI STANDAR ATS) -->
        <div id="cv-preview-sheet" class="cv-sheet-font w-full max-w-[780px] bg-white text-slate-800 shadow-2xl rounded-sm p-8 sm:p-12 min-h-[1050px] border border-slate-200">
          
          <!-- HEADER SECTION (NAMA, KONTAK, DAN FOTO) -->
          <div id="cv-header-container" class="pb-4 border-b theme-accent-border flex flex-col sm:flex-row items-center sm:items-start gap-5">
            
            <!-- AVATAR FOTO (JIKA DIAKTIFKAN) -->
            <div id="view-photo-wrap" class="hidden shrink-0">
              <img id="view-photo-img" class="w-20 h-20 sm:w-24 sm:h-24 rounded-xl object-cover border border-slate-300 shadow-sm" src="" alt="Profile" />
            </div>

            <!-- DETAIL IDENTITAS -->
            <div class="flex-grow text-center sm:text-left">
              <h1 id="view-name" class="text-2xl sm:text-3xl font-extrabold uppercase tracking-tight theme-accent-text">
                NAMA LENGKAP
              </h1>
              <p id="view-title" class="text-sm sm:text-base font-semibold text-slate-700 mt-0.5 tracking-wide">
                Target Posisi / Profesi
              </p>

              <!-- BARIS KONTAK LEMBUT (SOFT SLATE) -->
              <div class="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-slate-600 mt-2.5 font-medium justify-center sm:justify-start">
                <span class="inline-flex items-center gap-1">
                  <svg class="w-3.5 h-3.5 text-slate-500" fill="currentColor" viewBox="0 0 20 20"><path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"></path><path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"></path></svg>
                  <span id="view-email">email@anda.com</span>
                </span>
                <span>•</span>
                <span class="inline-flex items-center gap-1">
                  <svg class="w-3.5 h-3.5 text-slate-500" fill="currentColor" viewBox="0 0 20 20"><path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"></path></svg>
                  <span id="view-phone">+62 8xx</span>
                </span>
                <span>•</span>
                <span class="inline-flex items-center gap-1">
                  <svg class="w-3.5 h-3.5 text-slate-500" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"></path></svg>
                  <span id="view-location">Kota, Negara</span>
                </span>
                <span id="sep-linkedin">•</span>
                <span id="wrap-linkedin" class="inline-flex items-center gap-1">
                  <span class="font-bold text-slate-500">in</span>
                  <span id="view-linkedin">linkedin.com/in/...</span>
                </span>
                <span id="sep-portfolio">•</span>
                <span id="wrap-portfolio" class="inline-flex items-center gap-1 text-slate-600 font-medium">
                  <span id="view-portfolio">gaeks.com</span>
                </span>
              </div>
            </div>

          </div>

          <!-- KATEGORI 1: SUMMARY -->
          <div class="mt-4">
            <h2 id="header-summary" class="text-xs font-bold uppercase tracking-wider theme-accent-text border-b theme-accent-border pb-1 mb-1.5">
              Ringkasan Profesional
            </h2>
            <p id="view-summary" class="text-xs leading-relaxed text-slate-700 text-justify"></p>
          </div>

          <!-- KATEGORI 2: EXPERIENCE -->
          <div class="mt-4">
            <h2 id="header-experience" class="text-xs font-bold uppercase tracking-wider theme-accent-text border-b theme-accent-border pb-1 mb-2">
              Pengalaman Kerja
            </h2>
            <div id="view-experience" class="space-y-3"></div>
          </div>

          <!-- KATEGORI 3: EDUCATION -->
          <div class="mt-4">
            <h2 id="header-education" class="text-xs font-bold uppercase tracking-wider theme-accent-text border-b theme-accent-border pb-1 mb-1.5">
              Pendidikan Formal
            </h2>
            <div id="view-education" class="space-y-1.5"></div>
          </div>

          <!-- KATEGORI 4: SKILLS & TOOLS -->
          <div class="mt-4">
            <h2 id="header-skills" class="text-xs font-bold uppercase tracking-wider theme-accent-text border-b theme-accent-border pb-1 mb-2">
              Keahlian & Penguasaan Teknologi
            </h2>
            <div class="space-y-2 text-xs">
              <div>
                <span id="header-core-skills" class="font-semibold text-slate-800 block mb-1">Keahlian Inti:</span>
                <div id="view-skills-chips" class="flex flex-wrap gap-1.5"></div>
              </div>
              <div id="view-tools-wrapper" class="pt-1">
                <span id="header-tools" class="font-semibold text-slate-800 block mb-1">Tools & Platform:</span>
                <div id="view-tools-chips" class="flex flex-wrap gap-1.5"></div>
              </div>
            </div>
          </div>

          <!-- KATEGORI 5: CERTIFICATIONS -->
          <div id="cv-section-certifications" class="mt-4">
            <h2 id="header-certifications" class="text-xs font-bold uppercase tracking-wider theme-accent-text border-b theme-accent-border pb-1 mb-1.5">
              Sertifikasi & Lisensi
            </h2>
            <div id="view-certifications" class="text-xs leading-relaxed text-slate-700"></div>
          </div>

        </div>
      </div>

    </div>
  </main>

  <!-- MODAL UPGRADE PRO -->
  <div id="proModal" class="no-print fixed inset-0 z-50 flex items-center justify-center bg-black/75 backdrop-blur-sm hidden">
    <div class="bg-slate-900 border border-amber-500/40 rounded-2xl w-full max-w-md p-6 m-4 shadow-2xl relative text-center">
      <div class="w-12 h-12 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/30 flex items-center justify-center mx-auto mb-3 text-xl">
        🔒
      </div>
      <h3 class="text-xl font-bold text-white tracking-tight">Tema Eksklusif PRO</h3>
      <p id="proModalDesc" class="text-xs text-slate-300 mt-2 leading-relaxed">
        Buka akses ke tema premium ini dengan paket langganan PRO GAEKS Digital Product.
      </p>
      <div class="flex gap-2 mt-6">
        <button onclick="closeProModal()" class="w-1/2 py-2.5 rounded-lg border border-slate-700 text-slate-300 text-xs font-semibold hover:bg-slate-800 transition">
          Tutup
        </button>
        <a href="https://wa.me/?text=Halo%20Admin%20Gaeks,%20saya%20ingin%20upgrade%20ke%20paket%20PRO" target="_blank" class="w-1/2 py-2.5 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 text-xs font-bold transition flex items-center justify-center">
          Upgrade Sekarang
        </a>
      </div>
    </div>
  </div>

  <footer class="no-print border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-500">
    <p>&copy; 2026 GAEKS DIGITAL PRODUCT. Standar Format ATS Internasional.</p>
  </footer>

  <!-- SCRIPT LOGIKA APLIKASI & DUAL-LANGUAGE TRANSLATOR -->
  <script>
    // THEMES PRESETS
    const themePacks = {
      navy: { primary: '#1e3a8a', light: '#eff6ff', border: '#dbeafe' },
      emerald: { primary: '#047857', light: '#ecfdf5', border: '#a7f3d0' },
      slate: { primary: '#334155', light: '#f8fafc', border: '#cbd5e1' }
    };
    let activeTheme = 'navy';

    // DICTIONARY DUAL BAHASA
    const i18n = {
      id: {
        summary: "Ringkasan Profesional",
        experience: "Pengalaman Kerja",
        education: "Pendidikan Formal",
        skills: "Keahlian & Penguasaan Teknologi",
        coreSkills: "Keahlian Inti:",
        tools: "Tools & Platform:",
        certifications: "Sertifikasi & Lisensi",
        badgeLabel: "Bahasa Indonesia",
        present: "Sekarang"
      },
      en: {
        summary: "Professional Summary",
        experience: "Work Experience",
        education: "Education",
        skills: "Skills & Technologies",
        coreSkills: "Core Competencies:",
        tools: "Tools & Platforms:",
        certifications: "Certifications & Licenses",
        badgeLabel: "English (Translated)",
        present: "Present"
      }
    };
    let currentLang = 'id';

    // SMART VOCABULARY TRANSLATOR (ID -> EN)
    const autoTranslateDict = [
      { id: /Sekarang/gi, en: "Present" },
      { id: /Memimpin/gi, en: "Spearheaded and directed" },
      { id: /Mengembangkan/gi, en: "Developed and implemented" },
      { id: /Meningkatkan/gi, en: "Increased and optimized" },
      { id: /Mengurangi/gi, en: "Reduced" },
      { id: /Mengelola/gi, en: "Managed and oversaw" },
      { id: /Menegosiasikan/gi, en: "Negotiated" },
      { id: /Mengkoordinasikan/gi, en: "Coordinated" },
      { id: /Mengawasi/gi, en: "Supervised" },
      { id: /Sarjana Teknik Industri/gi, en: "Bachelor of Industrial Engineering" },
      { id: /Sarjana Ekonomi/gi, en: "Bachelor of Economics" },
      { id: /Universitas Indonesia/gi, en: "University of Indonesia" },
      { id: /Universitas/gi, en: "University" },
      { id: /per kuartal/gi, en: "per quarter" },
      { id: /per tahun/gi, en: "annually" },
      { id: /setara/gi, en: "equivalent to" },
      { id: /Kepabeanan/gi, en: "Customs Clearance" },
      { id: /ekspor-impor/gi, en: "export-import" },
      { id: /kargo/gi, en: "cargo" },
      { id: /rantai pasok/gi, en: "supply chain" },
      { id: /armada/gi, en: "fleet" },
      { id: /pergudangan/gi, en: "warehousing" }
    ];

    function applyTranslation(text) {
      if (!text || currentLang === 'id') return text;
      let translated = text;
      autoTranslateDict.forEach(item => {
        translated = translated.replace(item.id, item.en);
      });
      return translated;
    }

    function setLanguage(lang) {
      currentLang = lang;
      const btnId = document.getElementById('btn-lang-id');
      const btnEn = document.getElementById('btn-lang-en');

      if (lang === 'en') {
        btnEn.className = "px-2.5 py-1 rounded bg-blue-600 text-white transition";
        btnId.className = "px-2.5 py-1 rounded text-slate-400 hover:text-white transition";
      } else {
        btnId.className = "px-2.5 py-1 rounded bg-blue-600 text-white transition";
        btnEn.className = "px-2.5 py-1 rounded text-slate-400 hover:text-white transition";
      }

      // Update Section Headings
      const labels = i18n[lang];
      document.getElementById('header-summary').innerText = labels.summary;
      document.getElementById('header-experience').innerText = labels.experience;
      document.getElementById('header-education').innerText = labels.education;
      document.getElementById('header-skills').innerText = labels.skills;
      document.getElementById('header-coreSkills').innerText = labels.coreSkills;
      document.getElementById('header-tools').innerText = labels.tools;
      document.getElementById('header-certifications').innerText = labels.certifications;
      document.getElementById('label-active-lang').innerText = labels.badgeLabel;

      renderCV();
    }

    // TAB SYSTEM
    function switchTab(tab) {
      ['profile', 'experience', 'education', 'skills'].forEach(t => {
        const content = document.getElementById(`tab-content-${t}`);
        const btn = document.getElementById(`tab-btn-${t}`);
        if (t === tab) {
          content.classList.remove('hidden');
          btn.className = "px-3 py-1.5 text-xs font-bold rounded-lg bg-blue-600 text-white transition whitespace-nowrap";
        } else {
          content.classList.add('hidden');
          btn.className = "px-3 py-1.5 text-xs font-semibold rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition whitespace-nowrap";
        }
      });
    }

    function setTheme(name) {
      if (!themePacks[name]) return;
      activeTheme = name;
      const theme = themePacks[name];
      document.documentElement.style.setProperty('--primary-color', theme.primary);
      document.documentElement.style.setProperty('--primary-light', theme.light);
      document.documentElement.style.setProperty('--primary-border', theme.border);

      ['navy', 'emerald', 'slate'].forEach(t => {
        const b = document.getElementById('btn-theme-' + t);
        if (b) {
          b.className = (t === name) 
            ? "px-2.5 py-1 text-xs font-semibold rounded-md bg-blue-950 text-blue-300 border border-blue-600 transition"
            : "px-2.5 py-1 text-xs font-semibold rounded-md bg-slate-950 text-slate-400 border border-slate-800 hover:border-slate-700 transition";
        }
      });
      renderCV();
    }

    function openProModal(name) {
      document.getElementById('proModalDesc').innerText = `Tema "${name}" terkunci. Dapatkan akses ke semua tema eksekutif dengan langganan PRO GAEKS.`;
      document.getElementById('proModal').classList.remove('hidden');
    }

    function closeProModal() {
      document.getElementById('proModal').classList.add('hidden');
    }

    // STATE DATA
    let experiences = [];
    let educations = [];
    let hasPhoto = false;
    let photoData = "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80";

    function togglePhoto() {
      hasPhoto = document.getElementById('toggle-photo').checked;
      const boxInput = document.getElementById('photo-box-input');
      const viewWrap = document.getElementById('view-photo-wrap');

      if (hasPhoto) {
        boxInput.classList.remove('hidden');
        viewWrap.classList.remove('hidden');
      } else {
        boxInput.classList.add('hidden');
        viewWrap.classList.add('hidden');
      }
      renderCV();
    }

    function uploadPhoto(event) {
      const file = event.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = function(e) {
        photoData = e.target.result;
        document.getElementById('thumb-photo').src = photoData;
        document.getElementById('view-photo-img').src = photoData;
      };
      reader.readAsDataURL(file);
    }

    function addExperience(data = { role: '', company: '', period: '', location: '', desc: '' }) {
      experiences.push(data);
      renderFormLists();
      renderCV();
    }

    function removeExperience(index) {
      experiences.splice(index, 1);
      renderFormLists();
      renderCV();
    }

    function addEducation(data = { degree: '', school: '', period: '', details: '' }) {
      educations.push(data);
      renderFormLists();
      renderCV();
    }

    function removeEducation(index) {
      educations.splice(index, 1);
      renderFormLists();
      renderCV();
    }

    function renderFormLists() {
      const expContainer = document.getElementById('experience-list');
      expContainer.innerHTML = '';
      experiences.forEach((exp, i) => {
        expContainer.innerHTML += `
          <div class="p-3 bg-slate-950 rounded-xl border border-slate-800 relative space-y-2">
            <button onclick="removeExperience(${i})" class="absolute top-2 right-2 text-xs text-rose-400">✕ Hapus</button>
            <div class="grid grid-cols-2 gap-2">
              <input type="text" placeholder="Jabatan" value="${exp.role}" oninput="experiences[${i}].role = this.value; renderCV()" class="px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded text-white" />
              <input type="text" placeholder="Perusahaan" value="${exp.company}" oninput="experiences[${i}].company = this.value; renderCV()" class="px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded text-white" />
            </div>
            <div class="grid grid-cols-2 gap-2">
              <input type="text" placeholder="Periode (mis: 2022 - Sekarang)" value="${exp.period}" oninput="experiences[${i}].period = this.value; renderCV()" class="px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded text-white" />
              <input type="text" placeholder="Lokasi" value="${exp.location}" oninput="experiences[${i}].location = this.value; renderCV()" class="px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded text-white" />
            </div>
            <textarea rows="3" placeholder="Pencapaian & angka kinerja" oninput="experiences[${i}].desc = this.value; renderCV()" class="w-full px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded text-white">${exp.desc}</textarea>
          </div>
        `;
      });

      const eduContainer = document.getElementById('education-list');
      eduContainer.innerHTML = '';
      educations.forEach((edu, i) => {
        eduContainer.innerHTML += `
          <div class="p-3 bg-slate-950 rounded-xl border border-slate-800 relative space-y-2">
            <button onclick="removeEducation(${i})" class="absolute top-2 right-2 text-xs text-rose-400">✕ Hapus</button>
            <div class="grid grid-cols-2 gap-2">
              <input type="text" placeholder="Gelar" value="${edu.degree}" oninput="educations[${i}].degree = this.value; renderCV()" class="px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded text-white" />
              <input type="text" placeholder="Kampus" value="${edu.school}" oninput="educations[${i}].school = this.value; renderCV()" class="px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded text-white" />
            </div>
            <div class="grid grid-cols-2 gap-2">
              <input type="text" placeholder="Tahun" value="${edu.period}" oninput="educations[${i}].period = this.value; renderCV()" class="px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded text-white" />
              <input type="text" placeholder="IPK / Keterangan" value="${edu.details}" oninput="educations[${i}].details = this.value; renderCV()" class="px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded text-white" />
            </div>
          </div>
        `;
      });
    }

    function highlightNumbers(text) {
      if (!text) return '';
      return text.replace(/(\b\d+(\.\d+)?%\b|\b(Rp|USD|\$)\s?[\d.,]+(\s?(juta|miliar|k|m))?|\b\d+x\b|\b\d{2,}\b)/gi, '<strong class="font-semibold text-slate-900">$1</strong>');
    }

    function renderCV() {
      // Data Pribadi
      document.getElementById('view-name').innerText = document.getElementById('input-name').value || 'NAMA LENGKAP';
      document.getElementById('view-title').innerText = applyTranslation(document.getElementById('input-title').value) || 'Target Posisi';
      document.getElementById('view-email').innerText = document.getElementById('input-email').value || 'nama@email.com';
      document.getElementById('view-phone').innerText = document.getElementById('input-phone').value || '+62 8xx';
      document.getElementById('view-location').innerText = document.getElementById('input-location').value || 'Kota, Negara';

      const li = document.getElementById('input-linkedin').value;
      document.getElementById('wrap-linkedin').style.display = li ? 'inline-flex' : 'none';
      document.getElementById('sep-linkedin').style.display = li ? 'inline' : 'none';
      document.getElementById('view-linkedin').innerText = li;

      const port = document.getElementById('input-portfolio').value;
      document.getElementById('wrap-portfolio').style.display = port ? 'inline-flex' : 'none';
      document.getElementById('sep-portfolio').style.display = port ? 'inline' : 'none';
      document.getElementById('view-portfolio').innerText = port;

      // Summary
      const rawSummary = document.getElementById('input-summary').value;
      document.getElementById('view-summary').innerHTML = highlightNumbers(applyTranslation(rawSummary)) || 'Ringkasan profesional Anda.';

      // Experiences
      const expView = document.getElementById('view-experience');
      expView.innerHTML = '';
      experiences.forEach(exp => {
        const bullets = exp.desc
          .split('\n')
          .filter(l => l.trim().length > 0)
          .map(l => `<li class="ml-4 list-disc">${highlightNumbers(applyTranslation(l.replace(/^[*-]\s*/, '')))}</li>`)
          .join('');

        expView.innerHTML += `
          <div>
            <div class="flex flex-wrap justify-between items-baseline gap-1">
              <div>
                <span class="font-bold text-slate-900 text-xs">${applyTranslation(exp.role)}</span>
                <span class="font-semibold text-slate-700 text-xs"> | ${exp.company}</span>
                ${exp.location ? `<span class="text-[11px] text-slate-500 italic"> (${exp.location})</span>` : ''}
              </div>
              <span class="theme-badge px-2 py-0.5 rounded text-[10px] font-semibold">${applyTranslation(exp.period)}</span>
            </div>
            <ul class="text-xs leading-relaxed text-slate-700 mt-1 space-y-0.5">${bullets || '<li>Tugas dan pencapaian...</li>'}</ul>
          </div>
        `;
      });

      // Educations
      const eduView = document.getElementById('view-education');
      eduView.innerHTML = '';
      educations.forEach(edu => {
        eduView.innerHTML += `
          <div class="flex justify-between items-baseline text-xs">
            <div>
              <span class="font-bold text-slate-900">${applyTranslation(edu.school)}</span>
              <span class="text-slate-700"> — ${applyTranslation(edu.degree)}</span>
              ${edu.details ? `<div class="text-[11px] text-slate-500">${applyTranslation(edu.details)}</div>` : ''}
            </div>
            <span class="text-slate-500 text-[11px] font-medium">${applyTranslation(edu.period)}</span>
          </div>
        `;
      });

      // Skill chips
      const rawSkills = document.getElementById('input-skills').value;
      const chipContainer = document.getElementById('view-skills-chips');
      chipContainer.innerHTML = '';
      if (rawSkills.trim()) {
        rawSkills.split(',').map(s => s.trim()).filter(Boolean).forEach(s => {
          chipContainer.innerHTML += `<span class="theme-badge px-2 py-0.5 rounded text-[11px] font-medium">${applyTranslation(s)}</span>`;
        });
      }

      // Tools chips
      const rawTools = document.getElementById('input-tools').value;
      const toolContainer = document.getElementById('view-tools-chips');
      toolContainer.innerHTML = '';
      if (rawTools.trim()) {
        document.getElementById('view-tools-wrapper').style.display = 'block';
        rawTools.split(',').map(s => s.trim()).filter(Boolean).forEach(t => {
          toolContainer.innerHTML += `<span class="bg-slate-100 text-slate-700 border border-slate-200 px-2 py-0.5 rounded text-[11px] font-medium">${t}</span>`;
        });
      } else {
        document.getElementById('view-tools-wrapper').style.display = 'none';
      }

      // Certifications
      const rawCert = document.getElementById('input-certifications').value;
      const certSec = document.getElementById('cv-section-certifications');
      if (rawCert.trim()) {
        certSec.style.display = 'block';
        document.getElementById('view-certifications').innerHTML = rawCert
          .split('\n')
          .filter(l => l.trim())
          .map(l => `• ${applyTranslation(l.trim())}`)
          .join('<br>');
      } else {
        certSec.style.display = 'none';
      }
    }

    function loadInitialData() {
      document.getElementById('input-name').value = "Denyt Yudhanusa, S.T.";
      document.getElementById('input-title').value = "Lead Operations & Logistics Ecosystem";
      document.getElementById('input-email').value = "contact@gaeks.com";
      document.getElementById('input-phone').value = "+62 812-3456-7890";
      document.getElementById('input-location').value = "Jakarta, Indonesia";
      document.getElementById('input-linkedin').value = "gaeks-executive";
      document.getElementById('input-portfolio').value = "gdp.gaeks.com";

      document.getElementById('input-summary').value = 
        "Praktisi senior dengan 7+ tahun pengalaman dalam operasional freight forwarding internasional, kepabeanan terintegrasi, dan digitalisasi ERP rantai pasok. Terbukti berhasil memangkas biaya logistik operasional sebesar 18% per tahun, meningkatkan SLA fulfillment hingga 98.6%, serta mengelola transaksi kargo ekspor-impor senilai lebih dari Rp 45 Miliar.";

      experiences = [
        {
          role: "Head of Freight Forwarding Operations",
          company: "GAEKS FREIGHT INTERNATIONAL",
          period: "2022 - Sekarang",
          location: "Jakarta",
          desc: "Memimpin divisi kepabeanan dan operasional ekspor-impor laut (FCL/LCL) serta udara dengan volume lebih dari 850 TEUs per kuartal.\nMenegosiasikan kontrak tarif langsung dengan 5 shipping lines global, menghemat biaya kargo sebesar 18% (setara Rp 1.4 Miliar).\nMengurangi dwell time kepabeanan dari 4.2 hari menjadi 2.1 hari melalui digitalisasi sistem."
        },
        {
          role: "Senior Logistics Coordinator",
          company: "PT Yudhanusa Ekspresindo",
          period: "2019 - 2022",
          location: "Tangerang",
          desc: "Mengelola pergerakan armada trucking antarpulau dan audit pergudangan terpadu untuk 40+ klien korporat.\nMeningkatkan on-time delivery rate dari 91% menjadi 98.6% dengan menerapkan pelacakan GPS real-time.\nMengawasi kepatuhan dokumen ekspor-impor dengan tingkat ketepatan laporan audit 99.8%."
        }
      ];

      educations = [
        {
          degree: "Sarjana Teknik Industri (S.T.)",
          school: "Universitas Indonesia",
          period: "2015 - 2019",
          details: "IPK 3.84 / 4.00 (Cum Laude)"
        }
      ];

      document.getElementById('input-skills').value = "Freight Forwarding, Supply Chain, Customs Clearance, ERP Systems, Sea & Air Cargo, Negosiasi Kontrak";
      document.getElementById('input-tools').value = "Dolibarr ERP, SAP, Excel Advanced, SQL, Cloudflare";
      document.getElementById('input-certifications').value = "Sertifikasi Ahli Kepabeanan (PPJK)\nCertified Supply Chain Professional (CSCP)";

      document.getElementById('view-photo-img').src = photoData;
      document.getElementById('thumb-photo').src = photoData;

      renderFormLists();
      setTheme('navy');
      renderCV();
    }

    window.onload = loadInitialData;
  </script>
</body>
</html>
HTML_CV

echo "=== Melakukan Commit dan Push ke GitHub ==="
git add cv.html
git commit -m "feat: enhance ATS CV with soft corporate typography, dual language auto-translate and tabbed editor"
git push origin main

echo "=== Selesai! Pembaruan langsung aktif di https://gdp.gaeks.com/cv.html ==="
