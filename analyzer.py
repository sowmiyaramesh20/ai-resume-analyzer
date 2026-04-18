from groq import Groq
import json
import re

def analyze_resume(resume_text: str, job_description: str, api_key: str) -> dict:
    """Send resume + JD to Groq and get structured analysis."""
    
    client = Groq(api_key=api_key)

    prompt = f"""
You are an expert HR consultant and resume coach. Analyze the resume against the job description and return a JSON response ONLY (no markdown, no explanation).

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return this exact JSON structure:
{{
  "match_score": <integer 0-100>,
  "summary": "<2-3 sentence overall assessment>",
  "matched_skills": ["skill1", "skill2"],
  "missing_skills": ["skill1", "skill2"],
  "strengths": ["strength1", "strength2"],
  "improvements": ["improvement1", "improvement2"],
  "keywords_to_add": ["keyword1", "keyword2"],
  "verdict": "<one of: Strong Match / Good Match / Moderate Match / Weak Match>"
}}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
        )
        raw = response.choices[0].message.content.strip()
        raw = re.sub(r"```json|```", "", raw).strip()
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"error": "Could not parse AI response. Please try again."}
    except Exception as e:
        return {"error": str(e)}