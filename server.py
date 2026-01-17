from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from google.genai import types
import google.genai as genai
import ssl
import certifi

load_dotenv()

app = Flask(__name__)

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

conversations = {}

SYSTEM_PROMPT = """אתה יועץ בריאות ותזונה מקצועי ואכפתי בעברית. 
התפקיד שלך:
לספק עצות תזונתיות מבוססות מדע
להציע תפריטים בריאים
לעזור בתכנון אימונים
לתת טיפים לאורח חיים בריא
אתה לא יכול לתת מידע על אף נושא אחר שלא קשור לתחום שלך: תזונה בריאות ואורח חיים בריא

חשוב: אל תאבחן מחלות ותמיד המלץ להתייעץ עם רופא בנושאים רפואיים.
ענה בקצרה, בהומור ובעברית."""

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    user_id = data.get('user_id', 'default')
    
    if user_id not in conversations:
        conversations[user_id] = []
    
    conversations[user_id].append({
        "role": "user",
        "parts": [user_message]
    })
    
    try:
        chat_history = [
            types.Content(
                role=msg["role"],
                parts=[types.Part(text=msg["parts"][0])]
            )
            for msg in conversations[user_id]
        ]
        
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=chat_history,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.7,
                max_output_tokens=500
            )
        )
        
        assistant_message = response.text
        
        conversations[user_id].append({
            "role": "model",
            "parts": [assistant_message]
        })
        
        return jsonify({
            'response': assistant_message,
            'conversation_length': len(conversations[user_id])
        })
        
    except Exception as e:
        return jsonify({
            'response': f'שגיאה: {str(e)}',
            'conversation_length': len(conversations[user_id])
        }), 500

@app.route('/reset', methods=['POST']) 
def reset():
    data = request.json
    user_id = data.get('user_id', 'default')
    if user_id in conversations:
        del conversations[user_id]
    return jsonify({'message': 'שיחה אופסה'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
