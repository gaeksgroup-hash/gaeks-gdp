# GDP Presentation Maker Flow

## Detected Presentation Files
```text
./api/presentation.php
./docs/GDP_PRESENTATION_FLOW.md
./presentation.html
```

## Storage / API / Export Evidence
```text
15:    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
16:    <script src="https://cdn.jsdelivr.net/gh/gitbrent/PptxGenJS/dist/pptxgen.bundle.js"></script>
46:        .anim-slide-up { animation: slideUp 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards; opacity: 0; transform: translateY(40px); }
47:        .anim-slide-left { animation: slideLeft 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards; opacity: 0; transform: translateX(-40px); }
52:        @keyframes slideUp { to { opacity: 1; transform: translateY(0); } }
53:        @keyframes slideLeft { to { opacity: 1; transform: translateX(0); } }
96:        .toast-enter { animation: slideInRight 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
98:        @keyframes slideInRight { from { transform: translateX(120%); opacity: 0; } to { transform: translateX(0); } }
105:        body.exporting-mode * {
110:        .pdf-background-render {
181:                    <p class="text-xs sm:text-sm text-slate-500 mt-1">Platform pembuatan slide presentasi pitch deck investor dan materi meeting eksekutif.</p>
193:                    <button onclick="runNativePPTXExport()" class="bg-[#d04423] hover:bg-[#b8381b] text-white px-5 py-2 rounded-lg font-bold text-sm shadow-md transition-all cursor-pointer flex items-center gap-2">📊 Download PPTX</button>
194:                    <button onclick="runNativePDFExport()" class="bg-indigo-600 hover:bg-indigo-500 text-white px-5 py-2 rounded-lg font-bold text-sm shadow-md transition-all cursor-pointer flex items-center gap-2">📄 Download PDF</button>
196:                    <button onclick="switchView('presentation')" class="bg-blue-500 hover:bg-blue-400 text-white px-5 py-2 rounded-lg font-bold text-sm shadow-md transition-colors cursor-pointer ml-2">📺 Play Presentation</button>
201:            <button onclick="addSlide()" class="fixed bottom-10 right-10 z-[100] bg-accent hover:bg-blue-600 text-white px-6 py-4 rounded-full font-extrabold shadow-[0_10px_30px_rgba(59,130,246,0.5)] transition-transform hover:scale-110 flex items-center gap-2 border-2 border-white cursor-pointer">
202:                + Tambah Slide Baru
225:                    <h3 id="anchorManajemenSlide" class="text-xl font-bold text-slate-800 scroll-mt-28">Manajemen Halaman (Slide)</h3>
226:                    <p class="text-xs text-slate-500">*Gunakan mode 'Play Presentation' untuk menambahkan Notes MOM.</p>
228:                <div id="slidesFormContainer" class="space-y-8 pb-20"></div>
238:                <div id="presHeader" class="border-b-2 border-slate-200 pb-4 mb-4 flex justify-between items-start transition-opacity anim-slide-up flex-shrink-0 z-50 bg-slate-50">
251:                            <img id="presCoverLogo" src="" alt="Logo" class="anim-slide-up h-24 md:h-32 mb-10 object-contain drop-shadow-[0_10px_20px_rgba(0,0,0,0.6)] brightness-110" onerror="this.style.display='none'" style="animation-delay: 200ms;">
252:                            <h1 id="presCoverTitle" class="anim-slide-up text-5xl md:text-[5.5rem] font-serif font-extrabold mb-8 leading-[1.1] tracking-tight text-center text-white drop-shadow-[0_10px_20px_rgba(0,0,0,0.5)]" style="animation-delay: 400ms;"></h1>
254:                            <div id="presCoverMeta" class="anim-slide-up flex flex-wrap justify-center items-center gap-x-6 gap-y-3 text-lg md:text-xl font-sans font-medium tracking-wide bg-black/30 px-8 py-3.5 rounded-full border border-white/10 backdrop-blur-md shadow-2xl" style="animation-delay: 800ms;"></div>
259:                        <div class="anim-slide-left sticky top-0 bg-slate-50 z-40 pt-2 pb-4 mb-8">
268:                            <h1 id="presSlideTitle" class="text-[3rem] font-extrabold text-brand leading-tight w-full anim-slide-up pb-2"></h1>
271:                        <div id="presSlideGrid" class="grid gap-12 items-start w-full flex-grow">
272:                            <div id="presSlideTextCol" class="w-full">
273:                                <ul id="presSlideBullets" class="w-full"></ul>
275:                            <div id="presSlideVisual" class="w-full hidden h-full anim-zoom-in" style="animation-delay: 300ms;"></div>
280:                        <div class="anim-slide-left sticky top-0 bg-slate-50 z-40 pt-2 pb-4 mb-8 border-b-2 border-slate-200">
295:                            <h1 class="anim-slide-up text-5xl md:text-[5.5rem] font-serif font-extrabold text-transparent bg-clip-text bg-gradient-to-br from-white via-slate-100 to-slate-400 mb-6 tracking-tight drop-shadow-lg" style="animation-delay: 200ms;">Thank You.</h1>
297:                            <p id="dynamicClosingText" class="anim-slide-up text-base md:text-lg text-slate-300 font-medium mb-10 w-full leading-relaxed text-center font-sans tracking-wide whitespace-pre-line" style="animation-delay: 600ms;"></p>
298:                            <button onclick="goToSlide(1); event.stopPropagation();" class="anim-slide-up group relative inline-flex items-center justify-center px-10 py-3.5 font-bold text-brand transition-all duration-300 bg-champagne font-sans rounded-xl hover:bg-white hover:-translate-y-1 focus:outline-none overflow-hidden cursor-pointer shadow-[0_15px_30px_rgba(212,175,55,0.4)]" style="animation-delay: 800ms;">
306:                <div id="presFooter" class="flex justify-between items-center text-slate-400 font-bold border-t border-slate-200 pt-4 mb-4 mt-2 transition-opacity anim-slide-up delay-200 flex-shrink-0 z-50 bg-slate-50 relative">
310:                        <div id="noteDrawer" class="hidden absolute bottom-full right-0 mb-4 w-[450px] bg-brand/95 border border-white/10 backdrop-blur-3xl rounded-[2rem] shadow-[0_30px_60px_rgba(0,0,0,0.6)] p-7 anim-slide-up origin-bottom-right transition-all duration-300">
344:                const raw = localStorage.getItem('gaeks_user_session_v3') || localStorage.getItem('gaeks_user_session_v2') || localStorage.getItem('gaeks_user_session');
354:            const raw = localStorage.getItem(GAEKS_PRES_LIST_KEY());
363:                        localStorage.removeItem(GAEKS_PRES_ITEM_KEY(m.id));
374:                localStorage.setItem(GAEKS_PRES_ITEM_KEY(starter.id), JSON.stringify(starter));
379:                localStorage.setItem(GAEKS_PRES_LIST_KEY(), JSON.stringify(filtered));
398:            localStorage.setItem(GAEKS_PRES_LIST_KEY(), JSON.stringify(list));
399:            localStorage.setItem(GAEKS_PRES_ITEM_KEY(data.id), JSON.stringify(data));
404:            const raw = localStorage.getItem(GAEKS_PRES_ITEM_KEY(id));
413:                    localStorage.removeItem(GAEKS_PRES_ITEM_KEY(id));
420:                localStorage.setItem(GAEKS_PRES_LIST_KEY(), JSON.stringify(list));
433:                slides: [
527:        window.exportJob = { active: false, paused: false, cancelled: false, id: 'exportToastMain', percent: 0, text: '' };
532:        let currentSlideIndex = 0;
559:            if(window.exportJob.active || presView.classList.contains('hidden')) return;
577:                if (x < screenWidth * 0.3) prevSlide(); else nextSlide();
602:        window.togglePauseExport = function() { window.exportJob.paused = !window.exportJob.paused; updateExportToastUI(); };
603:        window.cancelExport = function() { window.exportJob.cancelled = true; window.exportJob.paused = false; updateExportToastUI(); };
605:        function updateExportToastUI() {
606:            const toast = document.getElementById(window.exportJob.id);
609:            const pauseText = window.exportJob.paused ? '▶ Resume' : '⏸ Pause';
610:            const pauseClass = window.exportJob.paused ? 'bg-emerald-100 text-emerald-700 hover:bg-emerald-200' : 'bg-amber-100 text-amber-700 hover:bg-amber-200';
611:            const spinClass = window.exportJob.paused ? '' : 'animate-spin';
612:            const statusLabel = window.exportJob.paused ? 'Menunggu (Paused)...' : 'Mengekspor Dokumen';
620:                    <span class="text-xs font-black text-indigo-500 bg-indigo-50 px-2 py-0.5 rounded">${window.exportJob.percent}%</span>
622:                <p class="text-[11px] text-slate-500 font-medium leading-tight">${window.exportJob.text}</p>
624:                    <div class="bg-indigo-500 h-1.5 rounded-full transition-all duration-300" style="width: ${window.exportJob.percent}%"></div>
627:                    <button onclick="window.togglePauseExport()" class="px-3 py-1.5 text-xs font-bold rounded-md transition-colors cursor-pointer flex-1 ${pauseClass}">${pauseText}</button>
628:                    <button onclick="window.cancelExport()" class="px-3 py-1.5 text-xs font-bold bg-red-100 text-red-700 hover:bg-red-200 rounded-md transition-colors cursor-pointer flex-1">✕ Cancel</button>
633:        function showExportToast(text, percent, showControls = false) {
634:            window.exportJob.text = text; window.exportJob.percent = percent;
635:            let toast = document.getElementById(window.exportJob.id);
639:                toast = document.createElement('div'); toast.id = window.exportJob.id;
643:            if (showControls) updateExportToastUI();
661:        function finalizeExportToast() {
662:            const toast = document.getElementById(window.exportJob.id);
665:                toast.innerHTML = `<div class="flex items-center gap-2"><svg class="w-5 h-5 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path></svg><span class="text-sm font-bold text-slate-800">Export Berhasil</span></div><p class="text-[11px] text-slate-500 font-medium">Dokumen telah diunduh ke perangkat Anda.</p>`;
670:        function failExportToast(errorMsg) {
671:            const toast = document.getElementById(window.exportJob.id);
674:                toast.innerHTML = `<div class="flex items-center gap-2"><svg class="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M6 18L18 6M6 6l12 12"></path></svg><span class="text-sm font-bold text-slate-800">Export Dihentikan</span></div><p class="text-[11px] text-red-500 font-medium leading-tight">${errorMsg}</p>`;
700:            if (!document.fullscreenElement && !document.getElementById('presentationView').classList.contains('hidden') && !window.exportJob.active) exitPresentation();
708:            if (e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); nextSlide(); }
709:            if (e.key === 'ArrowLeft') { e.preventDefault(); prevSlide(); }
710:            if (e.key === 'Escape' && !window.exportJob.active) exitPresentation(); 
719:                setTimeout(() => { const anchor = document.getElementById('anchorManajemenSlide'); if (anchor) anchor.scrollIntoView({ behavior: 'smooth', block: 'start' }); }, 150);
812:            data.slides = Array.isArray(data.slides) ? data.slides : [];
815:            data.slides.forEach(slide => {
816:                slide.title = slide.title || ""; slide.layout = slide.layout || "standard"; slide.chartType = slide.chartType || "bar";
817:                slide.chartData = slide.chartData || ""; slide.tableData = slide.tableData || "";
818:                slide.momNote = slide.momNote || "";
820:                if (!Array.isArray(slide.points)) {
822:                    if (typeof slide.content === 'string' && slide.content.trim() !== '') {
823:                        slide.content.split('\n').filter(l => l.trim() !== '').forEach(l => {
827:                    slide.points = extractedPoints.length > 0 ? extractedPoints : [{title: "", desc: ""}];
828:                } else { slide.points = slide.points.map(pt => ({ title: pt && pt.title ? pt.title : "", desc: pt && pt.desc ? pt.desc : "" })); }
830:                if (!Array.isArray(slide.images)) { slide.images = [{url:"", caption:""},{url:"", caption:""},{url:"", caption:""},{url:"", caption:""}]; } 
832:                    slide.images = [0,1,2,3].map(idx => {
833:                        let img = slide.images[idx];
844:                let rawData = { id: null, meetingName: "Presentasi Baru", meetingDate: new Date().toISOString().split('T')[0], authorName: "", companyName: "", logoUrl: "", slides: [{ title: "Pendahuluan", points: [{title: "Poin Pembuka", desc: "Keterangan poin..."}], layout: "standard", momNote: "", images: [{url:"", caption:""},{url:"", caption:""},{url:"", caption:""},{url:"", caption:""}], chartType: "bar", chartData: "", tableData: "" }] };
869:            if (!activeMeeting || currentSlideIndex < 2 || currentSlideIndex >= activeMeeting.slides.length + 2) return;
870:            const slideIdx = currentSlideIndex - 2;
873:            activeMeeting.slides[slideIdx].momNote = liveInput.value;
890:        function addSlide() { 
893:                if(!Array.isArray(activeMeeting.slides)) activeMeeting.slides = [];
894:                activeMeeting.slides.push({ 
895:                    title: "Slide Baru", 
904:                    const newIdx = activeMeeting.slides.length - 1;
905:                    const newCard = document.getElementById(`slide_card_${newIdx}`);
908:            } catch(e) { console.error("Add Slide Error: ", e); }
911:        function removeSlide(index) { 
912:            if(!confirm("Hapus slide ini?")) return; 
914:            activeMeeting.slides.splice(index, 1); 
918:        function addPoint(slideIndex) { pullDataFromForm(); if(!Array.isArray(activeMeeting.slides[slideIndex].points)) activeMeeting.slides[slideIndex].points = []; activeMeeting.slides[slideIndex].points.push({title: "", desc: ""}); renderEditor(); }
919:        function removePoint(slideIndex, pointIndex) { pullDataFromForm(); activeMeeting.slides[slideIndex].points.splice(pointIndex, 1); renderEditor(); }
935:                const container = document.getElementById('slidesFormContainer');
938:                container.innerHTML = activeMeeting.slides.map((slide, i) => {
939:                    const imgs = Array.isArray(slide.images) ? slide.images : [{url:"", caption:""},{url:"", caption:""},{url:"", caption:""},{url:"", caption:""}];
940:                    const pts = Array.isArray(slide.points) ? slide.points : [];
951:                    <div id="slide_card_${i}" class="p-6 bg-white border border-slate-200 rounded-2xl relative shadow-sm hover:shadow-md transition-shadow scroll-mt-32">
954:                                <span class="bg-brand text-white text-xs font-bold px-4 py-1.5 rounded-full uppercase">Slide ${i+1}</span>
956:                                    <option value="standard" ${slide.layout === 'standard' ? 'selected' : ''}>Teks Saja (Standar)</option>
957:                                    <option value="image" ${slide.layout === 'image' ? 'selected' : ''}>Teks + Gambar Dinamis</option>
958:                                    <option value="table" ${slide.layout === 'table' ? 'selected' : ''}>Teks + Tabel Excel</option>
959:                                    <option value="chart" ${slide.layout === 'chart' ? 'selected' : ''}>Teks + Grafik Statistik</option>
962:                            <button onclick="removeSlide(${i})" class="text-red-500 bg-red-50 font-bold text-sm hover:bg-red-100 hover:text-red-600 px-4 py-1.5 rounded-lg border border-red-200 transition-colors cursor-pointer">🗑️ Hapus Slide</button>
966:                                <div><label class="block text-xs font-bold text-slate-500 mb-1">Judul Slide</label><input type="text" id="title_${i}" value="${slide.title}" class="w-full font-bold border border-slate-300 rounded-lg p-2.5 focus:border-accent outline-none"></div>
976:                                <div id="field_img_${i}" class="${slide.layout === 'image' ? 'block' : 'hidden'} space-y-3">
993:                                <div id="field_table_${i}" class="${slide.layout === 'table' ? 'block' : 'hidden'} flex-grow flex flex-col">
995:                                    <textarea id="table_${i}" class="w-full flex-grow border border-emerald-300 rounded-lg p-2 font-mono text-xs whitespace-pre outline-none focus:border-emerald-500 min-h-[150px] bg-emerald-50/30 custom-scrollbar">${slide.tableData || ''}</textarea>
997:                                <div id="field_chart_${i}" class="${slide.layout === 'chart' ? 'block' : 'hidden'} flex-grow flex flex-col">
1001:                                            <option value="bar" ${slide.chartType === 'bar' ? 'selected' : ''}>Bar Chart</option>
1002:                                            <option value="line" ${slide.chartType === 'line' ? 'selected' : ''}>Line Chart</option>
1003:                                            <option value="pie" ${slide.chartType === 'pie' ? 'selected' : ''}>Pie Chart</option>
1004:                                            <option value="doughnut" ${slide.chartType === 'doughnut' ? 'selected' : ''}>Doughnut Chart</option>
1008:                                    <textarea id="chart_${i}" class="w-full flex-grow border border-blue-300 rounded-lg p-2 font-mono text-sm outline-none focus:border-blue-500 bg-blue-50/30 custom-scrollbar">${slide.chartData || ''}</textarea>
1010:                                <div id="field_std_${i}" class="${slide.layout === 'standard' || !slide.layout ? 'flex' : 'hidden'} flex-grow items-center justify-center text-slate-400 text-sm font-medium bg-white rounded-lg border border-dashed border-slate-300">
1021:        function clearImageSlot(slideIndex, imgIndex) { 
1022:            const img = document.getElementById(`img_${slideIndex}_${imgIndex}`); if(img) img.value = ""; 
1023:            const cap = document.getElementById(`cap_${slideIndex}_${imgIndex}`); if(cap) cap.value = ""; 
1024:            const prev = document.getElementById(`preview_img_${slideIndex}_${imgIndex}`); if(prev) { prev.src = ""; prev.classList.add('hidden'); }
1025:            const st = document.getElementById(`statusImg_${slideIndex}_${imgIndex}`); if(st) st.innerText = ""; 
1046:                if(Array.isArray(activeMeeting.slides)) {
1047:                    activeMeeting.slides.forEach((slide, i) => {
1048:                        const titleEl = document.getElementById(`title_${i}`); slide.title = titleEl ? titleEl.value : slide.title;
1049:                        const layoutEl = document.getElementById(`layout_${i}`); slide.layout = layoutEl ? layoutEl.value : slide.layout;
1050:                        const chartTypeEl = document.getElementById(`chartType_${i}`); slide.chartType = chartTypeEl ? chartTypeEl.value : slide.chartType;
1051:                        const chartDataEl = document.getElementById(`chart_${i}`); slide.chartData = chartDataEl ? chartDataEl.value : slide.chartData;
1052:                        const tableDataEl = document.getElementById(`table_${i}`); slide.tableData = tableDataEl ? tableDataEl.value : slide.tableData;
1055:                        for(let p=0; p < (slide.points ? slide.points.length : 0); p++) {
1057:                            if(tEl && dEl) { newPoints.push({ title: tEl.value, desc: dEl.value }); } else if (slide.points[p]) { newPoints.push(slide.points[p]); }
1059:                        slide.points = newPoints;
1062:                            slide.images = [{ url: document.getElementById(`img_${i}_0`).value, caption: document.getElementById(`cap_${i}_0`).value }, { url: document.getElementById(`img_${i}_1`).value, caption: document.getElementById(`cap_${i}_1`).value }, { url: document.getElementById(`img_${i}_2`).value, caption: document.getElementById(`cap_${i}_2`).value }, { url: document.getElementById(`img_${i}_3`).value, caption: document.getElementById(`cap_${i}_3`).value }];
1063:                        } else { slide.images = [{url:"",caption:""},{url:"",caption:""},{url:"",caption:""},{url:"",caption:""}]; }
1086:            const slides = meetingData.slides || [];
1089:            slides.forEach(s => { 
1138:            let hasMOM = slides.some(s => s.momNote && s.momNote.trim() !== '');
1160:                return `<li class="relative bg-white p-6 rounded-xl border border-slate-100 shadow-sm anim-slide-up" style="animation-delay: ${delay}ms;"><div class="absolute left-0 top-0 bottom-0 w-1.5 bg-accent rounded-l-xl"></div><div class="pl-4">${html}</div></li>`;
1164:        function parseTableToHTML(tsvData, slideIndex) {
1167:            let html = `<div class="relative group w-full h-full flex flex-col justify-center">`; const tableId = `rendered_tbl_${slideIndex}`;
1179:        function goToSlide(targetIndex) { currentSlideIndex = targetIndex; renderSlideView(currentSlideIndex); }
1186:            if(activeMeeting && activeMeeting.slides) {
1187:                activeMeeting.slides.forEach((slide, idx) => {
1188:                    if(slide.momNote && slide.momNote.trim() !== '') {
1192:                        <div class="bg-white p-6 rounded-2xl border-2 border-slate-200 shadow-sm break-inside-avoid mb-4 anim-slide-up" style="animation-delay: ${delay}ms;">
1195:                                ${slide.title}
1197:                            <p class="text-slate-700 text-lg leading-relaxed whitespace-pre-wrap font-medium">${slide.momNote}</p>
1203:            if(!hasNotes) { html = `<div class="bg-slate-100 p-10 rounded-2xl text-center text-slate-500 font-bold border border-slate-200 anim-slide-up">Tidak ada catatan (Minutes of Meeting) yang direkam pada presentasi ini.</div>`; }
1207:        function renderSlideView(index, isExportMode = false) {
1212:                const totalPresentationSlides = activeMeeting.slides.length + 4; 
1217:                if (widgetTot) widgetTot.innerText = totalPresentationSlides;
1240:                if(index >= 2 && index < activeMeeting.slides.length + 2 && !window.exportJob.active) { 
1244:                    if(liveInput) liveInput.value = activeMeeting.slides[index - 2].momNote || "";
1251:                    const animEls = el.querySelectorAll('.anim-slide-up, .anim-slide-left, .anim-zoom-in, .anim-fade-in, .anim-line-grow');
1255:                if (index === 0 || index === totalPresentationSlides - 1) {
1265:                    if(!isExportMode) triggerReflow(layoutCover);
1291:                    document.getElementById('presAgendaGrid').innerHTML = activeMeeting.slides.map((s, idx) => {
1294:                        <div class="agenda-card group flex flex-row items-center gap-6 p-6 border-b-2 border-slate-100 hover:border-corporateTeal transition-all duration-300 cursor-pointer bg-white/50 hover:bg-white rounded-xl shadow-sm hover:shadow-md anim-slide-up" style="animation-delay: ${delay}ms;" onclick="if(!window.exportJob.active)goToSlide(${idx + 2}); event.stopPropagation();">
1306:                    if(!isExportMode) triggerReflow(layoutAgenda);
1308:                else if (index >= 2 && index < activeMeeting.slides.length + 2) {
1312:                    const dataIndex = index - 2; const slide = activeMeeting.slides[dataIndex];
1313:                    document.getElementById('presSlideTitle').innerText = slide.title;
1315:                    const validPts = (slide.points || []).filter(p => p && typeof p.title === 'string' && p.title.trim() !== '');
1318:                    const grid = document.getElementById('presSlideGrid'); const textCol = document.getElementById('presSlideTextCol'); const visualCol = document.getElementById('presSlideVisual');
1322:                        textCol.classList.remove('hidden'); const isStandard = slide.layout === 'standard' || !slide.layout;
1323:                        if (isStandard) { grid.classList.remove('xl:grid-cols-2'); grid.classList.add('grid-cols-1'); document.getElementById('presSlideBullets').className = 'grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-6 w-full list-none animated-list'; } 
1324:                        else { grid.classList.add('xl:grid-cols-2'); grid.classList.remove('grid-cols-1'); document.getElementById('presSlideBullets').className = 'flex flex-col gap-5 w-full list-none animated-list'; }
1325:                        document.getElementById('presSlideBullets').innerHTML = renderPointsHTML(slide.points);
1328:                    if (slide.layout === 'standard' || !slide.layout) { visualCol.classList.add('hidden'); } 
1329:                    else if (slide.layout === 'image') {
1330:                        const validImages = (slide.images || []).map(img => typeof img === 'string' ? {url: img, caption: ""} : img).filter(img => img && img.url && img.url.trim() !== "");
1334:                            if(!isExportMode) { visualCol.style.animation = 'none'; void visualCol.offsetWidth; visualCol.style.animation = null; }
1346:                                imgHTML += `<div class="${colSpan} ${heightClass} relative rounded-2xl shadow-lg border border-slate-200 overflow-hidden bg-slate-100 group cursor-zoom-in transition-transform duration-300 hover:shadow-2xl" onclick="if(!window.exportJob.active)openLightbox('image','${url}', '${safeCaption}');event.stopPropagation();"><img src="${url}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-out" data-export-img="true">${renderCap}</div>`;
1351:                    else if (slide.layout === 'table') { visualCol.classList.remove('hidden'); let tableWrapperClass = !hasText ? 'max-w-5xl mx-auto' : 'w-full'; visualCol.innerHTML = `<div class="${tableWrapperClass} h-full" id="rendered_table_container_${dataIndex}">${parseTableToHTML(slide.tableData, dataIndex)}</div>`; }
1352:                    else if (slide.layout === 'chart') {
1355:                        const chartData = parseChartData(slide.chartData); const cType = slide.chartType || 'bar'; const ctx = document.getElementById('canvasChart').getContext('2d');
1357:                        let animOptions = window.exportJob.active ? false : { duration: 1200, easing: 'easeOutExpo' };
1360:                    if(!isExportMode) triggerReflow(layoutContent);
1362:                else if (index === activeMeeting.slides.length + 2) {
1366:                    if(!isExportMode) triggerReflow(layoutMOM);
1370:                    if(!isExportMode) {
1382:                    if(!isExportMode) triggerReflow(layoutThankYou);
1384:            } catch (err) { console.error("Render Slide View Error: ", err); alert("Kesalahan saat merender layar presentasi: " + err.message); }
1387:        function nextSlide() { const maxIdx = activeMeeting.slides.length + 3; if(currentSlideIndex < maxIdx) { currentSlideIndex++; renderSlideView(currentSlideIndex); } }
1388:        function prevSlide() { if(currentSlideIndex > 0) { currentSlideIndex--; renderSlideView(currentSlideIndex); } }
1411:                    try { localStorage.setItem(GAEKS_PRES_ITEM_KEY(id), JSON.stringify(details)); } catch(e){}
1428:            document.body.classList.remove('exporting-mode');
1452:                currentSlideIndex = 0; 
1453:                renderSlideView(0); 
1485:            if (window.exportJob.cancelled) return false;
1486:            while (window.exportJob.paused && !window.exportJob.cancelled) { await new Promise(r => setTimeout(r, 300)); }
1487:            return !window.exportJob.cancelled;
1490:        async function runNativePPTXExport() {
1491:            if (window.exportJob.active) return;
1492:            window.exportJob = { active: true, paused: false, cancelled: false, id: 'toastPPTX', percent: 0, text: '' };
1496:                showExportToast('Merakit Microsoft PowerPoint asli...', 10, true);
1498:                let pres = new PptxGenJS();
1501:                document.documentElement.classList.add('exporting-mode'); document.body.classList.add('exporting-mode');
1503:                presView.classList.remove('hidden'); presView.classList.add('pdf-background-render');
1510:                let slideCover = pres.addSlide();
1511:                slideCover.background = { color: '0A0F1D' };
1512:                slideCover.addShape(pres.ShapeType.rect, { x: 0, y: 0, w: '4%', h: '100%', fill: { color: 'D4AF37' } }); 
1513:                if(logoB64 && logoB64.startsWith('data:')) slideCover.addImage({ data: logoB64, x: 1.0, y: 1.0, w: 2, h: 0.8, sizing: { type: 'contain' } });
1514:                slideCover.addText(activeMeeting.meetingName || "Presentasi", { x: 1.0, y: 2.5, w: '80%', h: 2.0, fontSize: 50, bold: true, color: 'FFFFFF', fontFace: 'Playfair Display' });
1518:                slideCover.addText(metaText, { x: 1.0, y: 4.8, w: '80%', h: 0.5, fontSize: 16, color: 'D4AF37', fontFace: 'Plus Jakarta Sans', bold: true });
1520:                let slideAgenda = pres.addSlide();
1521:                slideAgenda.background = { color: 'FFFFFF' };
1522:                slideAgenda.addText("Daftar Bahasan Utama", { x: 0.5, y: 0.4, w: '90%', h: 0.8, fontSize: 32, bold: true, color: '0A0F1D', fontFace: 'Plus Jakarta Sans' });
1523:                slideAgenda.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.3, w: 1, h: 0.05, fill: { color: '2563EB' } });
1526:                activeMeeting.slides.forEach((s, idx) => {
1527:                    slideAgenda.addText(`${idx+1}. ${s.title}`, { x: 0.5, y: yPosAgenda, w: '90%', h: 0.4, fontSize: 18, color: '334155', fontFace: 'Plus Jakarta Sans' });
1531:                for(let i = 0; i < activeMeeting.slides.length; i++) {
1533:                    const s = activeMeeting.slides[i];
1534:                    let slide = pres.addSlide();
1535:                    slide.background = { color: 'FFFFFF' };
1537:                    if(logoB64 && logoB64.startsWith('data:')) slide.addImage({ data: logoB64, x: '88%', y: 0.2, w: 1, h: 0.4, sizing: { type: 'contain' } });
1538:                    slide.addText(s.title, { x: 0.5, y: 0.4, w: '80%', h: 0.8, fontSize: 28, bold: true, color: '0A0F1D', fontFace: 'Plus Jakarta Sans' });
1539:                    slide.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.2, w: '90%', h: 0.02, fill: { color: 'E2E8F0' } });
1540:                    slide.addText("GAEKS GROUP &bull; 2026", { x: 0.5, y: '93%', w: '20%', h: 0.3, fontSize: 9, color: '94A3B8', bold: true });
1551:                    if(textBlocks.length > 0) slide.addText(textBlocks, { x: 0.5, y: 1.5, w: textWidth, h: 3.5, valign: 'top' });
1556:                            const slideImgB64 = await getDirectBase64(validImgs[0].url);
1557:                            if(slideImgB64) { slide.addImage({ data: slideImgB64, x: '52%', y: 1.5, w: '43%', h: 3.5, sizing: { type: 'contain' } }); } 
1558:                            else { slide.addShape(pres.ShapeType.rect, { x: '52%', y: 1.5, w: '43%', h: 3.5, fill: { color: 'F1F5F9' } }); slide.addText("Gambar gagal dimuat.", { x: '52%', y: 1.5, w: '43%', h: 3.5, align: 'center', color: '94A3B8' }); }
1561:                        renderSlideView(i + 2, true);
1563:                        const targetEl = document.getElementById('presSlideVisual');
1566:                            slide.addImage({ data: snapCanvas.toDataURL('image/jpeg', 0.9), x: '52%', y: 1.5, w: '43%', h: 3.5, sizing: { type: 'contain' } });
1569:                    showExportToast(`Merakit PPTX: Materi ${i+1}/${activeMeeting.slides.length}`, 30 + Math.round(((i+1)/activeMeeting.slides.length)*50), true);
1574:                let slideMOM = pres.addSlide();
1575:                slideMOM.background = { color: 'F8FAFC' };
1576:                slideMOM.addText("Minutes of Meeting (MOM)", { x: 0.5, y: 0.5, w: '90%', h: 0.8, fontSize: 32, bold: true, color: '0F766E' });
1578:                activeMeeting.slides.forEach((s, idx) => {
1581:                        slideMOM.addText(`Bagian ${idx+1}: ${s.title}`, { x: 0.5, y: yPosMOM, w: '90%', h: 0.3, fontSize: 14, bold: true, color: '2563EB' });
1582:                        slideMOM.addText(s.momNote, { x: 0.5, y: yPosMOM + 0.3, w: '90%', h: 0.5, fontSize: 12, color: '334155' });
1586:                if(!hasMOM) slideMOM.addText("Tidak ada catatan.", { x: 0.5, y: 1.5, w: '90%', h: 1, fontSize: 16, color: '94A3B8' });
1588:                let slideTy = pres.addSlide();
1589:                slideTy.background = { color: '0A0F1D' }; 
1590:                slideTy.addText("Thank You.", { x: 0.5, y: 2.0, w: '90%', h: 1.5, align: 'center', fontSize: 56, bold: true, color: 'FFFFFF', fontFace: 'Playfair Display' });
1591:                slideTy.addText(getSmartClosing(activeMeeting).replace(/\n/g, ' '), { x: 1, y: 3.5, w: '80%', h: 2, align: 'center', fontSize: 16, color: '94A3B8' });
1594:                showExportToast('Menyimpan file PPTX...', 95, false);
1595:                pres.writeFile({ fileName: `Presentasi_${(activeMeeting.meetingName || "Materi").replace(/[^a-zA-Z0-9]/g, '_')}.pptx` }).then(() => { finalizeExportToast(); });
1598:                if(err.message === "Cancelled") failExportToast("Proses dibatalkan oleh pengguna.");
1599:                else failExportToast("Gagal merakit PPTX: " + err.message);
1601:                window.exportJob.active = false; document.documentElement.classList.remove('exporting-mode'); document.body.classList.remove('exporting-mode'); document.getElementById('presentationView').classList.add('hidden'); document.getElementById('presentationView').classList.remove('pdf-background-render'); switchView('admin');
1605:        async function runNativePDFExport() {
1606:            if (window.exportJob.active) return;
1607:            window.exportJob = { active: true, paused: false, cancelled: false, id: 'toastPDF', percent: 0, text: '' };
1611:                showExportToast('Menyusun PDF Asli...', 5, true);
1613:                document.documentElement.classList.add('exporting-mode'); document.body.classList.add('exporting-mode');
1615:                presView.classList.remove('hidden'); presView.classList.add('pdf-background-render');
1617:                const { jsPDF } = window.jspdf;
1618:                const doc = new jsPDF({ orientation: 'landscape', unit: 'px', format: [1920, 1080] });
1638:                const totalSlides = activeMeeting.slides.length + 4; 
1641:                // 1. COVER SLIDE
1658:                // 2. AGENDA SLIDE
1660:                drawHeader(doc, activeMeeting.meetingName, logoB64); drawFooter(doc, currentPage, totalSlides);
1668:                activeMeeting.slides.forEach((s, idx) => {
1674:                showExportToast('Merakit Halaman Materi...', 30, true);
1676:                // 3. CONTENT SLIDES
1677:                for(let i = 0; i < activeMeeting.slides.length; i++) {
1679:                    const s = activeMeeting.slides[i];
1682:                    drawHeader(doc, activeMeeting.meetingName, logoB64); drawFooter(doc, currentPage, totalSlides);
1712:                                const slideImgB64 = await getDirectBase64(validImgs[0].url);
1713:                                if (slideImgB64 && slideImgB64.startsWith('data:')) {
1714:                                    doc.addImage(slideImgB64, 'JPEG', visualX, visualY, visualW, visualH);
1722:                            renderSlideView(i + 2, true);
1724:                            const targetEl = document.getElementById('presSlideVisual');
1732:                    showExportToast(`Merakit PDF: Materi ${i+1}/${activeMeeting.slides.length}`, 30 + Math.round(((i+1)/activeMeeting.slides.length)*50), true);
1738:                // 4. MOM SLIDE
1740:                drawHeader(doc, activeMeeting.meetingName, logoB64); drawFooter(doc, currentPage, totalSlides);
1748:                activeMeeting.slides.forEach((s, idx) => {
1765:                // 5. THANK YOU SLIDE
1777:                showExportToast('Menyimpan file PDF ke perangkat...', 95, false);
1778:                doc.save(`Deck_${(activeMeeting.meetingName || "Materi").replace(/[^a-zA-Z0-9]/g, '_')}.pdf`);
1779:                finalizeExportToast();
1782:                if(err.message === "Cancelled") failExportToast("Proses dibatalkan oleh pengguna.");
1783:                else failExportToast("Gagal menyusun PDF: " + err.message);
1785:                window.exportJob.active = false; document.documentElement.classList.remove('exporting-mode'); document.body.classList.remove('exporting-mode'); document.getElementById('presentationView').classList.add('hidden'); document.getElementById('presentationView').classList.remove('pdf-background-render'); switchView('admin');
```

## Target Flow
User → authenticated session → owned presentation → editor/autosave → dashboard → playback/PDF/PPTX export

## Main Risks To Verify
- Browser-only persistence
- Cross-device consistency
- Cross-user access
- Export fidelity
- Internal sample data appearing in new presentations
