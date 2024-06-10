import random

def Average(lst): 
    return sum(lst) / len(lst)
    
l1 = [random.randint(0, 1000) for i in range(0, 100)]
    
for i in range(0, len(l1)):
    for j in range(i+1, len(l1)):
        if l1[i] >= l1[j]:
            l1[i], l1[j] = l1[j],l1[i]
            
avg_odd_list = []
avg_even_list = []
 
for i in range(0, len(l1)):
    if l1[i] % 2 != 0 :
        avg_odd_list.append(l1[i])
    else:
        avg_even_list.append(l1[i])

print("Average value for the even list is {0}".format(Average(avg_even_list)))
print("Average value for the odd list is {0}".format(Average(avg_odd_list)))
