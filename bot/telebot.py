from telegram.ext import ApplicationBuilder
from bot.handlers import start, chat, image, web_search
from config.settings import TELEGRAM_BOT_TOKEN

def main():
    # Build the bot application
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Register handlers
    app.add_handler(start.start_handler)
    app.add_handler(start.contact_handler) 
    app.add_handler(chat.chat_handler)
    app.add_handler(image.image_handler)
    app.add_handler(image.doc_handler)
    app.add_handler(web_search.web_search_handler)

    # Start the bot
    app.run_polling()

if __name__ == "__main__":
    main()
