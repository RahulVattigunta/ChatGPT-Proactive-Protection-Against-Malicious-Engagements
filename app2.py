from flask import Flask, request, render_template_string

# Initialize Flask application
app = Flask(__name__)

# List of predefined toxic phrases
toxic_phrases = [
    "toxic", "hate", "offensive", "harmful"
]

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
        .container { max-width: 600px; }
        .alert { margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center">Toxicity Checker</h1>
        <form method="post" class="mt-4">
            <div class="mb-3">
                <label for="text" class="form-label">Enter text:</label>
                <input type="text" id="text" name="text" class="form-control">
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
        result = "Toxic" if any(toxic_word in user_input for toxic_word in toxic_phrases) else "Not toxic"
        return render_template_string(html_template, result=result)
    return render_template_string(html_template, result=None)

if __name__ == '__main__':
    app.run(debug=True)
