// Frontend-only Groq integration (no backend).
// The API key is kept in-memory only (input field) and not persisted.

document.addEventListener('DOMContentLoaded', ()=>{
  const form = document.getElementById('genForm');
  const submitBtn = document.getElementById('submitBtn');
  const loading = document.getElementById('loading');
  const resumeEl = document.getElementById('resume');
  const coverEl = document.getElementById('cover');
  const modelInput = document.getElementById('model');
  const status = document.getElementById('status');

  let API_KEY = '';

  // If a generated config.js was loaded, it may set window.__GROQ_API_KEY
  if (window.__GROQ_API_KEY) {
    API_KEY = ('' + window.__GROQ_API_KEY).trim();
    status.textContent = 'API key loaded from config.js (in-memory)';
  } else {
    // No API key available in frontend; instruct user to create config.js
    status.textContent = 'No API key found. Run `python create_config.py` to generate config.js from .env';
    // disable the generate button until key exists
    submitBtn.disabled = true;
  }

  // No API input: config.js or .env-driven config is used instead.

  // model input sanitization
  modelInput.addEventListener('input', ()=>{
    // no storage here, we will read value on submit
    const v = modelInput.value || '';
    if(!v.trim()){
      modelInput.value = 'llama-3.1-8b-instant';
    }
  });

  form.addEventListener('submit', async (e)=>{
    e.preventDefault();
    if(!API_KEY){
      alert('Please paste your Groq API key in the top field.');
      return;
    }

    submitBtn.disabled = true;
    loading.classList.remove('hidden');
    resumeEl.textContent = '';
    coverEl.textContent = '';

    const fd = new FormData(form);
    const data = Object.fromEntries(fd.entries());

    const prompt = buildPrompt(data);
    const model = (modelInput.value || 'llama-3.1-8b-instant').trim();

    try{
      const responseText = await callGroqAPI(API_KEY, prompt, model);
      const parts = splitOutput(responseText);
      resumeEl.textContent = parts.resume || 'No resume returned.';
      coverEl.textContent = parts.cover || 'No cover letter returned.';
    }catch(err){
      resumeEl.textContent = 'Error: ' + (err.message || err);
      coverEl.textContent = '';
    }finally{
      submitBtn.disabled = false;
      loading.classList.add('hidden');
    }
  });

  document.querySelectorAll('.copy-btn').forEach(btn=>{
    btn.addEventListener('click', ()=>{
      const target = btn.dataset.target;
      const txt = document.getElementById(target==='resume'?'resume':'cover').textContent || '';
      navigator.clipboard.writeText(txt);
      btn.textContent = 'Copied';
      setTimeout(()=>btn.textContent='Copy',1500);
    });
  });

  document.querySelectorAll('.download-btn').forEach(btn=>{
    btn.addEventListener('click', ()=>{
      const target = btn.dataset.target;
      const txt = document.getElementById(target==='resume'?'resume':'cover').textContent || '';
      const name = target==='resume'? 'resume.txt':'cover_letter.txt';
      const blob = new Blob([txt], {type:'text/plain;charset=utf-8'});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = name; document.body.appendChild(a); a.click(); a.remove();
      URL.revokeObjectURL(url);
    });
  });

});

function buildPrompt(data){
  // build structured prompt for the model
  const lines = [];
  lines.push('You are a professional resume writer and career coach.');
  lines.push('Produce an ATS-friendly resume and a personalized cover letter.');
  lines.push('Output MUST be plain text, no markdown, no emojis.');
  lines.push('Separate the outputs using exact separators:');
  lines.push('===== RESUME =====');
  lines.push('===== COVER LETTER =====');
  lines.push('');

  lines.push('User details:');
  lines.push(`Full Name: ${data.full_name || ''}`);
  lines.push(`Email: ${data.email || ''}`);
  lines.push(`Phone: ${data.phone || ''}`);
  lines.push(`Target Role: ${data.target_role || ''}`);
  lines.push('');

  if(data.education) lines.push('Education:\n' + data.education.trim());
  if(data.skills) lines.push('Skills: ' + data.skills.trim());
  if(data.projects) lines.push('Projects:\n' + data.projects.trim());
  if(data.experience) lines.push('Experience:\n' + data.experience.trim());
  if(data.certifications) lines.push('Certifications:\n' + data.certifications.trim());

  lines.push('');
  lines.push('Instructions for RESUME:');
  lines.push('- Create sections: Summary, Skills, Experience, Projects, Education, Certifications.');
  lines.push("- Use bullet points for achievements and responsibilities.");
  lines.push('- Keep language professional and ATS-friendly.');
  lines.push('- Do not use emojis or markdown. Use clear plaintext bullets.');
  lines.push('');
  lines.push('Instructions for COVER LETTER:');
  lines.push('- Include a short greeting, an intro paragraph, 1-2 paragraphs aligning skills to the role, and a closing paragraph.');
  lines.push('- Keep tone professional and tailored to the target role.');
  lines.push('');
  lines.push('Return the resume first under the exact separator, then the cover letter under its separator.');

  return lines.join('\n');
}

async function callGroqAPI(key, prompt, model='llama-3.1-8b-instant'){
  const url = 'https://api.groq.com/openai/v1/chat/completions';
  const body = {
    model: model,
    messages: [{role: 'user', content: prompt}],
    max_tokens: 2000,
    temperature: 0.2
  };

  const res = await fetch(url,{
    method: 'POST',
    headers: {
      'Content-Type':'application/json',
      'Authorization': 'Bearer ' + key
    },
    body: JSON.stringify(body)
  });

  if(!res.ok){
    const txt = await res.text();
    throw new Error(`API error ${res.status}: ${txt}`);
  }

  const data = await res.json();
  // OpenAI-compatible response: choices[0].message.content
  const content = data.choices && data.choices[0] && (data.choices[0].message?.content || data.choices[0].text) ? (data.choices[0].message?.content || data.choices[0].text) : JSON.stringify(data);
  return content;
}

function splitOutput(text){
  const resumeSep = '===== RESUME =====';
  const coverSep = '===== COVER LETTER =====';
  let resume = '';
  let cover = '';

  if(text.includes(resumeSep) && text.includes(coverSep)){
    const afterResume = text.split(resumeSep)[1];
    const parts = afterResume.split(coverSep);
    resume = parts[0].trim();
    cover = (parts[1]||'').trim();
  } else {
    // Fallback: try to heuristically split by newline blocks
    const idx = text.indexOf('\n\n');
    resume = text;
    cover = '';
  }
  return {resume, cover};
}
