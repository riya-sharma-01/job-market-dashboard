import plotly.express as px
import pandas as pd


def job_role_chart(df):
    role_counts = df["Job Title"].value_counts().head(10)
    fig = px.bar(
        x=role_counts.values,
        y=role_counts.index,
        orientation="h",
        title="Top Job Roles",
        labels={"x": "Number of Jobs", "y": "Job Title"},
        color=role_counts.values,
        color_continuous_scale="blues"
    )
    fig.update_layout(height=400)
    return fig


def salary_distribution(df):
    fig = px.histogram(
        df,
        x="Salary",
        nbins=30,
        title="Salary Distribution",
        color_discrete_sequence=["#636EFA"]
    )
    fig.update_layout(height=400)
    return fig


def city_wise_demand(df):
    city_counts = df["Location"].value_counts().head(10)
    fig = px.bar(
        x=city_counts.index,
        y=city_counts.values,
        title="City-wise Job Demand",
        labels={"x": "City", "y": "Number of Jobs"},
        color=city_counts.values,
        color_continuous_scale="greens"
    )
    fig.update_layout(height=400)
    return fig


def skill_analysis(df):
    skill_counts = df["Skill"].value_counts().head(10)
    fig = px.pie(
        names=skill_counts.index,
        values=skill_counts.values,
        title="Top Skills in Demand"
    )
    fig.update_layout(height=400)
    return fig


def experience_vs_salary(df):
    fig = px.scatter(
        df,
        x="Experience",
        y="Salary",
        color="Job Title",
        title="Experience vs Salary",
        hover_data=["Company", "Location"]
    )
    fig.update_layout(height=450)
    return fig


def salary_trend(df):
    df["Date"] = pd.to_datetime(df["Date"])
    trend = df.groupby("Date")["Salary"].mean().reset_index()

    fig = px.line(
        trend,
        x="Date",
        y="Salary",
        title="Salary Trend Over Time"
    )
    fig.update_layout(height=400)
    return fig
def top_paying_jobs(df):
    top_jobs = df.groupby("Job Title")["Salary"].mean().sort_values(ascending=False).head(10)

    fig = px.bar(
        x=top_jobs.values,
        y=top_jobs.index,
        orientation="h",
        title="Top Paying Job Roles",
        labels={"x": "Average Salary", "y": "Job Title"},
        color=top_jobs.values,
        color_continuous_scale="reds"
    )
    fig.update_layout(height=400)
    return fig