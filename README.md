# Secure Python CI/CD Pipeline

A complete GitHub Actions pipeline with secure environment variable handling.

## Project Structure

```
.
├── app.py                          # Main application
├── conftest.py                     # Pytest root config (required for Kali Linux)
├── requirements.txt                # Python dependencies
├── tests/
│   └── test_app.py                 # Pytest test cases
└── .github/
    └── workflows/
        └── ci.yml                  # GitHub Actions pipeline
```

---

## How to Run Locally (Standard)

```bash
pip install -r requirements.txt
export API_KEY="your-api-key"
export DB_URL="your-db-url"
python app.py --check-env
```

---

## How to Run on Kali Linux

Kali Linux uses an externally managed Python environment, so a virtual environment is required.

**Step 1 — Create a virtual environment**
```bash
python3 -m venv venv
```
This creates an isolated Python environment so system packages don't get affected.

**Step 2 — Activate it**
```bash
source venv/bin/activate
```
You will see `(venv)` appear at the start of your terminal prompt — that means it is active.

**Step 3 — Install dependencies**
```bash
pip install -r requirements.txt
```
This installs pytest inside the venv only, not system-wide.

**Step 4 — Set secret environment variables**
```bash
export API_KEY="test-key-123"
export DB_URL="sqlite:///test.db"
```
These simulate what GitHub Secrets injects automatically during the pipeline run.

**Step 5 — Run the app**
```bash
python app.py --check-env
```

Expected output:
```
✅ All required environment variables are present.
   API_KEY  : *************
   DB_URL   : ****************
```

**Step 6 — Create conftest.py (one time only)**
```bash
touch conftest.py
```
This empty file tells pytest that the project root is here, so `app.py` can be imported correctly.

**Step 7 — Run the tests**
```bash
pytest tests/ -v
```

Expected output:
```
tests/test_app.py::test_get_config_missing_env   PASSED
tests/test_app.py::test_get_config_present        PASSED
tests/test_app.py::test_api_key_not_empty         PASSED

3 passed in 0.XXs
```

---

## What Each Test Checks

| Test | What it verifies |
|------|-----------------|
| `test_get_config_missing_env` | App crashes loudly if secrets are missing |
| `test_get_config_present` | App works correctly when secrets are injected |
| `test_api_key_not_empty` | Empty string "" is also rejected as invalid |

---

## Setting Up GitHub Secrets

1. Go to your GitHub repo
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add the following secrets:

| Secret Name | Value |
|-------------|-------|
| `MY_API_KEY` | your actual API key |
| `DATABASE_URL` | your database connection string |

---

## Pipeline Stages

| Stage | What it does |
|-------|-------------|
| Checkout | Clones your repo into the runner VM |
| Setup Python | Installs Python 3.11 |
| Install deps | Runs pip install -r requirements.txt |
| Run tests | Runs pytest — pipeline fails if any test fails |
| Secrets step | Injects secrets from GitHub Vault at runtime |

---

## Security Rules Followed

- No hardcoded credentials anywhere in code
- Secrets injected at runtime only, never stored in files
- Secrets are masked in all GitHub Actions logs
- Tests validate secret presence before deployment
- Fresh VM per run — no state leakage between runs

---

## Quick Reminder — GitHub Actions Does This Automatically

When you push to GitHub, the pipeline runs all of these steps on a fresh Ubuntu VM — checkout, pip install, pytest, secrets injection — without you running anything manually. Your local run is just for verifying before the push.
