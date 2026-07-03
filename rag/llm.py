import os
from google import genai
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Initialize the modern client. 
# It automatically picks up "GEMINI_API_KEY" from your environment.
client = genai.Client()

# To generate text moving forward, you will call the client like this:
# response = client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents="Your prompt here"
# )