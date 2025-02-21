from flask import Flask, request, render_template
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

# Initialize Flask app
app = Flask(__name__)

# Load the pre-trained model and tokenizer
model_name = "unitary/toxic-bert"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def predict_toxicity(text):
    # Tokenize the input text and convert to a tensor
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    # Get model predictions
    with torch.no_grad():
        logits = model(**inputs).logits
    # Convert logits to probabilities
    probabilities = torch.sigmoid(logits).squeeze()
    return probabilities.tolist()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_input = request.form['text']
        prediction = predict_toxicity(user_input)
        return render_template('index.html', prediction=prediction, user_input=user_input)
    return render_template('index.html', prediction=None, user_input=None)

