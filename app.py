from pathlib import Path

import pandas as pd
import streamlit as st

from utils.analysis import (
    format_inr,
    market_summary,
    prepare_data,
    role_recommendations,
    skill_opportunities,
)
from utils.charts import (
    city_wise_demand,
    experience_vs_salary,
    job_role_chart,
    salary_distribution,
    salary_trend,
    skill_analysis,
    top_paying_jobs,
)
from utils.filters import apply_filters
from utils.insight import generate_insights


DATA_PATH = Path(__file__).parent / "data" / "jobs.csv"

st.set_page_config(
    page_title="CareerPulse | Job Market Intelligence",
    page_icon="📈",
    layout="wide",
)

st.markdown(
    """
    <style>
      .block-container {padding-top: 2rem; max-width: 1320px;}
      [data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(108,99,255,.10), rgba(32,201,151,.08));
        border: 1px solid rgba(108,99,255,.18);
        border-radius: 16px;
        padding: 1rem;
      }
      .hero {
        padding: 1.4rem 1.6rem;
        border-radius: 20px;
        background: linear-gradient(120deg, #201B4F, #4438A8 60%, #187F70);
        color: white;
        margin-bottom: 1.2rem;
      }
      .hero h1 {margin: 0; font-size: 2.15rem;}
      .hero p {margin: .45rem 0 0; opacity: .88;}
      .insight {
        border-left: 4px solid #6C63FF;
        padding: .75rem 1rem;
        background: rgba(108,99,255,.07);
        border-radius: 0 12px 12px 0;
        margin: .45rem 0;
      }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    return prepare_data(pd.read_csv(path))


try:
    jobs = load_data(DATA_PATH)
except (OSError, ValueError) as error:
    st.error(f"The dataset could not be loaded: {error}")
    st.stop()

st.markdown(
    """
    <div class="hero">
      <h1>CareerPulse</h1>
      <p>Turn job listings into clear salary, skill and career signals.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

filtered = apply_filters(jobs)
overview_tab, planner_tab, explorer_tab = st.tabs(
    ["Market overview", "Career fit", "Job explorer"]
)

with overview_tab:
    if filtered.empty:
        st.warning("No jobs match these filters. Try widening the salary range or clearing a filter.")
    else:
        summary = market_summary(filtered)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Jobs", f"{summary['jobs']:,}")
        col2.metric("Average salary", format_inr(summary["average_salary"]))
        col3.metric("Companies", f"{summary['companies']:,}")
        col4.metric("Top skill", summary["top_skill"])

        left, right = st.columns(2)
        with left:
            st.plotly_chart(job_role_chart(filtered), use_container_width=True)
            st.plotly_chart(skill_analysis(filtered), use_container_width=True)
            st.plotly_chart(experience_vs_salary(filtered), use_container_width=True)
        with right:
            st.plotly_chart(salary_distribution(filtered), use_container_width=True)
            st.plotly_chart(city_wise_demand(filtered), use_container_width=True)
            st.plotly_chart(salary_trend(filtered), use_container_width=True)

        st.plotly_chart(top_paying_jobs(filtered), use_container_width=True)

        st.subheader("What the data says")
        for label, value in generate_insights(filtered):
            st.markdown(
                f'<div class="insight"><strong>{label}</strong><br>{value}</div>',
                unsafe_allow_html=True,
            )

with planner_tab:
    st.subheader("Find where your skills fit")
    st.caption(
        "Choose skills you already have or want to learn. CareerPulse ranks the roles, "
        "locations and salary signals connected to them."
    )
    available_skills = sorted(jobs["Skill"].unique().tolist())
    selected_skills = st.multiselect(
        "Your skills",
        available_skills,
        placeholder="Select one or more skills",
    )

    if not selected_skills:
        st.info("Select at least one skill to build your career-fit report.")
    else:
        opportunities = skill_opportunities(filtered, selected_skills)
        roles = role_recommendations(filtered, selected_skills)

        if opportunities.empty:
            st.warning("Those skills do not appear in the current filtered market. Clear a sidebar filter and try again.")
        else:
            best = opportunities.iloc[0]
            first, second, third = st.columns(3)
            first.metric("Strongest skill signal", best["Skill"])
            second.metric("Matching openings", int(opportunities["Openings"].sum()))
            third.metric("Best skill average", format_inr(best["Average Salary"]))

            display_opportunities = opportunities.copy()
            display_opportunities["Average Salary"] = display_opportunities["Average Salary"].map(format_inr)
            display_opportunities["Market Share"] = display_opportunities["Market Share"].map(lambda x: f"{x:.1%}")
            st.markdown("#### Skill opportunity map")
            st.dataframe(display_opportunities, use_container_width=True, hide_index=True)

            display_roles = roles.copy()
            display_roles["Average Salary"] = display_roles["Average Salary"].map(format_inr)
            st.markdown("#### Roles to explore")
            st.dataframe(display_roles, use_container_width=True, hide_index=True)

with explorer_tab:
    st.subheader("Explore the underlying listings")
    if filtered.empty:
        st.info("There are no rows to display for the current filters.")
    else:
        visible_columns = [
            "Job Title",
            "Company",
            "Location",
            "Salary",
            "Skill",
            "Experience",
            "Date",
        ]
        table = filtered[visible_columns].copy()
        table["Date"] = table["Date"].dt.date
        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Salary": st.column_config.NumberColumn("Salary", format="₹%d"),
                "Date": st.column_config.DateColumn("Posted"),
            },
        )
        st.download_button(
            "Download filtered CSV",
            data=filtered.to_csv(index=False).encode("utf-8"),
            file_name="careerpulse_filtered_jobs.csv",
            mime="text/csv",
            use_container_width=True,
        )

st.caption("Built with Python, Pandas, Plotly and Streamlit • Sample dataset for portfolio analysis")
