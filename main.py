import functions
from functions import say_hello

# name = input("Who are you? ")

# say_hello(name)
# food = functions.fish_or_chicken()

# print(f"{name} сейчас будет есть {food}")

questions = functions.read_file("вопросы.txt")
answer = functions.read_file("ответы.txt")
functions.quiz(questions, answer)