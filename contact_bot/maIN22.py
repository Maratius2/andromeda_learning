from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, ConversationHandler
from telegram.ext.filters import Filters
from telegram import Update
from config import TOKEN

NAME, SURNAME, PATERNAME, NUMBER, RESULT = range(5)

def start(update: Update, context: CallbackContext):
    # - Входящее сообщение, context - это чат в целом
    bot_name = context.bot.name
    update.message.reply_text(f"Я бот, меня зовут{ bot_name }")
    update.message.reply_text(f"Начинаю сбор инормации. Назови своё имя")
    return NAME
    
def end(update: Update, context: CallbackContext):
    bot_name = context.bot.name
    update.message.reply_text(f"Ты выбрал конец")
    
def get_name(update: Update, context: CallbackContext):
    name = update.message.text
    context.user_data["name"] = name
    update.message.reply_text(f"Вы ввели имя {name}")
    update.message.reply_text(f"Введите фмилию")
    return SURNAME
    
def get_surname(update: Update, context: CallbackContext):
    name = context.user_data["name"]
    surname = update.message.text
    context.user_data["surname"] = surname
    update.message.reply_text(f"""Вас зовут {name} {surname},
                              Введите отчество""")
    return PATERNAME

def get_patername(update: Update, context: CallbackContext):
    patername = update.message.text
    context.user_data["patername"] = patername
    update.message.reply_text(f"Введите номер телефона")
    return NUMBER
    
def get_number(update: Update, context: CallbackContext):
    number = update.message.text
    if not number.isdigit():
        update.message.reply_text(f"Введите НОМЕР телефона")
        return None
    context.user_data["number"] = number
    print(context.user_data["number"])
    update.message.reply_text(f"Сбор информации завершен. Отправьте какой-нибудь текст для продолжения")
    return RESULT

def get_result(update: Update, context: CallbackContext):
    name = context.user_data["name"]
    surname = context.user_data["surname"]
    patername =  context.user_data["patername"]
    number = context.user_data["number"]
    update.message.reply_contact(number, f"{name} {patername}",surname)
    return ConversationHandler.END



#Сам бот и его зам.
updater = Updater(TOKEN)
dispatcher = updater.dispatcher


contact_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
            NAME:[MessageHandler(Filters.text, get_name)],
            SURNAME:[MessageHandler(Filters.text, get_surname)],
            PATERNAME:[MessageHandler(Filters.text, get_patername)],
            NUMBER:[MessageHandler(Filters.text, get_number)],
            RESULT:[MessageHandler(Filters.text, get_result)]
        },
    fallbacks=[CommandHandler("end", end)]
)


dispatcher.add_handler(contact_handler)



print("server started")
updater.start_polling()
updater.idle()