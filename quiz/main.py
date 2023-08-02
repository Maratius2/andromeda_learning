import quiz.functions as functions
from quiz.functions import say_hello

# name = input("Who are you? ")

# say_hello(name)
# food = functions.fish_or_chicken()

# print(f"{name} сейчас будет есть {food}")
print()
questions = functions.read_file("quiz/вопросы.txt")
answer = functions.read_file("quiz/ответы.txt")
functions.quiz(questions, answer)