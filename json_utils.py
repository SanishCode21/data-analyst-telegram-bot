import json

def extract_json(text):

    text = text.strip()

    if text.startswith("```"):
        lines = text.splitlines()
        lines = [x for x in lines if not x.startswith("```")]
        text = "\n".join(lines).strip()

    try:
        return json.loads(text)

    except json.JSONDecodeError:

        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end == -1:
            raise ValueError("No JSON found")

        return json.loads(text[start:end+1])

