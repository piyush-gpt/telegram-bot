from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from bot.services.serpapi import perform_web_search
from bot.services.gemini import summarize_search_results

async def web_search(update: Update, context: CallbackContext):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Please provide a search query.")
        return

    search_results = perform_web_search(query)
    summary = summarize_search_results(search_results)

    await update.message.reply_text(f"Summary: {summary}\n\nTop Links:\n{search_results[0]['link']}")

# Handler
web_search_handler = CommandHandler("websearch", web_search)