"""Plain-language market insights derived from the filtered data."""

from .analysis import format_inr


def generate_insights(df):
    if df.empty:
        return []

    top_role = df["Job Title"].mode().iloc[0]
    top_city = df["Location"].mode().iloc[0]
    top_skill = df["Skill"].mode().iloc[0]
    average_salary = format_inr(df["Salary"].mean())
    highest_paying_role = df.groupby("Job Title")["Salary"].median().idxmax()

    return [
        ("Most in-demand role", top_role),
        ("Strongest hiring city", top_city),
        ("Most requested skill", top_skill),
        ("Average listed salary", average_salary),
        ("Highest median-pay role", highest_paying_role),
    ]
