import threading

from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
)

from config import TELEGRAM_BOT_TOKEN
from telegram_handler import handle_message
from web_server import run_web_server


def start_bot():

    app = (
        ApplicationBuilder()
        .token(TELEGRAM_BOT_TOKEN)
        .build()
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message,
        )
    )

    print("Telegram Bot Started...")

    app.run_polling()


if __name__ == "__main__":

    # Start Telegram bot in background thread
    bot_thread = threading.Thread(
        target=start_bot,
        daemon=True,
    )

    bot_thread.start()

    # Start Flask server (Render detects this port)
    run_web_server()

