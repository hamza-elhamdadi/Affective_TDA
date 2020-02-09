import os

filesindir = os.listdir('../Data')

for i in range(len(filesindir)):
    for j in range(i+1,len(filesindir)):
        if filesindir[j][0:3] == '111' and filesindir[i][0:3] == '065':
            print(filesindir[i][0:3]+','+filesindir[j][0:3])