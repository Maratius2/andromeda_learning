import time
first_name = input("Как тебя зовут?: ")
time.sleep(0.8)
famil = input("Какая у тебя фамилия?: ")
print(f" Тебя зовут: {first_name} {famil}")

age = input("Твой возраст: ")
time.sleep(1)
age = int(age)
if age>12 and age <65:
    time.sleep(1)
    print(f" Отлично! Ты можешь войти в игру {first_name} {famil} !")
else:
    time.sleep(1)
    print(f" Ты не подходишь по возрасту {first_name} {famil}")
    time.sleep(1)
    exit()
    
questions = [
    "Висит груша нельзя скушать? - ",
    "Столица Норвегии? - ",
    "Относятся ли дельфины к млекопитающим? - ",
    "В каком году основали Российскую Империю? - ",
    "Из какого дерева делают спички? - "
    ]

answers = [
    "лампочка",
    "осло",
    "да",
    "в 1721",
    "из осины"
]


def quiz(questions, answers):
    for number,que in enumerate(questions):
        answer = answers[number]
        user_ans = ""
        while user_ans!= answer:
            user_ans = input(f" {number + 1}, {que}").lower()
            if user_ans == answer:
                print("Молодец! Правильно ответил!")
            else:
                print("Неправильно! Попробуй еще раз!")

quiz(questions=questions, answers=answers)
