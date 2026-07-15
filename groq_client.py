from dotenv import load_dotenv
import os
from groq import Groq

# lazy initilazation
client = None

def get_notes(prompt):
    # client access
    global client

    if client is None:
        # api import
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")
        # client set
        client = Groq(api_key=api_key)

    # create request with model & messages
    request = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    response = request.choices[0].message.content

    return response