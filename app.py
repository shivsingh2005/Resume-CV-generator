import os
import tempfile
import importlib.util
from flask import Flask, render_template, request, jsonify
import nbformat
from nbconvert import PythonExporter
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'AI_Resume_Generator', '.env'))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NOTEBOOK_PATH = os.path.join(BASE_DIR, 'AI_Resume_Generator', 'generator_notebook.ipynb')

app = Flask(__name__, template_folder='templates', static_folder='static')


def load_notebook_module(nb_path: str):
    nb = nbformat.read(nb_path, as_version=4)
    exporter = PythonExporter()
    body, _ = exporter.from_notebook_node(nb)
    tmp_py = os.path.join(tempfile.gettempdir(), 'ai_resume_notebook_converted.py')
    with open(tmp_py, 'w', encoding='utf-8') as f:
        f.write(body)
    spec = importlib.util.spec_from_file_location('ai_notebook_module', tmp_py)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def call_notebook_generator(inputs: dict):
    if not os.path.exists(NOTEBOOK_PATH):
        return {'error': f'Notebook not found at {NOTEBOOK_PATH}'}
    try:
        module = load_notebook_module(NOTEBOOK_PATH)
    except Exception as e:
        return {'error': f'Failed to load notebook: {e}'}

    # Common function name candidates
    fn_names = [
        'generate_resume_and_cover_letter',
        'generate',
        'main',
        'run',
        'create_resume_and_cover_letter',
        'create',
    ]

    for name in fn_names:
        fn = getattr(module, name, None)
        if callable(fn):
            try:
                result = fn(inputs)
            except TypeError:
                # maybe takes multiple args or no args
                try:
                    result = fn(**inputs)
                except Exception:
                    try:
                        result = fn()
                    except Exception as e:
                        return {'error': f'Calling {name} failed: {e}'}
            return _normalize_result(result, module)

    # If no function match, search for output variables
    for varname in ('resume_text', 'resume', 'generated_resume'):
        if hasattr(module, varname):
            resume = getattr(module, varname)
            cover = None
            for cvar in ('cover_letter_text', 'cover_letter', 'generated_cover_letter'):
                if hasattr(module, cvar):
                    cover = getattr(module, cvar)
                    break
            return {'resume': str(resume), 'cover_letter': str(cover or '')}

    return {'error': 'No callable generator or expected output variables found in notebook.'}


def _normalize_result(result, module):
    # If module returns dict
    if isinstance(result, dict):
        resume = result.get('resume') or result.get('resume_text') or result.get('generated_resume')
        cover = result.get('cover_letter') or result.get('cover_letter_text') or result.get('generated_cover_letter')
        return {'resume': str(resume or ''), 'cover_letter': str(cover or '')}

    # If tuple/list
    if isinstance(result, (list, tuple)):
        if len(result) >= 2:
            return {'resume': str(result[0] or ''), 'cover_letter': str(result[1] or '')}
        if len(result) == 1:
            return {'resume': str(result[0] or ''), 'cover_letter': ''}

    # If single string
    if isinstance(result, str):
        # try to find cover letter variable
        cover = getattr(module, 'cover_letter_text', None) or getattr(module, 'cover_letter', None)
        return {'resume': result, 'cover_letter': str(cover or '')}

    return {'error': 'Unexpected return type from notebook generator.'}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    data = request.json or request.form.to_dict()
    result = call_notebook_generator(data)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
