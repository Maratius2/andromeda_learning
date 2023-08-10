import csv
from telegram.ext import Updater, CallbackContext, ConversationHandler
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from constans import *
from stickersi import *
import random


def read_csv():
    with open("victorina/database.csv", encoding="utf-8") as file:
        read_data = list(csv.reader(file, delimiter="|"))
        return read_data


def write_to_csv(row):
    with open("victorina/database.csv",mode="a", encoding="utf-8") as file:
        writter = csv.writer(file, delimiter="|", lineterminator="\n")
        writter.writerow(row)
        
def start(update:Update, context:CallbackContext):
    keyboard = [[GO]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_sticker(START_STIC[1])
    context.bot.send_message(update.effective_chat.id, "Добро пожаловать в викторину. Отвечайна вопросы, выбирая один из вариантов ответа ")
    update.message.reply_text(f"Для начала нажми на {GO}", reply_markup=markup)
    
    questions_list = read_csv()
    random.shuffle(questions_list)
    length = QUESTIONS_ON_ROUND if len(questions_list) > QUESTIONS_ON_ROUND else len(questions_list)
    
    questions_list = questions_list[:length]
    context.user_data["questions"] = questions_list
    context.user_data["index"] = 0
    return GAME
    
    return GAME

def cancel(update:Updater, context:CallbackContext):
    update.message.reply_sticker(START_STIC[0])
    update.message.reply_text("Спасибо за участие!")
    update.message.reply_text("Нажми на /start, чтобы начать заново")
    return ConversationHandler.END
    
    
def game(update:Updater, context:CallbackContext):
    questions_list = context.user_data["questions"]    
    index = context.user_data["index"] 
    answers = questions_list[index] #ответы
    question = answers.pop(0) #вопросы
    update.message.reply_text(question)
    