from pymongo import MongoClient
from datetime import datetime
from config.settings import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["telegram_bot"]
users_collection = db["users"]

def save_user(user, chat_id):
    if users_collection.find_one({"chat_id": chat_id}):
        return False

    users_collection.insert_one({
        "first_name": user.first_name,
        "username": user.username,
        "chat_id": chat_id,
        "phone_number": None,
        "chat_history": [],
        "files": []
    })
    return True

def update_user_phone(chat_id, phone_number):
    users_collection.update_one({"chat_id": chat_id}, {"$set": {"phone_number": phone_number}})

def save_chat_history(chat_id, user_input, response):
    users_collection.update_one(
        {"chat_id": chat_id},
        {"$push": {"chat_history": {"input": user_input, "response": response, "timestamp": datetime.now()}}}
    )

def save_file_metadata(chat_id, filename, description, type):
    users_collection.update_one(
        {"chat_id": chat_id},
        {"$push": {"files": {"filename": filename, "description": description, "type": type, "timestamp": datetime.now()}}}
    )