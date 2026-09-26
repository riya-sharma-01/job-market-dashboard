"""Consistently styled Plotly charts for CareerPulse."""

import pandas as pd
import plotly.express as px


PRIMARY = "#6C63FF"
ACCENT = "#20C997"


def _polish(fig, height=390):
    fig.update_layout(
        height=height,
        margin=dict(l=12, r=12, t=58, b=12),
        coloraxis_showscale=False,
        legend_title_text="",
        hoverlabel=dict(bgcolor="white"),
    )
    return fig


def job_role_chart(df):
    counts = df["Job Title"].value_counts().head(10).sort_values()
    fig = px.bar(
        x=counts.values,
        y=counts.index,
        orientation="h",
        title="Most advertised roles",
        labels={"x": "Openings", "y": ""},
        color=counts.values,
        color_continuous_scale=["#DCD9FF", PRIMARY],
    )
    return _polish(fig)


def salary_distribution(df):
    fig = px.histogram(
        df,
        x="Salary",
        nbins=24,
        title="Salary distribution",
        labels={"Salary": "Annual salary (₹)"},
        color_discrete_sequence=[PRIMARY],
    )
    return _polish(fig)


def city_wise_demand(df):
    counts = df["Location"].value_counts().head(10)
    fig = px.bar(
        x=counts.index,
        y=counts.values,
        title="Demand by city",
        labels={"x": "", "y": "Openings"},
        color=counts.values,
        color_continuous_scale=["#D8F8EE", ACCENT],
    )
    return _polish(fig)


def skill_analysis(df):
    counts = df["Skill"].value_counts().head(10).sort_values()
    fig = px.bar(
        x=counts.values,
        y=counts.index,
        orientation="h",
        title="Skills employers request",
        labels={"x": "Openings", "y": ""},
        color=counts.values,
        color_continuous_scale=["#D8F8EE", ACCENT],
    )
    return _polish(fig)


def experience_vs_salary(df):
    summary = (
        df.groupby("Experience", as_index=False)["Salary"]
        .median()
        .sort_values("Salary")
    )
    fig = px.bar(
        summary,
        x="Experience",
        y="Salary",
        title="Median salary by experience",
        labels={"Experience": "", "Salary": "Median annual salary (₹)"},
        color="Salary",
        color_continuous_scale=["#FFE8C7", "#FF9F43"],
    )
    return _polish(fig)


def salary_trend(df):
    monthly = (
        df.assign(Month=pd.to_datetime(df["Date"]).dt.to_period("M").dt.to_timestamp())
        .groupby("Month", as_index=False)["Salary"]
        .median()
        .sort_values("Month")
    )
    fig = px.line(
        monthly,
        x="Month",
        y="Salary",
        markers=True,
        title="Median salary trend",
        labels={"Month": "", "Salary": "Median annual salary (₹)"},
        color_discrete_sequence=[PRIMARY],
    )
    return _polish(fig)


def top_paying_jobs(df):
    roles = df.groupby("Job Title")["Salary"].median().nlargest(10).sort_values()
    fig = px.bar(
        x=roles.values,
        y=roles.index,
        orientation="h",
        title="Highest-paying roles",
        labels={"x": "Median annual salary (₹)", "y": ""},
        color=roles.values,
        color_continuous_scale=["#FDE2EA", "#E64980"],
    )
    return _polish(fig)
