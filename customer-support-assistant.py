import os

from groq import Groq

client = Groq(
    # This is the default and can be omitted
    api_key=("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"),
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