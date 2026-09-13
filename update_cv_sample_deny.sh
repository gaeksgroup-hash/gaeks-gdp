#!/bin/bash
set -e

echo "=== Memperbarui cv.html dengan Data Asli CV Deny Triawan ==="

cat << 'HTML_CV' > cv.html
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>GAEKS ATS CV Studio | Deny Triawan Resume</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; }
    .cv-sheet-font { font-family: 'Inter', sans-serif; }
    
    :root {
      --primary-color: #1e3a8a;
      --primary-light: #eff6ff;
      --primary-border: #bfdbfe;
    }

    .theme-accent-text { color: var(--primary-color) !important; }
    .theme-accent-border { border-color: var(--primary-color) !important; }
    .theme-badge {
      background-color: var(--primary-light) !important;
      color: var(--primary-color) !important;
      border: 1px solid var(--primary-border) !important;
    }

    /* CSS CETAK A4 PRESISI KHUSUS ATS & PDF */
    @media print {
      body * { visibility: hidden !important; }
      #cv-preview-sheet, #cv-preview-sheet * { visibility: visible !important; }
      #cv-preview-sheet {
        position: absolute !important;
        left: 0 !important;
        top: 0 !important;
        width: 100% !important;
        margin: 0 !important;
        padding: 12mm 15mm !important;
        box-shadow: none !important;
        border: none !important;
        background: #ffffff !important;
        color: #1e293b !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
      }
      .no-print { display: none !important; }
      @page { size: A4 portrait; margin: 0; }
    }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 antialiased min-h-screen flex flex-col justify-between selection:bg-blue-600 selection:text-white">

  <!-- NAVBAR UTAMA -->
  <header class="no-print sticky top-0 z-40 w-full backdrop-blur-md bg-slate-950/90 border-b border-slate-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <a href="index.html" class="text-xs sm:text-sm font-semibold text-slate-400 hover:text-white flex items-center gap-1.5 py-1 px-2 rounded-lg hover:bg-slate-900 transition">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
          <span class="hidden sm:inline">Beranda</span>
        </a>
        <span class="text-slate-700">|</span>
        <div class="flex items-center space-x-2">
          <span class="font-extrabold text-base sm:text-lg bg-gradient-to-r from-blue-400 to-indigo-300 bg-clip-text text-transparent">
            GAEKS ATS Studio
          </span>
          <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-950 text-blue-300 border border-blue-800">
            Europass & ATS Pro
          </span>
        </div>
      </div>

      <div class="flex items-center space-x-2">
        <button id="nav-btn-dashboard" onclick="showDashboardView()" class="hidden px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 transition">
          Daftar CV
        </button>
        <button id="nav-btn-print" onclick="window.print()" class="hidden px-3.5 py-1.5 text-xs font-bold rounded-lg bg-blue-600 hover:bg-blue-500 text-white transition shadow-sm flex items-center gap-1.5">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
          <span>Download PDF</span>
        </button>
      </div>
    </div>
  </header>

  <!-- ================= VIEW 1: DASHBOARD LIST ================= -->
  <section id="view-dashboard" class="max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8 flex-grow">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-6 mb-6 border-b border-slate-800 gap-4">
      <div>
        <h1 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">Manajemen CV & Dokumen ATS</h1>
        <p class="text-xs sm:text-sm text-slate-400 mt-1">Kelola portofolio resume eksekutif Anda, duplikasi untuk spesialisasi role, atau buat baru.</p>
      </div>
      <button onclick="createNewCV()" class="px-4 py-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold text-xs sm:text-sm shadow-lg shadow-blue-500/20 flex items-center space-x-2 transition">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
        <span>+ Buat CV Baru</span>
      </button>
    </div>

    <!-- TABS ACTIVE VS TRASH -->
    <div class="flex items-center space-x-2 border-b border-slate-800 mb-6">
      <button onclick="switchDashboardTab('active')" id="tab-dash-active" class="px-4 py-2 text-xs sm:text-sm font-bold border-b-2 border-blue-500 text-blue-400 transition flex items-center gap-2">
        <span>Semua CV Aktif</span>
        <span id="badge-active-count" class="px-1.5 py-0.2 rounded-full text-[10px] bg-blue-950 text-blue-300 border border-blue-800">0</span>
      </button>
      <button onclick="switchDashboardTab('trash')" id="tab-dash-trash" class="px-4 py-2 text-xs sm:text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-300 transition flex items-center gap-2">
        <span>Tempat Sampah (Trash)</span>
        <span id="badge-trash-count" class="px-1.5 py-0.2 rounded-full text-[10px] bg-slate-900 text-slate-400 border border-slate-800">0</span>
      </button>
    </div>

    <div id="trash-notice" class="hidden mb-6 p-3.5 bg-amber-950/40 border border-amber-800/60 rounded-xl text-xs text-amber-300 flex items-center gap-2">
      <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
      <span>Dokumen di tempat sampah tersimpan selama <strong>3 hari</strong> sebelum dihapus permanen oleh sistem.</span>
    </div>

    <div id="cv-grid-container" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"></div>
  </section>

  <!-- ================= VIEW 2: CV EDITOR STUDIO ================= -->
  <section id="view-editor" class="hidden max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-6 flex-grow">
    
    <!-- SUBBAR TOOLBAR -->
    <div class="no-print flex flex-col md:flex-row md:items-center justify-between pb-4 mb-5 border-b border-slate-800 gap-4">
      <div class="flex items-center space-x-3">
        <button onclick="showDashboardView()" class="p-2 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 text-xs flex items-center gap-1">
          &larr; <span class="hidden sm:inline">Daftar CV</span>
        </button>
        <div>
          <input type="text" id="current-cv-title" onchange="updateCvTitle(this.value)" class="text-sm sm:text-base font-bold text-white bg-transparent border-b border-dashed border-slate-700 hover:border-blue-500 focus:border-blue-500 focus:outline-none px-1 py-0.5" value="CV Deny Triawan - Supply Chain & Operations" />
          <div class="flex items-center space-x-2 text-[11px] text-slate-400 mt-0.5">
            <span id="save-indicator" class="text-emerald-400 flex items-center gap-1 font-medium">✓ Tersimpan Otomatis</span>
          </div>
        </div>
      </div>

      <!-- KONTROL FITUR -->
      <div class="flex flex-wrap items-center gap-2">
        <div class="flex items-center bg-slate-900 p-1 rounded-lg border border-slate-800 space-x-1">
          <button onclick="undo()" id="btn-undo" title="Undo (Ctrl+Z)" disabled class="px-2 py-1 rounded text-xs text-slate-500 disabled:opacity-40 hover:text-white transition">↶ Undo</button>
          <button onclick="redo()" id="btn-redo" title="Redo (Ctrl+Y)" disabled class="px-2 py-1 rounded text-xs text-slate-500 disabled:opacity-40 hover:text-white transition">↷ Redo</button>
        </div>

        <div class="bg-slate-900 p-1 rounded-lg border border-slate-800 flex items-center text-xs font-bold">
          <button onclick="setLanguage('id')" id="btn-lang-id" class="px-2.5 py-1 rounded bg-blue-600 text-white transition">ID 🇮🇩</button>
          <button onclick="setLanguage('en')" id="btn-lang-en" class="px-2.5 py-1 rounded text-slate-400 hover:text-white transition">EN 🇬🇧</button>
        </div>

        <div class="flex items-center space-x-1 bg-slate-900 p-1 rounded-lg border border-slate-800 text-xs font-semibold">
          <button onclick="setTheme('navy')" id="btn-theme-navy" class="px-2.5 py-1 rounded bg-blue-950 text-blue-300 border border-blue-600">Executive</button>
          <button onclick="setTheme('emerald')" id="btn-theme-emerald" class="px-2.5 py-1 rounded text-slate-400 hover:text-white">Split Line</button>
          <button onclick="setTheme('slate')" id="btn-theme-slate" class="px-2.5 py-1 rounded text-slate-400 hover:text-white">Classic ATS</button>
        </div>
      </div>
    </div>

    <!-- WORKSPACE TWO COLUMNS -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
      
      <!-- FORMULIR INPUT (5 KOLOM) -->
      <div class="no-print lg:col-span-5 bg-slate-900/90 rounded-2xl border border-slate-800 p-4 sm:p-5 max-h-[85vh] overflow-y-auto space-y-4">
        
        <!-- TABS FORMULIR -->
        <div class="flex border-b border-slate-800 pb-2 space-x-1 overflow-x-auto">
          <button onclick="switchFormTab('profile')" id="ftab-btn-profile" class="px-3 py-1.5 text-xs font-bold rounded-lg bg-blue-600 text-white whitespace-nowrap">Profil & Kontak</button>
          <button onclick="switchFormTab('experience')" id="ftab-btn-experience" class="px-3 py-1.5 text-xs font-semibold rounded-lg text-slate-400 hover:text-white whitespace-nowrap">Pengalaman</button>
          <button onclick="switchFormTab('education')" id="ftab-btn-education" class="px-3 py-1.5 text-xs font-semibold rounded-lg text-slate-400 hover:text-white whitespace-nowrap">Pendidikan</button>
          <button onclick="switchFormTab('skills')" id="ftab-btn-skills" class="px-3 py-1.5 text-xs font-semibold rounded-lg text-slate-400 hover:text-white whitespace-nowrap">Keahlian</button>
        </div>

        <!-- FORM 1: PROFIL -->
        <div id="ftab-content-profile" class="space-y-3">
          <div class="flex justify-between items-center pb-2 border-b border-slate-800">
            <span class="text-xs font-bold uppercase text-blue-400">Data Utama</span>
            <label class="flex items-center space-x-1.5 text-xs text-slate-300 cursor-pointer">
              <input type="checkbox" id="input-toggle-photo" onchange="togglePhoto()" class="rounded bg-slate-950 border-slate-700 text-blue-600 focus:ring-0" />
              <span>Gunakan Pas Foto</span>
            </label>
          </div>

          <div id="photo-box-input" class="hidden p-3 bg-slate-950 rounded-xl border border-slate-800 flex items-center gap-3">
            <img id="thumb-photo" class="w-12 h-12 rounded-lg object-cover border border-slate-700" src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80" alt="Preview" />
            <div class="text-xs flex-grow">
              <span class="block text-slate-300 font-medium mb-1">Unggah Foto Formal</span>
              <input type="file" id="input-photo-file" accept="image/*" onchange="uploadPhoto(event)" class="text-[11px] text-slate-400 file:mr-2 file:py-1 file:px-2 file:rounded file:border-0 file:bg-blue-950 file:text-blue-300 cursor-pointer" />
            </div>
          </div>

          <div>
            <label class="block text-[11px] text-slate-400 mb-1">Nama Lengkap & Gelar</label>
            <input type="text" id="input-name" oninput="handleInputChange()" class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white" />
          </div>
          <div>
            <label class="block text-[11px] text-slate-400 mb-1">Target Posisi / Profesi</label>
            <input type="text" id="input-title" oninput="handleInputChange()" class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white" />
          </div>
          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="block text-[11px] text-slate-400 mb-1">Email Profesional</label>
              <input type="email" id="input-email" oninput="handleInputChange()" class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white" />
            </div>
            <div>
              <label class="block text-[11px] text-slate-400 mb-1">No. WhatsApp / HP</label>
              <input type="text" id="input-phone" oninput="handleInputChange()" class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white" />
            </div>
          </div>
          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="block text-[11px] text-slate-400 mb-1">Domisili / Alamat</label>
              <input type="text" id="input-location" oninput="handleInputChange()" class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white" />
            </div>
            <div>
              <label class="block text-[11px] text-slate-400 mb-1">LinkedIn Profile</label>
              <input type="text" id="input-linkedin" oninput="handleInputChange()" class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white" />
            </div>
          </div>
          <div>
            <label class="block text-[11px] text-slate-400 mb-1">Portfolio / Website</label>
            <input type="text" id="input-portfolio" oninput="handleInputChange()" class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white" />
          </div>
          <div>
            <div class="flex justify-between items-center mb-1">
              <label class="text-[11px] text-slate-400">Ringkasan Profesional (Executive Summary)</label>
              <button onclick="aiTranslateField('input-summary')" type="button" class="text-[10px] text-blue-400 hover:text-blue-300 font-semibold flex items-center gap-1">
                <span>✨ Terjemahkan ke English</span>
              </button>
            </div>
            <textarea id="input-summary" rows="4" oninput="handleInputChange()" class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white"></textarea>
          </div>
        </div>

        <!-- FORM 2: PENGALAMAN -->
        <div id="ftab-content-experience" class="hidden space-y-3">
          <div class="flex justify-between items-center pb-2 border-b border-slate-800">
            <span class="text-xs font-bold uppercase text-blue-400">Riwayat Karir</span>
            <button onclick="addExperience()" class="text-xs px-2.5 py-1 bg-blue-950 text-blue-300 hover:bg-blue-900 rounded-lg border border-blue-800 transition">
              + Tambah Pengalaman
            </button>
          </div>
          <div id="experience-list" class="space-y-3.5"></div>
        </div>

        <!-- FORM 3: PENDIDIKAN -->
        <div id="ftab-content-education" class="hidden space-y-3">
          <div class="flex justify-between items-center pb-2 border-b border-slate-800">
            <span class="text-xs font-bold uppercase text-blue-400">Pendidikan & Pelatihan</span>
            <button onclick="addEducation()" class="text-xs px-2.5 py-1 bg-blue-950 text-blue-300 hover:bg-blue-900 rounded-lg border border-blue-800 transition">
              + Tambah Gelar
            </button>
          </div>
          <div id="education-list" class="space-y-3.5"></div>
        </div>

        <!-- FORM 4: KEAHLIAN -->
        <div id="ftab-content-skills" class="hidden space-y-3">
          <div class="pb-2 border-b border-slate-800">
            <span class="text-xs font-bold uppercase text-blue-400">Keahlian & Lisensi</span>
          </div>
          <div>
            <label class="block text-[11px] text-slate-400 mb-1">Keahlian Utama (Pisahkan koma)</label>
            <textarea id="input-skills" rows="3" oninput="handleInputChange()" class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white"></textarea>
          </div>
          <div>
            <label class="block text-[11px] text-slate-400 mb-1">Tools, Software & ERP (Pisahkan koma)</label>
            <input type="text" id="input-tools" oninput="handleInputChange()" class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white" />
          </div>
          <div>
            <label class="block text-[11px] text-slate-400 mb-1">Sertifikasi & Publikasi</label>
            <textarea id="input-certifications" rows="3" oninput="handleInputChange()" class="w-full px-3 py-2 text-xs sm:text-sm bg-slate-950 border border-slate-800 rounded-lg text-white"></textarea>
          </div>
        </div>

      </div>

      <!-- PRATINJAU LEMBAR A4 ATS (7 KOLOM) -->
      <div class="lg:col-span-7 flex flex-col items-center">
        
        <div class="no-print w-full flex justify-between items-center mb-2 px-2 text-xs text-slate-400">
          <div class="flex items-center space-x-2">
            <span class="inline-block w-2 h-2 rounded-full bg-emerald-400"></span>
            <span class="font-bold text-slate-300">Format Lembar A4 ATS</span>
            <span id="label-active-lang" class="px-1.5 py-0.2 rounded text-[10px] font-bold bg-blue-950 text-blue-300 border border-blue-800">Bahasa Indonesia</span>
          </div>
          <button onclick="window.print()" class="font-bold text-blue-400 hover:text-blue-300 flex items-center gap-1">
            <span>Download PDF</span> &rarr;
          </button>
        </div>

        <!-- LEMBAR A4 RESUME -->
        <div id="cv-preview-sheet" class="cv-sheet-font w-full max-w-[780px] bg-white text-slate-800 shadow-2xl rounded-sm p-8 sm:p-12 min-h-[1050px] border border-slate-200">
          
          <!-- 1. HEADER DENGAN KONTAK BERIKON -->
          <div id="cv-header-container" class="pb-4 border-b-2 theme-accent-border flex flex-col sm:flex-row items-center sm:items-start gap-5">
            <div id="view-photo-wrap" class="hidden shrink-0">
              <img id="view-photo-img" class="w-20 h-20 sm:w-24 sm:h-24 rounded-xl object-cover border border-slate-300 shadow-sm" src="" alt="Profile" />
            </div>

            <div class="flex-grow text-center sm:text-left">
              <h1 id="view-name" class="text-2xl sm:text-3xl font-extrabold uppercase tracking-tight theme-accent-text">DENY TRIAWAN</h1>
              <p id="view-title" class="text-xs sm:text-sm font-bold text-slate-800 mt-0.5 tracking-wide">
                Supply Chain Manager / Logistics Operations Manager / ERP Implementer / Solution Architect
              </p>

              <!-- BARIS KONTAK DENGAN IKON VEKTOR RAPI -->
              <div class="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-slate-600 mt-2.5 font-medium justify-center sm:justify-start">
                
                <!-- Email -->
                <span class="inline-flex items-center gap-1">
                  <svg class="w-3.5 h-3.5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
                  <span id="view-email">triawan25@gmail.com</span>
                </span>
                
                <!-- Phone / WA -->
                <span class="inline-flex items-center gap-1">
                  <svg class="w-3.5 h-3.5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path></svg>
                  <span id="view-phone">+62 856-0856-1745</span>
                </span>
                
                <!-- Location -->
                <span class="inline-flex items-center gap-1">
                  <svg class="w-3.5 h-3.5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                  <span id="view-location">Semarang, Indonesia</span>
                </span>
                
                <!-- LinkedIn -->
                <span id="wrap-linkedin" class="inline-flex items-center gap-1">
                  <span class="font-bold text-[10px] text-slate-600 px-1 py-0.2 rounded bg-slate-100 border border-slate-200">in</span>
                  <span id="view-linkedin">linkedin.com/in/triawan25</span>
                </span>
                
                <!-- Portfolio -->
                <span id="wrap-portfolio" class="inline-flex items-center gap-1 text-slate-600 font-medium">
                  <svg class="w-3.5 h-3.5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"></path></svg>
                  <span id="view-portfolio">gaeks.com</span>
                </span>
              </div>
            </div>
          </div>

          <!-- 2. SUMMARY -->
          <div class="mt-4">
            <h2 id="header-summary" class="text-xs font-bold uppercase tracking-wider theme-accent-text border-b theme-accent-border pb-1 mb-1.5">Ringkasan Profesional</h2>
            <p id="view-summary" class="text-xs leading-relaxed text-slate-700 text-justify"></p>
          </div>

          <!-- 3. EXPERIENCE -->
          <div class="mt-4">
            <h2 id="header-experience" class="text-xs font-bold uppercase tracking-wider theme-accent-text border-b theme-accent-border pb-1 mb-2">Pengalaman Kerja</h2>
            <div id="view-experience" class="space-y-3.5"></div>
          </div>

          <!-- 4. EDUCATION -->
          <div class="mt-4">
            <h2 id="header-education" class="text-xs font-bold uppercase tracking-wider theme-accent-text border-b theme-accent-border pb-1 mb-1.5">Pendidikan Formal</h2>
            <div id="view-education" class="space-y-2"></div>
          </div>

          <!-- 5. SKILLS & TOOLS -->
          <div class="mt-4">
            <h2 id="header-skills" class="text-xs font-bold uppercase tracking-wider theme-accent-text border-b theme-accent-border pb-1 mb-2">Keahlian & Penguasaan Teknologi</h2>
            <div class="space-y-2 text-xs">
              <div>
                <span id="header-coreSkills" class="font-semibold text-slate-800 block mb-1">Keahlian Inti:</span>
                <div id="view-skills-chips" class="flex flex-wrap gap-1.5"></div>
              </div>
              <div id="view-tools-wrapper" class="pt-1">
                <span id="header-tools" class="font-semibold text-slate-800 block mb-1">Tools & Platform:</span>
                <div id="view-tools-chips" class="flex flex-wrap gap-1.5"></div>
              </div>
            </div>
          </div>

          <!-- 6. CERTIFICATIONS -->
          <div id="cv-section-certifications" class="mt-4">
            <h2 id="header-certifications" class="text-xs font-bold uppercase tracking-wider theme-accent-text border-b theme-accent-border pb-1 mb-1.5">Sertifikasi & Publikasi</h2>
            <div id="view-certifications" class="text-xs leading-relaxed text-slate-700"></div>
          </div>

        </div>
      </div>

    </div>
  </section>

  <footer class="no-print border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-500">
    <p>&copy; 2026 GAEKS DIGITAL PRODUCT. Standard ATS Resume Engine.</p>
  </footer>

  <!-- SCRIPT LOGIKA UTAMA -->
  <script>
    const themePacks = {
      navy: { primary: '#1e3a8a', light: '#eff6ff', border: '#bfdbfe', layout: 'executive' },
      emerald: { primary: '#047857', light: '#ecfdf5', border: '#a7f3d0', layout: 'split' },
      slate: { primary: '#334155', light: '#f8fafc', border: '#cbd5e1', layout: 'classic' }
    };
    let activeTheme = 'navy';

    const i18n = {
      id: {
        summary: "Ringkasan Profesional",
        experience: "Pengalaman Kerja",
        education: "Pendidikan & Pelatihan",
        skills: "Keahlian & Penguasaan Teknologi",
        coreSkills: "Keahlian Inti:",
        tools: "Tools & Platform:",
        certifications: "Sertifikasi & Publikasi",
        badgeLabel: "Bahasa Indonesia",
        present: "Sekarang"
      },
      en: {
        summary: "Professional Summary",
        experience: "Work Experience",
        education: "Education & Training",
        skills: "Skills & Technologies",
        coreSkills: "Core Competencies:",
        tools: "Tools & Platforms:",
        certifications: "Certifications & Publications",
        badgeLabel: "English (Translated)",
        present: "Present"
      }
    };
    let currentLang = 'id';

    const advancedTranslationDict = [
      { id: /\bSekarang\b/gi, en: "Present" },
      { id: /\bSaat Ini\b/gi, en: "Present" },
      { id: /\bJanuari\b/gi, en: "January" },
      { id: /\bFebruari\b/gi, en: "February" },
      { id: /\bMaret\b/gi, en: "March" },
      { id: /\bMei\b/gi, en: "May" },
      { id: /\bJuni\b/gi, en: "June" },
      { id: /\bJuli\b/gi, en: "July" },
      { id: /\bAgustus\b/gi, en: "August" },
      { id: /\bOktober\b/gi, en: "October" },
      { id: /\bDesember\b/gi, en: "December" },
      { id: /\bMemimpin\b/gi, en: "Spearheaded and directed" },
      { id: /\bMengembangkan\b/gi, en: "Developed and engineered" },
      { id: /\bMeningkatkan\b/gi, en: "Increased and optimized" },
      { id: /\bMengurangi\b/gi, en: "Reduced and minimized" },
      { id: /\bMengelola\b/gi, en: "Managed and orchestrated" },
      { id: /\bMenegosiasikan\b/gi, en: "Negotiated" },
      { id: /\bMengkoordinasikan\b/gi, en: "Coordinated" },
      { id: /\bMengawasi\b/gi, en: "Supervised and audited" },
      { id: /\bMenerapkan\b/gi, en: "Implemented" },
      { id: /\bMembangun\b/gi, en: "Architected and built" },
      { id: /\bMerancang\b/gi, en: "Designed and structured" },
      { id: /\bMengeksekusi\b/gi, en: "Executed" },
      { id: /\bSarjana Teknik Industri\b/gi, en: "Bachelor of Industrial Engineering" },
      { id: /\bSarjana Komputer\b/gi, en: "Bachelor of Computer Science" },
      { id: /\bUniversitas Indonesia\b/gi, en: "University of Indonesia" },
      { id: /\bUniversitas\b/gi, en: "University" },
      { id: /\bKepabeanan\b/gi, en: "Customs Clearance" },
      { id: /\bekspor-impor\b/gi, en: "export and import" },
      { id: /\bkargo\b/gi, en: "cargo" },
      { id: /\brantai pasok\b/gi, en: "supply chain" },
      { id: /\barmada\b/gi, en: "fleet" },
      { id: /\bpergudangan\b/gi, en: "warehousing" }
    ];

    function applyTranslation(text) {
      if (!text || currentLang === 'id') return text;
      let res = text;
      advancedTranslationDict.forEach(dict => {
        res = res.replace(dict.id, dict.en);
      });
      return res;
    }

    let cvList = [];
    let currentCvId = null;
    let currentDashboardTab = 'active';
    let historyStack = [];
    let historyIndex = -1;
    const STORAGE_KEY = 'gaeks_cv_master_list';

    // DATA DEFAULT RESMI: DENY TRIAWAN
    function createDenyTriawanCV() {
      return {
        id: 'cv_deny_triawan_europass',
        title: "CV Deny Triawan - Supply Chain & Operations",
        updatedAt: Date.now(),
        deletedAt: null,
        data: {
          name: "Deny Triawan",
          title: "Supply Chain Manager / Logistics Operations Manager / ERP Implementer / Solution Architect",
          email: "triawan25@gmail.com",
          phone: "+62 856-0856-1745",
          location: "Perum P4A Blok I, Banyumanik, Semarang, 50265, Indonesia",
          linkedin: "triawan25",
          portfolio: "gaeks.com",
          summary: "Profesional berpengalaman dalam manajemen operasional rantai pasok (Supply Chain), implementasi ERP (Odoo & ESB Cloud), kepabeanan ekspor-impor, serta arsitektur solusi bisnis. Berhasil memimpin proyek impor strategis 100 bus Transjakarta, mengefisiensikan alur kerja pergudangan berbasis ISO 31000, serta merancang standarisasi KPI divisi operasional.",
          skills: "Supply Chain Management, Freight Forwarding, Customs Clearance (PIB, PEB, Manifest, BL, COO), Odoo ERP, ESB ERP, Business Process Mapping (COBIT/UML), Vendor Negotiation, ISO 31000 Risk Management, KPI Development",
          tools: "Odoo ERP, SAP Analytics Cloud, Power BI, Google Data Studio, Figma, GitBash, Slack, Mikrotik, Ubiquiti, PostgreSQL, Python, Linux",
          certifications: "Database Design and Programming with SQL — Oracle Academy\nMicrosoft Office Desktop Mastery — Microsoft Partner Program\nPublikasi Ilmiah IEEE: Increased Information Retrieval on E-Commerce Websites Using Scraping Techniques (SIET 2017)",
          isPhotoEnabled: true,
          theme: 'navy',
          experiences: [
            {
              role: "Head of Operations",
              company: "PT. Milenial Solusi Internusa",
              period: "May 2024 - Present",
              location: "South Tangerang, Banten",
              desc: "Memimpin perancangan alur kerja CS, Dokumentasi, dan Sourcing, serta mendukung penuh implementasi Odoo ERP untuk merampingkan proses operasional.\nMengawasi pembuatan dan kepatuhan dokumen logistik internasional penting (PIB, PEB, Manifest, Bill of Lading, COO).\nMemimpin proyek impor strategis bernilai tinggi untuk 100 unit bus Transjakarta, mengelola seluruh logistik kompleks mulai dari negosiasi kapal hingga perjanjian agensi.\nMenerapkan KPI divisi operasional dan merancang mitigasi risiko untuk meminimalkan kendala harian pengiriman."
            },
            {
              role: "Head Of Operations",
              company: "PT Mangkok Besar Cuan",
              period: "May 2022 - June 2023",
              location: "South Jakarta, DKI Jakarta",
              desc: "Mengembangkan workflow, job descriptions, dan pemetaan proses seluruh departemen sesuai budaya korporat.\nMenyelesaikan implementasi ERP Cloud System mencakup migrasi data POS, pemetaan BOM, dan pelaporan digital.\nMenerapkan praktik manajemen inventaris terstruktur (ISO 31000) untuk mengoptimalkan penataan stok dan alur permintaan barang."
            },
            {
              role: "Customer Service & Logistics Specialist",
              company: "Surya Cemerlang Logistic",
              period: "Jan 2022 - May 2022",
              location: "West Jakarta",
              desc: "Mengelola komunikasi dengan agen luar negeri dan pelanggan lokal untuk jadwal pengiriman kargo.\nMembuat dan mereview dokumen pengapalan krusial (Shipping Instruction, BC Documents, Manifest, PIB, PEB, Bill of Lading).\nMengkoordinasikan vendor domestik dan transportasi darat (inland trucking) untuk ketepatan waktu pengiriman akhir."
            },
            {
              role: "Head Of Research And Development",
              company: "Nusaputera",
              period: "June 2019 - Feb 2022",
              location: "Semarang, Central Java",
              desc: "Merancang Business Process Mapping dan worksheet departemen menggunakan IBM project management tools.\nMengembangkan tata kelola IT berbasis framework COBIT dan arsitektur Education ERP.\nMembangun sistem jaringan terintegrasi menggunakan perangkat Ubiquiti dan portal MikroTik dengan perlindungan DDoS dan optimasi bandwidth tree queue."
            }
          ],
          educations: [
            {
              degree: "Master Of Information System (42 SKS)",
              school: "Diponegoro University",
              period: "Sept 2017 - Jan 2020",
              details: "Semarang, Central Java • Proyek: Node JS & TCP/IP on Linux Enterprise"
            },
            {
              degree: "Bachelor Of Computer Science (S.Kom)",
              school: "Universitas Teknologi Digital Indonesia (STMIK Akakom)",
              period: "Sept 2012 - Aug 2016",
              details: "IPK 3.38 • Best Paper Research IEEE: Information Retrieval on E-Commerce Websites"
            }
          ]
        }
      };
    }

    function loadCvList() {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        try { cvList = JSON.parse(raw); } catch(e) { cvList = []; }
      }
      
      // Jika kosong atau belum ada CV Deny Triawan, masukkan sebagai CV Utama
      if (!cvList || cvList.length === 0) {
        cvList = [createDenyTriawanCV()];
        saveCvList();
      }
      autoPurgeTrash();
    }

    function saveCvList() {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(cvList));
      updateDashboardCounts();
    }

    function autoPurgeTrash() {
      const now = Date.now();
      const THREE_DAYS_MS = 3 * 24 * 60 * 60 * 1000;
      let changed = false;
      cvList = cvList.filter(cv => {
        if (cv.deletedAt && (now - cv.deletedAt > THREE_DAYS_MS)) {
          changed = true;
          return false;
        }
        return true;
      });
      if (changed) saveCvList();
    }

    function updateDashboardCounts() {
      document.getElementById('badge-active-count').innerText = cvList.filter(c => !c.deletedAt).length;
      document.getElementById('badge-trash-count').innerText = cvList.filter(c => c.deletedAt).length;
    }

    function showDashboardView() {
      document.getElementById('view-dashboard').classList.remove('hidden');
      document.getElementById('view-editor').classList.add('hidden');
      document.getElementById('nav-btn-dashboard').classList.add('hidden');
      document.getElementById('nav-btn-print').classList.add('hidden');
      renderDashboardGrid();
    }

    function switchDashboardTab(tab) {
      currentDashboardTab = tab;
      const tabActive = document.getElementById('tab-dash-active');
      const tabTrash = document.getElementById('tab-dash-trash');
      const trashNotice = document.getElementById('trash-notice');

      if (tab === 'trash') {
        tabTrash.className = "px-4 py-2 text-xs sm:text-sm font-bold border-b-2 border-amber-500 text-amber-400 transition flex items-center gap-2";
        tabActive.className = "px-4 py-2 text-xs sm:text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-300 transition flex items-center gap-2";
        trashNotice.classList.remove('hidden');
      } else {
        tabActive.className = "px-4 py-2 text-xs sm:text-sm font-bold border-b-2 border-blue-500 text-blue-400 transition flex items-center gap-2";
        tabTrash.className = "px-4 py-2 text-xs sm:text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-300 transition flex items-center gap-2";
        trashNotice.classList.add('hidden');
      }
      renderDashboardGrid();
    }

    function renderDashboardGrid() {
      const container = document.getElementById('cv-grid-container');
      container.innerHTML = '';
      const items = cvList.filter(c => currentDashboardTab === 'trash' ? c.deletedAt : !c.deletedAt);

      if (items.length === 0) {
        container.innerHTML = `
          <div class="col-span-full py-12 text-center text-slate-500 text-sm">
            ${currentDashboardTab === 'trash' ? 'Tempat sampah kosong.' : 'Belum ada CV yang dibuat. Klik "+ Buat CV Baru" di atas.'}
          </div>
        `;
        return;
      }

      const now = Date.now();
      const ONE_DAY_MS = 24 * 60 * 60 * 1000;

      items.forEach(cv => {
        const d = cv.data;
        let trashMeta = '';
        if (cv.deletedAt) {
          const daysLeft = Math.max(0, 3 - Math.floor((now - cv.deletedAt) / ONE_DAY_MS));
          trashMeta = `<span class="text-[11px] text-amber-400 font-medium">Sisa ${daysLeft} hari lagi di sampah</span>`;
        }

        container.innerHTML += `
          <div class="p-5 bg-slate-900/90 rounded-2xl border border-slate-800 hover:border-slate-700 transition flex flex-col justify-between shadow-lg">
            <div>
              <div class="flex items-start justify-between gap-2 mb-2">
                <h3 class="font-bold text-white text-base truncate">${cv.title || 'CV Tanpa Judul'}</h3>
                <span class="text-[10px] uppercase font-semibold px-2 py-0.5 rounded bg-blue-950 text-blue-300 border border-blue-800">Europass & ATS</span>
              </div>
              <p class="text-xs text-slate-400 font-medium">${d.title || 'Target Posisi'}</p>
              <div class="mt-4 pt-3 border-t border-slate-800/80 text-[11px] text-slate-500 space-y-1">
                <div>Diperbarui: ${new Date(cv.updatedAt).toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' })}</div>
                ${trashMeta}
              </div>
            </div>

            <div class="mt-5 pt-3 border-t border-slate-800 flex items-center justify-between gap-2">
              ${currentDashboardTab === 'active' ? `
                <button onclick="openEditor('${cv.id}')" class="px-3.5 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold transition">
                  Buka & Edit
                </button>
                <div class="flex items-center space-x-1">
                  <button onclick="duplicateCV('${cv.id}')" class="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs transition">
                    Duplikat
                  </button>
                  <button onclick="moveToTrash('${cv.id}')" class="p-1.5 rounded-lg bg-rose-950/40 hover:bg-rose-900/60 text-rose-400 border border-rose-900/50 text-xs transition">
                    Hapus
                  </button>
                </div>
              ` : `
                <button onclick="restoreFromTrash('${cv.id}')" class="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold transition">
                  Pulihkan
                </button>
                <button onclick="deletePermanent('${cv.id}')" class="px-3 py-1.5 rounded-lg bg-rose-900/60 hover:bg-rose-800 text-white text-xs font-semibold transition">
                  Hapus Permanen
                </button>
              `}
            </div>
          </div>
        `;
      });
    }

    function createNewCV() {
      const newCv = createDenyTriawanCV();
      newCv.id = 'cv_' + Date.now();
      newCv.title = "CV Deny Triawan (Baru)";
      cvList.unshift(newCv);
      saveCvList();
      openEditor(newCv.id);
    }

    function duplicateCV(id) {
      const src = cvList.find(c => c.id === id);
      if (!src) return;
      const clone = JSON.parse(JSON.stringify(src));
      clone.id = 'cv_' + Date.now() + '_' + Math.random().toString(36).substr(2, 4);
      clone.title = src.title + " (Salinan)";
      clone.updatedAt = Date.now();
      clone.deletedAt = null;
      cvList.unshift(clone);
      saveCvList();
      renderDashboardGrid();
    }

    function moveToTrash(id) {
      const t = cvList.find(c => c.id === id);
      if (t) { t.deletedAt = Date.now(); saveCvList(); renderDashboardGrid(); }
    }

    function restoreFromTrash(id) {
      const t = cvList.find(c => c.id === id);
      if (t) { t.deletedAt = null; saveCvList(); renderDashboardGrid(); }
    }

    function deletePermanent(id) {
      if (!confirm("Hapus CV ini secara permanen?")) return;
      cvList = cvList.filter(c => c.id !== id);
      saveCvList();
      renderDashboardGrid();
    }

    // 2. EDITOR
    function openEditor(id) {
      currentCvId = id;
      const cv = cvList.find(c => c.id === id);
      if (!cv) return;

      document.getElementById('view-dashboard').classList.add('hidden');
      document.getElementById('view-editor').classList.remove('hidden');
      document.getElementById('nav-btn-dashboard').classList.remove('hidden');
      document.getElementById('nav-btn-print').classList.remove('hidden');

      document.getElementById('current-cv-title').value = cv.title;
      loadFormData(cv.data);

      historyStack = [JSON.stringify(cv.data)];
      historyIndex = 0;
      updateUndoRedoButtons();

      renderCV();
    }

    function updateCvTitle(title) {
      const cv = cvList.find(c => c.id === currentCvId);
      if (cv) { cv.title = title; cv.updatedAt = Date.now(); saveCvList(); }
    }

    function loadFormData(d) {
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
      document.getElementById('input-certifications').value = d.certifications || '';
      document.getElementById('input-toggle-photo').checked = !!d.isPhotoEnabled;
      
      togglePhoto();
      renderFormLists(d.experiences || [], d.educations || []);
      setTheme(d.theme || 'navy');
    }

    function extractFormData() {
      const exps = [];
      document.querySelectorAll('.exp-item').forEach(el => {
        exps.push({
          role: el.querySelector('.exp-role').value,
          company: el.querySelector('.exp-company').value,
          period: el.querySelector('.exp-period').value,
          location: el.querySelector('.exp-loc').value,
          desc: el.querySelector('.exp-desc').value
        });
      });

      const edus = [];
      document.querySelectorAll('.edu-item').forEach(el => {
        edus.push({
          degree: el.querySelector('.edu-deg').value,
          school: el.querySelector('.edu-school').value,
          period: el.querySelector('.edu-period').value,
          details: el.querySelector('.edu-det').value
        });
      });

      return {
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
        certifications: document.getElementById('input-certifications').value,
        isPhotoEnabled: document.getElementById('input-toggle-photo').checked,
        theme: activeTheme,
        experiences: exps,
        educations: edus
      };
    }

    function handleInputChange() {
      const data = extractFormData();
      const cv = cvList.find(c => c.id === currentCvId);
      if (cv) {
        cv.data = data;
        cv.updatedAt = Date.now();
        saveCvList();
      }

      const currentJson = JSON.stringify(data);
      if (historyStack[historyIndex] !== currentJson) {
        historyStack = historyStack.slice(0, historyIndex + 1);
        historyStack.push(currentJson);
        if (historyStack.length > 30) historyStack.shift();
        historyIndex = historyStack.length - 1;
        updateUndoRedoButtons();
      }

      renderCV();
    }

    function undo() {
      if (historyIndex > 0) {
        historyIndex--;
        const data = JSON.parse(historyStack[historyIndex]);
        loadFormData(data);
        const cv = cvList.find(c => c.id === currentCvId);
        if (cv) { cv.data = data; cv.updatedAt = Date.now(); saveCvList(); }
        updateUndoRedoButtons();
        renderCV();
      }
    }

    function redo() {
      if (historyIndex < historyStack.length - 1) {
        historyIndex++;
        const data = JSON.parse(historyStack[historyIndex]);
        loadFormData(data);
        const cv = cvList.find(c => c.id === currentCvId);
        if (cv) { cv.data = data; cv.updatedAt = Date.now(); saveCvList(); }
        updateUndoRedoButtons();
        renderCV();
      }
    }

    function updateUndoRedoButtons() {
      document.getElementById('btn-undo').disabled = (historyIndex <= 0);
      document.getElementById('btn-redo').disabled = (historyIndex >= historyStack.length - 1);
    }

    // AUTO ANCHOR
    function addExperience(item = { role: '', company: '', period: '', location: '', desc: '' }) {
      const list = document.getElementById('experience-list');
      const div = document.createElement('div');
      div.className = "exp-item p-3.5 bg-slate-950 rounded-xl border border-slate-800 relative space-y-2.5 transition-all duration-300";
      div.innerHTML = `
        <button onclick="this.parentElement.remove(); handleInputChange();" class="absolute top-2.5 right-2.5 text-xs text-rose-400 hover:text-rose-300">✕ Hapus</button>
        <div class="grid grid-cols-2 gap-2">
          <div>
            <label class="block text-[10px] text-slate-400 mb-0.5">Jabatan / Posisi</label>
            <input type="text" placeholder="Jabatan" value="${item.role}" oninput="handleInputChange()" class="exp-role w-full px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded text-white focus:border-blue-500 focus:outline-none" />
          </div>
          <div>
            <label class="block text-[10px] text-slate-400 mb-0.5">Nama Perusahaan</label>
            <input type="text" placeholder="Perusahaan" value="${item.company}" oninput="handleInputChange()" class="exp-company w-full px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded text-white focus:border-blue-500 focus:outline-none" />
          </div>
        </div>
        <div class="grid grid-cols-2 gap-2">
          <div>
            <label class="block text-[10px] text-slate-400 mb-0.5">Periode Kerja</label>
            <input type="text" placeholder="mis: 2022 - Sekarang" value="${item.period}" oninput="handleInputChange()" class="exp-period w-full px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded text-white focus:border-blue-500 focus:outline-none" />
          </div>
          <div>
            <label class="block text-[10px] text-slate-400 mb-0.5">Lokasi / Kota</label>
            <input type="text" placeholder="mis: Jakarta" value="${item.location}" oninput="handleInputChange()" class="exp-loc w-full px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded text-white focus:border-blue-500 focus:outline-none" />
          </div>
        </div>
        <div>
          <div class="flex justify-between items-center mb-0.5">
            <label class="text-[10px] text-slate-400">Poin Pencapaian Kinerja</label>
            <button type="button" onclick="translateItemDesc(this)" class="text-[10px] text-blue-400 hover:text-blue-300 font-semibold">
              ✨ Format ke English
            </button>
          </div>
          <textarea rows="3" placeholder="Pencapaian kinerja (pisahkan dengan baris baru)" oninput="handleInputChange()" class="exp-desc w-full px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded text-white focus:border-blue-500 focus:outline-none">${item.desc}</textarea>
        </div>
      `;
      list.appendChild(div);

      div.scrollIntoView({ behavior: 'smooth', block: 'center' });
      div.classList.add('ring-2', 'ring-blue-500');
      setTimeout(() => {
        div.classList.remove('ring-2', 'ring-blue-500');
        const roleInput = div.querySelector('.exp-role');
        if (roleInput) roleInput.focus();
      }, 300);

      handleInputChange();
    }

    function addEducation(item = { degree: '', school: '', period: '', details: '' }) {
      const list = document.getElementById('education-list');
      const div = document.createElement('div');
      div.className = "edu-item p-3.5 bg-slate-950 rounded-xl border border-slate-800 relative space-y-2.5 transition-all duration-300";
      div.innerHTML = `
        <button onclick="this.parentElement.remove(); handleInputChange();" class="absolute top-2.5 right-2.5 text-xs text-rose-400 hover:text-rose-300">✕ Hapus</button>
        <div class="grid grid-cols-2 gap-2">
          <div>
            <label class="block text-[10px] text-slate-400 mb-0.5">Gelar / Jurusan</label>
            <input type="text" placeholder="Gelar" value="${item.degree}" oninput="handleInputChange()" class="edu-deg w-full px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded text-white focus:border-blue-500 focus:outline-none" />
          </div>
          <div>
            <label class="block text-[10px] text-slate-400 mb-0.5">Institusi / Universitas</label>
            <input type="text" placeholder="Kampus" value="${item.school}" oninput="handleInputChange()" class="edu-school w-full px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded text-white focus:border-blue-500 focus:outline-none" />
          </div>
        </div>
        <div class="grid grid-cols-2 gap-2">
          <div>
            <label class="block text-[10px] text-slate-400 mb-0.5">Tahun</label>
            <input type="text" placeholder="Tahun" value="${item.period}" oninput="handleInputChange()" class="edu-period w-full px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded text-white focus:border-blue-500 focus:outline-none" />
          </div>
          <div>
            <label class="block text-[10px] text-slate-400 mb-0.5">Keterangan / IPK</label>
            <input type="text" placeholder="IPK / Cum Laude" value="${item.details}" oninput="handleInputChange()" class="edu-det w-full px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded text-white focus:border-blue-500 focus:outline-none" />
          </div>
        </div>
      `;
      list.appendChild(div);

      div.scrollIntoView({ behavior: 'smooth', block: 'center' });
      div.classList.add('ring-2', 'ring-blue-500');
      setTimeout(() => {
        div.classList.remove('ring-2', 'ring-blue-500');
        const degInput = div.querySelector('.edu-deg');
        if (degInput) degInput.focus();
      }, 300);

      handleInputChange();
    }

    function renderFormLists(exps, edus) {
      document.getElementById('experience-list').innerHTML = '';
      exps.forEach(exp => addExperience(exp));
      document.getElementById('education-list').innerHTML = '';
      edus.forEach(edu => addEducation(edu));
    }

    function translateItemDesc(btn) {
      const ta = btn.closest('div').parentElement.querySelector('textarea');
      if (ta && ta.value.trim()) {
        ta.value = applyTranslation(ta.value);
        handleInputChange();
      }
    }

    function aiTranslateField(fieldId) {
      const el = document.getElementById(fieldId);
      if (el && el.value.trim()) {
        el.value = applyTranslation(el.value);
        handleInputChange();
      }
    }

    function switchFormTab(tab) {
      ['profile', 'experience', 'education', 'skills'].forEach(t => {
        const content = document.getElementById(`ftab-content-${t}`);
        const btn = document.getElementById(`ftab-btn-${t}`);
        if (t === tab) {
          content.classList.remove('hidden');
          btn.className = "px-3 py-1.5 text-xs font-bold rounded-lg bg-blue-600 text-white whitespace-nowrap";
        } else {
          content.classList.add('hidden');
          btn.className = "px-3 py-1.5 text-xs font-semibold rounded-lg text-slate-400 hover:text-white whitespace-nowrap";
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
            ? "px-2.5 py-1 rounded font-semibold bg-blue-950 text-blue-300 border border-blue-600"
            : "px-2.5 py-1 rounded font-semibold text-slate-400 hover:text-white";
        }
      });

      renderCV();
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

    function togglePhoto() {
      const enabled = document.getElementById('input-toggle-photo').checked;
      document.getElementById('photo-box-input').classList.toggle('hidden', !enabled);
      document.getElementById('view-photo-wrap').classList.toggle('hidden', !enabled);
      renderCV();
    }

    let photoData = "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80";
    function uploadPhoto(e) {
      const file = e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = function(evt) {
        photoData = evt.target.result;
        document.getElementById('thumb-photo').src = photoData;
        document.getElementById('view-photo-img').src = photoData;
      };
      reader.readAsDataURL(file);
    }

    function highlightNumbers(text) {
      if (!text) return '';
      return text.replace(/(\b\d+(\.\d+)?%\b|\b(Rp|USD|\$)\s?[\d.,]+(\s?(juta|miliar|k|m))?|\b\d+x\b|\b\d{2,}\b)/gi, '<strong class="font-bold text-slate-900">$1</strong>');
    }

    // RENDER LEMBAR A4 RESUME
    function renderCV() {
      // 1. Data Personal
      document.getElementById('view-name').innerText = document.getElementById('input-name').value || 'DENY TRIAWAN';
      document.getElementById('view-title').innerText = applyTranslation(document.getElementById('input-title').value) || 'Target Posisi';
      document.getElementById('view-email').innerText = document.getElementById('input-email').value || 'triawan25@gmail.com';
      document.getElementById('view-phone').innerText = document.getElementById('input-phone').value || '+62 856-0856-1745';
      document.getElementById('view-location').innerText = document.getElementById('input-location').value || 'Semarang, Indonesia';

      const li = document.getElementById('input-linkedin').value;
      document.getElementById('wrap-linkedin').style.display = li ? 'inline-flex' : 'none';
      document.getElementById('view-linkedin').innerText = li;

      const port = document.getElementById('input-portfolio').value;
      document.getElementById('wrap-portfolio').style.display = port ? 'inline-flex' : 'none';
      document.getElementById('view-portfolio').innerText = port;

      // 2. Summary
      const rawSummary = document.getElementById('input-summary').value;
      document.getElementById('view-summary').innerHTML = highlightNumbers(applyTranslation(rawSummary)) || 'Ringkasan profesional Anda.';

      // 3. Experience
      const expView = document.getElementById('view-experience');
      expView.innerHTML = '';
      const themeCfg = themePacks[activeTheme] || themePacks.navy;

      document.querySelectorAll('.exp-item').forEach(el => {
        const role = el.querySelector('.exp-role').value;
        const comp = el.querySelector('.exp-company').value;
        const per = el.querySelector('.exp-period').value;
        const loc = el.querySelector('.exp-loc').value;
        const desc = el.querySelector('.exp-desc').value;

        const bullets = desc
          .split('\n')
          .filter(l => l.trim().length > 0)
          .map(l => `<li class="ml-4 list-disc">${highlightNumbers(applyTranslation(l.replace(/^[*-]\s*/, '')))}</li>`)
          .join('');

        if (themeCfg.layout === 'split') {
          expView.innerHTML += `
            <div class="pl-3 border-l-2 theme-accent-border relative">
              <div class="flex flex-wrap justify-between items-baseline gap-1">
                <div>
                  <span class="font-extrabold text-[13px] tracking-tight theme-accent-text">${applyTranslation(role)}</span>
                  <div class="text-xs font-semibold text-slate-700 flex items-center gap-1.5 mt-0.5">
                    <span class="px-1.5 py-0.2 rounded bg-slate-100 text-slate-800 text-[10px] font-bold">INSTITUSI</span>
                    <span>${comp}</span>
                    ${loc ? `<span class="text-[11px] text-slate-500 italic">(${loc})</span>` : ''}
                  </div>
                </div>
                <span class="theme-badge px-2 py-0.5 rounded text-[10px] font-bold">${applyTranslation(per)}</span>
              </div>
              <ul class="text-xs leading-relaxed text-slate-700 mt-1.5 space-y-0.5">${bullets || '<li>Tugas dan pencapaian...</li>'}</ul>
            </div>
          `;
        } else if (themeCfg.layout === 'classic') {
          expView.innerHTML += `
            <div>
              <div class="flex justify-between items-baseline text-xs">
                <div>
                  <span class="font-bold text-slate-900 text-[13px]">${applyTranslation(role)}</span>
                  <span class="text-slate-600 font-medium"> — ${comp}</span>
                  ${loc ? `<span class="text-[11px] text-slate-500 italic">, ${loc}</span>` : ''}
                </div>
                <span class="text-slate-500 font-medium text-[11px]">${applyTranslation(per)}</span>
              </div>
              <ul class="text-xs leading-relaxed text-slate-700 mt-1 space-y-0.5">${bullets || '<li>Tugas dan pencapaian...</li>'}</ul>
            </div>
          `;
        } else {
          expView.innerHTML += `
            <div>
              <div class="flex flex-wrap justify-between items-baseline gap-1">
                <div>
                  <div class="font-extrabold text-[13px] tracking-tight theme-accent-text">${applyTranslation(role)}</div>
                  <div class="text-xs font-semibold text-slate-700 flex items-center gap-1.5 mt-0.5">
                    <span class="px-2 py-0.2 rounded bg-slate-100 border border-slate-200 text-slate-800 text-[11px] font-medium">${comp}</span>
                    ${loc ? `<span class="text-[11px] text-slate-500 italic">(${loc})</span>` : ''}
                  </div>
                </div>
                <span class="theme-badge px-2 py-0.5 rounded text-[10px] font-bold">${applyTranslation(per)}</span>
              </div>
              <ul class="text-xs leading-relaxed text-slate-700 mt-1.5 space-y-0.5">${bullets || '<li>Tugas dan pencapaian...</li>'}</ul>
            </div>
          `;
        }
      });

      // 4. Education
      const eduView = document.getElementById('view-education');
      eduView.innerHTML = '';
      document.querySelectorAll('.edu-item').forEach(el => {
        const deg = el.querySelector('.edu-deg').value;
        const school = el.querySelector('.edu-school').value;
        const per = el.querySelector('.edu-period').value;
        const det = el.querySelector('.edu-det').value;

        eduView.innerHTML += `
          <div class="flex justify-between items-baseline text-xs">
            <div>
              <span class="font-bold text-slate-900">${applyTranslation(school)}</span>
              <span class="text-slate-700"> — ${applyTranslation(deg)}</span>
              ${det ? `<div class="text-[11px] text-slate-500">${applyTranslation(det)}</div>` : ''}
            </div>
            <span class="text-slate-500 text-[11px] font-medium">${applyTranslation(per)}</span>
          </div>
        `;
      });

      // 5. Skills Chips
      const rawSkills = document.getElementById('input-skills').value;
      const chipContainer = document.getElementById('view-skills-chips');
      chipContainer.innerHTML = '';
      if (rawSkills.trim()) {
        rawSkills.split(',').map(s => s.trim()).filter(Boolean).forEach(s => {
          chipContainer.innerHTML += `<span class="theme-badge px-2 py-0.5 rounded text-[11px] font-medium">${applyTranslation(s)}</span>`;
        });
      }

      // 6. Tools Chips
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

      // 7. Certifications
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

      document.getElementById('view-photo-img').src = photoData;
      document.getElementById('thumb-photo').src = photoData;
    }

    // RESET KE DATA DENY TRIAWAN
    function resetToDenyTriawan() {
      localStorage.removeItem(STORAGE_KEY);
      loadCvList();
      showDashboardView();
    }

    window.onload = function() {
      // Periksa apakah sudah ada data lokal yang lama; jika ingin selalu mengutamakan CV Deny Triawan, kita muat
      loadCvList();
      showDashboardView();
    };
  </script>
</body>
</html>
HTML_CV

echo "=== Melakukan Commit & Push ke GitHub ==="
git add cv.html
git commit -m "feat: integrate official Deny Triawan Europass data as system default CV"
git push origin main

echo "=== Selesai! Buka https://gdp.gaeks.com/cv.html untuk melihat hasilnya ==="
