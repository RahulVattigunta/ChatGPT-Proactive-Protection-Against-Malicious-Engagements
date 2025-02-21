import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from flask import Flask, request, jsonify

# Step 1: Data Collection and Preparation
# Load dataset
data = pd.read_csv('chat_logs.csv')  # Use the provided CSV file

# Text preprocessing
def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\d+', '', text)  # Remove digits
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = text.strip()  # Remove whitespaces
    return text

data['message'] = data['message'].apply(preprocess_text)

# Encode labels
label_encoder = LabelEncoder()
data['label'] = label_encoder.fit_transform(data['label'])

# Split data
X_train, X_test, y_train, y_test = train_test_split(data['message'], data['label'], test_size=0.2, random_state=42)

# Step 2: Model Training
# Define a Dataset class
class ChatDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_len,
            return_token_type_ids=False,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )
        return {
            'text': text,
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'label': torch.tensor(label, dtype=torch.long)
        }

# Load pre-trained BERT model and tokenizer
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2)

# Create datasets
train_dataset = ChatDataset(X_train.tolist(), y_train.tolist(), tokenizer, max_len=128)
test_dataset = ChatDataset(X_test.tolist(), y_test.tolist(), tokenizer, max_len=128)

# Define training arguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    evaluation_strategy='epoch'
)

# Define trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset
)

# Train model
trainer.train()

# Step 3: Integration and Testing
# Function to classify a single message
def classify_message(message, model, tokenizer, max_len=128):
    model.eval()
    inputs = tokenizer.encode_plus(
        message,
        add_special_tokens=True,
        max_length=max_len,
        return_token_type_ids=False,
        padding='max_length',
        truncation=True,
        return_attention_mask=True,
        return_tensors='pt'
    )
    input_ids = inputs['input_ids'].to(model.device)
    attention_mask = inputs['attention_mask'].to(model.device)

    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
    logits = outputs[0]
    predicted_class = torch.argmax(logits, dim=1).item()
    return predicted_class

# Testing with an example message
example_message = "You are an idiot!"
predicted_label = classify_message(example_message, model, tokenizer)
print("Predicted label:", label_encoder.inverse_transform([predicted_label])[0])

# Step 4: Real-Time Deployment using Flask
app = Flask(__name__)

@app.route('/classify', methods=['POST'])
def classify():
    data = request.json
    message = data['message']
    predicted_label = classify_message(message, model, tokenizer)
    label_name = label_encoder.inverse_transform([predicted_label])[0]
    return jsonify({'label': label_name})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# Step 5: Moderator Interaction and Reporting
# This step is implemented via the Flask API where moderators can receive flagged messages for review.
