from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, ConversationHandler
from telegram.ext.filters import Filters
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from config import TOKEN
import pymorphy2


BEGIN, GAME, END = range(3)
START = "НАЧАТЬ"
morph = pymorphy2.MorphAnalyzer()
CHARATERS = {
    "кот" : "https://s1.1zoom.ru/big3/764/357677-admin.jpg",
    "кошка" : "https://s1.1zoom.ru/big3/764/357677-admin.jpg",
    "собака" : "https://w.forfun.com/fetch/d0/d05bccd02c1478d21ac7e4778f69d5b3.jpeg"
}


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
    if tag.tag.animacy != "anim": 
        update.message.reply_text(f"Звали мы {tag.normal_form}: никого не дозвались")
        return None
    nomn = tag.inflect({"nomn"}).word # слово в иминительном падеже
    accs = tag.inflect({"accs"}).word # слово в винительном падеже
    if nomn in CHARATERS:
        update.message.reply_photo(CHARATERS[nomn])
    heroes = context.user_data["heroes"]
    heroes[0].insert(0, nomn)
    heroes.insert(0, [accs])
    result =""
    for nom, ac in heroes[1:]:
        result += f"{nom} - за {ac}. ".title()
    update.message.reply_text(result)
    if "мыш" in nomn:
       return victory(update, context)
    update.message.reply_text("Тянут - потянуть - вытянуть не могут")
   
   
def victory(update: Update, context: CallbackContext):
    update.message.reply_photo("https://geroickazok.ru/wp-content/uploads/2021/11/i-1.jpg")
    update.message.reply_text(f"Вытащили репку наконец. Вот и сказочке конец, а кто слушал молодец! Хотите сыграть еще напишите /start")
    return ConversationHandler.END
   
    
    
    
    
    
    
    
def end(update: Update, context: CallbackContext):
    bot_name = context.bot.name
    update.message.reply_text(f"Ты выбрал конец")
    return ConversationHandler.END




game_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        BEGIN:[MessageHandler(Filters.regex(f"^({START})"), begin)],
        GAME:[MessageHandler(Filters.text & ~Filters.command, game)],
        END:[MessageHandler(Filters.text & ~Filters.command, victory)]
    },
    fallbacks=[CommandHandler("end", end)]
)




updater = Updater(TOKEN)  # Ядро нашего бота
dispatcher = updater.dispatcher

dispatcher.add_handler(game_handler)

print("server started")
updater.start_polling()
updater.idle()
