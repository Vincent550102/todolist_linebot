mess = "iajsdi aisjdoiad ajdoisa"
mess = mess.split(" ")
resul = str()
[resul += i for i in mess if i != mess[0]]
print(resul)