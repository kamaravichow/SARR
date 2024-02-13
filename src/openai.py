import os
import openai

OPENAI_KEY = os.getenv("OPENAI_KEY", "sk-<your-api-key>")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo-0125")


def get_ai_response(prompt, max_tokens=160, store="Google Play Store"):
    openai.api_key = OPENAI_KEY
    completion = openai.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": f"Write a reply to review on {store}, Review:\n",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        max_tokens=max_tokens,
        temperature=0.76,
    )
    response = completion.choices[0].message.content

    # Check if response contains any restricted(./instructions/restricted_words.txt) words
    restricted_words = open("./src/instructions/restricted_words.txt", "r").read().split("\n")

    restricted = False
    for word in restricted_words:
        if word in response:
            restricted = True
            break

    if restricted:
        response = "Hello, Please contact our support team at support@aravi.me for further assistance."

    print(f"\n ...  \n\n Response : \n ", response)
    return response
