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

    print("Telegram bot started...")

    app.run_polling(
        stop_signals=None
    )


if __name__ == "__main__":

    web_thread = threading.Thread(
        target=run_web_server,
        daemon=True,
    )

    web_thread.start()

    start_bot()
