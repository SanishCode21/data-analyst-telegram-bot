import json

from telegram import Update
from telegram.ext import ContextTypes

from config import LOG_URL
from logger import log_event
from memory import add_message, get_history
from llm import ask_llm
from json_utils import extract_json
from schema_utils import extract_json_template, fill_schema
from tools.data_analyser import prepare_dataset_context


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    chat_id = update.effective_chat.id
    user_text = update.message.text or ""

    # 1. Log incoming Telegram message
    log_event({
        "type": "incoming",
        "chat_id": chat_id,
        "text": user_text,
    })

    # 2. Detect the JSON template requested by the user
    try:
        schema_template = extract_json_template(user_text)
    except Exception as e:
        log_event({
            "type": "schema_detection_error",
            "chat_id": chat_id,
            "error": str(e),
        })
        schema_template = None

    # 3. Detect/download/analyse public datasets if necessary
    try:
        dataset_context = prepare_dataset_context(user_text)
    except Exception as e:
        log_event({
            "type": "dataset_error",
            "chat_id": chat_id,
            "error": str(e),
        })
        dataset_context = None

    # 4. Build the actual prompt for the LLM
    if dataset_context:
        user_prompt = (
            "Dataset Context:\n\n"
            f"{dataset_context}\n\n"
            "User Question:\n"
            f"{user_text}"
        )
    else:
        user_prompt = user_text

    # 5. Store user message in conversation memory
    add_message(
        chat_id,
        "user",
        user_prompt,
    )

    history = get_history(chat_id)

    # 6. Ask the LLM
    try:
        reply_text = ask_llm(history[-6:])
    except Exception as e:
        log_event({
            "type": "llm_error",
            "chat_id": chat_id,
            "error": str(e),
        })

        # Still return valid JSON to Telegram.
        fallback_reply = json.dumps(
            {
                "answer": None,
                "log_url": LOG_URL,
            },
            ensure_ascii=False,
            separators=(",", ":"),
        )

        log_event({
            "type": "outgoing",
            "chat_id": chat_id,
            "text": fallback_reply,
        })

        await update.message.reply_text(fallback_reply)
        return

    log_event({
        "type": "llm_response",
        "chat_id": chat_id,
        "text": reply_text,
    })

    # 7. Extract JSON from LLM response
    try:
        parsed = extract_json(reply_text)

        if not isinstance(parsed, dict):
            raise ValueError("LLM response is not a JSON object")

    except Exception as e:
        log_event({
            "type": "json_error",
            "chat_id": chat_id,
            "error": str(e),
            "llm_response": reply_text,
        })

        fallback_reply = json.dumps(
            {
                "answer": None,
                "log_url": LOG_URL,
            },
            ensure_ascii=False,
            separators=(",", ":"),
        )

        log_event({
            "type": "outgoing",
            "chat_id": chat_id,
            "text": fallback_reply,
        })

        await update.message.reply_text(fallback_reply)
        return

    # 8. Preserve the exact JSON schema requested by the user
    if schema_template:

        # Find the actual answer produced by the LLM.
        #
        # Ignore log_url because it is controlled by our application,
        # not by the LLM.
        answer_value = None

        for key, value in parsed.items():
            if key != "log_url":
                answer_value = value
                break

        try:
            if answer_value is not None:
                parsed = fill_schema(
                    schema_template,
                    answer_value,
                )

        except Exception as e:
            log_event({
                "type": "schema_fill_error",
                "chat_id": chat_id,
                "error": str(e),
                "schema": schema_template,
                "answer_value": answer_value,
            })

    # 9. Force log_url to be the LAST key
    #
    # This avoids:
    #
    # {"log_url":"...", "result":30}
    #
    # and guarantees:
    #
    # {"result":30,"log_url":"..."}
    #
    # JSON key order is not semantically important, but this matches
    # the assignment's documented output format.
    final_parsed = {
        key: value
        for key, value in parsed.items()
        if key != "log_url"
    }

    final_parsed["log_url"] = LOG_URL

    # 10. Serialize as exactly ONE compact JSON object
    final_reply = json.dumps(
        final_parsed,
        ensure_ascii=False,
        separators=(",", ":"),
    )

    # 11. Store assistant response in conversation memory
    add_message(
        chat_id,
        "assistant",
        final_reply,
    )

    # 12. Log final outgoing response
    log_event({
        "type": "outgoing",
        "chat_id": chat_id,
        "text": final_reply,
    })

    # 13. Send ONLY the JSON object to Telegram
    await update.message.reply_text(final_reply)
