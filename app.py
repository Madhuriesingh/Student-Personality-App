
import streamlit as st
from textblob import TextBlob
import matplotlib.pyplot as plt
import numpy as np

# Big Five keyword mappings (sample version)
trait_keywords = {
    'Openness': ['creative', 'imagine', 'curious', 'explore', 'dream', 'novel', 'ideas', 'art'],
    'Conscientiousness': ['organized', 'plan', 'schedule', 'discipline', 'focus', 'neat', 'goal'],
    'Extraversion': ['talk', 'friend', 'party', 'social', 'outgoing', 'meet', 'group'],
    'Agreeableness': ['kind', 'help', 'care', 'friendly', 'support', 'team', 'listen'],
    'Neuroticism': ['worried', 'nervous', 'anxious', 'upset', 'stressed', 'tense', 'panic']
}

def analyze_personality(text):
    blob = TextBlob(text.lower())
    sentiment = blob.sentiment.polarity
    scores = {}

    for trait, keywords in trait_keywords.items():
        keyword_score = sum(word in text.lower() for word in keywords)
        if trait == 'Neuroticism':
            combined_score = min(100, (keyword_score * 20 + (1 - sentiment) * 50))
        else:
            combined_score = min(100, (keyword_score * 20 + sentiment * 50))
        scores[trait] = round(combined_score, 1)

    return scores

def draw_radar_chart(scores):
    labels = list(scores.keys())
    values = list(scores.values())
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, linewidth=2, linestyle='solid')
    ax.fill(angles, values, alpha=0.3)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_title('Personality Profile (Big Five)', size=16)
    st.pyplot(fig)

# Streamlit UI
st.title("Student Personality Analyzer (Big Five Model)")

with st.form("personality_form"):
    name = st.text_input("Student Name")
    age = st.number_input("Age", min_value=10, max_value=25)
    grade = st.text_input("Grade / Year")
    prompt = st.selectbox("Choose a prompt", [
        "Describe yourself and your ideal day.",
        "What motivates you and why?",
        "Tell us about a challenge you overcame."
    ])
    response = st.text_area("Your Response", height=200)
    submitted = st.form_submit_button("Analyze Personality")

if submitted:
    scores = analyze_personality(response)
    st.subheader(f"{name}'s Personality Profile")
    draw_radar_chart(scores)

    st.markdown("### Summary")
    for trait, score in scores.items():
        if score >= 70:
            level = "High"
        elif score >= 40:
            level = "Moderate"
        else:
            level = "Low"
        st.write(f"**{trait}:** {level} ({score}/100)")
