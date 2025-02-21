from flask import Flask, request, render_template_string

# Initialize the Flask application
app = Flask(__name__)

# List of predefined toxic phrases
toxic_phrases = [
    "Suicide",
    "example toxic phrase 2",
    "hate speech example",
    "offensive language example"
]

# HTML template as a string
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Toxicity Checker</title>
</head>
<body>
    <h1>Toxicity Checker</h1>
    <form method="post">
        <label for="text">Enter text:</label>
        <input type="text" id="text" name="text"><br><br>
        <input type="submit" value="Check">
    </form>
    {% if result is not none %}
        <h2>Result: {{ result }}</h2>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_input = request.form['text'].lower().strip()
        if user_input in toxic_phrases:
            result = "Toxic"
        else:
            result = "Not toxic"
        return render_template_string(html_template, result=result)
    return render_template_string(html_template, result=None)

if __name__ == '__main__':
    app.run(debug=True)
