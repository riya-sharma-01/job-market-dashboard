<div align="center">

# 📈 CareerPulse

### Job market intelligence for students and early-career professionals

[![Live app](https://img.shields.io/badge/Live_App-Open-6C63FF?style=for-the-badge&logo=streamlit&logoColor=white)](https://job-market-dashboard-36b5vjygjhqfmgxnvkznaq.streamlit.app/)
[![Tests](https://github.com/riya-sharma-01/job-market-dashboard/actions/workflows/tests.yml/badge.svg)](https://github.com/riya-sharma-01/job-market-dashboard/actions/workflows/tests.yml)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-20C997?style=flat-square)](LICENSE)

Turn a sample job-listing dataset into clear signals about roles, skills, salaries and locations.

</div>

## Why CareerPulse?

Job datasets are easy to chart but harder to turn into a useful decision tool. CareerPulse combines an interactive market dashboard with a **Career Fit planner** that connects a learner's selected skills to matching roles, salary signals and hiring locations.

## Highlights

- Filter by title, location, skill, experience and annual salary
- Compare role demand, city demand and salary distributions
- Track median salary trends and experience-level pay
- Build a personal skill-opportunity report in the Career Fit tab
- Rank relevant roles for selected skills
- Explore and export the filtered dataset
- Handle empty filters and malformed data gracefully
- Verify analytics helpers through automated tests on every pull request

> **Data note:** The included CSV is a synthetic portfolio dataset. Results demonstrate the analysis workflow and are not live employment-market claims.

## Quick start

```bash
git clone https://github.com/riya-sharma-01/job-market-dashboard.git
cd job-market-dashboard
python -m venv .venv
```

Activate the environment, then run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

## Test the analytics

```bash
pip install -r requirements-dev.txt
pytest -q
```

## Project structure

```text
job-market-dashboard/
├── .github/workflows/tests.yml
├── data/jobs.csv
├── tests/test_analysis.py
├── utils/
│   ├── analysis.py
│   ├── charts.py
│   ├── filters.py
│   └── insight.py
├── app.py
├── requirements.txt
└── requirements-dev.txt
```

## Built with

- **Streamlit** for the interactive product interface
- **Pandas** for validation, filtering and aggregation
- **Plotly** for interactive visualizations
- **Pytest + GitHub Actions** for reliable analytics logic

## Roadmap

- Add a real, refreshable job-data source
- Support multi-skill listings and weighted match scores
- Add city cost-of-living context
- Publish a methodology and data dictionary

## Contributing

Ideas and improvements are welcome. Open an issue describing the problem and expected outcome before submitting a larger pull request.

## Author

Built by [Riya Sharma](https://github.com/riya-sharma-01), a Data Science & AI student interested in practical analytics products.

If CareerPulse helps you learn or sparks an idea, consider starring the repository.
