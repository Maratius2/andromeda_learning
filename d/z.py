import time
 
num = list(range(10))
nextnum = 1
for i in num:
    sum = nextnum + i
    print(" текущее число {i} следующее число {nextnum} сумма - " (str(sum)) )
    nextnum = i