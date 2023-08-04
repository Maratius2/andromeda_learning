from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler
from telegram.ext.filters import Filters
from telegram import Update
from config import TOKEN
import random

def game(update: Update, context: CallbackContext):
    user_name = update._effective_user.first_name


        
def gateway(update: Update, context: CallbackContext):
    user_name = update._effective_user.first_name
    my_word = update.message.text
    if "секрет" not in context.user_data:
        with open("cows _and_bulls/words.txt", encoding="utf-8") as file:
            words = file.read().split("\n")
        secret_word = random.choice(words)
        context.user_data["секрет"] = secret_word #записываем
    else:
        secret_word = context.user_data["секрет"]  #достаем
    if len(secret_word) != len(my_word):
        update.message.reply_text(f"Количество букв должно быть{len(secret_word)}")   
        return None 
    bulls = 0 
    cows = 0
    for index, letter in enumerate(my_word):
        if letter in secret_word:
            if secret_word[index] == my_word[index]:
                bulls+= 1
            else:
                cows+= 1
    update.message.reply_text(f"В вашем слове {bulls} быков и {cows} коров")
    if bulls == len(secret_word):
        update.message.reply_photo("https://w7.pngwing.com/pngs/815/457/png-transparent-league-of-legends-victory-league-of-legends-riven-command-conquer-generals-age-of-empires-video-game-victory-miscellaneous-blue-game.png")
        
        
message_handler = MessageHandler(Filters.text, gateway)

#Сам бот и его зам.
updater = Updater(TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(message_handler)


print("server started")
updater.start_polling()
updater.idle()