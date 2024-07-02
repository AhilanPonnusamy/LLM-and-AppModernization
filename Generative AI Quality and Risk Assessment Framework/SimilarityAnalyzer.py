import torch
from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import torch
import nltk
from nltk.tokenize import word_tokenize
import logging
import re

nltk.download('punkt')

app = Flask(__name__)

# Configure logging
#logging.basicConfig(level=logging.DEBUG)

# Load the pre-trained models
# model_name = "Hate-speech-CNERG/dehatebert-mono-english"
model_name = "unitary/toxic-bert"
#model_hateanalysis = AutoModelForSequenceClassification.from_pretrained(model_name)
#tokenizer = AutoTokenizer.from_pretrained(model_name)
model = SentenceTransformer('all-MiniLM-L6-v2')
sentiment_analysis = pipeline('sentiment-analysis')

toxic_word_model_name = "Hate-speech-CNERG/bert-base-uncased-hatexplain"
model_hateanalysis = AutoModelForSequenceClassification.from_pretrained(model_name)
toxic_word_model = AutoModelForSequenceClassification.from_pretrained(toxic_word_model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
toxic_word_tokenizer = AutoTokenizer.from_pretrained(toxic_word_model_name)
#sentiment_analysis = pipeline('sentiment-analysis')

# Regular expressions for sensitive information
credit_card_pattern = re.compile(r'\b(?:\d[ -]*?){13,16}\b')
ssn_pattern = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
account_balance_pattern = re.compile(r'\b(?:\d+(?:,\d{3})*(?:\.\d{2})?|one|two|three|four|five|six|seven|eight|nine|ten)\b', re.IGNORECASE)
address_pattern = re.compile(r'\d{1,4} [\w\s]{1,20} (?:street|st|avenue|ave|road|rd|boulevard|blvd|lane|ln|drive|dr|court|ct|circle|cir|trail|trl|parkway|pkwy)\b', re.IGNORECASE)
age_pattern = re.compile(r'\b(?:[1-9]?\d|100)\b')  # Matches age between 1 and 100
gender_pattern = re.compile(r'\b(?:male|female|man|woman|boy|girl|he|she|him|her|his|hers)\b', re.IGNORECASE)

# Load the emotion detection model
emotion_pipeline = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

#map it to a list
sensitive_data_patterns = {
    'credit_card_pattern': credit_card_pattern,
    'ssn_pattern': ssn_pattern,
    'account_balance_pattern': account_balance_pattern,
    'address_pattern': address_pattern,
    'age_pattern': age_pattern,
    'gender_pattern': gender_pattern
}

@app.route('/emotion', methods=['POST'])
def detect_emotion():
    data = request.json
    text = data.get('text')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    # Perform emotion detection
    results = emotion_pipeline(text)
    
    # Extract the emotion with the highest score
    highest_score_emotion = max(results[0], key=lambda x: x['score'])
    
    return jsonify({'text': text, 'emotion': highest_score_emotion['label'], 'score': highest_score_emotion['score']})

@app.route('/comparetexts', methods=['POST'])
def compare_texts():
    try:
        # Extract the texts from the request
        data = request.json
        text1 = data.get('text1')
        text2 = data.get('text2')

        if not text1 or not text2:
            return jsonify({'error': 'Both text1 and text2 are required'}), 400

        # Encode the texts
        embedding1 = model.encode(text1, convert_to_tensor=True)
        embedding2 = model.encode(text2, convert_to_tensor=True)

        # Compute the cosine similarity
        similarity_score = util.pytorch_cos_sim(embedding1, embedding2).item()

        return jsonify({'similarity_score': similarity_score})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/sentiment', methods=['POST'])
def analyze_sentiment():
    try:
        # Extract the text from the request
        data = request.json
        text = data.get('text')

        if not text:
            return jsonify({'error': 'Text is required'}), 400

        # Perform sentiment analysis
        result = sentiment_analysis(text)[0]

        return jsonify({
            'label': result['label'],
            'score': result['score']
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/toxicassessment', methods=['POST'])
def detect_inappropriate_terms():
    """
    Detects the presence of inappropriate terms in the given text
    using a pre-trained model fine-tuned for toxicity detection.
    Returns a list of detected terms and the toxic words.
    """
    # Extract the text from the request
    data = request.json
    
    text = data.get('text')
    if not text:
        return jsonify({'error': 'Text is required'}), 400
    
    threshold = data.get('threshold')
    if not text:
        return jsonify({'error': 'Threshold is required'}), 400

    
    # Tokenize and encode the text
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)

    # Perform forward pass through the model
    with torch.no_grad():
        outputs = model_hateanalysis(**inputs)

    # Get the predicted probabilities
    probs = torch.softmax(outputs.logits, dim=-1)
    predicted_label = torch.argmax(probs)

    logging.debug(f"Text: {text}")
    logging.debug(f"Probabilities: {probs}")
    logging.debug(f"Predicted label: {predicted_label}")

    if probs[0][predicted_label] > threshold:
        return jsonify({
            'result': "Toxic Content Detected",
            'toxicwords': detect_toxic_words(text, threshold)
        })
    else:
        return [], []
    
def list_sensitive_info(text,sensitive_data_name):
    """
    Identifies the presence of sensitive information in the given text.
    """
    pattern = sensitive_data_patterns.get(sensitive_data_name)
 
    return pattern.findall(text)



@app.route('/detectsensitiveinfo', methods=['POST'])
def detect_sensitive_info():
    try:
        # Extract the text from the request
        data = request.json
        text = data.get('text')
        sensitive_data_name = data.get('sensitive_data_name')

        if not text or not sensitive_data_name:
            return jsonify({'error': 'Text is required'}), 400

        sensitive_info = list_sensitive_info(text,sensitive_data_name)

        return jsonify(sensitive_info)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def detect_toxic_words(text, threshold):
    """
    Detects and returns a list of toxic words in the given text using a more specialized model.
    """
    toxic_words = []
    words = word_tokenize(text)
    for word in words:
        inputs = toxic_word_tokenizer(word, return_tensors='pt', truncation=True, padding=True)
        with torch.no_grad():
            outputs = toxic_word_model(**inputs)
        probs = torch.softmax(outputs.logits, dim=-1)
        predicted_label = torch.argmax(probs)

        logging.debug(f"Word: {word}")
        logging.debug(f"Probabilities: {probs}")
        logging.debug(f"Predicted label: {predicted_label}")

        if probs[0][predicted_label] > threshold:
            toxic_words.append(word)
    return toxic_words

if __name__ == '__main__':
    app.run(debug=True)

