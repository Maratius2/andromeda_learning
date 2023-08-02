import time

def calculator (a,b):
    summa = a + b
    res = a*b
    if res >= 1000:
        print (res)
    else:
        print(summa)
        
print("Добро пожаловать в калькулятор")      
a = int(input("Введите число:"))  
b = int(input("Введите число:"))
print ("Подождите...........")
time.sleep(3)
calculator(a,b)










