"""Streamlit sidebar filters."""

import streamlit as st


def apply_filters(df):
    st.sidebar.header("Explore the market")

    search = st.sidebar.text_input(
        "Search job titles",
        placeholder="e.g. Data Analyst",
    ).strip()

    locations = sorted(df["Location"].dropna().unique().tolist())
    skills = sorted(df["Skill"].dropna().unique().tolist())
    experience_levels = sorted(df["Experience"].dropna().unique().tolist())

    selected_locations = st.sidebar.multiselect("Locations", locations)
    selected_skills = st.sidebar.multiselect("Skills", skills)
    selected_experience = st.sidebar.multiselect("Experience", experience_levels)

    min_salary = int(df["Salary"].min())
    max_salary = int(df["Salary"].max())
    salary_range = st.sidebar.slider(
        "Annual salary range (₹)",
        min_salary,
        max_salary,
        (min_salary, max_salary),
        step=max(10_000, (max_salary - min_salary) // 100),
    )

    filtered = df.copy()
    if search:
        filtered = filtered[
            filtered["Job Title"].str.contains(search, case=False, na=False, regex=False)
        ]
    if selected_locations:
        filtered = filtered[filtered["Location"].isin(selected_locations)]
    if selected_skills:
        filtered = filtered[filtered["Skill"].isin(selected_skills)]
    if selected_experience:
        filtered = filtered[filtered["Experience"].isin(selected_experience)]

    return filtered[
        filtered["Salary"].between(salary_range[0], salary_range[1], inclusive="both")
    ]
