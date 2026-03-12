import os
import re
import json

# Load .env
env_path = os.path.join(os.path.dirname(__file__), '.env')
api_key = None
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            m = re.match(r"^GROQ_API_KEY=(.*)$", line.strip())
            if m:
                api_key = m.group(1).strip()
                # strip surrounding quotes if present
                if (api_key.startswith('"') and api_key.endswith('"')) or (api_key.startswith("'") and api_key.endswith("'")):
                    api_key = api_key[1:-1]
                break

if not api_key:
    print('No GROQ_API_KEY found in .env. Paste your key into .env or set GROQ_API_KEY in environment.')
    raise SystemExit(1)

try:
    import groq
    from groq import Groq
except Exception as e:
    print('groq package not installed or failed to import:', e)
    raise

client = Groq(api_key=api_key)

prompt = (
    "You are a professional resume writer. Provide a one-paragraph confirmation that the API is reachable." 
)

try:
    # Allow overriding model via .env variable GROQ_MODEL, default to 'llama3-70b'
    model = os.environ.get('GROQ_MODEL')
    if not model:
        # try to read from .env file variable if present
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                m = re.match(r"^GROQ_MODEL=(.*)$", line.strip())
                if m:
                    model = m.group(1).strip().strip('"').strip("'")
                    break
    if not model:
        model = 'llama-3.1-8b-instant'
    print(f'Using model: {model}')
    response = client.chat.completions.create(model=model, messages=[{'role':'user','content':prompt}], max_tokens=200, temperature=0.2)
    content = None
    if 'choices' in response and response['choices']:
        choice = response['choices'][0]
        if 'message' in choice and 'content' in choice['message']:
            content = choice['message']['content']
        elif 'text' in choice:
            content = choice['text']
    if not content:
        print('No content returned from Groq API. Full response:')
        print(json.dumps(response, indent=2))
    else:
        print('--- Groq response ---')
        print(content)
except Exception as e:
    print('API call failed:', e)
    raise
