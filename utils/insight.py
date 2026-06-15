def generate_insights(df):
    insights = []

    top_role = df["Job Title"].value_counts().idxmax()
    insights.append(f"📌 Most in-demand role: **{top_role}**")

    top_city = df["Location"].value_counts().idxmax()
    insights.append(f"📍 Highest job postings are from: **{top_city}**")

    top_skill = df["Skill"].value_counts().idxmax()
    insights.append(f"🧠 Most required skill: **{top_skill}**")

    avg_salary = int(df["Salary"].mean())
    insights.append(f"💰 Average salary in dataset: **{avg_salary}**")

    max_salary_role = df.groupby("Job Title")["Salary"].mean().idxmax()
    insights.append(f"🚀 Highest paying role on average: **{max_salary_role}**")

    return insights