#Блок импортов
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler
from telegram.ext.filters import Filters
from telegram import Update
from config import TOKEN
import random


        
def gateway(update: Update, context: CallbackContext):
    user_name = update._effective_user.first_name
    message = update.message.text
    with open("cows _and_bulls/words.txt", encoding="utf-8") as file:
        words = file.read().split("\n")
    secret_word = random.choice(words)
    context.user_data["секрет"] = secret_word
    update.message.reply_text(secret_word)
        
        
message_handler = MessageHandler(Filters.text, gateway)

#Сам бот и его зам.
updater = Updater(TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(message_handler)


print("server started")
updater.start_polling()
updater.idle()