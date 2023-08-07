from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, ConversationHandler
from telegram.ext.filters import Filters
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from config import TOKEN

GENDER, NAME, SURNAME, PATERNAME, NUMBER, RESULT  = range(6)
MALE, FEMALE = "МУЖСКОЙ", "ЖЕНСКИЙ"
REPLY_CONTACT = "далее"

def start(update: Update, context: CallbackContext):
    # - Входящее сообщение, context - это чат в целом
    keyboard = [[MALE, FEMALE]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Что такое плейсхолдер?")
    bot_name = context.bot.name
    update.message.reply_text(f"Я бот, меня зовут{ bot_name }", reply_markup=markup)
    update.message.reply_text(f"Начинаю сбор инормации. Выбери свой пол или нажми /end, чтобы закончить разговор")
    return GENDER
    
def end(update: Update, context: CallbackContext):
    bot_name = context.bot.name
    update.message.reply_text(f"Ты выбрал конец")
    return ConversationHandler.END
    
def get_gender(update: Update, context: CallbackContext):
    gender = update.message.text
    context.user_data["gender"] = gender
    update.message.reply_text("Попрошу Вас ввести имя", reply_markup=ReplyKeyboardRemove())
    return NAME
    
    
    
def get_name(update: Update, context: CallbackContext):
    name = update.message.text
    context.user_data["name"] = name
    update.message.reply_text(f"Вы ввели имя {name}")
    update.message.reply_text(f"Введите фамилию")
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
    keyboard = [[REPLY_CONTACT]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    context.user_data["number"] = number
    print(context.user_data["number"])
    update.message.reply_text(f"Сбор информации завершен. Нажмите кнопку {REPLY_CONTACT}",  reply_markup=markup)
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
            GENDER:[MessageHandler(Filters.regex(f"^({MALE}|{FEMALE})$"), get_gender)],
            NAME:[MessageHandler(Filters.text & ~Filters.command, get_name)],
            SURNAME:[MessageHandler(Filters.text & ~Filters.command, get_surname)],
            PATERNAME:[MessageHandler(Filters.text & ~Filters.command, get_patername)],
            NUMBER:[MessageHandler(Filters.text & ~Filters.command, get_number)],
            RESULT:[MessageHandler(Filters.regex(f"^({REPLY_CONTACT})$"), get_result)]
        },
    fallbacks=[CommandHandler("end", end)]
)


dispatcher.add_handler(contact_handler)



print("server started")
updater.start_polling()
updater.idle()