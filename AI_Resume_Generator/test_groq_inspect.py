import os, re
from groq import Groq

# load key from .env
env_path = os.path.join(os.path.dirname(__file__), '.env')
api_key = None
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            m = re.match(r"^GROQ_API_KEY=(.*)$", line.strip())
            if m:
                api_key = m.group(1).strip()
                break
if not api_key:
    print('No GROQ_API_KEY found in .env')
    raise SystemExit(1)

client = Groq(api_key=api_key)
print('Groq client created. Dir of client.chat:')
print([a for a in dir(client.chat) if not a.startswith('_')])
print('\nDir of client:')
print([a for a in dir(client) if not a.startswith('_')])
