import numpy as np
def convertAllToValue(currentHand):
    arrValue = []
    for i in currentHand:
        arrValue.append(np.ceil(i/4))
    return arrValue
def findWhereInArray(listValueCard,number):
    arrArgWhere = []
    for i in range(len(listValueCard)):
        if number == listValueCard[i]:
            arrArgWhere.append(i)
    return arrArgWhere
def handStraight(arrValue, listNumber):

    arrArg = {}
    index = 0
    totalHands = 1
    for i in range(len(listNumber)):
        arrArg[i] = findWhereInArray(arrValue, listNumber[i])
        index += 1
    for j in range(index):
        totalHands = len(arrArg[j]) * totalHands
    lstIndex = []
    for k in range(totalHands):
        lstIndex.append([])
    for i in range(index):
        start = 0
        end = 0
        for j in range(len(arrArg[i])):
            start = int(end)
            end = int(totalHands/len(arrArg[i])*(j+1))
            for k in range(start, end, 1):
                lstIndex[k].append(arrArg[i][j])
    return lstIndex

check = True
play = 3
a = 6
c = 3
while check:
    play +=1
    c += 1
    if play == 5: 
        play = 1
    if c != a:
        check = True
    else: check = False
print(play)