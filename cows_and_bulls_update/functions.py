from telegram.ext import CallbackContext, ConversationHandler

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
import random
from constans import *
from stickers import *
import time
import rsa

def start(update: Update, context: CallbackContext):
    keyboard = [[GO]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    bot_name = context.bot.name
    update.message.reply_sticker(HELLO_STIC[0])
    update.message.reply_text("""Привет! Ты зашел в бота который играет с тобой в быки и коровы. ПРАВИЛА: компьютер загадывает слово из трех букв. Вы должны его отгадать. Если вы угадали букву в слове, которая стоит на том же самом месте буквы в слове, то бот говорит "в вашем слове 1 бык" и наоборот . Чтобы выиграть вы должны отгадать слово тобишь - в вашем слове должно быть 3 быка. УДАЧИ!!! (если захотите сдаться, можете в любое время игры нажать кнопку CANCEL) """, reply_markup=markup)
    return LEVEL

    
def choose_level(update: Update, context: CallbackContext): 
    with open(f"cows_and_bulls_update/ssh/key", encoding="utf-8") as file:
        private_key = file.read().split(", ")
        private_key = [int(number) for number in private_key]
        private_key = rsa.PrivateKey(*private_key)
    with open(f"cows_and_bulls_update/coins.txt", "rb") as file:
        money = file.read()
        message = rsa.decrypt(money, private_key)
        money = message.decode("utf-8")
    context.user_data["money"] = int(money)
    context.user_data["attemps"] = 0
    update.message.reply_text(f"У вас {money} монет,  цена уровня easy - бесплатно, цена уровня medium - {MEDIUM_PRICE}, цена уровня hard {HARD_PRICE}. Награда за слово в уровне easy - 5 монет в medium - 10, в hard - 20")
    keyboard = [[EASY], [MEDIUM], [HARD]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Выбирай сложность уровня который тебе по силам")
    update.message.reply_text("Выбери уровень сложности", reply_markup=markup)
    return FIRST



def cancel(update: Update, context: CallbackContext):
    if "секрет" in context.user_data:
        secret_word = context.user_data["секрет"]
        update.message.reply_sticker(GOODBYE_STIC)
        update.message.reply_text(f"Загаданное слово было {secret_word}")
        change_money(context,plus=False)
    else:
        update.message.reply_text("Если захотите сыграть еще - введите команду /start",reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def begin(update: Update, context: CallbackContext):
    money = context.user_data["money"]
    difficulty =  update.message.text
    if money < MEDIUM_PRICE and difficulty == MEDIUM:
        difficulty = EASY
        update.message.reply_photo("https://yt3.googleusercontent.com/ytc/AGIKgqOeW60adm7IzKVmTmn1OiSC-D_aeJJakFi5NlKi=s900-c-k-c0x00ffffff-no-rj")
        update.message.reply_text("У вас недостаточно монет. Вы автоматически переключены на уровень easy")
    elif money < HARD_PRICE and difficulty == HARD:
        difficulty = EASY
        update.message.reply_photo("https://yt3.googleusercontent.com/ytc/AGIKgqOeW60adm7IzKVmTmn1OiSC-D_aeJJakFi5NlKi=s900-c-k-c0x00ffffff-no-rj")
        update.message.reply_text("У вас недостаточно монет. Вы автоматически переключены на уровень easy")
    elif difficulty == MEDIUM:
        money -= MEDIUM_PRICE
        update.message.reply_text(f"Вы приобрели уровень medium за {MEDIUM_PRICE}")
    elif difficulty == HARD:
        money -= HARD_PRICE
        update.message.reply_text(f"Вы приобрели уровень hard за {HARD_PRICE}")
    count = LEVELS[difficulty]    
    context.user_data["difficulty"] = count
    
    
    with open(f"cows_and_bulls_update/{difficulty}_words{count}.txt", encoding="utf-8") as file:
       words = file.read().split("\n")
    secret_word = random.choice(words).strip()
    context.user_data["секрет"] = secret_word #записываем
    update.message.reply_text(f"Подождите.....")
    time.sleep(0.7)
    update.message.reply_text(f"Слово загадано. Можете начать отгадывать слово из {count} букв", reply_markup=KEYPAD)
    return CLUE
    



        
def game(update: Update, context: CallbackContext):
    user_name = update._effective_user.first_name
    my_word = update.message.text
    if my_word == BALANCE:
        money = context.user_data["money"]
        update.message.reply_text(f"баланс - {money} монет")
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
    word_cow = inclide_words(COW, cows)
    word_bull = inclide_words(BULL, bulls)
    update.message.reply_text(f"В вашем слове {bulls} {word_bull}  и {cows} {word_cow}", reply_markup=KEYPAD)
    if bulls == len(secret_word):
        update.message.reply_photo("https://w7.pngwing.com/pngs/815/457/png-transparent-league-of-legends-victory-league-of-legends-riven-command-conquer-generals-age-of-empires-video-game-victory-miscellaneous-blue-game.png", 
                                   reply_markup=ReplyKeyboardRemove())
        context.user_data["секрет"]
        change_money(context,plus=True)
        return ConversationHandler.END
        
        
        
def change_money(context, plus = False): #Если включен, то прибавляет, включен - отнимаем
    difficulty = context.user_data["difficulty"]
    money = context.user_data["money"]   
    if plus == False: #если мы вычитаем
        money *= -1 #делаем число отрицательным
    money += int(difficulty) +2 #прибавляем или отнимаем монеты
    with open(f"cows_and_bulls_update/ssh/key.pub", encoding="utf-8") as file:
        public_key = file.read().split(", ")
        public_key = [int(number) for number in public_key]
        public_key = rsa.PublicKey(*public_key)
    with open(f"cows_and_bulls_update/coins.txt", mode ="wb") as file:
        message = f"{money}".encode('utf8')
        crypto = rsa.encrypt(message, public_key)
        file.write(crypto)
        
def inclide_words(animal:pymorphy2.analyzer.Parse, count:int):
    
    if count == 1:
        animal = animal.inflect({"nomn"}).word
    elif count in [2,3,4]:
        animal = animal.inflect({"gent"}).word
    else: 
        animal = animal.inflect({"gent", "plur"}).word
    return animal
 
