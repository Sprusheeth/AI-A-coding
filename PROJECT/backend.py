import os
import json
import traceback
import pdfplumber
import google.generativeai as genai
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

try:
    from bytez import Bytez
except ImportError:
    Bytez = None

app = Flask(__name__, static_folder='frontend')
# Enable CORS for the frontend to hit this API without origin issues
CORS(app)

@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)

def get_ai_service():
    """
    Returns a dictionary with 'type' ('google' or 'bytez') and 'client'.
    Prefers Google Gemini API via environment variables, falls back to Bytez.
    """
    api_key = os.getenv("GEMINI_API_KEY", "")
    
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
        except Exception as e:
            print(f"Bytez initialisation error: {e}")
            pass
            
    return None

def extract_text_from_pdf(file_stream) -> str:
    full_text = ""
    with pdfplumber.open(file_stream) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"
    return full_text.strip()

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
    jd_context = f"\nTarget Job Description:\n{job_desc}" if job_desc else ""
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

    if ai_service["type"] == "google":
        response = ai_service["client"].generate_content(prompt)
        output_text = response.text
    else:
        response = ai_service["client"].run([{"role": "user", "content": prompt}])
        output_text = response.output

    # If the response is already a dictionary, return it directly
    if isinstance(output_text, dict):
        return output_text
        
    # If the response is a list, extract the generated text
    if isinstance(output_text, list):
        if len(output_text) > 0 and isinstance(output_text[0], dict):
            if "generated_text" in output_text[0]:
                output_text = output_text[0]["generated_text"]
            elif "text" in output_text[0]:
                output_text = output_text[0]["text"]
            else:
                output_text = str(output_text)
        else:
            output_text = str(output_text)

    clean_text = str(output_text).replace("```json", "").replace("```", "").strip()
    return json.loads(clean_text)

def simulate_analysis(resume_text: str) -> dict:
    text_lower = resume_text.lower()

    # Common tech skills
    skill_keywords = [
        "python", "java", "javascript", "react", "node.js", "sql", "html", "css",
        "machine learning", "deep learning", "tensorflow", "pytorch", "docker",
        "kubernetes", "aws", "azure", "git", "linux", "c++", "typescript",
        "mongodb", "postgresql", "rest api", "agile", "scrum", "pandas", "numpy"
    ]
    found_skills = [s.title() for s in skill_keywords if s in text_lower][:12]

    edu_patterns = ["bachelor", "master", "phd", "b.tech", "m.tech", "b.e", "m.e",
                    "b.sc", "m.sc", "degree", "university", "college", "institute"]
    education = []
    for line in resume_text.split("\n"):
        if any(p in line.lower() for p in edu_patterns):
            education.append(line.strip())
    education = [e for e in education if len(e) > 5][:4]

    exp_patterns = ["intern", "engineer", "developer", "analyst", "manager",
                    "lead", "architect", "consultant", "associate"]
    experience = []
    for line in resume_text.split("\n"):
        if any(p in line.lower() for p in exp_patterns):
            if len(line.strip()) > 10:
                experience.append(line.strip())
    experience = experience[:5]

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

@app.route("/api/analyze", methods=["POST"])
def analyze():
    # Ensure PDF is uploaded
    if "resume" not in request.files:
        return jsonify({"error": "No resume file provided"}), 400

    file = request.files["resume"]
    job_desc = request.form.get("job_desc", "")

    if file.filename == "":
        return jsonify({"error": "Empty file provided"}), 400

    try:
        # Extract text
        resume_text = extract_text_from_pdf(file.stream)
        if not resume_text or len(resume_text) < 50:
            return jsonify({"error": "Could not extract meaningful text. Ensure the PDF has selectable text."}), 400

        res_data = {
            "resume_text": resume_text,
            "analysis": None,
            "score": None,
            "suggestions": None,
            "fallback": False
        }

        ai_service = get_ai_service()
        if ai_service:
            try:
                result = analyze_resume_with_ai(resume_text, ai_service, job_desc)
                res_data["analysis"] = result["analysis"]
                res_data["score"] = result["score"]
                res_data["suggestions"] = result["suggestions"]
            except Exception as e:
                # Fall back to simulated AI
                print(f"AI error, falling back to simulated analysis: {e}")
                sim_res = simulate_analysis(resume_text)
                res_data["analysis"] = sim_res["analysis"]
                res_data["score"] = sim_res["score"]
                res_data["suggestions"] = sim_res["suggestions"]
                res_data["fallback"] = True
        else:
            print("No AI Service available, using simulated analysis")
            sim_res = simulate_analysis(resume_text)
            res_data["analysis"] = sim_res["analysis"]
            res_data["score"] = sim_res["score"]
            res_data["suggestions"] = sim_res["suggestions"]
            res_data["fallback"] = True

        return jsonify(res_data), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"An internal server error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
