# GBP Change Policy & Engineering Governance

## 1. Absolute Directives

### 1.1 Preserve Unrelated Work
Never overwrite, revert, or modify code, files, configurations, or data that fall outside the explicit boundaries of the current task.

### 1.2 Protection of Pre-Existing Modifications
The Task 00 repository audit identified two critical pre-existing states prior to audit inception:
- `api/db.php`: Uncommitted working-tree modifications (`M`).
- `deploy_codespaces.py`: Pre-existing uncommitted script (`A` or untracked).

**Mandatory Protection Rules**:
1. Never treat `api/db.php` or `deploy_codespaces.py` as clean baseline files.:2. Never overwrite either file with a wholesale template or destructive write.
3. Always inspect `git diff` on these files before any proposed interaction.
4. All