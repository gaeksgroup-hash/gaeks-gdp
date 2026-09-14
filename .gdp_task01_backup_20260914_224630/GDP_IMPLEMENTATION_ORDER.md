# GBP Implementation Order

## Architectural Baseline & Principles
Based on the completed Task 00 comprehensive system audit of the GAEKS Digital Platform (GDP) (`gakesgroup-hash/gaeks-gdp`):
1. **Reuse Existing Server Assets**: The repository already contains functional server-side backend adapters (`api/db.php`, `api/cv.php`, `api/presentation.php`, `api/auth_otp.php`, `api/config.php`, `api/mailer.php`). We do not rebuild backend architectures from scratch; we harden and connect them.
2. **Eliminate Fragile LocalStorage Reliance**: Currently, `cv.html`, `cv-dashboard.html`, and `presentation.html` store document state in browser `localStorage`. These must be systematically migrated to use the existing PHP APIs with robust server persistence.
3. **Strict Tenancy & Session Isolation**: Replace client-driven user impersonation and unvalidated user IDs with verified server-side session authentication.
4. **Preserve Pre-Existing Repository State**: Pre-existing uncommitted modifications in `api/db.php` and additions in `deploy_codespaces.py` are strictly protected and never blindly overwritten.
5. **Bounded Scope**: Product focus is strictly bounded to the ATS CV Maker and Presentation Maker. No expansion into ERP, SMM, e-books, marketplace, or affiliate systems.

---

## 10-Phase Core Implementation Sequence

### Phase 01: Baseline & Governance (Current Task)
- **Objective**: Establish foundational change policy, verification contract, and implementation sequence.
- **Dependencies**: Task 00 Audit artifacts.
- **Scope**: Create `docs/GDP_IMPLEMENTATION_ORDER&.md` and `docs/GDP_CHANGE_POLICY.md`. Zero production code modified.

### Phase 02: Authentication & Server Session Hardening
- **Objective**: Harden session handling and server-side verification using existing `api/auth_otp.php` and `auth.js`.
- **Dependencies**: Phase 01.
- **Scope**:
  - Secure session cookies (`HttpOnly`, `SameSite=Lax`, `Secure`).
  - Integrate server-side OTP issuance and token verification.
  - Server-side validation of Google OAuth identity rather than client-only decoding.
  - Validate user session on all authenticated routes before granting access.

### Phase 03: Existing Database & API Hardening
- **Objective**: Harden and standardize `api/db.php` without destroying pre-existing logic.
- **Dependencies**: Phase 02.
- **Scope**:
  - Audit and consolidate SQLite PDO schema creation and indexing for `cvs` and `presentations` tables.
  - Implement uniform JSON response envelope ({ success, data, error, timestamp }).
  - Enforce server-side user tenancy on all SQL queries (`WHERE user_id = :session_user_id`).
  - Verify JSON backup directory write permissions and sanitize inputs against SQL injection.

### Phase 04: CV Existing API Integration
- **Objective**: Transition ATS CV editor (`cv.html`) from browser `localStorage` to existing `api/cv.php`.
- **Dependencies**: Phase 03.
- **Scope**:
  - Implement debounced auto-save (1500ms) transmitting structured CV state to `api/cv.php?action=save`.
  - Fetch existing CV data via `api/cv.php?action=get&id=...` on document load.
  - Connect `cv-dashboard.html` to server-side `api/cv.php?action=list`.
  - Standardize completeness score calculation and 3-day trash lifecycle management.

### Phase 05: Presentation Existing API Integration
- **Objective**: Transition slide deck builder (`presentation.html`) from browser `localStorage` to `api/presentation.php`.
- **Dependencies**: Phase 03.
- **Scope**:
  - Persist full presentation JSON (slides, themes, layout metadata, shapes, typography) via `api/presentation.php?action=save`.
  - Implement payload size optimization and client-side image compression prior to transmission.
  - Clear canvas annotation buffers upon slide switching to prevent memory leaks.
-  Connect presentation dashboard listings and duplication to server endpoints.

### Phase 06: Export & Upload Security Hardening
- **Objective**: Secure media upload surfaces and harden document export pipelines.
- **Dependencies**: Phase 04, Phase 05.
- **Scope**:
  - Standardize @media print rules, A4 dimensions, and page-break isolation across all 15 ATS resume templates.
  - Enforce 16:9 landscape export fidelity for presentation slides.
-  Enforce strict MIME-type inspection, file-size limits (<= 2MBŠK[™]˜]™\œØ[›ÝXÝ[ÛˆÛˆ[XYÙH\ØY[™Ú[Ë‚‚ˆÈÈÈ\ÙHÎˆV[YÛ›Y[	ˆ[\˜XÝ[ÛˆÛ\Ú‹H
Š“Øš™XÝ]™JŠŽˆ[]˜]H[\™˜XÙHÛ\ÚØY[™È™YY˜XÚË[™™\ÜÛœÚ]™[™\ÜË‚‹H
Š‘\[™[˜ÚY\ÊŠŽˆ\ÙH‹‚‹H
Š”ØÛÜJŠŽ‚ˆH[YÜ˜]H[šYšYY›Û‹Z[\Ú]™HØ\Ý›ÝYšXØ][ÛœÈ›ÜˆØ]™K[]K[™™\ÝÜ™HXÝ[ÛœË‚‹H[\[Y[XØÙ\ÜÚX›H[Ù[X[ÙÜËØY[™ÈÚÙ[]ÛœË[™[›[™H\œ›Üˆ˜[Y][ÛˆÝ]\Ë‚ˆH[œÝ\™H[™\ÜÛœÚ]™[™\ÜÈXÜ›ÜÜÈ\ÚÝÜX›][™[Øš[HšY]ÜÜË‚‚ˆÈÈÈ\ÙHˆ[][Y[	ˆ\Ù\ˆY\ˆ\˜Ú]XÝ\™B‹H
Š“Øš™XÝ]™JŠŽˆ›Ü›X[^™HÙ\™\‹\ÚYH[][Y[[™›Ü˜Ù[Y[›Üˆœ™YK“Ë[™’TY\œË‚‹H
Š‘\[™[˜ÚY\ÊŠŽˆ\ÙH‹\ÙHË\ÙHË‚‹H
Š”ØÛÜJŠŽ‚ˆH™[ØØ]H“ËÕ’TØ][™Èœ›ÛHÛY[\ÚYH\œ˜^\È[ˆ]]šœØÈÙ\™\‹\ÚYHÚXÚÜÈ[ˆ\KÙ‹œ‚‹H[™›Ü˜ÙHØÝ[Y[Ü™X][Ûˆ[Z]È]HTH^Y\ˆ›Üˆœ™YHY\œË‚‹H™\ÝšXÝ™[Z][HUÈ[\]\È[™YÚ\™\ÛÛ][Ûˆ^ÜÈÈ™\šYšYY[][Y[Ë‚‚ˆÈÈÈ\ÙHNˆÙXÝ\š]HPH	ˆÛÛ\™Z[œÚ]™H™YÜ™\ÜÚ[Û‚‹H
Š“Øš™XÝ]™JŠŽˆšYÛÜ›Ý\ÈY™[œÚ]™HÙXÝ\š]H]Y][™[™]ËY[™™YÜ™\ÜÚ[ÛˆXÜ›ÜÜÈ[\Ù\ˆ›Ý\›™^\Ë‚‹H
Š‘\[™[˜ÚY\ÊŠŽˆ\Ù\ÈKL‚‹H
Š”ØÛÜJŠŽ‚ˆH™\šYžH[[][š]HYØZ[œÝÔS[š™XÝ[Û‹ÔË[™ÔÔ‘ˆXÜ›ÜÜÈ[[™Ú[Ë‚ˆH[˜[˜ÞH\ÛÛ][Ûˆ\ÝÎˆÛÛ™š\›H™\›ÈÜ›ÜÜË][˜[™XYÝÜš]HØ\Xš[]K‚ˆH[™]ËY[™\Ý[™ÈÙˆ]]ÕˆY™XÞXÛK™\Ù[][ÛˆY™XÞXÛK[™YYXH[™[™Ë‚‚ˆÈÈÈ\ÙHLˆ›ÙXÝ[Ûˆ™XY[™\ÜÈ	ˆ™[X\ÙHÚYÛ‹SÙ™‚‹H
Š“Øš™XÝ]™JŠŽˆš[˜[\Þ[Y[™\šYšXØ][Ûˆ[™›ÙXÝ[ÛˆÜ\˜][ÛœÈÚYÛ‹[Ù™‹‚‹H
Š‘\[™[˜ÚY\ÊŠŽˆ\Ù\ÈKLK‚‹H
Š”ØÛÜJŠŽ‚ˆH˜[Y]H\Þ[Y[\[[™HÚ]\ÞWØÛÙ\ÜXÙ\ËœX‚‹HÛX[ˆ\ØœÛÛ]H›Û‹\›ÙXÝ[ÛˆØÜš\È[™XY™Y™\™[˜Ù\Ë‚ˆH[œÝ\™H™\›È[˜ÛÛ[Z]YšYÛˆ™[X\ÙHœ˜[˜Ú