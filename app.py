import os
import json
import re
from flask import Flask, request, jsonify, render_template
import joblib
from google import genai

app = Flask(__name__)

# Load FAQ knowledge base
with open('faq.json', 'r') as f:
    FAQS = json.load(f)

# Load Intent Classifier Model
classifier = None
if os.path.exists('model.pkl'):
    classifier = joblib.load('model.pkl')

LOGS = []
STATS = {
    "ratings": {"up": 0, "down": 0},
    "categories": {cat: 0 for cat in ["requirements", "schedule", "payment", "scholarship", "registrar services", "unknown"]}
}

STOPWORDS = {"the", "ang", "a", "an", "in", "on", "at", "for", "is", "are", "sa", "na", "ng", "mga", "ako", "ikaw", "ano", "paano"}

def retrieve_top_faqs(user_query, top_n=3):
    query_words = set(re.findall(r'\w+', user_query.lower())) - STOPWORDS
    
    scored_faqs = []
    for faq in FAQS:
        faq_text = f"{faq['question']} {faq['answer']}".lower()
        faq_words = set(re.findall(r'\w+', faq_text)) - STOPWORDS
        overlap = len(query_words.intersection(faq_words))
        scored_faqs.append((overlap, faq))
    
    scored_faqs.sort(key=lambda x: x[0], reverse=True)
    return [faq for score, faq in scored_faqs[:top_n]]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    user_message = data.get('message', '').strip()

    if not user_message or len(user_message) > 500:
        return jsonify({"error": "Message must be between 1 and 500 characters."}), 400

    category = "unknown"
    if classifier:
        try:
            category = classifier.predict([user_message])[0]
        except Exception:
            category = "unknown"
    STATS["categories"][category] = STATS["categories"].get(category, 0) + 1

    top_faqs = retrieve_top_faqs(user_message, top_n=3)
    faq_context = json.dumps(top_faqs, indent=2)
    faq_ids = [faq['id'] for faq in top_faqs]

    api_key = "AQ.Ab8RN6LOHfJgvhv8hnAePF9LaK7vFWwYsQzmj6LuUGmRYRWT7A"
    if not api_key:
        return jsonify({"error": "Server missing GEMINI_API_KEY environment variable."}), 500

    prompt = f"""
You are the official Bayanihan College Enrollment Helpdesk Assistant.
Answer the user's question STRICTLY using only the provided FAQ context below.
Rules:
1. Respond in the language the user wrote in (English, Filipino, or Taglish).
2. If the question cannot be answered directly from the provided FAQ entries, reply: "I'm sorry, but I don't have information on that topic based on official FAQ guidelines. Please contact the Registrar's Office directly."
3. Do NOT make up any information or use external facts.

FAQ Context:
{faq_context}

User Question: {user_message}
"""

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)
        answer = response.text.strip()
    except Exception as e:
        print(f"Gemini API Error: {e}")
        answer = "Sorry, an error occurred while connecting to the Gemini model."

    log_id = len(LOGS) + 1
    LOGS.append({
        "id": log_id,
        "question": user_message,
        "category": category,
        "rating": None
    })

    return jsonify({
        "log_id": log_id,
        "answer": answer,
        "faq_ids": faq_ids,
        "predicted_category": category
    })

@app.route('/api/feedback', methods=['POST'])
def feedback():
    data = request.get_json() or {}
    log_id = data.get('log_id')
    rating = data.get('rating')

    if rating in ['up', 'down']:
        STATS["ratings"][rating] += 1
        if log_id and 0 < log_id <= len(LOGS):
            LOGS[log_id - 1]["rating"] = rating
        return jsonify({"status": "success"})
    return jsonify({"error": "Invalid rating"}), 400

@app.route('/api/stats', methods=['GET'])
def stats():
    total_ratings = STATS["ratings"]["up"] + STATS["ratings"]["down"]
    thumbs_up_pct = (STATS["ratings"]["up"] / total_ratings * 100) if total_ratings > 0 else 0
    return jsonify({
        "questions_per_category": STATS["categories"],
        "thumbs_up_percentage": round(thumbs_up_pct, 1),
        "total_feedbacks": total_ratings
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)