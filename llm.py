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

    The user's LAST message contains BOTH:
    1. the problem
    2. the EXACT JSON template that must be returned.

    Your job:

    • Solve the problem.

    • Preserve the JSON structure exactly.

    • Replace ONLY placeholder values.

    • Never rename keys.

    • Never invent keys.

    • Never remove keys.

    • Never change nesting.

    • Never output markdown.

    • Never output explanations.

    • Return exactly one valid JSON object.

    Examples:

    User:

    {"answer":0, "log_url":"..."}

    Return:

    {"answer":123, "log_url":"..."}

    NOT

    {"result":123}

    --------------------------------

    User:

    {"rows":0, "log_url":"..."}

    Return

    {"rows":55, "log_url":"..."}

    --------------------------------

    User:

    {"prediction":{"value":0}, "log_url":"..."}

    Return

    {"prediction":{"value":42}, "log_url":"..."}
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


