
def say_hello(name:str):
    """
    Говорит Hello, обращаясь по имени.
    """
    print(f"Hello, {name}")
    
def fish_or_chicken():
    """
    
    """
    answer = input("Хочешь курицу или рыбу?")
    need_answers = ["курицу", "рыбу"]
    if answer not in need_answers:
        print ("Такого нет в меню")
        return fish_or_chicken()
    print(f"Вы выбрали {answer}")
    return answer
def read_file(filename:str):
    with open(filename, encoding= "utf-8") as file:
        data_list = file.read().split("\n")
    return data_list

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
