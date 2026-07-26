import json

from telegram import Update
from telegram.ext import ContextTypes

from config import LOG_URL
from logger import log_event
from memory import add_message, get_history
from llm import ask_llm
from json_utils import extract_json

from tools.data_analyser import prepare_dataset_context


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    chat_id = update.effective_chat.id
    user_text = update.message.text

    # Log incoming message
    log_event({
        "type": "incoming",
        "chat_id": chat_id,
        "text": user_text
    })

    # Prepare dataset context
    try:
        dataset_context = prepare_dataset_context(user_text)
    except Exception as e:
        log_event({
            "type": "dataset_error",
            "chat_id": chat_id,
            "error": str(e)
        })
        dataset_context = None

    # Build prompt
    if dataset_context:
        user_prompt = f"""
        Dataset Context

        {dataset_context}

        User Question

        {user_text}
        """.strip()
    else:
        user_prompt = user_text

    # Store conversation
    add_message(chat_id, "user", user_prompt)

    history = get_history(chat_id)

    # Ask the LLM
    reply_text = ask_llm(history[-6:])

    log_event({
        "type": "llm_response",
        "chat_id": chat_id,
        "text": reply_text
    })

    # Extract valid JSON
    parsed = extract_json(reply_text)

    # Force correct log_url
    parsed["log_url"] = LOG_URL

    if "answer" in parsed and "result" not in parsed:
        parsed["result"] = parsed.pop("answer")

    final_reply = json.dumps(
        parsed,
        ensure_ascii=False,
        separators=(",", ":")
    )

    # Store assistant response
    add_message(chat_id, "assistant", final_reply)

    # Log outgoing response
    log_event({
        "type": "outgoing",
        "chat_id": chat_id,
        "text": final_reply
    })

    # Reply to Telegram
    await update.message.reply_text(final_reply)

