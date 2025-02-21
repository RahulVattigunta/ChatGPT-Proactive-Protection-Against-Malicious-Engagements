from flask import Flask, request, render_template_string, session, redirect, url_for
from textblob import TextBlob
import logging
import re
import uuid
import time

# Initialize Flask application
app = Flask(__name__)
app.secret_key = '\xe08\xe1=\xb9\x8b\x81\x0bg-b?\x86\xa0Vo'

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

# List of predefined toxic phrases
toxic_phrases = ["suicide", "hate", "war", "harm"]

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
        .history { margin-top: 20px; font-size: 0.9em; color: #666; }
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
        <div class="history">
            <h5>Session History:</h5>
            <ul>
                {% for entry in session.get('history', []) %}
                    <li>{{ entry }}</li>
                {% endfor %}
            </ul>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# Function to simulate fetching data from the web
def fetch_answer(question):
    try:
        sentiment = TextBlob(question).sentiment
        logging.debug(f"Question: {question}, Sentiment: {sentiment}")
        
        # Adding delay to simulate a complex operation
        time.sleep(1.5)
        
        if sentiment.polarity < -0.3:
            return f"Your question seems a bit negative. Here's a neutral response: '{question}'"
        elif sentiment.polarity > 0.3:
            return f"You seem positive! Here's an enthusiastic response: '{question}'"
        return f"Response to your query about '{question}' will be shown here."
    except Exception as e:
        logging.error(f"Error processing question: {e}")
        return "Sorry, we couldn't process your question."

# Sanitizing user input
def sanitize_input(user_input):
    sanitized = re.sub(r'[^a-zA-Z0-9\s\.,?!]', '', user_input)
    logging.debug(f"Sanitized Input: {sanitized}")
    return sanitized

# Error handling for bad requests
@app.errorhandler(400)
def bad_request(error):
    logging.error(f"Bad Request: {error}")
    return "Bad Request!", 400

# Error handling for page not found
@app.errorhandler(404)
def page_not_found(error):
    logging.error(f"Page Not Found: {error}")
    return "Page Not Found!", 404

# Error handling for internal server errors
@app.errorhandler(500)
def server_error(error):
    logging.error(f"Server Error: {error}")
    return "Internal Server Error!", 500

# Additional route to clear session history
@app.route('/clear_history')
def clear_history():
    session.pop('history', None)
    return redirect(url_for('home'))

# Main route
@app.route('/', methods=['GET', 'POST'])
def home():
    try:
        if 'history' not in session:
            session['history'] = []
        result = None
        
        if request.method == 'POST':
            user_input = request.form['text'].strip()
            sanitized_input = sanitize_input(user_input)
            session_id = str(uuid.uuid4())  # Unique session ID
            
            if any(toxic_word in sanitized_input.lower() for toxic_word in toxic_phrases):
                result = "Sorry, we can't answer that as it doesn't align with our ethics."
                logging.warning(f"Toxic input detected: {sanitized_input}")
            else:
                result = fetch_answer(sanitized_input)
            
            session['history'].append(f"Session {session_id}: Q: {sanitized_input} - A: {result}")
            session.modified = True  # Ensure the session is marked as modified
        
        return render_template_string(html_template, result=result)
    
    except Exception as e:
        logging.error(f"Error in home route: {e}")
        return "An unexpected error occurred.", 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
