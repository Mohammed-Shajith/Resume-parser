import pandas as pd
from rapidfuzz import fuzz

SKILL_WEIGHT = 0.45
EXPERIENCE_WEIGHT = 0.20
EDUCATION_WEIGHT = 0.35

skills_options = [
    "machine learning", "web development", "full stack",
    "python", "flask", "sql", "html", "css", "javascript"
]

experience_options = [
    "fresher", "1-2 years", "3-5 years", "5+ years"
]

education_options = [
    "b.e", "b.tech", "computer science", "artificial intelligence",
    "cybersecurity", "cse", "information technology"
]

print("\nSelect SKILLS (comma-separated numbers):")
for i, skill in enumerate(skills_options, 1):
    print(f"{i}. {skill}")
skill_input = input("Enter choices (e.g., 1,3,5): ")
selected_skills = [skills_options[int(i.strip()) - 1].lower() for i in skill_input.split(',') if i.strip().isdigit()]

print("\nSelect EXPERIENCE (comma-separated numbers):")
for i, exp in enumerate(experience_options, 1):
    print(f"{i}. {exp}")
exp_input = input("Enter choices (e.g., 2,3): ")
selected_exp = [experience_options[int(i.strip()) - 1].lower() for i in exp_input.split(',') if i.strip().isdigit()]

print("\nSelect EDUCATION (comma-separated numbers):")
for i, edu in enumerate(education_options, 1):
    print(f"{i}. {edu}")
edu_input = input("Enter choices (e.g., 1,3,5): ")
selected_edu = [education_options[int(i.strip()) - 1].lower() for i in edu_input.split(',') if i.strip().isdigit()]

try:
    df = pd.read_csv("parsed_resumes.csv")
except FileNotFoundError:
    print(" parsed_resumes.csv not found.")
    exit()
#fuzzy
def fuzzy_match_score(text, keywords):
    if not isinstance(text, str) or not keywords:
        return 0.0
    scores = []
    for kw in keywords:
        best_score = max([fuzz.partial_ratio(kw, part) for part in text.lower().split()])
        scores.append(best_score)
    return sum(scores) / (len(keywords) * 100)

results = []
for _, row in df.iterrows():
    filename = row.get("Filename", "Unknown")
    name = row.get("Name", "Unknown")

    skill_score = fuzzy_match_score(row.get("Skills", ""), selected_skills)
    exp_score = fuzzy_match_score(row.get("Experience", ""), selected_exp)
    edu_score = fuzzy_match_score(row.get("Education", ""), selected_edu)

    final_score = round((
        skill_score * SKILL_WEIGHT +
        exp_score * EXPERIENCE_WEIGHT +
        edu_score * EDUCATION_WEIGHT
    ) * 10, 2)

    results.append({
        "Filename": filename,
        "Name": name,
        "Skill Score (/10)": round(skill_score * 10, 2),
        "Skill (Weight 45%)": round(skill_score * SKILL_WEIGHT * 10, 2),
        "Experience Score (/10)": round(exp_score * 10, 2),
        "Experience (Weight 20%)": round(exp_score * EXPERIENCE_WEIGHT * 10, 2),
        "Education Score (/10)": round(edu_score * 10, 2),
        "Education (Weight 35%)": round(edu_score * EDUCATION_WEIGHT * 10, 2),
        "Final Score (/10)": final_score
    })

scored_df = pd.DataFrame(results)
scored_df = scored_df.sort_values(by="Final Score (/10)", ascending=False).reset_index(drop=True)
scored_df.insert(0, "Rank", scored_df.index + 1)  #Rank coloumn

scored_df.to_csv("scored_resumes.csv", index=False)

# Top 3 
print("\n Top 3 Candidates:\n")
print(scored_df[["Rank", "Name", "Filename", "Final Score (/10)"]].head(3).to_string(index=False))
print("\n Done! 'CHECK scored_resumes.csv' ")
