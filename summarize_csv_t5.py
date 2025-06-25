import pandas as pd
from transformers import pipeline

# Load small summarizer
summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")

# Load CSV
df = pd.read_csv("parsed_resumes.csv")

# Columns to summarize
columns_to_summarize = ["Experience", "Projects", "Education"]

def summarize_text(text):
    try:
        if isinstance(text, str) and len(text.split()) > 20:
            summary = summarizer(text, max_length=50, min_length=15, do_sample=False)
            return summary[0]['summary_text']
        return text
    except Exception as e:
        print("⚠️ Error summarizing:", e)
        return text

# Apply
for column in columns_to_summarize:
    if column in df.columns:
        print(f"🧠 Summarizing: {column} (T5)")
        df[column] = df[column].apply(summarize_text)

# Save result
df.to_csv("parsed_resumes_t5.csv", index=False)
print("✅ T5 Summary done! Output saved to parsed_resumes_t5.csv")
