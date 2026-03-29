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
