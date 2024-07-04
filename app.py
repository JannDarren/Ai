from flask import Flask, request, jsonify, render_template
import random

app = Flask(__name__)

# Business Sentiment Lexicons (Sample)
sentiment_words = {
  "accommodation": {
    "positive": ["comfortable", "clean", "relaxing", "helpful"],
    "negative": ["noisy", "dirty", "uncomfortable", "rude"]
  },
  "restaurant": {
    "positive": ["delicious", "great", "wonderful", "recommend"],
    "negative": ["bland", "slow", "disappointing", "unclean"]
  },
  "brand": {
    "positive": ["reliable", "innovative", "trustworthy", "excellent"],
    "negative": ["unreliable", "outdated", "unethical", "poor"]
  },
  "product": {
    "positive": ["effective", "user-friendly", "durable", "value"],
    "negative": ["ineffective", "confusing", "cheap", "overpriced"]
  }
}

def get_sentiment(text, context):
  sentiment_score = 0
  for word in text.split():
    if word.lower() in sentiment_words[context]["positive"]:
      sentiment_score += 1
    elif word.lower() in sentiment_words[context]["negative"]:
      sentiment_score -= 1
  return sentiment_score

def get_response(sentiment, context):
  responses = {
    "positive": {
      "accommodation": "We're glad you enjoyed your stay! Thank you for choosing us.",
      "restaurant": "We appreciate your kind words! We strive to provide a wonderful dining experience.",
      "brand": "Thank you for being a loyal customer! We value your trust.",
      "product": "We're happy to hear you're satisfied with our product!",
    },
    "negative": {
      "accommodation": "We apologize for any inconvenience. Please let us know how we can improve your experience.",
      "restaurant": "We're sorry to hear you didn't enjoy your meal. We'll take your feedback seriously.",
      "brand": "We value your feedback. Please let us know how we can regain your trust.",
      "product": "We apologize for any issues with our product. Would you like to discuss a replacement or refund?"
    }
  }
  return responses[sentiment][context]

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
  data = request.json
  user_text = data.get('message')
  context = data.get('context', 'accommodation')  # default context

  sentiment = get_sentiment(user_text, context)
  response_type = "positive" if sentiment > 0 else "negative"
  response = get_response(response_type, context)

  return jsonify({"response": response})

if __name__ == '__main__':
  app.run(debug=True, port=8000)


