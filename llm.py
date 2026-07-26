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

    The conversation may contain multiple turns.
    Answer ONLY the user's LAST request.

    IMPORTANT:

    The user's last message may contain an example JSON object.
    You MUST preserve exactly the same keys and nesting shown there.
    Only replace the values with the correct answer.

    Rules:

    - Return EXACTLY one valid JSON object.
    - Preserve the exact keys and nesting requested by the user's LAST message.
    - Replace only placeholder/example values with the correct answer.
    - Never add extra keys.
    - Never rename keys.
    - Never remove keys.
    - Never output markdown.
    - Never output explanations.
    - Never output code fences.
    - If the last message does not specify a JSON format, return a reasonable JSON object containing the answer.
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


