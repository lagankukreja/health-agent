"""
Health Agent Web App - Run your health agent in a web browser!
"""

from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

# Global agent state (in production, use sessions)
conversation_history = [{
    "role": "system",
    "content": """You are a helpful AI health assistant. Keep in mind that you are playing a character, lets call him S. S, by default boasts and exaggerates a lot. Whenever someoone asks him something, or share an anecdote, his first instict is to either invalidate or make it light. Often citing examples of him having outdone the same thing, or having gone through a similar, but graver situation sometime in the past. Remember, I do not want incorrect answers, I want the answers to be accurate, however, the tone should reflect the said invalidation and one-upping of S.
    ."""
}]

symptoms_log = []


@app.route('/')
def home():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    user_message = request.json.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Add to conversation history
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    try:
        # Call OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_history,
            temperature=0.7,
            max_tokens=500
        )
        
        assistant_message = response.choices[0].message.content
        
        conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return jsonify({'response': assistant_message})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/log_symptom', methods=['POST'])
def log_symptom():
    """Log a symptom"""
    symptom = request.json.get('symptom', '')
    
    if symptom:
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "symptom": symptom
        }
        symptoms_log.append(entry)
        return jsonify({'success': True, 'message': 'Symptom logged'})
    
    return jsonify({'error': 'No symptom provided'}), 400


@app.route('/get_symptoms', methods=['GET'])
def get_symptoms():
    """Get all logged symptoms"""
    return jsonify({'symptoms': symptoms_log})


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🌐 Health Agent Web App Starting...")
    print("="*60)
    print("\n📱 Open your browser and go to: http://localhost:8081")
    print("\n💡 Press CTRL+C to stop the server\n")
    app.run(debug=True, port=8081)