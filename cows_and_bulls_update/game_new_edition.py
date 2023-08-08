from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, ConversationHandler
from telegram.ext.filters import Filters
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from config import TOKEN
import random
from constans import *
import time


def start(update: Update, context: CallbackContext):
    keyboard = [[GO]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    bot_name = context.bot.name
    update.message.reply_text("""
                                Привет! Ты зашел в бота который играет с тобой 
                                в быки и коровы. 
                                ПРАВИЛА: компьютер загадывает слово из трех букв.
                                Вы должны его отгадать. Если вы угадали букву в слове, которая стоит 
                                на том же самом месте буквы в слове, то бот говорит "в вашем слове 1 бык" и 
                                наоборот . Чтобы выиграть вы должны отгадать слово тобишь - в вашем слове должно
                                быть 3 быка.
                                УДАЧИ!!! 
                                (если захотите сдаться, можете в любое время игры нажать кнопку CANCEL)
                                  """, reply_markup=markup)
    return LEVEL

    
def choose_level(update: Update, context: CallbackContext):
    keyboard = [[EASY], [MEDIUM], [HARD]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Выбирай сложность уровня который тебе по силам")
    update.message.reply_text("Выбери уровень сложности", reply_markup=markup)
    return FIRST



def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("Вы хотите закончить? Нажмите кнопку CANCEL. Если захотите сыграть еще - введите команду /start")
    return ConversationHandler.END


def begin(update: Update, context: CallbackContext):
    difficulty =  update.message.text
    count = LEVELS[difficulty]
    with open(f"cows_and_bulls_update/{difficulty}_words{count}.txt", encoding="utf-8") as file:
       words = file.read().split("\n")
    secret_word = random.choice(words)
    context.user_data["секрет"] = secret_word #записываем
    update.message.reply_text(f"Подождите.....")
    time.sleep(0.7)
    update.message.reply_text(f"Слово загадано. Можете начать отгадывать слово из {count} букв")
    return CLUE
    



        
def game(update: Update, context: CallbackContext):
    user_name = update._effective_user.first_name
    my_word = update.message.text
    secret_word = context.user_data["секрет"]  #достаем
    if len(secret_word) != len(my_word):
        update.message.reply_text(f"Количество букв должно быть {len(secret_word)}")   
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
        
        
#message_handler = MessageHandler(Filters.text & ~Filters.command, gateway)

#Сам бот и его зам.
updater = Updater(TOKEN)
dispatcher = updater.dispatcher

contact_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        LEVEL:[MessageHandler(Filters.regex(f"^({GO})$"), choose_level)],
        FIRST:[MessageHandler(Filters.regex(f"^({EASY}|{MEDIUM}|{HARD})$"), begin)],
        CLUE:[MessageHandler(Filters.text & ~Filters.command(f"({CLUE})$"), game)]
        
        },
    fallbacks=[CommandHandler("cancel", cancel), CommandHandler("stop", cancel)]

)











dispatcher.add_handler(contact_handler)
#dispatcher.add_handler(message_handler)


print("server started")
updater.start_polling()
updater.idle()