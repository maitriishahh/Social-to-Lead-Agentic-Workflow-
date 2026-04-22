import json
import os
from dotenv import load_dotenv
from google import genai
import time

load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

def generate_response(prompt):
    for attempt in range(2):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text.strip() if response.text else "No response generated."

        except Exception:
            # print(f"[INFO] Retry {attempt+1}...")

            time.sleep(1)

    # Fallback model
    try:
        # print("[INFO] Switching to fallback model...")

        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )
        return response.text.strip() if response.text else "No response generated."

    except Exception:
        return "Sorry, I'm facing high traffic right now. Please try again."

def load_knowledge():
    with open('knowledge_base.json','r')as f:
        return json.load(f)


def retrieve_answer(query):
    data = load_knowledge()

    prompt = f"""
    You are an AI assistant for AutoStream.

Answer the user's question using ONLY this data:
{data}

User question: {query}

IMPORTANT:
- Do NOT greet the user
- Do NOT say "Hi", "Hello", or similar
- Continue the conversation naturally
- Be concise and professional
- Use bullet points if needed
    """

    return generate_response(prompt)


def detect_intent(user_input):
    text = user_input.lower()

    if any(word in text for word in ["buy", "subscribe", "sign up", "interested", "try"]):
        return 'high_intent'
    
    elif any(word in text for word in ['hi','hello','hey']):
        return 'greeting'
    
    elif any(word in text for word in ["price", "pricing", "plan", "plans", "cost","feature", "features"]):
        return 'pricing'
    
    elif any(word in text for word in ["policy", "policies", "refund", "support"]):  
        return "policies"
    else:
        return 'unknown'