#!/bin/bash
set -e

echo "=== 1. Memperbarui index.html dengan Fitur CV Maker ATS ==="

cat << 'HTML_EOF' > index.html
<!DOCTYPE html>
<html lang="id" class="scroll-smooth">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>GAEKS DIGITAL PRODUCT | CV Maker & Layanan Digital</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Merriweather:wght@400;700&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Inter', sans-serif; }
    .serif-heading { font-family: 'Merriweather', serif; }
    
    /* STYLING CETAK PDF KHUSUS ATS */
    @media print {
      body * {
        visibility: hidden;
      }
      #cv-preview-sheet, #cv-preview-sheet * {
        visibility: visible;
      }
      #cv-preview-sheet {
        position: absolute;
        left: 0;
        top: 0;
        width: 100% !important;
        margin: 0 !important;
        padding: 20mm !important;
        box-shadow: none !important;
        border: none !important;
        background: white !important;
        color: #0f172a !important;
      }
      @page {
        size: A4;
        margin: 0;
      }
    }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 antialiased min-h-screen flex flex-col justify-between">

  <!-- NAVBAR -->
  <header class="sticky top-0 z-40 w-full backdrop-blur-md bg-slate-950/90 border-b border-slate-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <span class="text-xl font-extrabold tracking-tight bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
          GAEKS DIGITAL PRODUCT
        </span>
        <span class="text-xs px-2 py-0.5 rounded bg-blue-900/60 text-blue-300 border border-blue-700/50 hidden sm:inline-block">
          Studio CV ATS
        </span>
      </div>
      <nav class="flex items-center space-x-4 sm:space-x-6 text-sm font-medium text-slate-300">
        <a href="#cv-studio" class="text-blue-400 hover:text-blue-300 transition">CV Maker</a>
        <a href="#products" class="hover:text-blue-400 transition">Produk Lainnya</a>
      </nav>
      <div class="flex items-center space-x-2">
        <button onclick="window.print()" class="px-3.5 py-1.5 text-xs sm:text-sm font-medium rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white transition flex items-center space-x-1.5 shadow-sm">
          <span>Unduh PDF</span>
        </button>
      </div>
    </div>
  </header>

  <!-- MAIN CV MAKER STUDIO (APP VIEW) -->
  <main id="cv-studio" class="max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
    
    <!-- HEADER APP -->
    <div class="flex flex-col md:flex-row md:items-center justify-between pb-6 mb-6 border-b border-slate-800 gap-4">
      <div>
        <h1 class="text-2xl sm:text-3xl font-bold text-white tracking-tight">ATS Resume & CV Builder</h1>
        <p class="text-xs sm:text-sm text-slate-400 mt-1">Format terstandarisasi industri, lolos pemindai ATS, dan langsung siap cetak.</p>
      </div>
      <div class="flex flex-wrap items-center gap-2">
        <button onclick="loadSampleData()" class="px-3 py-2 text-xs font-semibold rounded-lg bg-indigo-950 text-indigo-300 hover:bg-indigo-900 border border-indigo-700/60 transition">
          Muat Contoh Data Eksekutif
        </button>
        <button onclick="resetForm()" class="px-3 py-2 text-xs font-semibold rounded-lg bg-slate-900 text-slate-400 hover:text-white border border-slate-800 transition">
          Reset Form
        </button>
        <button onclick="window.print()" class="px-4 py-2 text-xs sm:text-sm font-bold rounded-lg bg-blue-600 hover:bg-blue-500 text-white transition shadow-md shadow-blue-600/30">
          Download PDF (ATS)
        </button>
      </div>
    </div>

    <!-- WORKSPACE: SPLIT SCREEN (FORM EDITOR & LIVE PREVIEW) -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
      
      <!-- KOLOM KIRI: FORM EDITOR (5 Kolom) -->
      <div class="lg:col-span-5 space-y-6 bg-slate-900/90 p-5 sm:p-6 rounded-2xl border border-slate-800 max-h-[85vh] overflow-y-auto">
        
        <!-- SECTION 1: PROFIL & KONTAK -->
        <div>
          <h2 class="text-sm font-bold uppercase tracking-wider text-blue-400 mb-3">1. Informasi Pribadi & Kontak</h2>
          <div class="space-y-3">
            <div>
              <label class="block text-xs text-slate-400 mb-1">Nama Lengkap</label>
              <input type="text" id="input-name" oninput="renderCV()" placeholder="contoh: Alex Pratama, S.E." class="w-full px-3 py-2 text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:outline-none focus:border-blue-500" />
            </div>
            <div>
              <label class="block text-xs text-slate-400 mb-1">Target Posisi / Job Title</label>
              <input type="text" id="input-title" oninput="renderCV()" placeholder="contoh: Senior Logistics & Supply Chain Manager" class="w-full px-3 py-2 text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:outline-none focus:border-blue-500" />
            </div>
            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="block text-xs text-slate-400 mb-1">Email</label>
                <input type="email" id="input-email" oninput="renderCV()" placeholder="nama@email.com" class="w-full px-3 py-2 text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:outline-none focus:border-blue-500" />
              </div>
              <div>
                <label class="block text-xs text-slate-400 mb-1">Nomor Telepon / WhatsApp</label>
                <input type="text" id="input-phone" oninput="renderCV()" placeholder="+62 812-xxxx-xxxx" class="w-full px-3 py-2 text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:outline-none focus:border-blue-500" />
              </div>
            </div>
            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="block text-xs text-slate-400 mb-1">Lokasi (Kota, Negara)</label>
                <input type="text" id="input-location" oninput="renderCV()" placeholder="Jakarta, Indonesia" class="w-full px-3 py-2 text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:outline-none focus:border-blue-500" />
              </div>
              <div>
                <label class="block text-xs text-slate-400 mb-1">LinkedIn Profile</label>
                <input type="text" id="input-linkedin" oninput="renderCV()" placeholder="linkedin.com/in/username" class="w-full px-3 py-2 text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:outline-none focus:border-blue-500" />
              </div>
            </div>
            <div>
              <label class="block text-xs text-slate-400 mb-1">Portfolio / Website (Opsional)</label>
              <input type="text" id="input-portfolio" oninput="renderCV()" placeholder="gaeks.com" class="w-full px-3 py-2 text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:outline-none focus:border-blue-500" />
            </div>
          </div>
        </div>

        <hr class="border-slate-800" />

        <!-- SECTION 2: PROFESSIONAL SUMMARY -->
        <div>
          <h2 class="text-sm font-bold uppercase tracking-wider text-blue-400 mb-2">2. Ringkasan Profesional (Summary)</h2>
          <p class="text-[11px] text-slate-500 mb-2">Jelaskan pengalaman kunci, keahlian utama, dan metrik pencapaian (3-4 baris).</p>
          <textarea id="input-summary" rows="3" oninput="renderCV()" placeholder="Profesional berpengalaman dengan rekam jejak dalam..." class="w-full px-3 py-2 text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:outline-none focus:border-blue-500"></textarea>
        </div>

        <hr class="border-slate-800" />

        <!-- SECTION 3: WORK EXPERIENCE -->
        <div>
          <div class="flex items-center justify-between mb-2">
            <h2 class="text-sm font-bold uppercase tracking-wider text-blue-400">3. Pengalaman Kerja</h2>
            <button onclick="addExperience()" class="text-xs px-2.5 py-1 bg-blue-950 text-blue-300 hover:bg-blue-900 rounded border border-blue-800">
              + Tambah Pekerjaan
            </button>
          </div>
          <div id="experience-list" class="space-y-4"></div>
        </div>

        <hr class="border-slate-800" />

        <!-- SECTION 4: EDUCATION -->
        <div>
          <div class="flex items-center justify-between mb-2">
            <h2 class="text-sm font-bold uppercase tracking-wider text-blue-400">4. Riwayat Pendidikan</h2>
            <button onclick="addEducation()" class="text-xs px-2.5 py-1 bg-blue-950 text-blue-300 hover:bg-blue-900 rounded border border-blue-800">
              + Tambah Pendidikan
            </button>
          </div>
          <div id="education-list" class="space-y-4"></div>
        </div>

        <hr class="border-slate-800" />

        <!-- SECTION 5: SKILLS -->
        <div>
          <h2 class="text-sm font-bold uppercase tracking-wider text-blue-400 mb-2">5. Keahlian (Skills & Tools)</h2>
          <p class="text-[11px] text-slate-500 mb-2">Pisahkan dengan koma (misal: Freight Forwarding, Supply Chain, ERP, Negosiasi).</p>
          <textarea id="input-skills" rows="2" oninput="renderCV()" placeholder="Skill 1, Skill 2, Tools A, Tools B..." class="w-full px-3 py-2 text-sm bg-slate-950 border border-slate-800 rounded-lg text-white focus:outline-none focus:border-blue-500"></textarea>
        </div>

      </div>

      <!-- KOLOM KANAN: LIVE ATS PREVIEW SHEET (7 Kolom) -->
      <div class="lg:col-span-7 flex flex-col items-center">
        <div class="w-full flex items-center justify-between mb-2 px-2">
          <span class="text-xs font-semibold uppercase tracking-wider text-slate-400">Pratinjau Lembar A4 (ATS Ready)</span>
          <span class="text-xs text-slate-500">Standar Format Teks HRD & Mesin ATS</span>
        </div>

        <!-- THE SHEET -->
        <div id="cv-preview-sheet" class="w-full bg-white text-slate-900 shadow-2xl rounded-sm p-8 sm:p-12 min-h-[850px] border border-slate-200">
          
          <!-- HEADER -->
          <div class="border-b-2 border-slate-900 pb-4 text-center">
            <h1 id="view-name" class="text-2xl sm:text-3xl font-bold uppercase tracking-wide text-slate-950 serif-heading">Nama Lengkap</h1>
            <p id="view-title" class="text-sm sm:text-base font-semibold text-slate-700 mt-0.5">Target Posisi / Profesi</p>
            
            <!-- CONTACT DETAILS -->
            <div id="view-contact" class="flex flex-wrap justify-center items-center gap-x-3 gap-y-1 text-xs text-slate-600 mt-2 font-medium">
              <span id="view-email">email@anda.com</span>
              <span>•</span>
              <span id="view-phone">+62 812-xxxx-xxxx</span>
              <span>•</span>
              <span id="view-location">Kota, Negara</span>
              <span id="sep-linkedin">•</span>
              <span id="view-linkedin">linkedin.com/in/...</span>
              <span id="sep-portfolio">•</span>
              <span id="view-portfolio">website.com</span>
            </div>
          </div>

          <!-- SUMMARY SECTION -->
          <div id="section-summary" class="mt-5">
            <h2 class="text-xs font-bold uppercase tracking-wider text-slate-900 border-b border-slate-300 pb-1 mb-2">
              Ringkasan Profesional
            </h2>
            <p id="view-summary" class="text-xs leading-relaxed text-slate-800 text-justify">
              Ringkasan deskripsi Anda akan muncul di sini.
            </p>
          </div>

          <!-- EXPERIENCE SECTION -->
          <div id="section-experience" class="mt-5">
            <h2 class="text-xs font-bold uppercase tracking-wider text-slate-900 border-b border-slate-300 pb-1 mb-2">
              Pengalaman Kerja
            </h2>
            <div id="view-experience" class="space-y-3">
              <!-- Render dynamic experiences -->
            </div>
          </div>

          <!-- EDUCATION SECTION -->
          <div id="section-education" class="mt-5">
            <h2 class="text-xs font-bold uppercase tracking-wider text-slate-900 border-b border-slate-300 pb-1 mb-2">
              Pendidikan
            </h2>
            <div id="view-education" class="space-y-2">
              <!-- Render dynamic education -->
            </div>
          </div>

          <!-- SKILLS SECTION -->
          <div id="section-skills" class="mt-5">
            <h2 class="text-xs font-bold uppercase tracking-wider text-slate-900 border-b border-slate-300 pb-1 mb-2">
              Keahlian & Kompetensi
            </h2>
            <div id="view-skills" class="text-xs leading-relaxed text-slate-800">
              <!-- Render skills -->
            </div>
          </div>

        </div>

      </div>

    </div>
  </main>

  <!-- PRODUK DIGITAL GAEKS -->
  <section id="products" class="max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-16 border-t border-slate-900">
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-white tracking-tight">Produk Digital GAEKS Lainnya</h2>
      <p class="text-xs sm:text-sm text-slate-400 mt-1">Layanan terpadu pendukung pertumbuhan bisnis digital.</p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="p-5 rounded-xl bg-slate-900/60 border border-slate-800">
        <h3 class="font-bold text-white text-base">E-Book Bisnis</h3>
        <p class="text-xs text-slate-400 mt-1">Panduan praktis sistem ekspor-impor, logistik, dan scale-up bisnis mandiri.</p>
      </div>
      <div class="p-5 rounded-xl bg-slate-900/60 border border-slate-800">
        <h3 class="font-bold text-white text-base">Website Builder Service</h3>
        <p class="text-xs text-slate-400 mt-1">Landing page, company profile, dan aplikasi web siap pakai mulai Rp 499rb.</p>
      </div>
      <div class="p-5 rounded-xl bg-slate-900/60 border border-slate-800">
        <h3 class="font-bold text-white text-base">Social Media Marketing</h3>
        <p class="text-xs text-slate-400 mt-1">Panel promosi sosial media untuk akselerasi jangkauan merek Anda.</p>
      </div>
    </div>
  </section>

  <!-- FOOTER -->
  <footer class="border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-500">
    <p>&copy; 2026 GAEKS DIGITAL PRODUCT. Format CV dioptimalkan untuk standar Applicant Tracking System (ATS).</p>
  </footer>

  <!-- SCRIPT LOGIKA CV MAKER -->
  <script>
    // State data dinamis
    let experiences = [];
    let educations = [];

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
      // Experience Form
      const expContainer = document.getElementById('experience-list');
      expContainer.innerHTML = '';
      experiences.forEach((exp, i) => {
        expContainer.innerHTML += `
          <div class="p-3 bg-slate-950/80 rounded-lg border border-slate-800 relative space-y-2">
            <button onclick="removeExperience(${i})" class="absolute top-2 right-2 text-xs text-rose-400 hover:text-rose-300">Hapus</button>
            <div class="grid grid-cols-2 gap-2">
              <input type="text" placeholder="Posisi / Role" value="${exp.role}" oninput="experiences[${i}].role = this.value; renderCV()" class="px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded text-white" />
              <input type="text" placeholder="Perusahaan" value="${exp.company}" oninput="experiences[${i}].company = this.value; renderCV()" class="px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded text-white" />
            </div>
            <div class="grid grid-cols-2 gap-2">
              <input type="text" placeholder="Periode (mis: 2023 - Sekarang)" value="${exp.period}" oninput="experiences[${i}].period = this.value; renderCV()" class="px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded text-white" />
              <input type="text" placeholder="Lokasi (mis: Jakarta)" value="${exp.location}" oninput="experiences[${i}].location = this.value; renderCV()" class="px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded text-white" />
            </div>
            <textarea rows="3" placeholder="Pencapaian (gunakan bullet * atau baris baru)" oninput="experiences[${i}].desc = this.value; renderCV()" class="w-full px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded text-white">${exp.desc}</textarea>
          </div>
        `;
      });

      // Education Form
      const eduContainer = document.getElementById('education-list');
      eduContainer.innerHTML = '';
      educations.forEach((edu, i) => {
        eduContainer.innerHTML += `
          <div class="p-3 bg-slate-950/80 rounded-lg border border-slate-800 relative space-y-2">
            <button onclick="removeEducation(${i})" class="absolute top-2 right-2 text-xs text-rose-400 hover:text-rose-300">Hapus</button>
            <div class="grid grid-cols-2 gap-2">
              <input type="text" placeholder="Gelar / Jurusan" value="${edu.degree}" oninput="educations[${i}].degree = this.value; renderCV()" class="px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded text-white" />
              <input type="text" placeholder="Nama Kampus / Sekolah" value="${edu.school}" oninput="educations[${i}].school = this.value; renderCV()" class="px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded text-white" />
            </div>
            <div class="grid grid-cols-2 gap-2">
              <input type="text" placeholder="Tahun (mis: 2018 - 2022)" value="${edu.period}" oninput="educations[${i}].period = this.value; renderCV()" class="px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded text-white" />
              <input type="text" placeholder="IPK / Keterangan (mis: IPK 3.80 / 4.00)" value="${edu.details}" oninput="educations[${i}].details = this.value; renderCV()" class="px-2.5 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded text-white" />
            </div>
          </div>
        `;
      });
    }

    function renderCV() {
      // Personal
      document.getElementById('view-name').innerText = document.getElementById('input-name').value || 'NAMA LENGKAP ANDA';
      document.getElementById('view-title').innerText = document.getElementById('input-title').value || 'Target Posisi / Profesi';
      document.getElementById('view-email').innerText = document.getElementById('input-email').value || 'nama@email.com';
      document.getElementById('view-phone').innerText = document.getElementById('input-phone').value || '+62 8xx-xxxx-xxxx';
      document.getElementById('view-location').innerText = document.getElementById('input-location').value || 'Kota, Negara';

      const linkedin = document.getElementById('input-linkedin').value;
      const linkedinEl = document.getElementById('view-linkedin');
      const linkedinSep = document.getElementById('sep-linkedin');
      if (linkedin) {
        linkedinEl.innerText = linkedin;
        linkedinEl.style.display = 'inline';
        linkedinSep.style.display = 'inline';
      } else {
        linkedinEl.style.display = 'none';
        linkedinSep.style.display = 'none';
      }

      const portfolio = document.getElementById('input-portfolio').value;
      const portEl = document.getElementById('view-portfolio');
      const portSep = document.getElementById('sep-portfolio');
      if (portfolio) {
        portEl.innerText = portfolio;
        portEl.style.display = 'inline';
        portSep.style.display = 'inline';
      } else {
        portEl.style.display = 'none';
        portSep.style.display = 'none';
      }

      // Summary
      const summaryText = document.getElementById('input-summary').value;
      document.getElementById('view-summary').innerText = summaryText || 'Ringkasan profesional Anda akan ditampilkan di sini.';

      // Experience View
      const expView = document.getElementById('view-experience');
      expView.innerHTML = '';
      if (experiences.length === 0) {
        expView.innerHTML = '<p class="text-xs text-slate-400 italic">Belum ada pengalaman kerja yang ditambahkan.</p>';
      } else {
        experiences.forEach(exp => {
          // Format bullet points
          const bulletPoints = exp.desc
            .split('\n')
            .filter(line => line.trim() !== '')
            .map(line => `<li class="ml-4 list-disc">${line.replace(/^[*-]\s*/, '')}</li>`)
            .join('');

          expView.innerHTML += `
            <div class="mb-3">
              <div class="flex justify-between items-baseline text-xs">
                <span class="font-bold text-slate-900">${exp.role || 'Jabatan'} <span class="font-semibold text-slate-700">| ${exp.company || 'Perusahaan'}</span></span>
                <span class="font-medium text-slate-600">${exp.period || 'Periode'}</span>
              </div>
              <div class="text-[11px] text-slate-500 italic mb-1">${exp.location || ''}</div>
              <ul class="text-xs leading-relaxed text-slate-800 space-y-0.5">
                ${bulletPoints || '<li>Pencapaian kerja...</li>'}
              </ul>
            </div>
          `;
        });
      }

      // Education View
      const eduView = document.getElementById('view-education');
      eduView.innerHTML = '';
      if (educations.length === 0) {
        eduView.innerHTML = '<p class="text-xs text-slate-400 italic">Belum ada riwayat pendidikan yang ditambahkan.</p>';
      } else {
        educations.forEach(edu => {
          eduView.innerHTML += `
            <div class="flex justify-between items-baseline text-xs mb-1">
              <div>
                <span class="font-bold text-slate-900">${edu.school || 'Institusi / Universitas'}</span>
                <span class="text-slate-700"> — ${edu.degree || 'Gelar'}</span>
                ${edu.details ? `<div class="text-[11px] text-slate-600">${edu.details}</div>` : ''}
              </div>
              <span class="font-medium text-slate-600 text-xs">${edu.period || ''}</span>
            </div>
          `;
        });
      }

      // Skills View
      const skillsRaw = document.getElementById('input-skills').value;
      const skillsView = document.getElementById('view-skills');
      if (skillsRaw.trim()) {
        const list = skillsRaw.split(',').map(s => s.trim()).filter(Boolean);
        skillsView.innerHTML = `<strong>Keahlian Teknis & Inti:</strong> ` + list.join(' • ');
      } else {
        skillsView.innerHTML = 'Keahlian teknis dan kompetensi utama akan terdaftar di sini.';
      }
    }

    function loadSampleData() {
      document.getElementById('input-name').value = "Denyt Yudhanusa, S.T.";
      document.getElementById('input-title').value = "Lead Operations & Digital Logistics Specialist";
      document.getElementById('input-email').value = "contact@gaeks.com";
      document.getElementById('input-phone').value = "+62 812-3456-7890";
      document.getElementById('input-location').value = "Jakarta, Indonesia";
      document.getElementById('input-linkedin').value = "linkedin.com/in/gaeks-operations";
      document.getElementById('input-portfolio').value = "gdp.gaeks.com";

      document.getElementById('input-summary').value = 
        "Praktisi operasional logistik dan transformasi digital dengan pengalaman lebih dari 6 tahun dalam pengelolaan freight forwarding internasional, automasi rantai pasok, dan digitalisasi ERP. Berhasil mengefisiensikan biaya pengiriman kargo laut dan udara hingga 18% serta mengimplementasikan sistem manajemen terpadu untuk ratusan klien B2B.";

      experiences = [
        {
          role: "Head of Freight Forwarding Operations",
          company: "GAEKS FREIGHT INTERNATIONAL",
          period: "2022 - Sekarang",
          location: "Jakarta, Indonesia",
          desc: "Memimpin operasional kepabeanan (customs clearance), rute ekspor-impor laut (FCL/LCL) dan udara.\nMengembangkan sistem integrasi pelacakan kontainer dan negosiasi tarif dengan shipping lines global, menghasilkan penghematan biaya logistik sebesar 14% per tahun.\nMengawasi kepatuhan regulasi kepabeanan dengan tingkat akurasi dokumen mencapai 99.8%."
        },
        {
          role: "Senior Logistics Coordinator",
          company: "PT Yudhanusa Ekspresindo",
          period: "2019 - 2022",
          location: "Tangerang, Banten",
          desc: "Mengkoordinasikan pergerakan armada trucking darat dan jadwal muat kontainer pelabuhan.\nMeningkatkan efisiensi SLA pengiriman barang antarpulau dari 91% menjadi 98.5%.\nMengelola operasional pergudangan dan audit stok bulanan untuk komoditas industri."
        }
      ];

      educations = [
        {
          degree: "Sarjana Teknik Industri (S.T.)",
          school: "Universitas Indonesia",
          period: "2015 - 2019",
          details: "IPK 3.82 / 4.00 (Cum Laude) • Fokus Rantai Pasok & Manajemen Operasi"
        }
      ];

      document.getElementById('input-skills').value = 
        "International Freight Forwarding, Supply Chain Management, Customs Clearance, Enterprise Resource Planning (ERP), Sea & Air Cargo, Negosiasi Kontrak, Data Analysis, Leadership";

      renderFormLists();
      renderCV();
    }

    function resetForm() {
      document.querySelectorAll('input, textarea').forEach(el => el.value = '');
      experiences = [];
      educations = [];
      renderFormLists();
      renderCV();
    }

    // Inisialisasi awal dengan contoh data
    window.onload = function() {
      loadSampleData();
    };
  </script>
</body>
</html>
HTML_EOF

echo "=== 2. Melakukan Commit & Push ke GitHub ==="
git add index.html
git commit -m "feat: implement ATS CV Maker studio and direct access without login"
git push origin main

echo "=== Sukses di-push! Hostinger akan meng-update gdp.gaeks.com secara otomatis ==="
