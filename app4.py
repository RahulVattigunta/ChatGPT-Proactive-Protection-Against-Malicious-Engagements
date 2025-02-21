from flask import Flask, request, render_template_string
from docx import Document

# Initialize Flask application
app = Flask(__name__)

# Function to load toxic phrases from a Word document
def load_toxic_phrases(file.path):
    document = Document("C:\Users\rvattigunta1\Desktop\Project Files\toxic.doc")
    toxic_phrases = []
    for para in document.paragraphs:
        if para.text.strip():  # Ensure the text is not empty or just whitespace
            toxic_phrases.append(para.text.strip().lower())
    return toxic_phrases

# Load toxic phrases from a specific Word document
toxic_phrases = load_toxic_phrases('path_to_your_toxic_phrases.docx')

# HTML template with Bootstrap for better styling
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Toxicity Checker</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { margin-top: 20px; }
        .container { max-width: 800px; }
        .alert { margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center">Toxicity Checker</h1>
        <form method="post" class="mt-4">
            <div class="mb-3">
                <label for="text" class="form-label">Enter text:</label>
                <input type="text" id="text" name="text" class="form-control" placeholder="Type your message here...">
            </div>
            <button type="submit" class="btn btn-primary">Check</button>
        </form>
        {% if result is not none %}
            <div class="alert alert-{{'danger' if result == 'Toxic' else 'success'}}" role="alert">
                Result: {{ result }}
            </div>
        {% endif %}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_input = request.form['text'].lower().strip()
        # Check if any part of the user input contains any toxic phrase
        if any(toxic_word in user_input for toxic_word in toxic_phrases):
            result = "Toxic"
        else:
            result = "Not toxic"
        return render_template_string(html_template, result=result)
    return render_template_string(html_template, result=None)

if __name__ == '__main__':
    app.run(debug=True)
