from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vectorizer = TfidfVectorizer()

def analyze_new_resume(resume_text, job_text):
    texts = [resume_text, job_text]
    vectors = vectorizer.fit_transform(texts)

    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

    resume_words = clean_text(resume_text)
    job_words = clean_text(job_text)
    
    missing = list(job_words - resume_words)[:10]
    matched = list(resume_words & job_words)[:10]

    if score > 0.75:
        advice = "Your resume strongly matches the job requirements. Focus on refining achievements and adding measurable impact."
    elif score > 0.5:
        advice = "Your resume partially matches the job. Improve by adding missing technical skills and aligning experience."
    else:
        advice = "Your resume has low relevance. You should improve core skills, add projects, and optimize keywords."

    suggestions = [
        f"Add skills like: {', '.join(missing[:5])}",
        "Use strong action verbs (Developed, Built, Designed)",
        "Add 2-3 real-world projects",
        "Include measurable achievements",
        "Customize resume for each job"
    ]

    return {
        "score": score,
        "missing": missing,
        "matched": matched,
        "advice": advice,
        "suggestions": suggestions
    }
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', '', text)  # remove symbols
    words = text.split()

    clean_words = [w for w in words if w not in ENGLISH_STOP_WORDS and len(w) > 2]

    return set(clean_words)