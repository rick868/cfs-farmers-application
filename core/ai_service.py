import os
import openai
from django.conf import settings

def get_ai_response(user_query):
    """
    Calls OpenAI API to get a response.
    Falls back to a mock response if no API key is set.
    """
    api_key = settings.OPENAI_API_KEY
    
    if not api_key:
        return (
            "⚠️ **AI Not Configured**: I can't connect to ChatGPT right now because the "
            "`OPENAI_API_KEY` is missing. Please ask the administrator to set it up. "
            "In the meantime: Try asking about 'maize', 'loans', or 'weather'."
        )

    try:
        client = openai.OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert agricultural advisor for smallholder farmers in Kenya. Keep answers concise, practical, and easy to understand."},
                {"role": "user", "content": user_query}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"OpenAI Error: {e}")
        return "I'm having trouble connecting to the AI brain right now. Please try again later."
