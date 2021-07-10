import numpy as np 
import pickle
two = 0
three = 0
four = 0
five = 0
six = 0
seven =0
eight = 0
nine = 0
ten = 0
eleven = 0
twelve = 0
thirteen = 0
twoCardIndices = np.zeros((13,13),dtype=int)
inverseTwoCardIndices = np.zeros((33,2),dtype=int)

for c_1 in range(12): # 0->11
    n_1 = min(c_1+4,13)
    for c_2 in range(c_1+1,n_1): # 0->12
        twoCardIndices[c_1,c_2] = two    
        inverseTwoCardIndices[two,:] = [c_1,c_2]
        two = two+1 

threeCardIndices = np.zeros((13,13,13),dtype=int)
inverseThreeCardIndices = np.zeros((246,3),dtype=int)

for c_1 in range(11): 
    n_1 = min(c_1+8,12)
    for c_2 in range(c_1+1,n_1): # 0->12
        n_2 = min(c_2+8,13)
        for c_3 in range(c_2+1,n_2):
            threeCardIndices[c_1,c_2,c_3] = three    
            inverseThreeCardIndices[three,:] = [c_1,c_2,c_3]
            three = three+1

fourCardIndices = np.zeros((13,13,13,13),dtype=int)
inverseFourCardIndices = np.zeros((670,4),dtype=int)
for c_1 in range(10): 
    n_1 = min(c_1+8,11)
    for c_2 in range(c_1+1,n_1): # 0->12
        n_2 = min(c_2+8,12)
        for c_3 in range(c_2+1,n_2):
            n_3 = min(c_3+8,13)
            for c_4 in range(c_3+1,n_3):
                fourCardIndices[c_1,c_2,c_3,c_4] = four    
                inverseFourCardIndices[four,:] = [c_1,c_2,c_3,c_4]
                four = four + 1

fiveCardIndices = np.zeros((13,13,13,13,13),dtype=int)
inverseFiveCardIndices = np.zeros((1263,5),dtype=int)
for c_1 in range(9): # 0->11
    n_1 = min(c_1+8,10)
    for c_2 in range(c_1+1,n_1): # 0->12
        n_2 = min(c_2+8,11)
        for c_3 in range(c_2+1,n_2):
            n_3 = min(c_3+8,12)
            for c_4 in range(c_3+1,n_3):
                n_4 = min(c_4+8,13)
                for c_5 in range(c_4+1,n_4):
                    fiveCardIndices[c_1,c_2,c_3,c_4,c_5] = five    
                    inverseFiveCardIndices[five,:] = [c_1,c_2,c_3,c_4,c_5]
                    five += 1
sixCardIndices = np.zeros((13,13,13,13,13,13),dtype=int)
inverseSixCardIndices = np.zeros((1711,6),dtype=int)
for c_1 in range(8): # 0->11
    n_1 = min(c_1+8,9)
    for c_2 in range(c_1+1,n_1): # 0->12
        n_2 = min(c_2+8,10)
        for c_3 in range(c_2+1,n_2):
            n_3 = min(c_3+8,11)
            for c_4 in range(c_3+1,n_3):
                n_4 = min(c_4+8,12)
                for c_5 in range(c_4+1,n_4):
                    n_5 = min(c_5+8,13)
                    for c_6 in range(c_5+1,n_5):
                        sixCardIndices[c_1,c_2,c_3,c_4,c_5,c_6] = six    
                        inverseSixCardIndices[six,:] = [c_1,c_2,c_3,c_4,c_5,c_6]
                        six += 1
sevenCardIndices_ = {}
for c_1 in range(7): # 0->11
    n_1 = min(c_1+8,8)
    for c_2 in range(c_1+1,n_1): # 0->12
        n_2 = min(c_2+8,9)
        for c_3 in range(c_2+1,n_2):
            n_3 = min(c_3+8,10)
            for c_4 in range(c_3+1,n_3):
                n_4 = min(c_4+8,11)
                for c_5 in range(c_4+1,n_4):
                    n_5 = min(c_5+8,12)
                    for c_6 in range(c_5+1,n_5):
                        n_6 = min(c_6+8,13)
                        for c_7 in range(c_6+1,n_6):
                            sevenCardIndices_[seven] =[c_1,c_2,c_3,c_4,c_5,c_6,c_7]    
                            seven += 1
sevenCardIndices = list(sevenCardIndices_.values())
inverseSevenCardIndices = list(sevenCardIndices_.keys())

eightCardIndices_ = {}
for c_1 in range(5): # 0->11
    n_1 = min(c_1+8,7)
    for c_2 in range(c_1+1,n_1): # 0->12
        n_2 = min(c_2+8,8)
        for c_3 in range(c_2+1,n_2):
            n_3 = min(c_3+8,9)
            for c_4 in range(c_3+1,n_3):
                n_4 = min(c_4+8,10)
                for c_5 in range(c_4+1,n_4):
                    n_5 = min(c_5+8,11)
                    for c_6 in range(c_5+1,n_5):
                        n_6 = min(c_6+8,12)
                        for c_7 in range(c_6+1,n_6):
                            n_7 = min(c_7+8,13)
                            for c_8 in range(c_7+1,n_7):
                                eightCardIndices_[eight]    = [c_1,c_2,c_3,c_4,c_5,c_6,c_7,c_8]
                                eight += 1
eightCardIndices = list(eightCardIndices_.values())
inverseEightCardIndices = list(eightCardIndices_.keys())



nineCardIndices_ = {}
for c_1 in range(5): # 0->11
    n_1 = min(c_1+8,7)
    for c_2 in range(c_1+1,n_1): # 0->12
        n_2 = min(c_2+8,7)
        for c_3 in range(c_2+1,n_2):
            n_3 = min(c_3+8,8)
            for c_4 in range(c_3+1,n_3):
                n_4 = min(c_4+8,9)
                for c_5 in range(c_4+1,n_4):
                    n_5 = min(c_5+8,10)
                    for c_6 in range(c_5+1,n_5):
                        n_6 = min(c_6+8,11)
                        for c_7 in range(c_6+1,n_6):
                            n_7 = min(c_7+8,12)
                            for c_8 in range(c_7+1,n_7):
                                n_8 = min(c_8+8,13)
                                for c_9 in range(c_8+1,n_8):
                                    nineCardIndices_[nine]=[c_1,c_2,c_3,c_4,c_5,c_6,c_7,c_8,c_9]
                                    nine += 1
nineCardIndices = list(nineCardIndices_.values())
inverseNineCardIndices = list(nineCardIndices_.keys())

tenCardIndices_ = {}
for c_1 in range(4): # 0->11
    n_1 = min(c_1+8,5)
    for c_2 in range(c_1+1,n_1): # 0->12
        n_2 = min(c_2+8,6)
        for c_3 in range(c_2+1,n_2):
            n_3 = min(c_3+8,7)
            for c_4 in range(c_3+1,n_3):
                n_4 = min(c_4+8,8)
                for c_5 in range(c_4+1,n_4):
                    n_5 = min(c_5+8,9)
                    for c_6 in range(c_5+1,n_5):
                        n_6 = min(c_6+8,10)
                        for c_7 in range(c_6+1,n_6):
                            n_7 = min(c_7+8,11)
                            for c_8 in range(c_7+1,n_7):
                                n_8 = min(c_8+8,12)
                                for c_9 in range(c_8+1,n_8):
                                    n_9 = min(c_9+8,13)
                                    for c_10 in range(c_9+1,n_9):
                                        tenCardIndices_[ten]=[c_1,c_2,c_3,c_4,c_5,c_6,c_7,c_8,c_9,c_10]
                                        ten += 1
tenCardIndices = list(tenCardIndices_.values())
inverseTenCardIndices = list(tenCardIndices_.keys())

elevenCardIndices_ = {}
for c_1 in range(3): # 0->11
    n_1 = min(c_1+8,4)
    for c_2 in range(c_1+1,n_1): # 0->12
        n_2 = min(c_2+8,5)
        for c_3 in range(c_2+1,n_2):
            n_3 = min(c_3+8,6)
            for c_4 in range(c_3+1,n_3):
                n_4 = min(c_4+8,7)
                for c_5 in range(c_4+1,n_4):
                    n_5 = min(c_5+8,8)
                    for c_6 in range(c_5+1,n_5):
                        n_6 = min(c_6+8,9)
                        for c_7 in range(c_6+1,n_6):
                            n_7 = min(c_7+8,10)
                            for c_8 in range(c_7+1,n_7):
                                n_8 = min(c_8+8,11)
                                for c_9 in range(c_8+1,n_8):
                                    n_9 = min(c_9+8,12)
                                    for c_10 in range(c_9+1,n_9):
                                        n_10 = min(c_10+8,13)
                                        for c_11 in range(c_10+1,n_10):
                                            elevenCardIndices_[eleven]=[c_1,c_2,c_3,c_4,c_5,c_6,c_7,c_8,c_9,c_10,c_11]
                                            eleven += 1
elevenCardIndices = list(elevenCardIndices_.values())
inverseElevenCardIndices = list(elevenCardIndices_.keys())

twelveCardIndices_ = {}
for c_1 in range(2): # 0->11
    n_1 = min(c_1+8,3)
    for c_2 in range(c_1+1,n_1): # 0->12
        n_2 = min(c_2+8,4)
        for c_3 in range(c_2+1,n_2):
            n_3 = min(c_3+8,5)
            for c_4 in range(c_3+1,n_3):
                n_4 = min(c_4+8,6)
                for c_5 in range(c_4+1,n_4):
                    n_5 = min(c_5+8,7)
                    for c_6 in range(c_5+1,n_5):
                        n_6 = min(c_6+8,8)
                        for c_7 in range(c_6+1,n_6):
                            n_7 = min(c_7+8,9)
                            for c_8 in range(c_7+1,n_7):
                                n_8 = min(c_8+8,10)
                                for c_9 in range(c_8+1,n_8):
                                    n_9 = min(c_9+8,11)
                                    for c_10 in range(c_9+1,n_9):
                                        n_10 = min(c_10+8,12)
                                        for c_11 in range(c_10+1,n_10+1):
                                            n_11 = min(c_11+8,13)
                                            for c_12 in range(c_11+1,n_11):
                                                twelveCardIndices_[twelve]=[c_1,c_2,c_3,c_4,c_5,c_6,c_7,c_8,c_9,c_10,c_11,c_12]
                                                twelve += 1
twelveCardIndices = list(twelveCardIndices_.values())
inverseTwelveCardIndices = list(twelveCardIndices_.keys())

thirTeenCardIndices_ = {0:[0,1,2,3,4,5,6,7,8,9,10,11,12]}
thirTeenCardIndices = list(twelveCardIndices_.values())
inverseThirTeenCardIndices = list(twelveCardIndices_.keys())

# How to use table index =>
print(inverseNineCardIndices[nineCardIndices.index([2, 4, 5, 6, 7, 9, 10, 11, 12])])
print(sixCardIndices[5][6][7][8][9][10])
print(np.array(nineCardIndices[700]))
print(inverseSixCardIndices[1683])
print([two,three,four,five,six,seven,eight,nine,ten,eleven,twelve])

table = [twoCardIndices,threeCardIndices,fourCardIndices,fiveCardIndices,sixCardIndices,sevenCardIndices,eightCardIndices,nineCardIndices,tenCardIndices,elevenCardIndices,twelveCardIndices,thirTeenCardIndices,
inverseTwoCardIndices,inverseThreeCardIndices,inverseFourCardIndices,inverseFiveCardIndices,inverseSixCardIndices,inverseSevenCardIndices,inverseEightCardIndices,inverseNineCardIndices,inverseTenCardIndices,inverseElevenCardIndices,inverseTwelveCardIndices,inverseThirTeenCardIndices]
with open ("actionIndexTable.pkl",'wb') as tablepikle:
    pickle.dump(table,tablepikle)