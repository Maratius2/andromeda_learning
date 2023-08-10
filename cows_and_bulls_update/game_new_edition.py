from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler
from telegram.ext.filters import Filters
from config import TOKEN
from functions import *

       
        
#message_handler = MessageHandler(Filters.text & ~Filters.command, gateway)

#Сам бот и его зам.
updater = Updater(TOKEN)
dispatcher = updater.dispatcher

contact_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        LEVEL:[MessageHandler(Filters.regex(f"^({GO})$"), choose_level)],
        FIRST:[MessageHandler(Filters.regex(f"^({EASY}|{MEDIUM}|{HARD})$"), begin)],
        CLUE:[MessageHandler(Filters.text & ~Filters.command, game)]
        
        },
    fallbacks=[CommandHandler("cancel", cancel), CommandHandler("stop", cancel)]

)











dispatcher.add_handler(contact_handler)
#dispatcher.add_handler(message_handler)


print("server started")
updater.start_polling()
updater.idle()