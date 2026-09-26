import pandas as pd
import pytest

from utils.analysis import (
    format_inr,
    market_summary,
    prepare_data,
    role_recommendations,
    skill_opportunities,
)


@pytest.fixture
def jobs():
    return pd.DataFrame(
        {
            "Job Title": ["Data Analyst", "Data Analyst", "ML Engineer"],
            "Company": ["A", "B", "C"],
            "Location": ["Mumbai", "Pune", "Mumbai"],
            "Salary": [600000, 900000, 1200000],
            "Skill": ["SQL", "Python", "Python"],
            "Experience": ["Fresher", "Mid", "Mid"],
            "Date": ["2026-01-01", "2026-02-01", "2026-03-01"],
        }
    )


def test_prepare_data_parses_and_sorts(jobs):
    prepared = prepare_data(jobs)
    assert prepared.iloc[0]["Job Title"] == "ML Engineer"
    assert pd.api.types.is_datetime64_any_dtype(prepared["Date"])


def test_prepare_data_reports_missing_columns():
    with pytest.raises(ValueError, match="Missing required columns"):
        prepare_data(pd.DataFrame({"Salary": [100]}))


def test_market_summary_handles_empty_frame(jobs):
    summary = market_summary(jobs.iloc[0:0])
    assert summary == {
        "jobs": 0,
        "average_salary": 0,
        "companies": 0,
        "top_skill": "—",
    }


def test_skill_opportunities_rank_by_openings(jobs):
    result = skill_opportunities(jobs, ["Python", "SQL"])
    assert result.iloc[0]["Skill"] == "Python"
    assert result.iloc[0]["Openings"] == 2
    assert result.iloc[0]["Market Share"] == pytest.approx(2 / 3)


def test_role_recommendations_match_selected_skills(jobs):
    result = role_recommendations(jobs, ["SQL"])
    assert result.iloc[0]["Job Title"] == "Data Analyst"
    assert result.iloc[0]["Matching Jobs"] == 1


@pytest.mark.parametrize(
    ("value", "expected"),
    [(123, "₹123"), (1234, "₹1,234"), (1234567, "₹12,34,567")],
)
def test_format_inr(value, expected):
    assert format_inr(value) == expected
