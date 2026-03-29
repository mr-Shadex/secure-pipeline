# Secure Python CI/CD Pipeline

A complete GitHub Actions pipeline with secure environment variable handling.

## Project Structure

```
.
├── app.py                          # Main application
├── requirements.txt                # Python dependencies
├── tests/
│   └── test_app.py                 # Pytest test cases
└── .github/
    └── workflows/
        └── ci.yml                  # GitHub Actions pipeline
```

## How to Run Locally

```bash
pip install -r requirements.txt
export API_KEY="your-api-key"
export DB_URL="your-db-url"
python app.py --check-env
```

## How to Run in kali Linux

Running the Secure Pipeline Locally on Kali Linux
Step 1 — Create a virtual environment
bashpython3 -m venv venv
This creates an isolated Python environment so system packages don't get affected.

Step 2 — Activate it
bashsource venv/bin/activate
You'll see (venv) appear at the start of your terminal prompt — that means it's active.

Step 3 — Install dependencies
bashpip install -r requirements.txt
This installs pytest inside the venv only, not system-wide.

Step 4 — Set secret environment variables
bashexport API_KEY="test-key-123"
export DB_URL="sqlite:///test.db"
These simulate what GitHub Secrets injects automatically during the pipeline run.

Step 5 — Run the app
bashpython app.py --check-env
```
Expected output:
```
✅ All required environment variables are present.
   API_KEY  : *************
   DB_URL   : ****************
Step 6 — Run the tests
bashpytest tests/ -v
```
Expected output:
```
tests/test_app.py::test_get_config_missing_env   PASSED
tests/test_app.py::test_get_config_present        PASSED
tests/test_app.py::test_api_key_not_empty         PASSED

3 passed in 0.XXs

What Each Test Actually Checks
TestWhat it verifiestest_get_config_missing_envApp crashes loudly if secrets are missingtest_get_config_presentApp works correctly when secrets are injectedtest_api_key_not_emptyEmpty string "" is also rejected as invalid

Quick Reminder — GitHub Actions does this automatically
When you push to GitHub, the pipeline does all of these steps on a fresh Ubuntu VM — checkout, pip install, pytest, secrets injection — without you running anything manually. Your local run is just for testing before the push. 💡
Try it and let me know what output you get! 🚀 Sonnet 4.6

## How to Run Tests

```bash
pytest tests/ -v
```

## Setting Up GitHub Secrets

1. Go to your GitHub repo
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add:
   - `MY_API_KEY` = your actual API key
   - `DATABASE_URL` = your database connection string

## Pipeline Stages

| Stage | What it does |
|-------|-------------|
| Checkout | Clones your repo into the runner VM |
| Setup Python | Installs Python 3.11 |
| Install deps | Runs pip install -r requirements.txt |
| Run tests | Runs pytest — pipeline fails if any test fails |
| Secrets step | Injects secrets from GitHub Vault at runtime |

## Security Rules Followed

- No hardcoded credentials anywhere in code
- Secrets injected at runtime only, never stored in files
- Secrets are masked in all GitHub Actions logs
- Tests validate secret presence before deployment
- Fresh VM per run — no state leakage between runs
