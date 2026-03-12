document.addEventListener('DOMContentLoaded', ()=>{
  const form = document.getElementById('genForm');
  const submitBtn = document.getElementById('submitBtn');
  const loading = document.getElementById('loading');
  const resumeEl = document.getElementById('resume');
  const coverEl = document.getElementById('cover');

  form.addEventListener('submit', async (e)=>{
    e.preventDefault();
    submitBtn.disabled = true;
    loading.classList.remove('hidden');
    resumeEl.textContent = '';
    coverEl.textContent = '';

    const formData = new FormData(form);
    const payload = {};
    formData.forEach((v,k)=>payload[k]=v);

    try{
      const res = await fetch('/generate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
      const data = await res.json();
      if(data.error){
        resumeEl.textContent = 'Error: ' + data.error;
      } else {
        resumeEl.textContent = data.resume || '';
        coverEl.textContent = data.cover_letter || '';
      }
    }catch(err){
      resumeEl.textContent = 'Request failed: '+err;
    } finally{
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
