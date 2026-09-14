# GDP Architecture

## Current Repository Boundary
- GDP repository: gaeksgroup-hash/gaeks-gdp
- Active product priority: ATS CV Maker and Presentation Maker
- GDP must remain separate from the public corporate website and ERP repository.

## Detected Application Surfaces
```text
./api/auth_otp.php
./api/config.php
./api/cv.php
./api/db.php
./api/mailer.php
./api/presentation.php
./api/send_welcome_email.php
./api/test_mail.php
./auth.js
./cv-dashboard.html
./cv.html
./editor.html
./index.html
./login.html
./presentation.html
./pricing.html
./profile.html
```

## Target Direction
User → secure server session → server-owned document data → CV/Presentation editor → reliable export
Browser storage should not remain the authority for identity, permissions, or durable documents.

## Dependency Principle
Authentication/session → persistence foundation → CV persistence → Presentation persistence → exports/uploads → UX → entitlement → QA → production readiness
