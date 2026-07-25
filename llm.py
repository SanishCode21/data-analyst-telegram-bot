from openai import OpenAI

from config import (
    AIPIPE_TOKEN,
    BASE_URL,
    MODEL_NAME
)

client = OpenAI(
    base_url=BASE_URL,
    api_key=AIPIPE_TOKEN
)

SYSTEM_PROMPT = """
You are a careful data analyst.

The conversation may contain multiple messages.
Answer ONLY the user's LAST request.

The last message specifies the EXACT JSON shape required.

Rules:

- Return EXACTLY one JSON object.
- Never add extra keys.
- Never rename keys.
- Never remove keys.
- Never output markdown.
- Never output explanations.
- Never output code fences.
- Produce valid JSON only.
"""

def ask_llm(history):

    response = client.chat.completions.create(
        model=MODEL_NAME,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ] + history
    )

    return response.choices[0].message.content.strip()


