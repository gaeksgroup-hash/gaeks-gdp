#!/bin/bash
set -e

echo "=== 1. Membuat Halaman Khusus CV: cv.html ==="

cat << 'HTML_CV' > cv.html
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>ATS CV Maker | GAEKS DIGITAL PRODUCT</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Merriweather:wght@400;700&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Inter', sans-serif; }
    .serif-heading { font-family: 'Merriweather', serif; }
    
    @media print {
      body * { visibility: hidden; }
      #cv-preview-sheet, #cv-preview-sheet * { visibility: visible; }
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
      @page { size: A4; margin: 0; }
    }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 antialiased min-h-screen flex flex-col justify-between">

  <!-- NAVBAR -->
  <header class="sticky top-0 z-40 w-full backdrop-blur-md bg-slate-950/90 border-b border-slate-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <a href="index.html" class="text-sm font-semibold text-slate-400 hover:text-white flex items-center gap-1 transition">
          &larr; Beranda
        </a>
        <span class="text-slate-600">|</span>
        <span class="text-lg font-bold tracking-tight text-white">
          Studio CV ATS
        </span>
      </div>
      <div class="flex items-center space-x-2">
        <button onclick="window.print()" class="px-4 py-2 text-xs sm:text-sm font-bold rounded-lg bg-blue-600 hover:bg-blue-500 text-white transition shadow-sm">
          Download PDF (ATS)
        </button>
      </div>
    </div>
  </header>

  <!-- STUDIO WORKSPACE -->
  <main class="max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex flex-col md:flex-row md:items-center justify-between pb-6 mb-6 border-b border-slate-800 gap-4">
      <div>
        <h1 class="text-2xl sm:text-3xl font-bold text-white tracking-tight">ATS Resume & CV Builder</h1>
        <p class="text-xs sm:text-sm text-slate-400 mt-1">Isi data di sebelah kiri, pratinjau lembar A4 ATS di sebelah kanan otomatis ter-update.</p>
      </div>
      <div class="flex flex-wrap items-center gap-2">
        <button onclick="loadSampleData()" class="px-3 py-2 text-xs font-semibold rounded-lg bg-indigo-950 text-indigo-300 hover:bg-indigo-900 border border-indigo-700/60 transition">
          Muat Contoh Data
        </button>
        <button onclick="resetForm()" class="px-3 py-2 text-xs font-semibold rounded-lg bg-slate-900 text-slate-400 hover:text-white border border-slate-800 transition">
          Kosongkan Form
        </button>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
      <!-- FORM INPUT -->
      <div class="lg:col-span-5 space-y-6 bg-slate-900/90 p-5 sm:p-6 rounded-2xl border border-slate-800 max-h-[85vh] overflow-y-auto">
        <div>
          <h2 class="text-sm font-bold uppercase tracking-wider text-blue-400 mb-3">1. Data Pribadi & Kontak</h2>
          <div class="space-y-3">
            <div>
              <label class="block text-xs text-slate-400 mb-1">Nama Lengkap & Gelar</label>
              <input type="text" id="input-name" oninput="renderCV()" class="w-full px-3 py-2 text-sm bg-slate-950 border border-slate-800 rounded-lg text-white" />
            </div>
            <div>
              <label class="block text-xs text-slate-400 mb-1">Target Posisi / Profesi</label>
              <input type="text" id="input-title" oninput="renderCV()" class="w-full px-3 py-2 text-sm bg-slate-950 border border-slate-800 rounded-lg text-white" />
            </div>
            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="block text-xs text-slate-400 mb-1">Email</label>
                <input type="email" id="input-email" oninput="renderCV()" class="w-full px-3 py-2 text-sm bg-slate-950 border border-slate-800 rounded-lg text-white" />
              </div>
              <div>
                <label class="block text-xs text-slate-400 mb-1">Nomor Telepon</label>
                <input type="text" id="input-phone" oninput="renderCV()" class="w-full px-3 py-2 text-sm bg-slate-950 border border-slate-800 rounded-lg text-white" />
              </div>
            </div>
            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="block text-xs text-slate-400 mb-1">Domisili (Kota, Negara)</label>
                <input type="text" id="input-location" oninput="renderCV()" class="w-full px-3 py-2 text-sm bg-slate-950 border border-slate-800 rounded-lg text-white" />
              </div>
              <div>
                <label class="block text-xs text-slate-400 mb-1">LinkedIn URL</label>
                <input type="text" id="input-linkedin" oninput="renderCV()" class="w-full px-3 py-2 text-sm bg-slate-950 border border-slate-800 rounded-lg text-white" />
              </div>
            </div>
            <div>
              <label class="block text-xs text-slate-400 mb-1">Portfolio / Website</label>
              <input type="text" id="input-portfolio" oninput="renderCV()" class="w-full px-3 py-2 text-sm bg-slate-950 border border-slate-800 rounded-lg text-white" />
            </div>
          </div>
        </div>

        <hr class="border-slate-800" />

        <div>
          <h2 class="text-sm font-bold uppercase tracking-wider text-blue-400 mb-2">2. Ringkasan Profesional</h2>
          <textarea id="input-summary" rows="3" oninput="renderCV()" class="w-full px-3 py-2 text-sm bg-slate-950 border border-slate-800 rounded-lg text-white"></textarea>
        </div>

        <hr class="border-slate-800" />

        <div>
          <div class="flex items-center justify-between mb-2">
            <h2 class="text-sm font-bold uppercase tracking-wider text-blue-400">3. Pengalaman Kerja</h2>
            <button onclick="addExperience()" class="text-xs px-2.5 py-1 bg-blue-950 text-blue-300 hover:bg-blue-900 rounded border border-blue-800">+ Tambah</button>
          </div>
          <div id="experience-list" class="space-y-4"></div>
        </div>

        <hr class="border-slate-800" />

        <div>
          <div class="flex items-center justify-between mb-2">
            <h2 class="text-sm font-bold uppercase tracking-wider text-blue-400">4. Pendidikan</h2>
            <button onclick="addEducation()" class="text-xs px-2.5 py-1 bg-blue-950 text-blue-300 hover:bg-blue-900 rounded border border-blue-800">+ Tambah</button>
          </div>
          <div id="education-list" class="space-y-4"></div>
        </div>

        <hr class="border-slate-800" />

        <div>
          <h2 class="text-sm font-bold uppercase tracking-wider text-blue-400 mb-2">5. Keahlian (Skills)</h2>
          <p class="text-[11px] text-slate-500 mb-2">Pisahkan dengan tanda koma.</p>
          <textarea id="input-skills" rows="2" oninput="renderCV()" class="w-full px-3 py-2 text-sm bg-slate-950 border border-slate-800 rounded-lg text-white"></textarea>
        </div>
      </div>

      <!-- PREVIEW A4 SHEET -->
      <div class="lg:col-span-7 flex flex-col items-center">
        <div class="w-full flex justify-between items-center mb-2 px-2 text-xs text-slate-400">
          <span>Pratinjau Lembar A4 (Format ATS Standar)</span>
          <button onclick="window.print()" class="text-blue-400 hover:underline">Unduh PDF</button>
        </div>

        <div id="cv-preview-sheet" class="w-full bg-white text-slate-900 shadow-2xl rounded-sm p-8 sm:p-12 min-h-[850px] border border-slate-200">
          <div class="border-b-2 border-slate-900 pb-4 text-center">
            <h1 id="view-name" class="text-2xl sm:text-3xl font-bold uppercase tracking-wide text-slate-950 serif-heading">NAMA LENGKAP</h1>
            <p id="view-title" class="text-sm sm:text-base font-semibold text-slate-700 mt-0.5">Target Posisi</p>
            <div id="view-contact" class="flex flex-wrap justify-center items-center gap-x-3 gap-y-1 text-xs text-slate-600 mt-2 font-medium">
              <span id="view-email">email@anda.com</span>
              <span>•</span>
              <span id="view-phone">+62 8xx</span>
              <span>•</span>
              <span id="view-location">Kota, Negara</span>
              <span id="sep-linkedin">•</span>
              <span id="view-linkedin">linkedin.com</span>
              <span id="sep-portfolio">•</span>
              <span id="view-portfolio">portfolio.com</span>
            </div>
          </div>

          <div id="section-summary" class="mt-5">
            <h2 class="text-xs font-bold uppercase tracking-wider text-slate-900 border-b border-slate-300 pb-1 mb-2">Ringkasan Profesional</h2>
            <p id="view-summary" class="text-xs leading-relaxed text-slate-800 text-justify"></p>
          </div>

          <div id="section-experience" class="mt-5">
            <h2 class="text-xs font-bold uppercase tracking-wider text-slate-900 border-b border-slate-300 pb-1 mb-2">Pengalaman Kerja</h2>
            <div id="view-experience" class="space-y-3"></div>
          </div>

          <div id="section-education" class="mt-5">
            <h2 class="text-xs font-bold uppercase tracking-wider text-slate-900 border-b border-slate-300 pb-1 mb-2">Pendidikan</h2>
            <div id="view-education" class="space-y-2"></div>
          </div>

          <div id="section-skills" class="mt-5">
            <h2 class="text-xs font-bold uppercase tracking-wider text-slate-900 border-b border-slate-300 pb-1 mb-2">Keahlian & Kompetensi</h2>
            <div id="view-skills" class="text-xs leading-relaxed text-slate-800"></div>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-500">
    <p>&copy; 2026 GAEKS DIGITAL PRODUCT. Standar Format ATS.</p>
  </footer>

  <script>
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
      const expContainer = document.getElementById('experience-list');
      expContainer.innerHTML = '';
      experiences.forEach((exp, i) => {
        expContainer.innerHTML += `
          <div class="p-3 bg-slate-950/80 rounded-lg border border-slate-800 relative space-y-2">
            <button onclick="removeExperience(${i})" class="absolute top-2 right-2 text-xs text-rose-400">Hapus</button>
            <div class="grid grid-cols-2 gap-2">
              <input type="text" placeholder="Posisi" value="${exp.role}" oninput="experiences[${i}].role = this.value; renderCV()" class="px-2 py-1 text-xs bg-slate-900 border border-slate-800 rounded text-white" />
              <input type="text" placeholder="Perusahaan" value="${exp.company}" oninput="experiences[${i}].company = this.value; renderCV()" class="px-2 py-1 text-xs bg-slate-900 border border-slate-800 rounded text-white" />
            </div>
            <div class="grid grid-cols-2 gap-2">
              <input type="text" placeholder="Periode" value="${exp.period}" oninput="experiences[${i}].period = this.value; renderCV()" class="px-2 py-1 text-xs bg-slate-900 border border-slate-800 rounded text-white" />
              <input type="text" placeholder="Lokasi" value="${exp.location}" oninput="experiences[${i}].location = this.value; renderCV()" class="px-2 py-1 text-xs bg-slate-900 border border-slate-800 rounded text-white" />
            </div>
            <textarea rows="3" placeholder="Poin pencapaian (pisahkan per baris)" oninput="experiences[${i}].desc = this.value; renderCV()" class="w-full px-2 py-1 text-xs bg-slate-900 border border-slate-800 rounded text-white">${exp.desc}</textarea>
          </div>
        `;
      });

      const eduContainer = document.getElementById('education-list');
      eduContainer.innerHTML = '';
      educations.forEach((edu, i) => {
        eduContainer.innerHTML += `
          <div class="p-3 bg-slate-950/80 rounded-lg border border-slate-800 relative space-y-2">
            <button onclick="removeEducation(${i})" class="absolute top-2 right-2 text-xs text-rose-400">Hapus</button>
            <div class="grid grid-cols-2 gap-2">
              <input type="text" placeholder="Gelar/Jurusan" value="${edu.degree}" oninput="educations[${i}].degree = this.value; renderCV()" class="px-2 py-1 text-xs bg-slate-900 border border-slate-800 rounded text-white" />
              <input type="text" placeholder="Kampus/Sekolah" value="${edu.school}" oninput="educations[${i}].school = this.value; renderCV()" class="px-2 py-1 text-xs bg-slate-900 border border-slate-800 rounded text-white" />
            </div>
            <div class="grid grid-cols-2 gap-2">
              <input type="text" placeholder="Tahun" value="${edu.period}" oninput="educations[${i}].period = this.value; renderCV()" class="px-2 py-1 text-xs bg-slate-900 border border-slate-800 rounded text-white" />
              <input type="text" placeholder="Keterangan / IPK" value="${edu.details}" oninput="educations[${i}].details = this.value; renderCV()" class="px-2 py-1 text-xs bg-slate-900 border border-slate-800 rounded text-white" />
            </div>
          </div>
        `;
      });
    }

    function renderCV() {
      document.getElementById('view-name').innerText = document.getElementById('input-name').value || 'NAMA LENGKAP';
      document.getElementById('view-title').innerText = document.getElementById('input-title').value || 'Target Posisi';
      document.getElementById('view-email').innerText = document.getElementById('input-email').value || 'email@anda.com';
      document.getElementById('view-phone').innerText = document.getElementById('input-phone').value || '+62 8xx';
      document.getElementById('view-location').innerText = document.getElementById('input-location').value || 'Kota, Negara';

      const linkedin = document.getElementById('input-linkedin').value;
      const linkedinEl = document.getElementById('view-linkedin');
      const sepLinkedin = document.getElementById('sep-linkedin');
      linkedinEl.innerText = linkedin;
      linkedinEl.style.display = linkedin ? 'inline' : 'none';
      sepLinkedin.style.display = linkedin ? 'inline' : 'none';

      const portfolio = document.getElementById('input-portfolio').value;
      const portEl = document.getElementById('view-portfolio');
      const sepPort = document.getElementById('sep-portfolio');
      portEl.innerText = portfolio;
      portEl.style.display = portfolio ? 'inline' : 'none';
      sepPort.style.display = portfolio ? 'inline' : 'none';

      document.getElementById('view-summary').innerText = document.getElementById('input-summary').value || 'Ringkasan profil Anda.';

      const expView = document.getElementById('view-experience');
      expView.innerHTML = '';
      experiences.forEach(exp => {
        const points = exp.desc.split('\n').filter(l => l.trim()).map(l => `<li class="ml-4 list-disc">${l.replace(/^[*-]\s*/, '')}</li>`).join('');
        expView.innerHTML += `
          <div class="mb-3">
            <div class="flex justify-between text-xs font-bold text-slate-900">
              <span>${exp.role || 'Jabatan'} <span class="font-semibold text-slate-700">| ${exp.company || 'Perusahaan'}</span></span>
              <span class="font-normal text-slate-600">${exp.period || ''}</span>
            </div>
            <div class="text-[11px] text-slate-500 italic">${exp.location || ''}</div>
            <ul class="text-xs leading-relaxed text-slate-800 space-y-0.5 mt-1">${points || '<li>Deskripsi tugas...</li>'}</ul>
          </div>
        `;
      });

      const eduView = document.getElementById('view-education');
      eduView.innerHTML = '';
      educations.forEach(edu => {
        eduView.innerHTML += `
          <div class="flex justify-between text-xs mb-1">
            <div>
              <span class="font-bold text-slate-900">${edu.school}</span> — <span>${edu.degree}</span>
              ${edu.details ? `<div class="text-[11px] text-slate-600">${edu.details}</div>` : ''}
            </div>
            <span class="text-slate-600">${edu.period}</span>
          </div>
        `;
      });

      const skillsRaw = document.getElementById('input-skills').value;
      document.getElementById('view-skills').innerHTML = skillsRaw.trim() 
        ? `<strong>Keahlian Utama:</strong> ` + skillsRaw.split(',').map(s => s.trim()).filter(Boolean).join(' • ')
        : 'Keahlian teknis dan kompetensi.';
    }

    function loadSampleData() {
      document.getElementById('input-name').value = "Denyt Yudhanusa, S.T.";
      document.getElementById('input-title').value = "Lead Operations & Logistics Specialist";
      document.getElementById('input-email').value = "contact@gaeks.com";
      document.getElementById('input-phone').value = "+62 812-3456-7890";
      document.getElementById('input-location').value = "Jakarta, Indonesia";
      document.getElementById('input-linkedin').value = "linkedin.com/in/gaeks";
      document.getElementById('input-portfolio').value = "gaeks.com";
      document.getElementById('input-summary').value = "Profesional operasional logistik dan sistem ERP dengan pengalaman 6+ tahun dalam freight forwarding internasional, kepabeanan, serta efisiensi rute multimoda.";
      
      experiences = [
        {
          role: "Head of Operations",
          company: "GAEKS FREIGHT INTERNATIONAL",
          period: "2022 - Sekarang",
          location: "Jakarta",
          desc: "Mengelola customs clearance dan jalur ekspor-impor laut/udara.\nMengefisienkan biaya pengiriman kargo sebesar 14% melalui negosiasi kontrak strategis."
        }
      ];

      educations = [
        {
          degree: "Sarjana Teknik Industri",
          school: "Universitas Indonesia",
          period: "2015 - 2019",
          details: "IPK 3.82 / 4.00 (Cum Laude)"
        }
      ];

      document.getElementById('input-skills').value = "Freight Forwarding, Supply Chain, ERP, Kepabeanan, Negosiasi Kontrak";
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

    window.onload = loadSampleData;
  </script>
</body>
</html>
HTML_CV

echo "=== 2. Memperbarui index.html (Beranda Bebas Syarat Login) ==="

cat << 'HTML_HOME' > index.html
<!DOCTYPE html>
<html lang="id" class="scroll-smooth">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>GAEKS DIGITAL PRODUCT | Solusi Layanan & Produk Digital</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>body { font-family: 'Inter', sans-serif; }</style>
</head>
<body class="bg-slate-950 text-slate-100 antialiased min-h-screen flex flex-col justify-between">

  <!-- NAVBAR -->
  <header class="sticky top-0 z-40 w-full backdrop-blur-md bg-slate-950/80 border-b border-slate-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <a href="index.html" class="flex items-center space-x-2">
        <span class="text-xl font-extrabold tracking-tight bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
          GAEKS DIGITAL PRODUCT
        </span>
      </a>
      <nav class="hidden md:flex items-center space-x-8 text-sm font-medium text-slate-300">
        <a href="#services" class="hover:text-blue-400 transition">Digital Services</a>
        <a href="#products" class="hover:text-blue-400 transition">Digital Products</a>
      </nav>
      <div>
        <a href="cv.html" class="px-4 py-2 text-sm font-medium rounded-lg bg-blue-600 hover:bg-blue-500 text-white transition">
          Buka CV Maker &rarr;
        </a>
      </div>
    </div>
  </header>

  <!-- HERO SECTION -->
  <section class="py-20 px-4 sm:px-6 lg:px-8 text-center bg-gradient-to-b from-slate-900 to-slate-950">
    <div class="max-w-4xl mx-auto space-y-6">
      <span class="inline-block px-3 py-1 text-xs font-semibold text-blue-400 uppercase bg-blue-950/60 rounded-full border border-blue-800/60">
        Ekosistem Digital GAEKS
      </span>
      <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-white leading-tight">
        Akselerasi Produktivitas dengan <span class="text-blue-400">Layanan & Produk Digital</span>
      </h1>
      <p class="text-lg text-slate-400 max-w-2xl mx-auto">
        Gunakan aplikasi pembuatan CV standar ATS langsung secara gratis tanpa perlu registrasi.
      </p>
      <div class="pt-4 flex flex-wrap justify-center gap-4">
        <a href="cv.html" class="px-6 py-3 rounded-lg bg-blue-600 hover:bg-blue-500 text-white font-medium shadow-lg shadow-blue-500/20">
          Buat CV ATS Sekarang (Gratis)
        </a>
        <a href="#products" class="px-6 py-3 rounded-lg border border-slate-700 hover:bg-slate-800 text-slate-200 font-medium">
          Lihat Produk Lainnya
        </a>
      </div>
    </div>
  </section>

  <!-- DIGITAL SERVICES SECTION -->
  <section id="services" class="py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full">
    <div class="mb-10 text-center md:text-left">
      <div class="inline-block px-2.5 py-0.5 rounded text-xs font-medium bg-indigo-950 text-indigo-300 border border-indigo-800 mb-2">
        Aplikasi & Tools
      </div>
      <h2 class="text-3xl font-bold text-white tracking-tight">Digital Services</h2>
      <p class="text-slate-400 mt-1">Gunakan langsung tanpa hambatan login.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      
      <!-- CV Maker (Langsung Mengarah ke cv.html) -->
      <div class="p-8 rounded-2xl bg-slate-900 border border-blue-600/40 hover:border-blue-500 transition flex flex-col justify-between shadow-lg shadow-blue-950/30">
        <div>
          <div class="flex items-center justify-between mb-4">
            <span class="px-3 py-1 text-xs font-semibold rounded-full bg-emerald-950 text-emerald-400 border border-emerald-800">
              Langsung Aktif
            </span>
            <span class="text-xs text-slate-400">Standar ATS</span>
          </div>
          <h3 class="text-2xl font-bold text-white">CV & Resume Maker ATS</h3>
          <p class="text-slate-400 mt-2 text-sm leading-relaxed">
            Format ATS profesional dengan live preview dan ekspor PDF langsung ukuran A4. Tanpa syarat login, langsung pakai sekarang.
          </p>
        </div>
        <div class="mt-8 pt-6 border-t border-slate-800">
          <a href="cv.html" class="w-full block text-center py-3 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-sm font-bold transition">
            Buka Aplikasi CV Maker &rarr;
          </a>
        </div>
      </div>

      <!-- Gaeks Presentation -->
      <div class="p-8 rounded-2xl bg-slate-900 border border-slate-800 flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between mb-4">
            <span class="px-3 py-1 text-xs font-semibold rounded-full bg-amber-950 text-amber-400 border border-amber-800">
              Segera Hadir
            </span>
            <span class="text-xs text-slate-400">Tahap Pengembangan</span>
          </div>
          <h3 class="text-2xl font-bold text-white">Gaeks Presentation Maker</h3>
          <p class="text-slate-400 mt-2 text-sm leading-relaxed">
            Tool pembuatan presentasi otomatis dan pitch deck terstruktur yang akan segera dirilis.
          </p>
        </div>
        <div class="mt-8 pt-6 border-t border-slate-800">
          <button disabled class="w-full py-3 rounded-lg bg-slate-800 text-slate-500 text-sm font-medium cursor-not-allowed">
            Dalam Proses Pengembangan
          </button>
        </div>
      </div>

    </div>
  </section>

  <!-- PRODUCTS SECTION -->
  <section id="products" class="py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full border-t border-slate-900">
    <div class="mb-10 text-center md:text-left">
      <h2 class="text-2xl font-bold text-white tracking-tight">Katalog Produk Digital</h2>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="p-6 rounded-2xl bg-slate-900/60 border border-slate-800">
        <h3 class="font-bold text-white text-lg">E-Book Bisnis</h3>
        <p class="text-slate-400 text-xs mt-2">Daftar buku digital ekspor-impor, logistik, dan otomasi kerja mandiri.</p>
      </div>
      <div class="p-6 rounded-2xl bg-slate-900/60 border border-slate-800">
        <h3 class="font-bold text-white text-lg">Website Builder</h3>
        <p class="text-slate-400 text-xs mt-2">Pricelist landing page (499rb), portfolio (999rb), dan custom app.</p>
      </div>
      <div class="p-6 rounded-2xl bg-slate-900/60 border border-slate-800">
        <h3 class="font-bold text-white text-lg">Social Media Marketing</h3>
        <p class="text-slate-400 text-xs mt-2">Panel layanan promosi dan optimasi jangkauan brand.</p>
        <a href="https://gaeks.com" target="_blank" class="text-blue-400 hover:underline text-xs mt-4 inline-block">Kunjungi Website SMM &rarr;</a>
      </div>
    </div>
  </section>

  <!-- FOOTER -->
  <footer class="border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-500">
    <p>&copy; 2026 GAEKS DIGITAL PRODUCT. Seluruh hak cipta dilindungi.</p>
  </footer>
</body>
</html>
HTML_HOME

echo "=== 3. Melakukan Commit & Push ke GitHub ==="
git add cv.html index.html
git commit -m "feat: separate dedicated cv.html page and remove login completely"
git push origin main

echo "=== Selesai di-push! ==="
