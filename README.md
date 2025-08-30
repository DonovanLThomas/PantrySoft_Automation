# PantrySoft Cleanup Automation (Playwright + Python)

Automates common PantrySoft admin cleanup tasks (searching clients, deleting notes/visits/registrations, and removing profiles) using **Playwright (sync API)**. Built to shrink a workflow that used to take **days** down to **a few hours**, running with minimal supervision.

## Features
- Logs into PantrySoft via UCSC SSO, handles Duo pause.
- Iterates over a list of student IDs and opens each client.
- Closes stray pop-ups reliably via `Escape`.
- Deletes **notes**, **visits**, **last registration**, and finally the **profile** (if possible).
- Prints success/failure per ID.

> ⚠️ **Data caution:** This script performs permanent deletions. Test in a safe environment and ensure you have authorization and backups.

---

## Prerequisites
- Python 3.9+ (3.10+ recommended)
- Google Chrome/Chromium installed (Playwright will install its own browsers if needed)
- Valid PantrySoft access with permission to perform deletions

## Install
```bash
# 1) Create & activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Install Playwright browsers (Chromium is required here)
playwright install chromium
```

---

## Configuration
Create a `.env` file in the project root with your credentials:
```
CruzID=your_username_here
PASSWORD=your_password_here
```

Provide a `Student_IDS.txt` file (one ID per line), e.g.:
```
abc123
bxy789
...
```

Update the PantrySoft URL if needed:
```python
Pantry_Soft_URL = "https://app.pantrysoft.com/login/ucsc"
```

---

## Usage
```bash
python main.py
```

What the script does at a glance:
1. Launches Chromium (currently **headful** with `slow_mo=300` for stability).
2. Navigates to PantrySoft SSO page, fills `CruzID` & `PASSWORD`.
3. Waits briefly in case **Duo** is present (prints a message for you to approve on your phone).
4. For each student ID:
   - Searches the client.
   - Sends `Escape` to close any residual modal.
   - Repeatedly clicks **Delete** for notes and visits until none remain.
   - Attempts to delete the **Last Registration**.
   - Opens profile edit and deletes the **Client Profile**.
5. Prints a success line (or an error line) for every ID.

---

## Customization Tips
- **Headless mode:** set `headless=True` once stable.
- **Speed:** adjust `slow_mo` and `wait_for_timeout` values to run faster.
- **Selectors:** if PantrySoft changes UI, update the selectors in each section.
- **Retry logic:** wrap delete loops with limited retries if needed.
- **Dry run:** add guards that _log_ actions instead of clicking to test safely.

---

## Troubleshooting
- **2FA/Duo hangs:** Approve on phone; if Duo screen changes, increase the timeout in this block:
  ```python
  page.wait_for_selector("h1#header-text:has-text('Check for a Duo Push')", timeout=5000)
  page.wait_for_url('https://app.pantrysoft.com/client/dashboard/', timeout=12000)
  ```
- **Elements not found / timeouts:** PantrySoft UI may have changed—inspect and update selectors.
- **“not a git repository” error:** You ran a git command outside a repo. Initialize one first:
  ```bash
  git init && git add . && git commit -m "init"
  ```
- **Rate limits / session lockouts:** Space out operations (`slow_mo`, `wait_for_timeout`) or run off-peak.
- **Ethics & compliance:** Ensure you have explicit authorization to delete records and that this aligns with data retention policies.

---

## File Layout (suggested)
```
project-root/
├─ main.py              # your script (the code you shared)
├─ requirements.txt
├─ .env                 # credentials (never commit this)
├─ Student_IDS.txt      # input list (one per line)
└─ README.md
```

---

## Security Notes
- Do **not** commit `.env` or real IDs to version control.
- Consider using a **service account** with scoped permissions.
- If you later schedule this, store secrets in a secure manager (e.g., OS keychain, cloud secret manager).

---

## License
Internal tooling for UCSC pantry operations. Adapt as needed within your organization’s policies.
