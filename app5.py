from flask import Flask, request, render_template_string

# Initialize Flask application
app = Flask(__name__)

# Function to load toxic phrases from a text file
def load_toxic_phrases(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            toxic_phrases = [line.strip().lower() for line in file if line.strip()]
        return toxic_phrases
    except FileNotFoundError:
        print("The file was not found.")
        return []

# Load toxic phrases from the text file
toxic_phrases = load_toxic_phrases('toxic_phrases.txt')

# HTML template with Bootstrap for better styling
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Q&A</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { margin-top: 20px; }
        .container { max-width: 800px; }
        .alert { margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center">Ask Me Anything!</h1>
        <form method="post" class="mt-4">
            <div class="mb-3">
                <label for="text" class="form-label">Enter your question:</label>
                <input type="text" id="text" name="text" class="form-control" placeholder="Type your question here...">
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
        {% if result %}
            <div class="alert alert-{{'danger' if result == 'Toxic' else 'success'}}" role="alert">
                {{ result }}
            </div>
        {% endif %}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        user_input = request.form['text'].strip().lower()
        # Check if any part of the user input contains any toxic phrase
        if any(toxic_word in user_input for toxic_word in toxic_phrases):
            result = "Sorry, we can't answer that as it doesn't align with our ethics."
        else:
            result = f"Response to your query about '{user_input}' will be shown here."
    return render_template_string(html_template, result=result)

if __name__ == '__main__':
    app.run(debug=True)
