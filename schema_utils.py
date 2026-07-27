import json
import re


def extract_json_template(text: str):
    """
    Extract the JSON template from the user's message.

    Example:

    Reply ONLY with

    {"answer":{"state":""}, "log_url":"..."}

    Returns the parsed JSON template.
    """

    match = re.search(r"\{.*\}", text, flags=re.DOTALL)

    if not match:
        return None

    try:
        return json.loads(match.group())
    except Exception:
        return None


def fill_schema(template, value):
    """
    Replace placeholder values while preserving keys.
    """

    if isinstance(template, dict):

        result = {}

        # Special case: preserve log_url placeholder
        if "log_url" in template:
            result["log_url"] = template["log_url"]

        non_log_keys = [k for k in template if k != "log_url"]

        if len(non_log_keys) == 1:

            key = non_log_keys[0]

            result[key] = fill_schema(template[key], value)

        else:

            for k in non_log_keys:

                result[k] = template[k]

        return result

    elif isinstance(template, list):

        if len(template) == 0:
            return value

        return [fill_schema(template[0], value)]

    else:

        return value


