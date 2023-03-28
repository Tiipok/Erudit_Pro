import  time
print(time.ctime())
with open('logs.txt', 'w') as f:
    f.write(time.ctime())
    f.write('\n')
