#1
#i think it will print hello 4 times
for i in range(4):
        print("hello")
#it printed hello 4 times, because it counted from 0-3 as the range ends before 4

#2
#it will count from 0 to 3
count = 0
while count < 3:
        count = count+ 1
print(count)
#it printed 3 because the loop ran before the pirnt command

#3
#I think it will print pass when the score is above 70, print great when the score is above
#80 and print fail when the score is below 70
score = 85
if score > 70:
        print("pass")
elif score > 80:
        print("great")
else:
        print("Fail")
#it printed pass because the first value was true and it ended before it ran the others

#4
#i think it will print integers goin gup from one until it shuts itself off
x = 5
while x > 0:
    print(x)
    x += 1
#it counted endlessly, because there was no stop function to prevent the loop from cycling

#5
#I think the outcome will be 11 12 21 22
for i in range(2):
    for j in range(2):
        print(i,j)
#it printed 00 01 10 11 because the range went from 0-1 because 2 is not included in the range