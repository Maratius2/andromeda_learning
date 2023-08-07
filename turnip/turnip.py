from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, ConversationHandler
from telegram.ext.filters import Filters
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from config import TOKEN
import pymorphy2


BEGIN, GAME = range(2)
START = "НАЧАТЬ"
morph = pymorphy2.MorphAnalyzer()


def start(update: Update, context: CallbackContext):
    # - Входящее сообщение, context - это чат в целом
    keyboard = [[START]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text("Хорошо. Давай поиграем. Ты любишь придумывать сказки? Я – очень люблю. Ты знаешь сказку, как посадил дед репку?А кто помогал её тянуть?", reply_markup=markup)
    heroes =[["дедку"], ["дедка", "репку"]]
    context.user_data["heroes"] = heroes
    return BEGIN
    
    
def begin(update: Update, context: CallbackContext):
    update.message.reply_text("Посадил дед репку. Выросла репка большая-пребольшая. Тянет-потянет, а вытянуть не может. Кого позвал дед?", reply_markup=ReplyKeyboardRemove())
    return GAME
    
def game(update: Update, context: CallbackContext):
    word = update.message.text
    tag = morph.parse(word)[0]
    nomn = tag.inflect({"nomn"}).word # слово в иминительном падеже
    accs = tag.inflect({"accs"}).word # слово в винительном падеже
    heroes = context.user_data["heroes"]
    heroes[0].insert(0, nomn)
    heroes.insert(0, [accs])
    result =""
    for nom, ac in heroes[1:]:
        result += f"{nom} - за {ac}. ".title()
    update.message.reply_text(result)
    
    
    
    
    
    
    
def end(update: Update, context: CallbackContext):
    bot_name = context.bot.name
    update.message.reply_text(f"Ты выбрал конец")
    return ConversationHandler.END




game_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        BEGIN:[MessageHandler(Filters.regex(f"^({START})"), begin)],
        GAME:[MessageHandler(Filters.text & ~Filters.command, game)]
    },
    fallbacks=[CommandHandler("end", end)]
)




updater = Updater(TOKEN)  # Ядро нашего бота
dispatcher = updater.dispatcher

dispatcher.add_handler(game_handler)

print("server started")
updater.start_polling()
updater.idle()
