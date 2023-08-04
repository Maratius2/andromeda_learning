#Блок импортов
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler
from telegram.ext.filters import Filters
from telegram import Update
from config import TOKEN

def get_factorial(update: Update, context: CallbackContext):
    num = context.args
    if not num or len(num) != 1 or not num[0].isdigit():
        update.message.reply_text("Введите одно число")
        return None
    num = int(num.pop())
    factorial = 1
    factorial_list = []
    for i in range(1, num+1):
        factorial *= i
        factorial_list.append(factorial)
        update.message.replay_text(f"{factorial_list}")




def start(update: Update, context: CallbackContext):
    bot_name = context.bot.name
    update.message.reply_text(f"Я бот, меня зовут{ bot_name }")
    update.message.reply_text(f"""
                              Вот что я умею:
                              /plus - сложение
                              /minus - вычитание
                              /multiply - умножение
                              /divide - деление
                              """)





def make_eval(update: Update, context: CallbackContext, message:list):
    if not message or len(message) !=2:
        update.message.reply_text("Введите ДВА числа через пробел после команды")
        return None
    num1, num2 = message
    if not num1.isdigit()or not num2.isdigit():
        update.message.reply_text("Вводить можно только числа")
        return None
    num1, num2 = int(num1), int(num2)
    return num1, num2
    
    
    
def plus(update: Update, context: CallbackContext):
    message = context.args
    if make_eval(update, context, message) is not None:
        num1, num2 = make_eval(update, context, message)
        result = num1 + num2
        update.message.reply_text(f" Это будет {result}")
    
    
def minus(update: Update, context: CallbackContext):
    message = context.args
    if make_eval(update, context, message) is not None:
        num1, num2 = make_eval(update, context, message)
        result = num1 - num2
        update.message.reply_text(f" Это будет {result}")
    
def multiply(update: Update, context: CallbackContext):
    message = context.args
    if make_eval(update, context, message) is not None:
        num1, num2 = make_eval(update, context, message)
        result = num1 * num2
        update.message.reply_text(f" Это будет {result}")

def divide(update: Update, context: CallbackContext):
    message = context.args
    if make_eval(update, context, message) is not None:
        num1, num2 = make_eval(update, context, message)
        if num2 == 0:
            update.message.reply_text("На ноль делить нельзя")
            return None
        result = num1/num2
        update.message.reply_text(f" Это будет {result}")

        
        
def gateway(update: Update, context: CallbackContext):
    user_name = update._effective_user.first_name
    message = update.message.text
    if message == "привет":
        update.message.reply_text(f"Привет, {user_name}")
    elif message == "пока":
        update.message.reply_text(f"Пока, {user_name}")
    elif "желт" in message:
        update.message.reply_text(f"Желтый - это мой любимый цвет, {user_name}")
    elif message == "Марат Ставицкий":
        update.message.reply_contact("79872910575", "Марат", "Ставицкий")
        update.message.reply_text(f"{message} - это мой создатель ")
    
        

        
        
        
        
    
    
plus_handler = CommandHandler("plus", plus)
minus_handler = CommandHandler("minus", minus)
divide_handler = CommandHandler("divide", divide)
multiply_handler = CommandHandler("multiply", multiply)
message_handler = MessageHandler(Filters.text, gateway)

#Сам бот и его зам.
updater = Updater(TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(plus_handler)
dispatcher.add_handler(minus_handler)
dispatcher.add_handler(divide_handler)
dispatcher.add_handler(multiply_handler)
dispatcher.add_handler(message_handler)


print("server started")
updater.start_polling()
updater.idle()