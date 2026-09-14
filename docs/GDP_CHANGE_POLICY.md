# GAEKS Digital — GDP Change Policy

## Core Rules
1. Inspect before editing.
2. Preserve unrelated user work.
3. Backup before significant changes.
4. Prefer targeted edits over wholesale replacement.
5. Reuse existing architecture where functional.
6. Never invent APIs, files, dependencies, infrastructure, or business facts.
7. Never expose secrets.
8. Browser storage must not be authoritative for identity, authorization, or durable documents.
9. User-owned documents require server-side ownership checks.
10. One task per execution.

## Protected Files
api/db.php and deploy_codespaces.py were already changed before TASK 00 and must be preserved.

## Data Safety
Database changes must be additive/reversible where practical. Existing user data must not be destroyed.

## Scope
Active GDP scope is ATS CV Maker and Presentation Maker.

## Validation
Every task must validate intended changes, run applicable checks, run git diff --check, inspect git diff --stat, and report PASS/WARN/FAIL.
