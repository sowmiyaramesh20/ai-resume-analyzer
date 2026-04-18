# 🧠 AI Resume Analyzer

An AI-powered web app that analyzes your resume against a job description and gives you a match score, missing skills, strengths, and improvement suggestions — built with Python, Streamlit, and Google Gemini AI.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red?logo=streamlit)
![Gemini](https://img.shields.io/badge/Google%20Gemini-AI-green?logo=google)

---

## ✨ Features

- 📄 **PDF Resume Parsing** — Upload your resume as a PDF and extract text automatically
- 💼 **Job Description Matching** — Paste any job description to compare against
- 📊 **Match Score (0–100)** — Instant AI-generated compatibility score
- ✅ **Matched & Missing Skills** — See exactly what you have and what you're lacking
- 💪 **Strengths & Improvements** — Detailed feedback to improve your resume
- 🔑 **Keywords to Add** — Boost your ATS score with suggested keywords
- 🎨 **Beautiful Dark UI** — Clean, modern interface built with Streamlit

---

## 🖥️ Demo

> Upload your resume PDF → Paste a job description → Get instant AI feedback!

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get your FREE Gemini API key
Go to → [https://aistudio.google.com](https://aistudio.google.com) and create a free API key.

### 4. Run the app
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 🗂️ Project Structure

```
ai-resume-analyzer/
│
├── app.py              # Main Streamlit UI
├── analyzer.py         # Google Gemini AI logic
├── pdf_parser.py       # PDF text extraction
├── requirements.txt    # Python dependencies
└── README.md           # You're reading this!
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Web UI framework |
| pdfplumber | PDF text extraction |
| Google Gemini API | AI analysis engine |

---

## 📸 How It Works

1. User uploads a **resume PDF**
2. App extracts all text using **pdfplumber**
3. User pastes the **job description**
4. Both are sent to **Google Gemini AI** with a structured prompt
5. AI returns a **JSON response** with score, skills, improvements
6. Results are displayed in a **beautiful dashboard**

---

## 🤝 Contributing

Pull requests are welcome! Feel free to open issues for bugs or feature suggestions.

---

## 📄 License

MIT License — free to use and modify.

---

## 👨‍💻 Author

Made with ❤️ using Python + AI
