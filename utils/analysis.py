"""Pure data preparation and analytics helpers for CareerPulse."""

from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = {
    "Job Title",
    "Company",
    "Location",
    "Salary",
    "Skill",
    "Experience",
    "Date",
}


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """Validate and clean the job-market dataset without mutating the input."""
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    clean = df.copy()
    clean["Salary"] = pd.to_numeric(clean["Salary"], errors="coerce")
    clean["Date"] = pd.to_datetime(clean["Date"], errors="coerce")

    text_columns = ["Job Title", "Company", "Location", "Skill", "Experience"]
    for column in text_columns:
        clean[column] = clean[column].astype("string").str.strip()

    clean = clean.dropna(subset=["Job Title", "Salary", "Skill", "Date"])
    clean = clean[clean["Salary"] > 0]
    return clean.sort_values("Date", ascending=False).reset_index(drop=True)


def format_inr(value: float | int) -> str:
    """Format a number using Indian digit grouping, e.g. INR 12,34,567."""
    amount = int(round(float(value)))
    sign = "-" if amount < 0 else ""
    digits = str(abs(amount))

    if len(digits) <= 3:
        grouped = digits
    else:
        tail = digits[-3:]
        head = digits[:-3]
        pairs = []
        while head:
            pairs.append(head[-2:])
            head = head[:-2]
        grouped = ",".join(reversed(pairs)) + "," + tail

    return f"{sign}₹{grouped}"


def market_summary(df: pd.DataFrame) -> dict[str, object]:
    """Return dashboard KPIs, with safe defaults for an empty result set."""
    if df.empty:
        return {
            "jobs": 0,
            "average_salary": 0,
            "companies": 0,
            "top_skill": "—",
        }

    return {
        "jobs": len(df),
        "average_salary": float(df["Salary"].mean()),
        "companies": int(df["Company"].nunique()),
        "top_skill": str(df["Skill"].mode().iloc[0]),
    }


def skill_opportunities(df: pd.DataFrame, selected_skills: list[str]) -> pd.DataFrame:
    """Rank selected skills by openings, pay and coverage of the filtered market."""
    columns = ["Skill", "Openings", "Average Salary", "Top City", "Market Share"]
    if df.empty or not selected_skills:
        return pd.DataFrame(columns=columns)

    selected = df[df["Skill"].isin(selected_skills)]
    if selected.empty:
        return pd.DataFrame(columns=columns)

    rows = []
    for skill, group in selected.groupby("Skill"):
        rows.append(
            {
                "Skill": skill,
                "Openings": len(group),
                "Average Salary": float(group["Salary"].mean()),
                "Top City": str(group["Location"].mode().iloc[0]),
                "Market Share": len(group) / len(df),
            }
        )

    return (
        pd.DataFrame(rows, columns=columns)
        .sort_values(["Openings", "Average Salary"], ascending=False)
        .reset_index(drop=True)
    )


def role_recommendations(df: pd.DataFrame, selected_skills: list[str], limit: int = 8) -> pd.DataFrame:
    """Return the strongest job-title matches for a user's selected skills."""
    columns = ["Job Title", "Matching Jobs", "Average Salary", "Top Location"]
    if df.empty or not selected_skills:
        return pd.DataFrame(columns=columns)

    matches = df[df["Skill"].isin(selected_skills)]
    if matches.empty:
        return pd.DataFrame(columns=columns)

    rows = []
    for role, group in matches.groupby("Job Title"):
        rows.append(
            {
                "Job Title": role,
                "Matching Jobs": len(group),
                "Average Salary": float(group["Salary"].mean()),
                "Top Location": str(group["Location"].mode().iloc[0]),
            }
        )

    return (
        pd.DataFrame(rows, columns=columns)
        .sort_values(["Matching Jobs", "Average Salary"], ascending=False)
        .head(limit)
        .reset_index(drop=True)
    )
