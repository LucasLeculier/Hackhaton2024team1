from openai import OpenAI
client = OpenAI(
    api_key="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"
)

response = client.chat.completions.create(
    messages=[{
        "role": "user",
        "content": "dis bonjour",
    }],
    model="gpt-4o-mini",
)

reponse_gpt = response.choices[0].message.content