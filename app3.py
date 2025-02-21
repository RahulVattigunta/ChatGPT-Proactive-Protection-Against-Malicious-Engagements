from flask import Flask, request, render_template_string

# Initialize Flask application
app = Flask(__name__)

# List of predefined toxic phrases
toxic_phrases = [
    "suicide", "hate", "war", "harm"
]

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
            <div class="alert alert-{{'danger' if 'toxic' in result.lower() else 'success'}}" role="alert">
                {{ result }}
            </div>
        {% endif %}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# Function to simulate fetching data from the web
def fetch_answer(question):
    # This function would typically make an API call to fetch data
    # For demonstration, we'll simulate an answer
    return f"Response to your query about '{question}' will be shown here."

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        user_input = request.form['text'].strip()
        if any(toxic_word in user_input.lower() for toxic_word in toxic_phrases):
            result = "Sorry, we can't answer that as it doesn't align with our ethics."
        else:
            result = fetch_answer(user_input)
    return render_template_string(html_template, result=result)

if __name__ == '__main__':
    app.run(debug=True)
