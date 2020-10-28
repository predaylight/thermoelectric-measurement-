import os

subDirectoryData = 'C:\\Users\\vcostanz\\Desktop\\Pyhton Projects\\test\\'
fileIDData = 'test'

completePath = os.path.join(subDirectoryData, fileIDData + '.txt')
file = open(completePath, 'a')
print(os.stat(file.buffer.name).st_size)

listData = []
header = '\t'
data = {"ciao": 54, "marco": 4865, "tury": 54}

for key in data:
    listData.append(key)
header = header.join(listData) + '\n'
file.write(header)
print(os.stat(file.buffer.name).st_size)

textData = file.readlines()
print(textData)


