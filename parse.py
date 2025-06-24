import streamlit as st
import pandas as pd
import os
import tempfile
from parser import parse_resume

st.set_page_config(page_title="Resume Parser", layout="centered")

st.title("Resume Parser")

uploaded_files = st.file_uploader("Upload PDF resumes", type="pdf", accept_multiple_files=True)

if uploaded_files:
    parsed_data = []

    for uploaded_file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_path = temp_file.name

        result = parse_resume(temp_path)
        result["Filename"] = uploaded_file.name
        parsed_data.append(result)

        os.remove(temp_path)

    df = pd.DataFrame(parsed_data)
    st.success("Parsing Complete!")
    st.dataframe(df)

    csv = df.to_csv(index=False)
    st.download_button("Download as CSV", csv, "parsed_resumes.csv", "text/csv")
