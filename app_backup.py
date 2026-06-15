import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Job Market Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
df = pd.read_csv("data/jobs.csv")
df["Date"] = pd.to_datetime(df["Date"])

# --------------------------------------------------
# TITLE
# --------------------------------------------------
st.title("📊 Job Market Analytics Dashboard")

st.markdown("""
Analyze hiring trends, salary insights, in-demand skills, and location-wise opportunities through an interactive dashboard.
""")

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------
st.sidebar.header("🔍 Filters")

selected_role = st.sidebar.multiselect(
    "Job Role",
    options=df["Job Title"].unique()
)

selected_city = st.sidebar.multiselect(
    "Location",
    options=df["Location"].unique()
)

selected_exp = st.sidebar.multiselect(
    "Experience Level",
    options=df["Experience"].unique()
)

# --------------------------------------------------
# FILTER DATA
# --------------------------------------------------
filtered_df = df.copy()

if selected_role:
    filtered_df = filtered_df[
        filtered_df["Job Title"].isin(selected_role)
    ]

if selected_city:
    filtered_df = filtered_df[
        filtered_df["Location"].isin(selected_city)
    ]

if selected_exp:
    filtered_df = filtered_df[
        filtered_df["Experience"].isin(selected_exp)
    ]

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------
st.divider()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Jobs",
    len(filtered_df)
)

col2.metric(
    "Average Salary",
    f"₹{int(filtered_df['Salary'].mean()):,}"
)

col3.metric(
    "Top City",
    filtered_df["Location"].mode()[0]
)

col4.metric(
    "Top Skill",
    filtered_df["Skill"].mode()[0]
)

# --------------------------------------------------
# DATA PREVIEW
# --------------------------------------------------
st.divider()

with st.expander("📄 View Filtered Dataset"):
    st.dataframe(filtered_df)

# --------------------------------------------------
# CHART DATA
# --------------------------------------------------
job_counts = (
    filtered_df["Job Title"]
    .value_counts()
    .reset_index()
)

job_counts.columns = ["Job Title", "Count"]

city_counts = (
    filtered_df["Location"]
    .value_counts()
    .reset_index()
)

city_counts.columns = ["City", "Jobs"]

skill_counts = (
    filtered_df["Skill"]
    .value_counts()
    .reset_index()
)

skill_counts.columns = ["Skill", "Count"]

# --------------------------------------------------
# CHARTS
# --------------------------------------------------
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📌 Top Job Roles")

    fig_roles = px.bar(
        job_counts,
        x="Job Title",
        y="Count",
        title="Most In-Demand Job Roles"
    )

    st.plotly_chart(fig_roles, use_container_width=True)

with col2:
    st.subheader("💰 Salary Distribution")

    fig_salary = px.histogram(
        filtered_df,
        x="Salary",
        nbins=20,
        title="Salary Distribution"
    )

    st.plotly_chart(fig_salary, use_container_width=True)

# --------------------------------------------------
# SECOND ROW OF CHARTS
# --------------------------------------------------
col3, col4 = st.columns(2)

with col3:
    st.subheader("🌆 City-wise Job Demand")

    fig_city = px.pie(
        city_counts,
        values="Jobs",
        names="City",
        title="Jobs by City"
    )

    st.plotly_chart(fig_city, use_container_width=True)

with col4:
    st.subheader("🚀 Most In-Demand Skills")

    fig_skill = px.bar(
        skill_counts,
        x="Skill",
        y="Count",
        title="Skill Demand"
    )

    st.plotly_chart(fig_skill, use_container_width=True)

# --------------------------------------------------
# TREND ANALYSIS
# --------------------------------------------------
st.divider()

st.subheader("📈 Job Posting Trends Over Time")

trend_data = (
    filtered_df.groupby(
        filtered_df["Date"].dt.to_period("M")
    )
    .size()
    .reset_index(name="Jobs")
)

trend_data["Date"] = trend_data["Date"].astype(str)

fig_trend = px.line(
    trend_data,
    x="Date",
    y="Jobs",
    markers=True,
    title="Job Postings Over Time"
)

st.plotly_chart(fig_trend, use_container_width=True)

# --------------------------------------------------
# INSIGHTS
# --------------------------------------------------
st.divider()

st.subheader("🔍 Key Insights")

top_role = filtered_df["Job Title"].mode()[0]
top_city = filtered_df["Location"].mode()[0]
avg_salary = int(filtered_df["Salary"].mean())

st.info(
    f"""
📌 Most demanded role: {top_role}

🌆 Highest hiring activity: {top_city}

💰 Average salary: ₹{avg_salary:,}
"""
)