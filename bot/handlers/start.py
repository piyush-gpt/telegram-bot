from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackContext
from bot.models.user import save_user, update_user_phone

async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    chat_id = update.message.chat_id

    if not save_user(user, chat_id):
        await update.message.reply_text("Welcome back!")
        return

    contact_button = KeyboardButton("Share Contact", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[contact_button]], one_time_keyboard=True)
    await update.message.reply_text("Please share your phone number.", reply_markup=reply_markup)

async def handle_contact(update: Update, context: CallbackContext):
    contact = update.message.contact  # Get contact details
    chat_id = update.message.chat_id
    
    if not contact:
        await update.message.reply_text("❌ No contact shared! Please try again.")
        return

    phone_number = contact.phone_number  # Extract phone number

    if not phone_number:
        await update.message.reply_text("❌ Could not retrieve phone number!")
        return

    update_user_phone(chat_id, phone_number)  # Update DB
    await update.message.reply_text("✅ Thank you! Your phone number has been saved.")

# Handlers
start_handler = CommandHandler("start", start)
contact_handler = MessageHandler(filters.CONTACT, handle_contact)
