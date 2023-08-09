from telegram import  ReplyKeyboardMarkup
import pymorphy2

GO = "НАЧАТЬ"
LEVEL, FIRST, CLUE = range(3)
morph = pymorphy2.MorphAnalyzer()
COW = morph.parse("корова")[0]
BULL = morph.parse("бык")[0]



EASY, MEDIUM, HARD, CANCEL, BALANCE = "easy", "medium", "hard","/cancel", "Баланс"
LEVELS = {
    EASY: 3,
    MEDIUM: 4,
    HARD: 5
}



KEYPAD = ReplyKeyboardMarkup([[CANCEL],[BALANCE]],
                            resize_keyboard=True,
                            input_field_placeholder="Чтобы сдаться нажми на /cancel. Нажми на Баланс, если хочешь увидеть баланс монет")
       
MEDIUM_PRICE = 50
HARD_PRICE = 100