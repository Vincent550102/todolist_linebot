mess = "dasd asda asa ad"
mess = mess.split(' ')

result = str()
for part in mess:
    result += part if part != mess[0] else ''
print(result)