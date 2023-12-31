#Блок импортов
from pathlib import Path
from config import TOKEN
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update

#Блок функций
def start(update: Update, context: CallbackContext):
    # - Входящее сообщение, context - это чат в целом
    bot_name = context.bot.name
    update.message.reply_text(f"Я бот, меня зовут{ bot_name }")
    update.message.reply_text(f"""
                              Вот что я умею:
                              /hello - я поздороваюсь с тобой
                              /goodbye - я попрощаюсь с тобой
                              /help - покажу еще раз этот список команд
                              /contact - отправлю  контакт создателя бота
                              /echo - напиши команду, через пробел сообщение и я его продублирую
                              /animation - отправлю смешную анимацию
                              /music - издам звук
                              """)

def send_music(update: Update, context: CallbackContext):
    update.message.reply_audio(Path("first_bot/audio/inecraft_level_u.mp3").read_bytes())


def send_animation(update: Update, context: CallbackContext):
    update.message.reply_animation("https://media.tenor.com/_0CKYTCvTswAAAAd/%D0%B5%D0%B6-%D0%B5%D1%81%D1%82.gif")


def hello(update: Update, context: CallbackContext):
    user_name = update.effective_user.first_name
    update.message.reply_text(f" Здравствуйте!  {user_name} ")
    update.message.reply_photo("https://i.pinimg.com/originals/d1/cd/0c/d1cd0cb37b013c348d989f0cd73cc73b.jpg")
    
def goodbye(update: Update, context: CallbackContext):
    user_name = update.effective_user.first_name
    context.bot.send_message(update.effective_chat.id, f"Пока, {user_name}")

def send_contact(update: Update, context: CallbackContext):
    update.message.reply_contact("79872910575", "Марат", "Ставицкий")
   
def echo(update: Update, context: CallbackContext):
    message = context.args
    if not message:
        update.message.reply_text("ПОСЛЕ КОМАНДЫ /echo НУЖНО НАБРАТЬ СООБЩЕНИЕ ЧЕРЕЗ ПРОБЕЛ")
        return None
    message = " ".join(message)
    update.message.reply_text(message)
    print(message)
    

#Блок обработчиков(хэндлеров)
start_handler = CommandHandler("start", start)
hello_handler = CommandHandler("hello", hello)
goodbye_handler = CommandHandler("goodbye", goodbye)
help_handler = CommandHandler("help", start)
contact_handler = CommandHandler("contact", send_contact)
echo_handler = CommandHandler("echo", echo)
animation_handler = CommandHandler("animation", send_animation)
music_handler = CommandHandler("music", send_music)

#Сам бот и его зам.
updater = Updater(TOKEN)  # Ядро нашего бота
dispatcher = updater.dispatcher

# работники диспетчера
dispatcher.add_handler(start_handler)
dispatcher.add_handler(hello_handler)
dispatcher.add_handler(goodbye_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(contact_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(animation_handler)
dispatcher.add_handler(music_handler)

print("Бот запущен!")
updater.start_polling()  # Запускает обновления
updater.idle()