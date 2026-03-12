ENV usage and running the notebook

If you want to store your Groq API key in a local `.env` file for notebook testing, follow these steps:

1. Copy `.env.example` to `.env`:

   - Windows (PowerShell):
     Copy-Item .env.example .env

2. Open `.env` and paste your API key after the `GROQ_API_KEY=` line.

3. Use one of these options to run the Jupyter notebook so the environment variable is available:

   - Temporary (PowerShell only, recommended for testing):

     ```powershell
     $env:GROQ_API_KEY = (Get-Content .env | Select-String -Pattern "^GROQ_API_KEY=([^"]*)" | ForEach-Object { $_.Matches[0].Groups[1].Value })
     jupyter notebook ai_resume_generator.ipynb
     ```

   - Persistent (PowerShell):

     ```powershell
     setx GROQ_API_KEY "your_key_here"
     # Then restart your shell and run the notebook
     jupyter notebook ai_resume_generator.ipynb
     ```

   - Or install `python-dotenv` and modify your notebook to load it (not included here).

Important Security Note

- This project is frontend-only for the web app; the browser cannot and does not read `.env` files. The `.env` file is provided only for the Jupyter notebook/testing environment.
- Never commit `.env` containing real API keys to public repositories. `.env` is included in `.gitignore` to help avoid accidental commits.

If you want, I can update the notebook to load `.env` automatically using `python-dotenv`. Do you want that? 
