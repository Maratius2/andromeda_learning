from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler
from telegram.ext.filters import Filters
from telegram import Update
from config import TOKEN
from anecAPI import anecAPI


def start(update: Update, context: CallbackContext):
    # - Входящее сообщение, context - это чат в целом
    bot_name = context.bot.name
    update.message.reply_text(f"Я бот, меня зовут{ bot_name }")
    update.message.reply_text(f"""
                              Вот что я умею:
                              /help - список команд
                              /rus - современный анекдот (Русский)
                              /usr - старый анекдот (Советский)
                              /rand - рандомный анекдот (Российский/Советский)
                              """)
    
def rus(update: Update, context: CallbackContext):
    update.message.reply_text(anecAPI.modern_joke())

def usr(update: Update, context: CallbackContext):
    update.message.reply_text(anecAPI.soviet_joke())

def rand(update: Update, context: CallbackContext):
   update.message.reply_text(anecAPI.random_joke())




rand_handler = CommandHandler("rand", rand)
usr_handler = CommandHandler("usr", usr)
rus_handler = CommandHandler("rus", rus)
start_handler = CommandHandler("start", start)
help_handler = CommandHandler("help", start)





#Сам бот и его зам.
updater = Updater(TOKEN)  # Ядро нашего бота
dispatcher = updater.dispatcher


dispatcher.add_handler(rand_handler)
dispatcher.add_handler(usr_handler)
dispatcher.add_handler(rus_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)





print("Бот запущен!")
updater.start_polling()  # Запускает обновления
updater.idle()