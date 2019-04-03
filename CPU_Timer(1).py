import time

file = open("dictionary.txt")
words = file.read().splitlines()
file.close()

str1 = "abcdefghi"
list1 = []
for i in range(10000000):
    list1.append(str1)
for i in range(10000000):
    list1.pop()
d1 = {}
for i in range(10000000):
  d1[str1 + str(i)] = str1
for i in range(10000000):
  del d1[str1 + str(i)]

print("Time taken (secs) = ", time.process_time())