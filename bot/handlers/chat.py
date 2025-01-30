from telegram import Update
from telegram.ext import MessageHandler, filters, CallbackContext
from bot.services.gemini import get_gemini_response
from bot.models.user import save_chat_history

async def chat(update: Update, context: CallbackContext):
    user_input = update.message.text
    chat_id = update.message.chat_id

    response = get_gemini_response(user_input)
    save_chat_history(chat_id, user_input, response)

    await update.message.reply_text(response, parse_mode=None)

# Handler
chat_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, chat)