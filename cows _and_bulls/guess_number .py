from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler
from telegram.ext.filters import Filters
from telegram import Update
from config import TOKEN
import random

def game(update: Update, context: CallbackContext):
    user_name = update._effective_user.first_name
    my_number = update.message.text
    if "секрет" not in context.user_data:
        secret_number = random.randint(1, 100)
        context.user_data["секрет"] = secret_number
    else:
        secret_number = context.user_data["секрет"]
    #здесь должна быть проверка
    my_number = int(my_number)
    if my_number > secret_number:
        update.message.reply_text(f"Мое число меньше")
    elif my_number < secret_number:
        update.message.reply_text(f"Мое число ,больше")
    else:
        update.message.reply_photo("https://w7.pngwing.com/pngs/815/457/png-transparent-league-of-legends-victory-league-of-legends-riven-command-conquer-generals-age-of-empires-video-game-victory-miscellaneous-blue-game.png")
        del context.user_data["секрет"]
        
    
        
message_handler = MessageHandler(Filters.text, game)

#Сам бот и его зам.
updater = Updater(TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(message_handler)


print("server started")
updater.start_polling()
updater.idle()