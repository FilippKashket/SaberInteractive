import json

with open('test1.txt', 'w') as f:
    for i in range(100000000):
        res = '{"level": "DEBUG", "message":' + str(i) + '}\n'
        f.write(res)
