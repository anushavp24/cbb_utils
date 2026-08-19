import sys

current_row = 0
max_row = 0
current_max = None

for line in sys.stdin:
    current_row += 1
    l_items = line.strip().split("\t")
    current_col=0

    for item in l_items:
        current_col +=1
        if item != '' and item != "\n":
            num = float(item)

            if current_max is None or num > current_max:
                current_max = num
                max_row = current_row
                max_col = current_col

print("Max:", current_max)
print("max row:", max_row)
print("max col:", max_col)

'''float_num.append(num)
        current_max = float_num [0] 
     
    for item in float_num:'''


'''current_min= num
for item in num:
    if (item < current_min):
        current_min = item
print ("Min:", current_min)'''



'''current_max= digits [0]
for item in digits:
    if (item > current_max):
        current_max = item
print ("Max:", current_max)
current_min= digits [0]
for item in digits:
    if (item < current_min):
        current_min = item
print ("Min:", current_min)'''
