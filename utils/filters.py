import streamlit as st


def apply_filters(df):
    st.sidebar.header("🔍 Filter Jobs")

    # Job title search
    search = st.sidebar.text_input("Search Job Title")

    # Location filter
    locations = df["Location"].unique()
    selected_location = st.sidebar.multiselect("Location", locations, default=locations)

    # Skill filter
    skills = df["Skill"].unique()
    selected_skills = st.sidebar.multiselect("Skill", skills, default=skills)

    # Salary filter
    min_salary = int(df["Salary"].min())
    max_salary = int(df["Salary"].max())

    salary_range = st.sidebar.slider(
        "Salary Range",
        min_salary,
        max_salary,
        (min_salary, max_salary)
    )

    # Apply filters
    filtered_df = df.copy()

    if search:
        filtered_df = filtered_df[
            filtered_df["Job Title"].str.contains(search, case=False, na=False)
        ]

    filtered_df = filtered_df[
        filtered_df["Location"].isin(selected_location)
    ]

    filtered_df = filtered_df[
        filtered_df["Skill"].isin(selected_skills)
    ]

    filtered_df = filtered_df[
        (filtered_df["Salary"] >= salary_range[0]) &
        (filtered_df["Salary"] <= salary_range[1])
    ]

    return filtered_df