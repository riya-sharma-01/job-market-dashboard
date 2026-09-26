# Contributing to CareerPulse

Thank you for helping improve CareerPulse. Contributions that make the dashboard clearer, more reliable, or more useful for students and early-career professionals are welcome.

## Ways to contribute

- Report a reproducible bug
- Improve documentation or onboarding
- Add or strengthen automated tests
- Improve accessibility and empty states
- Propose a focused analytics or visualization improvement

For larger changes, open an issue first and describe the problem, expected outcome, and proposed scope.

## Local setup

```bash
git clone https://github.com/riya-sharma-01/job-market-dashboard.git
cd job-market-dashboard
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# macOS/Linux
source .venv/bin/activate
```

Install the project and development dependencies:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Before opening a pull request

Run the automated tests:

```bash
pytest -q
```

Start the app and check the affected workflow:

```bash
streamlit run app.py
```

Keep each pull request focused on one problem. Include:

- A clear explanation of the problem and solution
- Screenshots for visible interface changes
- Tests for changed analytics behavior
- Any limitations or follow-up work

Do not commit virtual environments, secrets, generated caches, or personal data.
