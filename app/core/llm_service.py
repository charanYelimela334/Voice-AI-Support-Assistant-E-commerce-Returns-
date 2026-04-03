from groq import Groq
import os

class LLMService:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def generate_response(self, user_query, context_data):
        prompt = f"""
You are an e-commerce support assistant.

User query:
{user_query}

Available data:
{context_data}

Rules:
- Answer ONLY using the data provided
- Be concise and clear
- If data is missing, say you don't know
"""

        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content
