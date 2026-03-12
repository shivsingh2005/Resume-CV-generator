import os
from groq import Groq

api_key = os.environ.get('GROQ_API_KEY')
if not api_key:
    raise RuntimeError('GROQ_API_KEY environment variable required.')

client = Groq(api_key=api_key)

MODEL = os.environ.get('GROQ_MODEL', 'llama-3.1-8b-instant')

def generate_resume_and_cover_letter(user_data: dict):
    \"\"\"
    Generate resume and cover letter using Groq.

    Args:
        user_data (dict): User inputs e.g. {'name': 'John'}

    Returns:
        dict: {'resume': str, 'cover_letter': str}
    \"\"\"
    prompt_lines = [
        'You are a professional resume writer and career coach.',
        'Produce an ATS-friendly resume and a personalized cover letter.',
        'Output MUST be plain text, no markdown, no emojis.',
        'Separate the outputs using exact separators:',
        '===== RESUME =====',
        '===== COVER LETTER =====',
        '',
        'User details:',
    ]
    for k,v in user_data.items():
        prompt_lines.append(f'{k}: {v}')
    prompt_lines += [
        '',
        'Instructions for RESUME:',
        '- Create sections: Summary, Skills, Experience, Projects, Education, Certifications.',
        '- Use bullet points for achievements and responsibilities.',
        '- Keep language professional and ATS-friendly.',
        '',
        'Instructions for COVER LETTER:',
        '- Include greeting, intro paragraph, skill alignment paragraph(s), and closing.',
    ]
    prompt = '\n'.join(prompt_lines)

    response = client.chat.completions.create(
        model=MODEL, 
        messages=[{'role':'user','content':prompt}], 
        max_tokens=2000, 
        temperature=0.2
    )

    content = response.choices[0].message.content
    if '===== RESUME =====' in content and '===== COVER LETTER =====' in content:
        after_resume = content.split('===== RESUME =====')[1]
        resume_part = after_resume.split('===== COVER LETTER =====')[0].strip()
        cover_part = after_resume.split('===== COVER LETTER =====')[1].strip()
    else:
        resume_part = content
        cover_part = ''
    return {'resume': resume_part, 'cover_letter': cover_part}
