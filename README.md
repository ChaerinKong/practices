# practices

#GPA Calculator
semester = []
while True:
    score = input('your score:')
    if score == 'done':
        break
    load = input('your load:')
    semester.append((score, load))

total = 0
for (x,y) in semester:
    total += float(y)

average = list()
for (a,b) in semester:
    val = float(a)*float(b)/float(total)
    average.append(val)

j = 0
for i in average:
    j += i
print(j)
