from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters
)

from config import TELEGRAM_BOT_TOKEN
from telegram_handler import handle_message

app = (
    ApplicationBuilder()
    .token(TELEGRAM_BOT_TOKEN)
    .build()
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_message
    )
)

print("Bot is running...")

app.run_polling()
