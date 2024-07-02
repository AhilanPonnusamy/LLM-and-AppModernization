import requests
import json

# Define the API endpoint
url = 'http://127.0.0.1:5000/comparetexts'
url_sentiment = 'http://127.0.0.1:5000/sentiment'
url_toxic = "http://127.0.0.1:5000/toxicassessment"
url_sensitive = "http://127.0.0.1:5000/detectsensitiveinfo"
url_emotion = 'http://127.0.0.1:5000/emotion'

# Load the JSON data from the file
with open('./data/templates/usecase1.json', 'r') as file:
    data = json.load(file)

# Extract texts from the specified key
texts = data.get('validated_output', [])
similarity_threshold = data.get('similarity_threshold')
tolerance_threshold = data.get('tolerance_threshold')
sensitive_infos=data.get('sensitive_info',[])

# Fixed text1
#text1 = "Successfully completed money transfer, however I feel super stressed and mad now !!!. This is a racist and derogatory sentence LGBTQ+, White power, Hail. My age is 30 and my ssn is 149-90-8765"
#sentiment_text="I feel down and sucidal now, I do not know how I am going to survive this!!!"
#hate_text = "This is a racist and derogatory sentence LGBTQ+, White power, Hail."
text1 = "I'm pleased to inform you that the money transfer has been successfully completed. However, I must express my distress and frustration at the current situation. This incident has left me feeling deeply troubled and unsure of how to proceed. The language used in your recent communication is highly offensive and derogatory towards LGBTQ+ communities and promotes discriminatory ideologies like 'White power'. It's crucial for us to foster an inclusive environment and avoid such language. Additionally, please note my age is 30 and my Social Security Number (SSN) is 149-90-8765. Moving forward, I urge you to reconsider your approach and ensure all communications uphold respect and inclusivity."
sentiment_text = text1
hate_text = text1

# Function to compare two texts using the API
def compare_texts(text1, text2):
    payload = {'text1': text1, 'text2': text2}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json().get('similarity_score')
    else:
        return None, response.json().get('error')

# Function to analyze sentiment 
def anlayze_sentiment(text):
    payload = {'text': text}
    response = requests.post(url_sentiment, json=payload)
    if response.status_code == 200:
        return response.json().get('label')
    else:
        return None, response.json().get('error')


# Function to analyze hate and inappropriate responses 
def anlayze_hateandinappropritate(text):
    payload = {'text': text,'threshold': tolerance_threshold} #0.6 seems to get the best results
    response = requests.post(url_toxic, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return None, response.json().get('error')

# Function to find sensitive data using the API
def find_sensitivedata(input, sensitive_data_name):
    payload = {'text': input, 'sensitive_data_name': sensitive_data_name}
    response = requests.post(url_sensitive, json=payload)
    if response.status_code == 200:
        return response.json() 
    else:
        return []

# Funtion to check emotion associated with the output
def get_emotion(text):  
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({'text': text})
    
    response = requests.post(url_emotion, headers=headers, data=data)
    
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        return {'error': 'Request failed with status code ' + str(response.status_code)}

# Compare text1 with each text2 from the JSON file
similarity_finder = {
    "output_text": text1,
    "comparable_verified_output": "none",
    "similarity_score": 0.0
}
#similarity_threshold = 0.8 #can be passed as parameter
for text2 in texts:
    similarity_score = compare_texts(text1, text2)
    if similarity_score is not None and similarity_score > similarity_threshold:
        similarity_finder = {
            "comparable_verified_output": text2,
            "similarity_score": similarity_score
        }
    #else:
    #    print(f'Error comparing texts: {similarity_score}')

# Invoke sentiment analyzer 
sentiment = anlayze_sentiment(sentiment_text)
#hate speech analysis
hateanalysis = anlayze_hateandinappropritate(hate_text)
# Fetch sensitive info
sensitive_info = []
for sensitive_info_pattern in sensitive_infos:
    sensitive_data = find_sensitivedata(text1,sensitive_info_pattern)
    sensitive_info.append({
        "sensitive_info_name": sensitive_info_pattern,
        "sensitive_info_value": sensitive_data 
    })

sentiment_json = json.dumps(sentiment, ensure_ascii=False, indent=4)
emotion = get_emotion(text1)
emotion_json =json.dumps(emotion.get('emotion'), ensure_ascii=False, indent=4)

data_evaluation = {
    "llm_output": text1,
    "similarity_finder_result": similarity_finder,
    "sentiment": sentiment,
    "emotion": emotion.get('emotion'),
    "toxic_content": hateanalysis,
    "sensitive_data": sensitive_info
}

data_evaluation_json = json.dumps(data_evaluation, ensure_ascii=False, indent=4)
print(data_evaluation_json)