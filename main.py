import os
import openai
from dotenv import load_dotenv
load_dotenv()


# Set your Hugging Face token as the API key if you use embeddings
# If you don't use embeddings, leave it empty
openai.api_key = os.getenv("OPENAI")  # Replace with your actual token

# Set the API base URL if needed, e.g., for a local development environment
openai.api_base = "http://localhost:1337/v1"

edited_news_text = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": """ """}
                , {"role": "user", "content": "Hello"}],
            stream=False,
        ).choices[0].message.content

print(edited_news_text)

