# GBP Implementation Order

## Architectural Baseline & Principles
Based on the completed Task 00 comprehensive system audit of the GAEKS Digital Platform (GDP) (`gakesgroup-hash/gaeks-gdp`):
1. **Reuse Existing Server Assets**: The repository already contains functional server-side backend adapters (`api/db.php`, `api/cv.php`, `api/presentation.php`, `api/auth_otp.php`, `api/config.php`, `api/mailer.php`). We do not rebuild backend architectures from scratch; we harden and connect them.
2. **Eliminate Fragile LocalStorage Reliance**: Currently, `cv.html`, `cv-dashboard.html`, and `presentation.html` store document state in browser `localStorage`. These must be systematically migrated to use the existing PHP APIs with robust server persistence.
3. **Strict Tenancy & Session Isolation**: Replace client-driven user impersonation and unvalidated user IDs with verified server-side session authentication.
4. **Preserve Pre-Existing Repository State**: Pre-existing uncommitted modifications in `api/db.php` and additions in `deploy_codespaces.py` are strictly protected and never blindly overwritten.
5. **Bounded Scope**: Product focus is strictly bounded to the ATS CV Maker and Presentation Maker. No expansion into ERP, SMM, e-books, marketplace, or affiliate systems.

---

## 19-Step Explicit Implementation Order

### Step 01: Baseline & Governance (Current Task)
- **Objective**: Establish foundational change policy, verification contract, and implementation sequence.
- **Dependencies**: Task 00 Audit artifacts.
- **Scope**: Create `docs/GDP_IMPLEMENTATION_ORDER.md` and `docs/GDP_CHANGE_POLICY.gd`. Zero production code modified.

### Step 02: Existing Auth & Session Hardening
- **Objective**: Harden session handling and server-side verification using existing `api/auth_otp.php` and `auth.js`.
- **Dependencies**: Step 01.
- **Scope**:
  - Secure session cookies (`HttpOnly`, `SameSite=Lax`, `Secure`).
  - Integrate server-side OTP issuance and token verification.
  - Eliminate client-only trust of Google OAuth JWT payloads in `auth.js`.
  - Validate user session on all authenticated routes before granting access.

### Step 03: Existing DB & API Hardening
- **Objective**: Harden and standardize `api/db.php` without destroying pre-existing logic.
- **Dependencies**: Step 02.
- **Scope**:
  - Audit and consolidate SQLite PDO schema creation and indexing for `cvs` and `presentations` tables.
-  Implement uniform JSON response envelope ({ success, data, error, timestamp }).
  - Enforce server-side user tenancy on all SQL queries (`WHERE user_id = :session_user_id`).
-  Verify JSON backup directory write permissions and sanitize inputs against SQL injection.

### Step 04: CV â†’ Existing api/cv.php Persistence Migration
- **Objective**: Transition ATS CV editor (`cv.html`) from browser `localStorage` to existing `api/cv.php`.
- **Dependencies**: Step 03.
- **Scope**:
  - Implement debounced auto-save (1500ms) transmitting structured CV state to `api/cv.php?action=save`.
-  Fetch existing CV data via `api/cv.php?action=get&id=...` on document load.
  - Handle offline graceful fallback while displaying persistent server sync status indicators.
  - Ensure data normalization across personal information, work experience, education, skills, and certifications.

### Step 05: CV Dashboard Synchronization
- **Objective**: Connect `cv-dashboard.html` to server-side `api/cv.php?action=list`.
- **Dependencies**: Step 04.
- **Scope**:
  - Populate dashboard cards dynamically from SQLite database rather than local storage.
  - Support server-side duplicate, delete, and rename actions with tenancy verification.
-  Implement 3-day trash lifecycle management and status badges (Draft vs. Siap).
  - Standardize completeness score calculation algorithm.

### Step 06: CV PDF Rendering & Export
- **Objective**: Harden print stylesheets and PDF-generation across all 15 ATS resume templates.
- **Dependencies**: Step 05.
- **Scope**:
  - Standardize @media print rules, A4 dimensions, and margins across all templates.
  - Apply `page-break-inside: avoid` to experience and education entry cards.
  - Ensure high-fidelity font rendering, crisp icon rasterization, and accurate page count indicators.

### Step 07: Presentation â„j Existing api/presentation.php Persistence Migration
- **Objective**: Transition slide deck builder (`presentation.html`) from browser `localStorage` to `api/presentation.php`.
- **Dependencies**: Step 03.
- **Scope**:
  - Persist full presentation JSON (slides, themes, layout metadata, shapes, typography) via `api/presentation.php?action=save`.
-  Implement payload size optimization and client-side image compression prior to transmission.
-  Clear canvas annotation buffers upon slide switching to prevent memory leaks.

### Step 08: Presentation Editor & Dashboard Integration
- **Objective**: Connect presentation management surfaces to server endpoints.
- **Dependencies**: Step 07.
- **Scope**:
  - Implement slide deck listing, duplication, template cloning, and deletion.
-  Ensure multi-slide reordering and slide thumbnail state synchronization.
  - Support presentation mode fullscreen preview with robust speaker notes state.

### Step 09: Presentation PDF / PPTX Export
- **Objective**: Standardize client-side and server-assisted export workflows for presentations.
- **Dependencies**: Step 08.
- **Scope**:
  - Enforce 16:9 landscape aspect ratio in @media print stylesheets.
-  Implement clean slide-by-slide export without clipping or overlapping elements.
  - Support reliable offline fallback export via client-side presentation generators.

### Step 10: Upload Security & Asset Handling
- **Objective**: Secure media upload surfaces (profile photos, logo graphics, presentation imagery).
- **Dependencies**: Step 04, Step 07.
- **Scope**:
  - Enforce MIME-type verification, magic number inspection, and maximum file size thresholds (<= 2MB).
  - Sanitize uploaded file names and store outside web-executable directories.
  - Prevent SVG-based Cross-Site Scripting (XSS) and path traversal vectors.

### Step 11: UX Polish & Error Feedback
- **Objective**: Elevate interface polish and responsiveness across CV and Presentation makers.
- **Dependencies**: Step 06, Step 09, Step 10.
- **Scope**:
  - Integrate unified non-intrusive toast notifications (Sonner pattern).
  - Implement accessible modal dialogs, loading skeletons, and inline error validation states.
  - Ensure full responsiveness across desktop, tablet, and mobile viewports.

### Step 12: Entitlement & User Tier Architecture
- **Objective**: Formalize server-side entitlement enforcement for Free, PRO, and VIP tiers.
- **Dependencies**: Step 02, Step 03, Step 11.
- **Scope**:
  - Relocate PRO/VIP gating from client-side arrays in `auth.js` to server-side checks in `api/db.php`.
  - Enforce document creation limits (e.g., maximum active CVs/presentations for free tier).
  - Restrict premium ATS templates and high-resolution exports to verified entitlements at the API layer.

### Step 13: Subscription & Monetization Readiness
- **Objective**: Prepare transactional architecture for Indonesian and global payment gateways.
- **Dependencies**: Step 12.
- **Scope**:
  - Define webhook listener specifications and subscription ledger database schema.
  - Implement idempotent webhook processing with cryptographic signature verification.
  - Establish automated notification templates via `api/mailer.php`.

### Step 14: Search Engine Optimization (SEO) & Meta Discovery
- **Objective**: Optimize public landing pages (`index.html`, `login.html`) for search discovery.
- **Dependencies**: Step 11.
- **Scope**:
  - Add semantic HTML5 tags, comprehensive Open Graph, Twitter Cards, and canonical URLs.
  - Inject JSON-LD structured data for SoftwareApplication and WebSite entities.
  - Verify robots.txt and sitemap.xml directives.

### Step 15: Performance, Caching & Accessibility (A11y)
- **Objective**: Optimize Core Web Vitals and meet WCAG 2.1 AA accessibility standards.
- **Dependencies**: Step 14.
- **Scope**:
  - Minimize layout shifts (CLS), optimize Largest Contentful Paint (LCP), and reduce main-thread blocking.
  - Ensure full keyboard navigability (tabbing, focus traps, escape handling) across all interactive tools.
  - Verify high-contrast color ratios across dark/light UI modes.

### Step 16: Legacy Script & Artifact Cleanup
- **Objective**: Purge and organize historical scripts without breaking production deployment.
- **Dependencies**: Step 15.
- **Scope**:
  - Audit historical root-level deploy/fix scripts (`fix_*.py`, `patch_*.sh`).
  - Move verified obsolete non-production scripts to an archived administrative directory.
  - Clean up dead dependencies and references across HTML files.

### Step 17: Security QA f Penetration Audit
- **Objective**: Comprehensive defensive security audit across all hardened surfaces.
- **Dependencies**: Steps 02-16.
- **Scope**:
  - Verify immunity against SQL injection, Stored/Reflected XSS, and Cross-Site Request Forgery (CSRF).
  - Test tenancy isolation: guarantee User A cannot read, update, or delete User B's documents.
  - Verify zero plaintext secrets, tokens, or credentials across repository commits and logs.

### Step 18: End-to-End Regression Verification
- **Objective**: Comprehensive automated and scripted smoke testing of complete user journeys.
- **Dependencies**: Step 17.
- **Scope**:
  - Validate auth flow: register -> OTP login -> session establishment -> logout.
-  Validate CV lifecycle: create -> edit -> auto-save -> dashboard list -> duplicate -> export PDF -> delete.
  - Validate Presentation lifecycle: create -> edit slides -> auto-save -> presenter mode -> export -> delete.

### Step 19: Production Readiness & Release Sign-Off
- **Objective**: Final deployment verification and production readiness sign-off.
- **Dependencies**: Steps 01-18.
- **Scope**:
  - Validate deployment pipeline with `deploy_codespaces.py`.
-  Ensure zero uncommitted drift on release branch.
  - Generate release notes and production operations checklist.