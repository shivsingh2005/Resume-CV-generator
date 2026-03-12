AI Resume & Cover Letter Generator (Frontend-only + Groq)

Overview

This is a frontend-only web application that calls the Groq API directly from the browser to generate an ATS-friendly resume and a personalized cover letter from user inputs. No backend is required.

Files

- index.html — The single HTML page with the form and results UI.
- style.css — Styles for the modern glassmorphism UI.
- script.js — Vanilla JavaScript that builds the prompt, calls Groq, and renders results.
- ai_resume_generator.ipynb — Jupyter notebook demonstrating how to call Groq from Python for testing prompts.

How to use

1. Open `index.html` in a browser (Chrome/Edge recommended).
2. Paste your Groq API key into the top field. This key is stored only in-memory while the page is open.
3. Fill the fields (name, email, education, skills, projects, experience, certifications, target role).
4. Click "Generate". The app will call the Groq API and display the Resume and Cover Letter.

Groq API details

- Endpoint used: `https://api.groq.com/openai/v1/chat/completions`
- Model: `llama3-70b-8192`
- Authorization: `Bearer YOUR_GROQ_API_KEY` (paste into UI)

Security warning

This is a pure frontend app. Embedding an API key in the browser exposes it to end users and is not secure for production. Use this only for quick testing or on trusted networks. For production use, proxy the requests through a secure server that stores the API key.

Jupyter Notebook

The included `ai_resume_generator.ipynb` demonstrates a Python-based approach to same prompts using the `groq` Python package. It expects `GROQ_API_KEY` to be set as an environment variable before running.

Deployment

Because this is a static site, you can deploy it to GitHub Pages, Vercel, Netlify, or any static-hosting provider:

- GitHub Pages: push the folder to a repo and enable Pages from the repository settings.
- Vercel/Netlify: connect the repository and deploy.

Notes & Troubleshooting

- If the Groq API returns an error, the app displays the error text in the result area.
- The UI disables the Generate button while the request runs and shows a spinner.

License

MIT
