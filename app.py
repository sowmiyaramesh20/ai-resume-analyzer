import streamlit as st
from pdf_parser import extract_text_from_pdf
from analyzer import analyze_resume

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Background */
.stApp {
    background: #0a0a0f;
    color: #e8e8f0;
}

/* Hero title */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 0.3rem;
}

.hero-sub {
    font-size: 1.05rem;
    color: #9090b0;
    font-weight: 300;
    margin-bottom: 2rem;
}

/* Cards */
.card {
    background: #13131e;
    border: 1px solid #2a2a40;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

/* Score ring */
.score-container {
    text-align: center;
    padding: 2rem 1rem;
}
.score-number {
    font-family: 'Syne', sans-serif;
    font-size: 5rem;
    font-weight: 800;
    line-height: 1;
}
.score-label {
    font-size: 0.85rem;
    color: #9090b0;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-top: 0.5rem;
}
.verdict-badge {
    display: inline-block;
    padding: 0.4rem 1.2rem;
    border-radius: 999px;
    font-size: 0.9rem;
    font-weight: 600;
    margin-top: 1rem;
    font-family: 'Syne', sans-serif;
}

/* Section headers */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 3px;
    color: #6060a0;
    margin-bottom: 0.8rem;
}

/* Tags */
.tag {
    display: inline-block;
    padding: 0.3rem 0.8rem;
    border-radius: 8px;
    font-size: 0.82rem;
    margin: 0.2rem;
    font-weight: 500;
}
.tag-green  { background: #0d2e1f; color: #34d399; border: 1px solid #1a5c3a; }
.tag-red    { background: #2e0d0d; color: #f87171; border: 1px solid #5c1a1a; }
.tag-blue   { background: #0d1a2e; color: #60a5fa; border: 1px solid #1a3a5c; }
.tag-purple { background: #1a0d2e; color: #a78bfa; border: 1px solid #3a1a5c; }

/* List items */
.list-item {
    padding: 0.6rem 0;
    border-bottom: 1px solid #1e1e30;
    font-size: 0.92rem;
    color: #c0c0d8;
    display: flex;
    align-items: flex-start;
    gap: 0.6rem;
}
.list-item:last-child { border-bottom: none; }

/* Divider */
.divider { border: none; border-top: 1px solid #1e1e30; margin: 1.5rem 0; }

/* Input labels */
label { color: #b0b0c8 !important; font-size: 0.9rem !important; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2.5rem !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
    transition: opacity 0.2s !important;
    width: 100% !important;
}
.stButton > button:hover { opacity: 0.88 !important; }

/* Text areas and inputs */
.stTextArea textarea, .stTextInput input {
    background: #0d0d18 !important;
    border: 1px solid #2a2a40 !important;
    border-radius: 10px !important;
    color: #e0e0f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 2px rgba(124,58,237,0.2) !important;
}

/* File uploader */
.stFileUploader {
    background: #0d0d18 !important;
    border: 1px dashed #2a2a40 !important;
    border-radius: 10px !important;
}

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">🧠 AI Resume Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Upload your resume · Paste the job description · Get instant AI-powered feedback</div>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ── Inputs ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("#### 📄 Your Resume")
    uploaded_file = st.file_uploader("Upload PDF resume", type=["pdf"], label_visibility="collapsed")
    if uploaded_file:
        st.success(f"✅ Loaded: **{uploaded_file.name}**")

with col2:
    st.markdown("#### 💼 Job Description")
    job_description = st.text_area(
        "Paste the job description here",
        height=180,
        placeholder="Paste the full job description here...",
        label_visibility="collapsed"
    )

st.markdown("#### 🔑 Gemini API Key")
api_key = st.text_input(
    "Gemini API Key",
    type="password",
    placeholder="Get free key at → aistudio.google.com",
    label_visibility="collapsed"
)
st.caption("🔒 Your key is never stored. Get a free key at [aistudio.google.com](https://aistudio.google.com)")

st.markdown("<br>", unsafe_allow_html=True)
analyze_btn = st.button("⚡ Analyze My Resume")


# ── Analysis ──────────────────────────────────────────────────────────────────
if analyze_btn:
    if not uploaded_file:
        st.error("Please upload your resume PDF.")
    elif not job_description.strip():
        st.error("Please paste the job description.")
    elif not api_key.strip():
        st.error("Please enter your Gemini API key.")
    else:
        with st.spinner("🔍 Analyzing your resume with AI..."):
            resume_text = extract_text_from_pdf(uploaded_file)

            if resume_text.startswith("Error"):
                st.error(resume_text)
            else:
                result = analyze_resume(resume_text, job_description, api_key.strip())

                if "error" in result:
                    st.error(f"AI Error: {result['error']}")
                else:
                    st.markdown('<hr class="divider">', unsafe_allow_html=True)
                    st.markdown("## 📊 Analysis Results")
                    st.markdown("<br>", unsafe_allow_html=True)

                    # ── Score + Summary ──────────────────────────────────────
                    score = result.get("match_score", 0)
                    verdict = result.get("verdict", "Unknown")
                    summary = result.get("summary", "")

                    # Score color
                    if score >= 75:
                        score_color = "#34d399"
                        badge_style = "background:#0d2e1f; color:#34d399; border:1px solid #1a5c3a;"
                    elif score >= 50:
                        score_color = "#fbbf24"
                        badge_style = "background:#2e2008; color:#fbbf24; border:1px solid #5c3a0a;"
                    else:
                        score_color = "#f87171"
                        badge_style = "background:#2e0d0d; color:#f87171; border:1px solid #5c1a1a;"

                    r1, r2 = st.columns([1, 2], gap="large")

                    with r1:
                        st.markdown(f"""
                        <div class="card score-container">
                            <div class="score-number" style="color:{score_color}">{score}</div>
                            <div class="score-label">Match Score</div>
                            <div><span class="verdict-badge" style="{badge_style}">{verdict}</span></div>
                        </div>
                        """, unsafe_allow_html=True)

                    with r2:
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.markdown('<div class="section-title">AI Summary</div>', unsafe_allow_html=True)
                        st.markdown(f'<p style="color:#c8c8e0;line-height:1.7;font-size:0.95rem">{summary}</p>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)

                    # ── Skills ───────────────────────────────────────────────
                    s1, s2 = st.columns(2, gap="large")

                    with s1:
                        matched = result.get("matched_skills", [])
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.markdown('<div class="section-title">✅ Matched Skills</div>', unsafe_allow_html=True)
                        tags_html = "".join([f'<span class="tag tag-green">{s}</span>' for s in matched]) if matched else '<span style="color:#606080">None found</span>'
                        st.markdown(tags_html, unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                    with s2:
                        missing = result.get("missing_skills", [])
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.markdown('<div class="section-title">❌ Missing Skills</div>', unsafe_allow_html=True)
                        tags_html = "".join([f'<span class="tag tag-red">{s}</span>' for s in missing]) if missing else '<span style="color:#606080">None — great job!</span>'
                        st.markdown(tags_html, unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)

                    # ── Strengths + Improvements ─────────────────────────────
                    t1, t2 = st.columns(2, gap="large")

                    with t1:
                        strengths = result.get("strengths", [])
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.markdown('<div class="section-title">💪 Your Strengths</div>', unsafe_allow_html=True)
                        for item in strengths:
                            st.markdown(f'<div class="list-item"><span style="color:#34d399">▸</span>{item}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                    with t2:
                        improvements = result.get("improvements", [])
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.markdown('<div class="section-title">🛠 Suggested Improvements</div>', unsafe_allow_html=True)
                        for item in improvements:
                            st.markdown(f'<div class="list-item"><span style="color:#a78bfa">▸</span>{item}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)

                    # ── Keywords ─────────────────────────────────────────────
                    keywords = result.get("keywords_to_add", [])
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown('<div class="section-title">🔑 Keywords to Add to Your Resume</div>', unsafe_allow_html=True)
                    tags_html = "".join([f'<span class="tag tag-blue">{k}</span>' for k in keywords]) if keywords else '<span style="color:#606080">None suggested</span>'
                    st.markdown(tags_html, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    st.balloons()
