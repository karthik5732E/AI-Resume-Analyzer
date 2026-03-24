import streamlit as st
import pandas as pd
from utils import analyze_new_resume
import PyPDF2

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(page_title="AI Resume Analyzer Pro", layout="wide")

# ------------------------------
# DARK UI (HIGH CONTRAST)
# ------------------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: #020617;
    color: #ffffff;
}
p, span, div {
    color: #e2e8f0 !important;
    font-size: 16px;
}
h1, h2, h3 {
    color: #38bdf8;
}
.stButton>button {
    background-color: #38bdf8;
    color: black;
    border-radius: 8px;
    padding: 10px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# TITLE
# ------------------------------
st.title("🚀 AI Resume Analyzer (Pro)")

# ------------------------------
# INPUT SECTION
# ------------------------------
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

with col2:
    job_desc = st.text_area("Paste Job Description")

# ------------------------------
# PDF TEXT EXTRACT
# ------------------------------
def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# ------------------------------
# ANALYZE BUTTON
# ------------------------------
if st.button("Analyze Resume"):

    if uploaded_file and job_desc:

        resume_text = extract_text(uploaded_file)

        result = analyze_new_resume(resume_text, job_desc)

        score = result["score"] * 100
        matched = result["matched"]
        missing = result["missing"]

        # ------------------------------
        # 1. TOP SUMMARY
        # ------------------------------
        st.subheader("📊 Overall Match")

        if score > 75:
            status = "Excellent Fit ✅"
            color = "green"
        elif score > 50:
            status = "Moderate Fit ⚠️"
            color = "orange"
        else:
            status = "Low Fit ❌"
            color = "red"

        st.metric("Match Score", f"{score:.2f}%")
        st.markdown(f"### Status: :{color}[{status}]")

        # ------------------------------
        # 2. SKILL MATCH PROGRESS
        # ------------------------------
        st.subheader("📈 Skill Match Overview")

        total = len(matched) + len(missing) + 1
        match_ratio = len(matched) / total

        st.progress(match_ratio)

        st.write(f"✅ Matched Skills: {len(matched)}")
        st.write(f"❌ Missing Skills: {len(missing)}")

        # ------------------------------
        # 3. SKILL TABLE
        # ------------------------------
        st.subheader("🧩 Skill Breakdown")

        skills_data = []

        for skill in matched:
            skills_data.append({"Skill": skill, "Status": "✅ Matched"})

        for skill in missing:
            skills_data.append({"Skill": skill, "Status": "❌ Missing"})

        df = pd.DataFrame(skills_data)
        st.dataframe(df, use_container_width=True)

        # ------------------------------
        # 4. AI ANALYSIS
        # ------------------------------
        st.subheader("🧠 AI Evaluation")

        st.info(result["advice"])

        # ------------------------------
        # 5. SUGGESTIONS
        # ------------------------------
        st.subheader("🚀 Improvement Suggestions")

        for s in result["suggestions"]:
            st.write(f"✔ {s}")

    else:
        st.warning("Please upload resume and paste job description")