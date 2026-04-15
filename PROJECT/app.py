"""
AI Resume Analyzer - Main Application
Built with Streamlit | Python | gemini API
"""

# from http import client
# from urllib import response

# from click import prompt
# from flask import json
import json

import streamlit as st
import pdfplumber
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import re
import os
import google.generativeai as genai
try:
    from bytez import Bytez
except ImportError:
    Bytez = None

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS - Clean & Professional UI
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* Global */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .main { background-color: #f8fafc; }

    /* Glassmorphism Cards */
    .result-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.75rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid #e2e8f0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .result-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04);
    }
    
    /* Left accent variants */
    .border-blue { border-left: 5px solid #3b82f6; }
    .border-green { border-left: 5px solid #10b981; }
    .border-red { border-left: 5px solid #ef4444; }
    .border-purple { border-left: 5px solid #8b5cf6; }
    .border-amber { border-left: 5px solid #f59e0b; }

    /* Score styling */
    .score-badge {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: -webkit-linear-gradient(45deg, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
    }

    /* Typography */
    .section-header {
        font-size: 1.15rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Skill Chips */
    .skill-chip {
        display: inline-flex;
        align-items: center;
        background: #f1f5f9;
        color: #334155;
        border: 1px solid #cbd5e1;
        border-radius: 9999px; /* full pill */
        padding: 4px 14px;
        margin: 4px;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.025em;
        transition: all 0.2s;
    }
    .skill-chip:hover {
        background: #e2e8f0;
        color: #0f172a;
    }
    .skill-chip.missing {
        background: #fef2f2;
        color: #b91c1c;
        border-color: #fecaca;
    }

    /* App Header */
    .app-header {
        text-align: center;
        padding: 2.5rem 0 1.5rem 0;
        background: linear-gradient(180deg, #f0fdfa 0%, #f8fafc 100%);
        border-radius: 0 0 24px 24px;
        margin-top: -3rem;
        margin-bottom: 2rem;
        border-bottom: 1px solid #e2e8f0;
    }
    .app-title {
        color: #0f172a;
        font-size: 2.75rem;
        font-weight: 800;
        letter-spacing: -0.025em;
        margin: 0;
    }
    .app-subtitle {
        color: #64748b;
        font-size: 1.15rem;
        margin-top: 0.5rem;
    }
    
    /* Tabs Overrides */
    div[data-baseweb="tab-list"] {
        gap: 1rem;
        border-bottom: 2px solid #e2e8f0;
    }
    div[data-baseweb="tab"] {
        font-size: 1rem;
        font-weight: 600;
        padding-bottom: 0.5rem;
    }
    
    /* Upload area */
    .stFileUploader { border-radius: 12px; }

    /* Sidebar */
    .css-1d391kg { background-color: #1e1b4b; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SECTION 1: PDF TEXT EXTRACTION
# ─────────────────────────────────────────────
def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract plain text from a PDF resume using pdfplumber.
    pdfplumber reads each page and joins the text together.
    Returns: string with all resume text
    """
    full_text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"
    return full_text.strip()


# ─────────────────────────────────────────────
# SECTION 2: AI-POWERED ANALYSIS via gemini
# ─────────────────────────────────────────────
def get_ai_service():
    """
    Returns a dictionary with 'type' ('google' or 'bytez') and 'client'.
    Prefers Google Gemini API via secrets, falls back to Bytez API.
    """
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    
    if api_key:
        genai.configure(api_key=api_key)
        return {
            "type": "google",
            "client": genai.GenerativeModel("models/gemini-2.5-flash-lite")
        }
    
    # Fallback to Bytez
    if Bytez is not None:
        try:
            bytez_key = "95e3d425613b1c1736a910b4c1512339"
            sdk = Bytez(bytez_key)
            return {
                "type": "bytez",
                "client": sdk.model("google/gemini-2.5-flash-lite")
            }
        except Exception:
            pass
            
    return None

PROMPT_1_ANALYSIS = """Analyze this resume text and extract skills, education, and experience.
Also identify strengths and weaknesses.

Resume: {resume_text}

Respond in this exact JSON format:
{ "skills": [...], "education":[...], "experience": [...], "strengths": [...], "weaknesses": [...] }"""

PROMPT_2_SCORING = """Based on the resume content, give a score out of 100 and explain why.

Resume: {resume_text}

Respond in this exact JSON format:
{ "score": <0-100>, "score_breakdown": { "skills": <0-25>, "experience": <0-25>, "education": <0-25>, "formatting": <0-25> }, "explanation": "..." }"""

PROMPT_3_SUGGESTIONS = """Suggest improvements to make this resume better for software engineering roles.
Target Job Description (optional): {job_desc}

Resume: {resume_text}

Respond in this exact JSON format:
{ "suggestions": ["suggestion 1", "suggestion 2", ...], "missing_skills": ["skill1", "skill2", ...] }"""

def analyze_resume_with_ai(resume_text: str, ai_service: dict, job_desc: str = "") -> dict:
    """
    Optimized token usage: Combines extraction, grading, and suggestions into a SINGLE AI call 
    instead of three back-to-back calls.
    """
    jd_context = f"\nTarget Job Description:\n{job_desc}" if job_desc else ""
    
    # Token optimization: reduce extra whitespace and limit length reasonably
    cleaned_resume = " ".join(resume_text.split())[:4000]

    prompt = f"""You are an expert AI resume analyzer and technical recruiter.
Analyze the following resume and return the result strictly in JSON.{jd_context}

Resume:
{cleaned_resume}

Respond EXACTLY in this JSON format. No markdown blocks, just the raw JSON:
{{
  "analysis": {{
    "skills": ["<skill1>", "<skill2>"],
    "education": ["<degree/institution - year>"],
    "experience": ["<job title at company - duration>"],
    "strengths": ["<strength1>", "<strength2>"],
    "weaknesses": ["<weakness1>"]
  }},
  "score": {{
    "score": <number 0-100>,
    "score_breakdown": {{
        "skills": <0-25>,
        "experience": <0-25>,
        "education": <0-25>,
        "formatting": <0-25>
    }},
    "explanation": "<short explanation>"
  }},
  "suggestions": {{
    "suggestions": ["<suggestion 1>", "<suggestion 2>"],
    "missing_skills": ["<skill1>", "<skill2>"]
  }}
}}"""

    try:
        if ai_service["type"] == "google":
            response = ai_service["client"].generate_content(prompt)
            output_text = response.text
        else:
            response = ai_service["client"].run([{
                "role": "user",
                "content": prompt
            }])
            output_text = response.output

        clean_text = output_text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)
    except Exception as e:
        print(f"AI API Error: {e}")
        raise e


# ─────────────────────────────────────────────
# SECTION 3: SIMULATED AI (Fallback if no API key)
# ─────────────────────────────────────────────
def simulate_analysis(resume_text: str) -> dict:
    """
    Keyword-based fallback analysis when AI API is unavailable.
    Searches for common skills, education patterns, and experience patterns.
    """
    text_lower = resume_text.lower()

    # Common tech skills to search for
    skill_keywords = [
        "python", "java", "javascript", "react", "node.js", "sql", "html", "css",
        "machine learning", "deep learning", "tensorflow", "pytorch", "docker",
        "kubernetes", "aws", "azure", "git", "linux", "c++", "typescript",
        "mongodb", "postgresql", "rest api", "agile", "scrum", "pandas", "numpy"
    ]
    found_skills = [s.title() for s in skill_keywords if s in text_lower][:12]

    # Education detection
    edu_patterns = ["bachelor", "master", "phd", "b.tech", "m.tech", "b.e", "m.e",
                    "b.sc", "m.sc", "degree", "university", "college", "institute"]
    education = []
    for line in resume_text.split("\n"):
        if any(p in line.lower() for p in edu_patterns):
            education.append(line.strip())
    education = [e for e in education if len(e) > 5][:4]

    # Experience detection
    exp_patterns = ["intern", "engineer", "developer", "analyst", "manager",
                    "lead", "architect", "consultant", "associate"]
    experience = []
    for line in resume_text.split("\n"):
        if any(p in line.lower() for p in exp_patterns):
            if len(line.strip()) > 10:
                experience.append(line.strip())
    experience = experience[:5]

    # Calculate score
    skill_score = min(25, len(found_skills) * 2)
    exp_score = min(25, len(experience) * 5)
    edu_score = min(25, len(education) * 8)
    fmt_score = 15 if len(resume_text) > 300 else 8

    total = skill_score + exp_score + edu_score + fmt_score

    return {
        "analysis": {
            "skills": found_skills if found_skills else ["No skills detected - try adding technical skills"],
            "education": education if education else ["Education section not clearly detected"],
            "experience": experience if experience else ["Experience section not clearly detected"],
            "strengths": [
                "Good technical skills listed" if len(found_skills) > 5 else "Has some technical skills",
                "Resume has proper structure" if len(resume_text) > 400 else "Resume has basic content",
                "Multiple sections present"
            ],
            "weaknesses": [
                "Could add more quantifiable achievements",
                "Missing keywords may reduce ATS score",
                "Could improve formatting and visual hierarchy"
            ]
        },
        "score": {
            "score": total,
            "score_breakdown": {
                "skills": skill_score,
                "experience": exp_score,
                "education": edu_score,
                "formatting": fmt_score
            },
            "explanation": f"Resume scored {total}/100 based on skills ({skill_score}/25), experience ({exp_score}/25), education ({edu_score}/25), and formatting ({fmt_score}/25)."
        },
        "suggestions": {
            "suggestions": [
                "Add quantifiable achievements (e.g., 'improved performance by 30%')",
                "Include a professional summary at the top",
                "Use action verbs (developed, built, led, optimized)",
                "Add links to GitHub, LinkedIn, or portfolio",
                "Tailor resume keywords to match job descriptions",
                "Ensure consistent date formatting throughout"
            ],
            "missing_skills": ["Docker", "Cloud (AWS/GCP/Azure)", "System Design", "Unit Testing"]
        }
    }


# ─────────────────────────────────────────────
# SECTION 4: VISUALIZATION - Score Chart
# ─────────────────────────────────────────────
def create_score_chart(score_breakdown: dict, total_score: int):
    """
    Create a horizontal bar chart showing score breakdown using matplotlib.
    Each category shows its score out of 25.
    """
    categories = list(score_breakdown.keys())
    values = list(score_breakdown.values())
    max_vals = [25, 25, 25, 25]

    # Color coding: green if >18, yellow if >12, red otherwise
    colors = []
    for v in values:
        if v >= 18:
            colors.append("#22c55e")
        elif v >= 12:
            colors.append("#f59e0b")
        else:
            colors.append("#ef4444")

    fig, ax = plt.subplots(figsize=(8, 3.5))
    fig.patch.set_facecolor('#f8fafc')
    ax.set_facecolor('#f8fafc')

    y_pos = np.arange(len(categories))

    # Background bars (max possible)
    ax.barh(y_pos, max_vals, color="#e2e8f0", height=0.5, zorder=1)
    # Score bars
    bars = ax.barh(y_pos, values, color=colors, height=0.5, zorder=2)

    # Add value labels
    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                f"{val}/25", va='center', fontsize=10, fontweight='bold', color='#1e293b')

    ax.set_yticks(y_pos)
    ax.set_yticklabels([c.title() for c in categories], fontsize=11, color='#374151')
    ax.set_xlim(0, 28)
    ax.set_xlabel("Score", fontsize=10, color='#6b7280')
    ax.set_title(f"Resume Score Breakdown — Total: {total_score}/100",
                 fontsize=13, fontweight='bold', color='#1e1b4b', pad=12)
    ax.spines[['top', 'right', 'bottom']].set_visible(False)
    ax.tick_params(axis='x', colors='#9ca3af')

    plt.tight_layout()
    return fig


# ─────────────────────────────────────────────
# SECTION 5: STREAMLIT UI
# ─────────────────────────────────────────────
def main():
    # ── Sidebar ──
    with st.sidebar:
        st.markdown("## 🤖 AI Resume Analyzer")
        st.markdown("---")
        st.markdown("**How it works:**")
        st.markdown("""
        1. 📤 Upload your PDF resume
        2. 🔍 AI extracts & analyzes content
        3. 📊 Get score, strengths & tips
        4. 🎯 Bonus: Paste job description
        """)
        st.markdown("---")
        st.markdown("**Tech Stack:**")
        st.markdown("- Python + Streamlit\n- pdfplumber\n- Google Gemini API\n- matplotlib")
        st.markdown("---")
        st.markdown("*No API key? Simulated AI will be used.*")

    # ── Main Header ──
    st.markdown("""
    <div class='app-header'>
        <h1 class='app-title'>⚡ Resume.AI</h1>
        <p class='app-subtitle'>
            Upload your resume and get deep, actionable insights instantly.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── File Upload ──
    col1, col2 = st.columns([2, 1])
    with col1:
        uploaded_file = st.file_uploader(
            "📁 Upload Resume (PDF only)",
            type=["pdf"],
            help="Upload your resume in PDF format for analysis"
        )
    with col2:
        st.markdown("#### 🎯 Bonus: Job Description")
        job_desc = st.text_area(
            "Paste job description (optional)",
            height=120,
            placeholder="Paste the job description here for keyword matching...",
            label_visibility="collapsed"
        )

    # ── Analysis ──
    if uploaded_file:
        with st.spinner("🔍 Extracting text from PDF..."):
            resume_text = extract_text_from_pdf(uploaded_file)

        if not resume_text or len(resume_text) < 50:
            st.error("⚠️ Could not extract meaningful text. Please ensure the PDF has selectable text (not scanned image).")
            return

        # Add spacing before button
        st.write("")
        
        # Analyze button
        if st.button("🚀 Analyze Resume", type="primary", use_container_width=True):
            ai_service = get_ai_service()

            if ai_service:
                # ── AI Analysis with st.status ──
                with st.status("🤖 Analyzing resume...", expanded=True) as status:
                    st.write("🔍 Parsing document semantics...")
                    try:
                        result = analyze_resume_with_ai(resume_text, ai_service, job_desc)
                        st.write("📊 Calculating optimal score...")
                        analysis = result["analysis"]
                        scoring = result["score"]
                        st.write("💡 Generating actionable suggestions...")
                        suggestions = result["suggestions"]
                        status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
                    except Exception as e:
                        status.update(label="⚠️ AI error. Using simulated fallback.", state="error", expanded=False)
                        result = simulate_analysis(resume_text)
                        analysis = result["analysis"]
                        scoring = result["score"]
                        suggestions = result["suggestions"]
            else:
                # ── Simulated AI Analysis ──
                with st.status("🔄 Running simulated analysis...", expanded=True) as status:
                    st.write("No API key found. Using fallback heuristics...")
                    result = simulate_analysis(resume_text)
                    analysis = result["analysis"]
                    scoring = result["score"]
                    suggestions = result["suggestions"]
                    status.update(label="✅ Fallback Analysis Complete", state="complete", expanded=False)

            # Show visual toast for success
            st.toast('Analysis completed successfully!', icon='🎉')

            # ════════════════════════════════
            # TABS LAYOUT
            # ════════════════════════════════
            st.markdown("<br>", unsafe_allow_html=True)
            tab1, tab2, tab3 = st.tabs(["📊 Analysis Report", "💡 Suggestions", "📋 Raw Data"])

            # ── TAB 1: Analysis ──
            with tab1:
                # Row 1: Score + Chart
                r1_col1, r1_col2 = st.columns([1, 2], gap="large")

                with r1_col1:
                    score = scoring.get("score", 0)
                    
                    # Dynamically set border color based on score
                    border_cls = "border-green" if score >= 75 else "border-amber" if score >= 50 else "border-red"
                    
                    st.markdown(f"""
                    <div class='result-card {border_cls}'>
                        <div class='section-header'>⭐ Overall Score</div>
                        <div class='score-badge'>{score}<span style='font-size:1.5rem; color:#64748b;'>/100</span></div>
                        <p style='color:#64748b; font-size:0.95rem; margin-top:1rem; text-align:center;'>
                            {scoring.get("explanation", "")}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                with r1_col2:
                    st.markdown("<div class='result-card border-blue' style='padding-bottom:0;'>", unsafe_allow_html=True)
                    st.markdown("<div class='section-header'>📈 Score Breakdown</div>", unsafe_allow_html=True)
                    fig = create_score_chart(scoring.get("score_breakdown", {}), score)
                    st.pyplot(fig, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                # Row 2: Skills, Education, Experience
                r2_col1, r2_col2, r2_col3 = st.columns(3, gap="medium")

                with r2_col1:
                    st.markdown("<div class='result-card border-purple'>", unsafe_allow_html=True)
                    st.markdown("<div class='section-header'>🛠️ Skills Detected</div>", unsafe_allow_html=True)
                    skills_html = " ".join([f"<span class='skill-chip'>{s}</span>" for s in analysis.get("skills", [])])
                    st.markdown(skills_html, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                with r2_col2:
                    st.markdown("<div class='result-card border-blue'>", unsafe_allow_html=True)
                    st.markdown("<div class='section-header'>🎓 Education</div>", unsafe_allow_html=True)
                    for edu in analysis.get("education", []):
                        st.markdown(f"<p style='margin:0.25rem 0; color:#334155;'>• {edu}</p>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                with r2_col3:
                    st.markdown("<div class='result-card border-blue'>", unsafe_allow_html=True)
                    st.markdown("<div class='section-header'>💼 Experience</div>", unsafe_allow_html=True)
                    for exp in analysis.get("experience", []):
                        st.markdown(f"<p style='margin:0.25rem 0; color:#334155;'>• {exp}</p>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                # Row 3: Strengths & Weaknesses
                r3_col1, r3_col2 = st.columns(2, gap="medium")

                with r3_col1:
                    st.markdown("<div class='result-card border-green'>", unsafe_allow_html=True)
                    st.markdown("<div class='section-header'>✅ Key Strengths</div>", unsafe_allow_html=True)
                    for s in analysis.get("strengths", []):
                        st.markdown(f"<p style='margin:0.4rem 0; color:#0f172a;'>✨ {s}</p>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                with r3_col2:
                    st.markdown("<div class='result-card border-red'>", unsafe_allow_html=True)
                    st.markdown("<div class='section-header'>⚠️ Areas for Improvement</div>", unsafe_allow_html=True)
                    for w in analysis.get("weaknesses", []):
                        st.markdown(f"<p style='margin:0.4rem 0; color:#0f172a;'>🎯 {w}</p>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

            # ── TAB 2: Suggestions ──
            with tab2:
                st.markdown("<div class='result-card border-amber'>", unsafe_allow_html=True)
                st.markdown("<div class='section-header'>💡 Actionable Suggestions</div>", unsafe_allow_html=True)
                for i, sug in enumerate(suggestions.get("suggestions", []), 1):
                    st.markdown(f"<p style='margin:0.75rem 0; color:#1e293b; font-size:1.05rem;'><strong>{i}.</strong> {sug}</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

                # Missing Skills
                missing = suggestions.get("missing_skills", [])
                if missing:
                    st.markdown("<div class='result-card border-red'>", unsafe_allow_html=True)
                    st.markdown("<div class='section-header'>🔴 Missing / Recommended Skills</div>", unsafe_allow_html=True)
                    chips = " ".join([f"<span class='skill-chip missing'>{s}</span>" for s in missing])
                    st.markdown(chips, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

            # ── TAB 3: Raw Data ──
            with tab3:
                st.markdown("<div class='result-card border-blue'>", unsafe_allow_html=True)
                st.markdown("<div class='section-header'>📋 Extracted Resume Text</div>", unsafe_allow_html=True)
                st.text_area("Extracted Text", resume_text, height=300, label_visibility="collapsed")
                st.markdown("</div>", unsafe_allow_html=True)
                
                if job_desc:
                    st.markdown("<div class='result-card border-purple'>", unsafe_allow_html=True)
                    st.markdown("<div class='section-header'>🎯 Provided Job Description</div>", unsafe_allow_html=True)
                    st.text_area("Job Desc", job_desc, height=150, label_visibility="collapsed")
                    st.markdown("</div>", unsafe_allow_html=True)

            # ── Download Results ──
            st.markdown("<br>", unsafe_allow_html=True)
            report = f"""AI RESUME ANALYSIS REPORT
==========================
File: {uploaded_file.name}
Overall Score: {score}/100

SKILLS: {', '.join(analysis.get('skills', []))}

EDUCATION:
{chr(10).join(analysis.get('education', []))}

EXPERIENCE:
{chr(10).join(analysis.get('experience', []))}

STRENGTHS:
{chr(10).join(['• ' + s for s in analysis.get('strengths', [])])}

WEAKNESSES:
{chr(10).join(['• ' + w for w in analysis.get('weaknesses', [])])}

SUGGESTIONS:
{chr(10).join([f'{i+1}. {s}' for i, s in enumerate(suggestions.get('suggestions', []))])}

MISSING SKILLS: {', '.join(suggestions.get('missing_skills', []))}
"""
            st.download_button(
                "📥 Download Full PDF Report",
                data=report,
                file_name="resume_analysis_report.txt",
                mime="text/plain",
                use_container_width=True
            )


if __name__ == "__main__":
    main()
