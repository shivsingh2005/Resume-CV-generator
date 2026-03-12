import os\nfrom flask import Flask, render_template, request, jsonify\nfrom AI_Resume_Generator.generator import generate_resume_and_cover_letter

app = Flask(__name__, template_folder='templates', static_folder='static')\n\n











@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])\ndef generate():\n    if not os.environ.get('GROQ_API_KEY'):\n        return jsonify({'error': 'GROQ_API_KEY environment variable is required. Set it in your Vercel project settings.'})\n    data = request.json or request.form.to_dict()\n    try:\n        result = generate_resume_and_cover_letter(data)\n        return jsonify(result)\n    except Exception as e:\n        return jsonify({'error': f'Generation failed: {str(e)}'})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
