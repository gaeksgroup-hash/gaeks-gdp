# GAEKS Digital — GDP Implementation Order

## Active Product Priority
1. ATS CV Maker
2. Presentation Maker

## Required Dependency Order
01. Foundation baseline
02. Authentication and session security
03. Existing database and API foundation
04. CV server persistence using existing api/cv.php
05. CV dashboard stabilization
06. CV A4 PDF reliability
07. Presentation server persistence using existing api/presentation.php
08. Presentation dashboard and editor stabilization
09. Presentation PDF/PPTX export reliability
10. Upload and media security
11. CV and Presentation product UX
12. Server-authoritative Free/PRO entitlement
13. Subscription readiness without live billing
14. Public positioning and SEO
15. Performance, mobile, and accessibility
16. Legacy and technical debt cleanup
17. Security hardening and QA
18. Full regression and release candidate
19. Production readiness

## Existing Architecture Rule
Reuse existing api/auth_otp.php, api/db.php, api/cv.php, and api/presentation.php when they provide the required capability.

## Protected Existing Work
api/db.php and deploy_codespaces.py had pre-existing changes before TASK 00 and must never be blindly overwritten.

## Dependency Rule
Never skip a prerequisite task. Every task must pass validation before the next task begins.
