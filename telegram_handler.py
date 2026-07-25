import json

from telegram import Update
from telegram.ext import ContextTypes

from config import LOG_URL
from logger import log_event
from memory import add_message, get_history
from llm import ask_llm
from json_utils import extract_json

async def handle_message(update: Update,
                         context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id
    user_text = update.message.text

    log_event({
        "type": "incoming",
        "chat_id": chat_id,
        "text": user_text
    })

    add_message(chat_id, "user", user_text)

    history = get_history(chat_id)

    reply_text = ask_llm(history[-6:])

    log_event({
        "type": "llm_response",
        "chat_id": chat_id,
        "text": reply_text
    })

    parsed = extract_json(reply_text)

    parsed["log_url"] = LOG_URL

    final_reply = json.dumps(
        parsed,
        ensure_ascii=False,
        separators=(",", ":")
    )

    add_message(chat_id, "assistant", final_reply)

    log_event({
        "type": "outgoing",
        "chat_id": chat_id,
        "text": final_reply
    })

    await update.message.reply_text(final_reply)

