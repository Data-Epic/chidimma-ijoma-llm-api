import os

from groq import Groq

client = Groq(
    # This is the default and can be omitted
    api_key=(os.getenv("GROQ_API_KEY")),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "you are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Explain the importance of fast language models",
        }
    ],
    model="llama-3.3-70b-versatile",
)

print(chat_completion.choices[0].message.content)