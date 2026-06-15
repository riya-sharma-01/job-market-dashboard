import streamlit as st
import pandas as pd

from utils.filters import apply_filters
from utils.charts import (
    job_role_chart,
    salary_distribution,
    city_wise_demand,
    skill_analysis,
    experience_vs_salary,
    salary_trend,
    top_paying_jobs
)
from utils.insight import generate_insights

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Job Market Dashboard",
    layout="wide",
    page_icon="📊"
)

# ---------------- LOAD DATA ----------------
df = pd.read_csv("data/jobs.csv")

# ---------------- HEADER ----------------
st.title("📊 Job Market Intelligence Dashboard")
st.markdown(
    "🚀 *Explore real-time job trends, salary insights, and in-demand skills across the market.*"
)
st.divider()

# ---------------- FILTERS ----------------
df_filtered = apply_filters(df)

# ---------------- KPI CARDS ----------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📌 Total Jobs", len(df_filtered))

with col2:
    st.metric("💰 Avg Salary", f"{int(df_filtered['Salary'].mean())}")

with col3:
    st.metric("🏢 Companies", df_filtered["Company"].nunique())

with col4:
    st.metric("🧠 Top Skill", df_filtered["Skill"].value_counts().idxmax())
st.divider()

# ---------------- CHARTS SECTION ----------------
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(job_role_chart(df_filtered), use_container_width=True)
    st.plotly_chart(skill_analysis(df_filtered), use_container_width=True)

with col2:
    st.plotly_chart(salary_distribution(df_filtered), use_container_width=True)
    st.plotly_chart(city_wise_demand(df_filtered), use_container_width=True)

st.divider()

# ---------------- ADVANCED ANALYTICS ----------------
st.subheader("📈 Advanced Analytics")

st.plotly_chart(experience_vs_salary(df_filtered), use_container_width=True)
st.plotly_chart(salary_trend(df_filtered), use_container_width=True)

st.divider()

# ---------------- INSIGHTS ----------------
st.subheader("💡 AI-Generated Insights")

insights = generate_insights(df_filtered)

for i in insights:
    st.markdown(i)

# ---------------- DATA PREVIEW ----------------
with st.expander("📂 View Dataset"):
    st.dataframe(df_filtered)

# ---------------- DOWNLOAD BUTTON ----------------
csv = df_filtered.to_csv(index=False).encode('utf-8')

st.download_button(
    "⬇ Download Filtered Data",
    data=csv,
    file_name="filtered_jobs.csv",
    mime="text/csv"
)