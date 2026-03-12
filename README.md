# AI Resume & Cover Letter Generator 🚀

## Overview

Professional web application that generates ATS-friendly resumes and personalized cover letters using **Groq AI** (Llama3 model). 

**Key Features:**
- Modern responsive UI with form inputs for candidate details (experience, skills, education, etc.).
- Server-side execution of Jupyter notebook via Flask for secure API calls (no browser key exposure).
- Real-time generation with copy/download buttons.
- Auto-loads `.env` for Groq API key.
- Debug mode for development.

**Architecture:**
```
Flask App (app.py) --> converts generator_notebook.ipynb --> Groq API --> JSON {resume, cover_letter}
├── templates/index.html + static/script.js/style.css (UI + AJAX)
└── AI_Resume_Generator/ (.env, notebooks)
```

## Quick Start (Windows)

1. **Virtual Environment & Dependencies** (done):
   ```
   python -m venv .venv
   .venv/Scripts/Activate.ps1
   pip install -r requirements.txt groq python-dotenv
   ```

2. **API Key Setup**:
   - Get free key from [console.groq.com/keys](https://console.groq.com/keys).
   - Edit `AI_Resume_Generator/.env`:
     ```
     GROQ_API_KEY=sk-your_actual_key_here
     ```
     (Optional) `GROQ_MODEL=llama3-70b-8192` (defaults llama-3.1-8b-instant)

3. **Run Server**:
   ```
   python app.py
   ```
   - Opens http://127.0.0.1:5000
   - Fill form, click **Generate** → Resume & Cover Letter appear!

4. **Test**:
   - Expected: Server logs notebook exec + Groq response.
   - Copy/Download TXT files.

## Usage

1. Open http://127.0.0.1:5000.
2. Enter details:
   - Personal: name, email, role.
   - Content: skills, projects, experience (bullets).
3. Generate → AI crafts professional output.
4. Copy to Word/Docs or download TXT.

**Screenshot**: Modern glassmorphism UI with spinner, outputs.

## Files

| File | Purpose |
|------|---------|
| `app.py` | Flask server, notebook executor |
| `generator_notebook.ipynb` | Groq prompt/function |
| `templates/index.html` + `static/*` | UI |
| `.env` | Secrets |
| `requirements.txt` | Deps |

**Bonus Static Frontend** (`AI_Resume_Generator/index.html`): Browser-only version (paste key, insecure for prod).

## Troubleshooting

- **No API key**: Edit `.env`, restart server.
- **Model error**: Set `GROQ_MODEL` in .env to available model (run `AI_Resume_Generator/list_models.py`).
- **Notebook fail**: Check server logs, ensure `generate_resume_and_cover_letter` func.
- **Port busy**: `app.run(port=5001)`.
- **Windows PS**: Use `Activate.ps1`.

## Development

- Edit notebook prompts in `generator_notebook.ipynb`.
- Add fields: Update UI/JS/payload.
- Prod: Use Gunicorn/NGINX, secure key proxy.

## Vercel Deployment\n\n1. Install Vercel CLI: `npm i -g vercel`\n2. Login: `vercel login`\n3. Deploy: `vercel --prod`\n4. Set env vars in dashboard:\n   - `GROQ_API_KEY`: your key\n   - `GROQ_MODEL`: optional (default llama-3.1-8b-instant)\n5. Visit deployed URL.\n\n**vercel.json** increases timeout to 30s for LLM.\n\n## License\n\nMIT. Powered by [Groq](https://groq.com).
