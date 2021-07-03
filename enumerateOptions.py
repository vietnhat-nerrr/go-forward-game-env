#enumerate options
import pickle
import numpy as np
import gameLogic_

nActions = np.array([13,33, 246, 670, 1263, 1711, 1716, 1286, 715, 286, 78, 13,1,8031])
nAcSum = np.cumsum(nActions[:-1]) # [  13   46  292  962 2225 3936 5652 6938 7653 7939 8017 8030]
#nActions = np.array([13,33,31,330,1287,1694]) luật chine
#print(nAcSum) => [  13   46   77  407 1694] cọng dồn kết quả 
with open('actionIndexTable.pkl','rb') as f:  # Python 3: open(..., 'rb')
    twoCardIndices, threeCardIndices, fourCardIndices, fiveCardIndices, sixCardIndices ,sevenCardIndices,eightCardIndices,nineCardIndices,tenCardIndices,elevenCardIndices,twelveCardIndices,thirTeenCardIndices,inverseTwoCardIndices, inverseThreeCardIndices, inverseFourCardIndices, inverseFiveCardIndices,inverseSixCardIndices,inverseSevenCardIndices,inverseEightCardIndices,inverseNineCardIndices,inverseTenCardIndices,inverseElevenCardIndices,inverseTwelveCardIndices,inverseThirTeenCardIndices = pickle.load(f)

passInd = nActions[-1] # passIndex
noTurn = passInd + 1 #8032
doneFinish = passInd + 2 #8033
def getIndex(option, nCards,info=[True,True]): # info mean check noTurn or doneFinish
    if info[0] == True:
        return noTurn
    if info[1] == True:
        return doneFinish
    if nCards==0: #pass
        return passInd

    sInd = 0
    for i in range(nCards-1):
        sInd += nActions[i]
    return sInd + option

def getOptionNC(ind):
    if ind == passInd:
        return -1, 0
    if ind < nAcSum[0]:
        return ind, 1
    elif ind < nAcSum[1]:
        return ind - nAcSum[0], 2
    elif ind < nAcSum[2]:
        return ind - nAcSum[1], 3
    elif ind < nAcSum[3]:
        return ind - nAcSum[2], 4
    elif ind < nAcSum[4]:
        return ind - nAcSum[3], 5
    elif ind < nAcSum[5]:
        return ind - nAcSum[4], 6    
    elif ind < nAcSum[6]:
        return ind - nAcSum[5], 7
    elif ind < nAcSum[7]:
        return ind - nAcSum[6], 8
    elif ind < nAcSum[8]:
        return ind - nAcSum[7], 9
    elif ind < nAcSum[9]:
        return ind - nAcSum[8], 10
    elif ind < nAcSum[10]:
        return ind - nAcSum[9], 11
    elif ind < nAcSum[11]:
        return ind - nAcSum[10], 12
    elif ind < nAcSum[12]:
        return ind - nAcSum[11], 13
def firstPlayerOptions(handOptions): # 
    if handOptions.cards[1].indexInHand == 0: ## 3 Bích đi trước kiêm tra 3 Bích có trong bài không
        card = handOptions.cards[1]
        validInds = np.zeros((100,), dtype=int) # 100 ước lượng
        c = 0
        if card.inPair != 0:

            cardInds = np.zeros((2,), dtype=int)
    
            if handOptions.nPairs > 0:
                for pair in handOptions.pairs:
                    cardInds[0] = handOptions.cards[pair[0]].indexInHand
                    cardInds[1] = handOptions.cards[pair[1]].indexInHand
                    if cardInds[0] == 0:
                        continue
                    validInds[c] = getIndex(twoCardIndices[cardInds[0]][cardInds[1]],2)
                    c += 1
        if card.inThreeOfAKind != 0:
            cardInds = np.zeros((3,), dtype=int)
    
            if handOptions.nThreeOfAKinds > 0:
                for three in handOptions.threeOfAKinds:
                    cardInds[0] = handOptions.cards[three[0]].indexInHand
                    cardInds[1] = handOptions.cards[three[1]].indexInHand
                    cardInds[2] = handOptions.cards[three[2]].indexInHand
                    if cardInds[0] == 0:
                        continue
                    validInds[c] = getIndex(twoCardIndices[cardInds[0]][cardInds[1]][cardInds[2]],3)
                    c += 1
        if card.inFourOfAKind != 0:
            cardInds = np.zeros((4,), dtype=int)
    
            if handOptions.nFourOfAKinds > 0:
                for four in handOptions.fourOfAKinds:
                    cardInds[0] = handOptions.cards[four[0]].indexInHand
                    cardInds[1] = handOptions.cards[four[1]].indexInHand
                    cardInds[2] = handOptions.cards[four[2]].indexInHand
                    cardInds[3] = handOptions.cards[four[3]].indexInHand
                    if cardInds[0] == 0:
                        continue
                    validInds[c] = getIndex(twoCardIndices[cardInds[0]][cardInds[1]][cardInds[2]],[cardInds[3]],4)
                    c += 1
        if card.inThreePines != 0:
            if handOptions.nThreePines > 0:
                for threepine in handOptions.threePines:
                    cardInds[0] = handOptions.cards[threepine[0]].indexInHand
                    cardInds[1] = handOptions.cards[threepine[1]].indexInHand
                    cardInds[2] = handOptions.cards[threepine[2]].indexInHand
                    cardInds[3] = handOptions.cards[threepine[3]].indexInHand
                    cardInds[4] = handOptions.cards[threepine[4]].indexInHand
                    cardInds[5] = handOptions.cards[threepine[5]].indexInHand
                    if cardInds[0] == 0:
                        continue
                    validInds[c] = getIndex(sixCardIndices[cardInds[0]][cardInds[1]][cardInds[2]][cardInds[3]][cardInds[4]][cardInds[5]],6)
                    c += 1
        if card.inFourPines !=0:
            if handOptions.nFourPines > 0:
                for four in handOptions.fourPines:
                    cardInds[0] = handOptions.cards[four[0]].indexInHand
                    cardInds[1] = handOptions.cards[four[1]].indexInHand
                    cardInds[2] = handOptions.cards[four[2]].indexInHand
                    cardInds[3] = handOptions.cards[four[3]].indexInHand
                    cardInds[4] = handOptions.cards[four[4]].indexInHand
                    cardInds[5] = handOptions.cards[four[5]].indexInHand
                    cardInds[6] = handOptions.cards[four[6]].indexInHand
                    cardInds[7] = handOptions.cards[four[7]].indexInHand
                    index_ =[cardInds[0],cardInds[1],cardInds[2],cardInds[3],cardInds[4],cardInds[5],cardInds[6],cardInds[7]]
                    if cardInds[0] == 0:
                        continue
                    validInds[c] = getIndex(inverseEightCardIndices[elevenCardIndices.index(index_)],8)
                    c += 1
        for i in range(len(card.inStraight)):
            if card.inStraight[i] !=0:
                index_  = []
                if handOptions.nStraights[i] > 0:
                    nCard = i + 3
                    for straight in handOptions.straights[i]:
                        for i in range(0,nCard):
                            cardInds[i] = handOptions.cards[straight[i]].indexInHand
                            index_.append(cardInds[i])
                        if cardInds[0] == 0:
                            continue
                        if nCard== 3:
                            validInds[c] = getIndex(threeCardIndices[cardInds[0]][cardInds[1]][cardInds[2]],3)
                            c += 1
                        if nCard == 4:
                            validInds[c] = getIndex(fourCardIndices[cardInds[0]][cardInds[1]][cardInds[2]][cardInds[3]],4)
                            c += 1
                        if nCard == 5:
                            validInds[c] = getIndex(fiveCardIndices[cardInds[0]][cardInds[1]][cardInds[2]][cardInds[3]][cardInds[4]],5)
                            c += 1
                        if nCard == 6:
                            validInds[c] = getIndex(sixCardIndices[cardInds[0]][cardInds[1]][cardInds[2]][cardInds[3]][cardInds[4]][cardInds[5]],6)
                            c += 1
                        if(nCard == 7):
                            validInds[c] = getIndex(inverseSevenCardIndices[sevenCardIndices.index(index_)],7)
                            c += 1
                        if(nCard == 8):
                            validInds[c] = getIndex(inverseEightCardIndices[eightCardIndices.index(index_)],8)
                            c += 1
                        if(nCard == 9):
                            validInds[c] = getIndex(inverseNineCardIndices[nineCardIndices.index(index_)],9)
                            c += 1
                        if(nCard == 10):
                            validInds[c] = getIndex(inverseTenCardIndices[tenCardIndices.index(index_)],10)
                            c += 1
                        if(nCard == 11):
                            validInds[c] = getIndex(inverseElevenCardIndices[elevenCardIndices.index(index_)],11)
                            c += 1
                        if(nCard == 12):
                            validInds[c] = getIndex(inverseTwelveCardIndices[twelveCardIndices.index(index_)],12)
                            c += 1
                        if(nCard == 13):
                            validInds[c] = getIndex(inverseThirTeenCardIndices[thirTeenCardIndices.index(index_)],13)
                            c += 1
                        index_ = []
        if c > 0:
            return validInds[0:c]
        else:
            return -1    
    return -1       
def greaterSixCardOptions(handOptions, prevHand=[],prevType = 0):
    #prevType = 0 - no hand, you have control and can play any 5 card
    #         = 1 - straight
    #         = 2 - fourPines
    nCard = len(prevHand)
    if(nCard == 8):
        validInds = np.zeros((nActions[7],),dtype=int)
        c = 0
        cardInds = np.zeros((8,),dtype=int) #reuse
        if prevType == 1:
            pass
        else:
            #four of a kinds
            if handOptions.nFourPines > 0:
                for four in handOptions.fourPines:
                    cardInds[0] = handOptions.cards[four[0]].indexInHand
                    cardInds[1] = handOptions.cards[four[1]].indexInHand
                    cardInds[2] = handOptions.cards[four[2]].indexInHand
                    cardInds[3] = handOptions.cards[four[3]].indexInHand
                    cardInds[4] = handOptions.cards[four[4]].indexInHand
                    cardInds[5] = handOptions.cards[four[5]].indexInHand
                    cardInds[6] = handOptions.cards[four[6]].indexInHand
                    cardInds[7] = handOptions.cards[four[7]].indexInHand
                    index_ =[cardInds[0],cardInds[1],cardInds[2],cardInds[3],cardInds[4],cardInds[5],cardInds[6],cardInds[7]]
                    if prevType == 2:
                        if handOptions.cHand[cardInds[7]] < prevHand[7]:
                            continue
                    validInds[c] = getIndex(inverseEightCardIndices[elevenCardIndices.index(index_)],8)
                    c += 1
        if prevType == 2:
            pass
        else:
            if handOptions.nStraights[5] > 0:
                for straight in handOptions.straights[5]:
                    cardInds[0] = handOptions.cards[straight[0]].indexInHand
                    cardInds[1] = handOptions.cards[straight[1]].indexInHand
                    cardInds[2] = handOptions.cards[straight[2]].indexInHand
                    cardInds[3] = handOptions.cards[straight[3]].indexInHand
                    cardInds[4] = handOptions.cards[straight[4]].indexInHand
                    cardInds[5] = handOptions.cards[straight[5]].indexInHand
                    cardInds[6] = handOptions.cards[straight[5]].indexInHand
                    cardInds[7] = handOptions.cards[straight[5]].indexInHand
                    index_ =[cardInds[0],cardInds[1],cardInds[2],cardInds[3],cardInds[4],cardInds[5],cardInds[6],cardInds[7]]
                    if prevType == 1:
                        if handOptions.cHand[cardInds[7]] < prevHand[7]:
                            continue
                    validInds[c] = getIndex(inverseEightCardIndices[elevenCardIndices.index(index_)],8)
                    c += 1


        if c > 0:
            return validInds[0:c]
        else:
            return -1 #no eight card hands
    else:
        #prevType = 0 - no hand, you have control and can play any 5 card
        #         = 1 - straight
      
        nCard = len(prevHand)
        validInds = np.zeros((nActions[nCard-1],),dtype=int)
        c = 0
        cardInds = np.zeros((nCard,),dtype=int) #reuse
        
        #first deal with straights
        index_  = []
        if handOptions.nStraights[nCard-3] > 0:
            for straight in handOptions.straights[2]:
                for i in range(0,nCard):
                    cardInds[i] = handOptions.cards[straight[i]].indexInHand
                    index_.append(cardInds[i])
                if prevType == 1:
                    if handOptions.cHand[cardInds[nCard-1]] < prevHand[nCard-1]:
                        continue
                if(nCard == 7):
                    validInds[c] = getIndex(inverseSevenCardIndices[sevenCardIndices.index(index_)],7)
                    c += 1
                if(nCard == 9):
                    validInds[c] = getIndex(inverseNineCardIndices[nineCardIndices.index(index_)],9)
                    c += 1
                if(nCard == 10):
                    validInds[c] = getIndex(inverseTenCardIndices[tenCardIndices.index(index_)],10)
                    c += 1
                if(nCard == 11):
                    validInds[c] = getIndex(inverseElevenCardIndices[elevenCardIndices.index(index_)],11)
                    c += 1
                if(nCard == 12):
                    validInds[c] = getIndex(inverseTwelveCardIndices[twelveCardIndices.index(index_)],12)
                    c += 1
                if(nCard == 13):
                    validInds[c] = getIndex(inverseThirTeenCardIndices[thirTeenCardIndices.index(index_)],13)
                    c += 1
                index_ = []
        if c > 0:
            return validInds[0:c]
        else:
            return -1
def sixCardOptions(handOptions, prevHand=[],prevType = 0):
    #prevType = 0 - no hand, you have control and can play any 5 card
    #         = 1 - straight
    #         = 2 - threePines
    validInds = np.zeros((nActions[5],),dtype=int)
    c = 0
    cardInds = np.zeros((6,),dtype=int) #reuse
    if prevType == 1:
        pass
    else:
        
        if handOptions.nThreePines > 0:
            for threepine in handOptions.threePines:
                cardInds[0] = handOptions.cards[threepine[0]].indexInHand
                cardInds[1] = handOptions.cards[threepine[1]].indexInHand
                cardInds[2] = handOptions.cards[threepine[2]].indexInHand
                cardInds[3] = handOptions.cards[threepine[3]].indexInHand
                cardInds[4] = handOptions.cards[threepine[4]].indexInHand
                cardInds[5] = handOptions.cards[threepine[5]].indexInHand
                if prevType == 2:
                    if handOptions.cHand[cardInds[0]] < prevHand[3]:
                        continue
                validInds[c] = getIndex(sixCardIndices[cardInds[0]][cardInds[1]][cardInds[2]][cardInds[3]][cardInds[4]][cardInds[5]],6)
                c += 1
        if prevType == 2:
            cardInds = np.zeros((4,),dtype=int)
            if len(handOptions.fourOfAKinds) > 0:
                for four in handOptions.fourOfAKinds:
                    cardInds[0] = handOptions.cards[four[0]].indexInHand
                    cardInds[1] = handOptions.cards[four[1]].indexInHand
                    cardInds[2] = handOptions.cards[four[2]].indexInHand
                    cardInds[3] = handOptions.cards[four[3]].indexInHand
                    validInds[c] = getIndex(fourCardIndices[cardInds[0]][cardInds[1]][cardInds[2]][cardInds[3]],4)
                    c += 1
            cardInds = np.zeros((8,),dtype=int)
            if handOptions.nFourPines > 0:
                for four in handOptions.fourPines:
                    cardInds[0] = handOptions.cards[four[0]].indexInHand
                    cardInds[1] = handOptions.cards[four[1]].indexInHand
                    cardInds[2] = handOptions.cards[four[2]].indexInHand
                    cardInds[3] = handOptions.cards[four[3]].indexInHand
                    cardInds[4] = handOptions.cards[four[4]].indexInHand
                    cardInds[5] = handOptions.cards[four[5]].indexInHand
                    cardInds[6] = handOptions.cards[four[5]].indexInHand
                    cardInds[7] = handOptions.cards[four[5]].indexInHand
                    validInds[c] = getIndex(inverseEightCardIndices[elevenCardIndices.index([cardInds[0],cardInds[1],cardInds[2],cardInds[3],cardInds[4],cardInds[5],cardInds[6],cardInds[7]])],8)
                    c += 1
    if prevType == 2:
        pass
    else:
        if handOptions.nStraights[3] > 0:
            for straight in handOptions.straights[3]:
                cardInds[0] = handOptions.cards[straight[0]].indexInHand
                cardInds[1] = handOptions.cards[straight[1]].indexInHand
                cardInds[2] = handOptions.cards[straight[2]].indexInHand
                cardInds[3] = handOptions.cards[straight[3]].indexInHand
                cardInds[4] = handOptions.cards[straight[4]].indexInHand
                cardInds[5] = handOptions.cards[straight[5]].indexInHand

                if prevType == 1:
                    if handOptions.cHand[cardInds[3]] < prevHand[3]:
                        continue
                validInds[c] = getIndex(sixCardIndices[cardInds[0]][cardInds[1]][cardInds[2]][cardInds[3]][cardInds[4]][cardInds[5]],6)
                c += 1


    if c > 0:
        return validInds[0:c]
    else:
        return -1 #no four card hands
def fiveCardOptions(handOptions, prevHand=[],prevType=0):
    #prevType = 0 - no hand, you have control and can play any 5 card
    #         = 1 - straight
      
        
    validInds = np.zeros((nActions[4],),dtype=int)
    c = 0
    cardInds = np.zeros((5,),dtype=int) #reuse
    
    #first deal with straights
    if handOptions.nStraights[2] > 0:
        for straight in handOptions.straights[2]:
            cardInds[0] = handOptions.cards[straight[0]].indexInHand
            cardInds[1] = handOptions.cards[straight[1]].indexInHand
            cardInds[2] = handOptions.cards[straight[2]].indexInHand
            cardInds[3] = handOptions.cards[straight[3]].indexInHand
            cardInds[4] = handOptions.cards[straight[3]].indexInHand

            if prevType == 1:
                if handOptions.cHand[cardInds[4]] < prevHand[4]:
                    continue
            validInds[c] = getIndex(fiveCardIndices[cardInds[0]][cardInds[1]][cardInds[2]][cardInds[3]][cardInds[4]],5)
            c += 1
    
    if c > 0:
        return validInds[0:c]
    else:
        return -1

    

def fourCardOptions(handOptions, prevHand = [], prevType = 0):
    #prevType: 1 - straight, 2 - fourofakind    
    validInds = np.zeros((nActions[3],),dtype=int)
    c = 0
    cardInds = np.zeros((4,),dtype=int) #reuse
    if prevType == 1:
        pass
    else:
        #four of a kinds
        if len(handOptions.fourOfAKinds) > 0:
            for four in handOptions.fourOfAKinds:
                cardInds[0] = handOptions.cards[four[0]].indexInHand
                cardInds[1] = handOptions.cards[four[1]].indexInHand
                cardInds[2] = handOptions.cards[four[2]].indexInHand
                cardInds[3] = handOptions.cards[four[3]].indexInHand
                if prevType == 2:
                    if handOptions.cHand[cardInds[0]] < prevHand[3]:
                        continue
                validInds[c] = getIndex(fourCardIndices[cardInds[0]][cardInds[1]][cardInds[2]][cardInds[3]],4)
                c += 1
        if prevType == 2: ## chặt 4 đôi thông   
            cardInds = np.zeros((8,),dtype=int)
            if handOptions.nFourPines > 0:
                for four in handOptions.fourPines:
                    cardInds[0] = handOptions.cards[four[0]].indexInHand
                    cardInds[1] = handOptions.cards[four[1]].indexInHand
                    cardInds[2] = handOptions.cards[four[2]].indexInHand
                    cardInds[3] = handOptions.cards[four[3]].indexInHand
                    cardInds[4] = handOptions.cards[four[4]].indexInHand
                    cardInds[5] = handOptions.cards[four[5]].indexInHand
                    cardInds[6] = handOptions.cards[four[5]].indexInHand
                    cardInds[7] = handOptions.cards[four[5]].indexInHand
                    validInds[c] = getIndex(inverseEightCardIndices[elevenCardIndices.index([cardInds[0],cardInds[1],cardInds[2],cardInds[3],cardInds[4],cardInds[5],cardInds[6],cardInds[7]])],8)
                    c += 1
    if prevType == 2:
        pass
    else:
        if handOptions.nStraights[1] > 0:
            for straight in handOptions.straights[1]:
                cardInds[0] = handOptions.cards[straight[0]].indexInHand
                cardInds[1] = handOptions.cards[straight[1]].indexInHand
                cardInds[2] = handOptions.cards[straight[2]].indexInHand
                cardInds[3] = handOptions.cards[straight[3]].indexInHand

                if prevType == 1:
                    if handOptions.cHand[cardInds[3]] < prevHand[3]:
                        continue
                validInds[c] = getIndex(fourCardIndices[cardInds[0]][cardInds[1]][cardInds[2]][cardInds[3]],4)
                c += 1


    if c > 0:
        return validInds[0:c]
    else:
        return -1 #no four card hands

def threeCardOptions(handOptions, prevHand = [], prevType = 0):
    #prevType = 1 - played three card strange
    #prevType = 2 - played three of a kind
    validInds = np.zeros((nActions[2],), dtype=int)
    c = 0
    cardInds = np.zeros((3,), dtype=int) #reuse
    if prevType == 1:
        pass 
    else:
        if handOptions.nThreeOfAKinds > 0:
            for three in handOptions.threeOfAKinds:
                cardInds[0] = handOptions.cards[three[0]].indexInHand
                cardInds[1] = handOptions.cards[three[1]].indexInHand
                cardInds[2] = handOptions.cards[three[2]].indexInHand
                if prevType == 1:
                    if handOptions.cHand[cardInds[2]] < prevHand[2]:
                        continue
                validInds[c] = getIndex(threeCardIndices[cardInds[0]][cardInds[1]][cardInds[2]],3)
                c += 1
    if prevType == 2:
        pass
    else:
        if handOptions.nStraights[0] > 0:
            for straight in handOptions.straights[0]:
                cardInds[0] = handOptions.cards[straight[0]].indexInHand
                cardInds[1] = handOptions.cards[straight[1]].indexInHand
                cardInds[2] = handOptions.cards[straight[2]].indexInHand

                if prevType == 1:
                    if handOptions.cHand[cardInds[2]] < prevHand[2]:
                        continue
                validInds[c] = getIndex(threeCardIndices[cardInds[0]][cardInds[1]][cardInds[2]],3)
                c += 1
    if c > 0:
        return validInds[0:c]
    else:
        return -1
    

def twoCardOptions(handOptions, prevHand = [], prevType = 0):
    #prevType = 1 - played a pair
    #prevType = 0 - played has control
    validInds = np.zeros((nActions[1],), dtype=int)
    c = 0
    cardInds = np.zeros((2,), dtype=int)
    
    if handOptions.nPairs > 0:
        for pair in handOptions.pairs:
            cardInds[0] = handOptions.cards[pair[0]].indexInHand
            cardInds[1] = handOptions.cards[pair[1]].indexInHand
            if prevType == 1:
                if handOptions.cHand[cardInds[1]] < prevHand[1]:
                    continue
            validInds[c] = getIndex(twoCardIndices[cardInds[0]][cardInds[1]],2)
            c += 1
    ### Chặt đôi heo với tứ quá và 4 đôi thông
    if prevType == 1 and ( prevHand[-1] == 52 or prevHand[-1] == 51 or prevHand[-1] == 50 or prevHand[-1] ==49):
        cardInds = np.zeros((4,),dtype=int)
        if len(handOptions.fourOfAKinds) > 0:
            for four in handOptions.fourOfAKinds:
                cardInds[0] = handOptions.cards[four[0]].indexInHand
                cardInds[1] = handOptions.cards[four[1]].indexInHand
                cardInds[2] = handOptions.cards[four[2]].indexInHand
                cardInds[3] = handOptions.cards[four[3]].indexInHand
                validInds[c] = getIndex(fourCardIndices[cardInds[0]][cardInds[1]][cardInds[2]][cardInds[3]],4)
                c += 1
        cardInds = np.zeros((8,),dtype=int)
        if handOptions.nFourPines > 0:
            for four in handOptions.fourPines:
                cardInds[0] = handOptions.cards[four[0]].indexInHand
                cardInds[1] = handOptions.cards[four[1]].indexInHand
                cardInds[2] = handOptions.cards[four[2]].indexInHand
                cardInds[3] = handOptions.cards[four[3]].indexInHand
                cardInds[4] = handOptions.cards[four[4]].indexInHand
                cardInds[5] = handOptions.cards[four[5]].indexInHand
                cardInds[6] = handOptions.cards[four[5]].indexInHand
                cardInds[7] = handOptions.cards[four[5]].indexInHand
                validInds[c] = getIndex(inverseEightCardIndices[elevenCardIndices.index([cardInds[0],cardInds[1],cardInds[2],cardInds[3],cardInds[4],cardInds[5],cardInds[6],cardInds[7]])],8)
                c += 1
    if c > 0:
        return validInds[0:c]
    else:
        return -1
    
def oneCardOptions(hand,handOptions, prevHand = [], prevType = 0,startPlay= False, endPlay= False):
    nCards = len(hand)
    validInds = np.zeros((nCards+999,), dtype=int) # 3 mean tứ quý chaặt
    c = 0
    for i in range(nCards):
        if prevType == 1:
            if prevHand > hand[i]:
                continue
        validInds[c] = getIndex(i,1)
        c += 1
    if prevType == 1 and ( prevHand[-1] == 52 or prevHand[-1] == 51 or prevHand[-1] == 50 or prevHand[-1] ==49):
        cardInds = np.zeros((4,),dtype=int)
        if len(handOptions.fourOfAKinds) > 0:
            for four in handOptions.fourOfAKinds:
                cardInds[0] = handOptions.cards[four[0]].indexInHand
                cardInds[1] = handOptions.cards[four[1]].indexInHand
                cardInds[2] = handOptions.cards[four[2]].indexInHand
                cardInds[3] = handOptions.cards[four[3]].indexInHand
                validInds[c] = getIndex(fourCardIndices[cardInds[0]][cardInds[1]][cardInds[2]][cardInds[3]],4)
                c += 1
        cardInds = np.zeros((6,),dtype=int)
        if handOptions.nThreePines > 0:
            for threepine in handOptions.threePines:
                cardInds[0] = handOptions.cards[threepine[0]].indexInHand
                cardInds[1] = handOptions.cards[threepine[1]].indexInHand
                cardInds[2] = handOptions.cards[threepine[2]].indexInHand
                cardInds[3] = handOptions.cards[threepine[3]].indexInHand
                cardInds[4] = handOptions.cards[threepine[4]].indexInHand
                cardInds[5] = handOptions.cards[threepine[5]].indexInHand
                validInds[c] = getIndex(sixCardIndices[cardInds[0]][cardInds[1]][cardInds[2]][cardInds[3]][cardInds[4]][cardInds[5]],6)
                c += 1
        cardInds = np.zeros((8,),dtype=int)
        if handOptions.nFourPines > 0:
            for four in handOptions.fourPines:
                cardInds[0] = handOptions.cards[four[0]].indexInHand
                cardInds[1] = handOptions.cards[four[1]].indexInHand
                cardInds[2] = handOptions.cards[four[2]].indexInHand
                cardInds[3] = handOptions.cards[four[3]].indexInHand
                cardInds[4] = handOptions.cards[four[4]].indexInHand
                cardInds[5] = handOptions.cards[four[5]].indexInHand
                cardInds[6] = handOptions.cards[four[5]].indexInHand
                cardInds[7] = handOptions.cards[four[5]].indexInHand
                validInds[c] = getIndex(inverseEightCardIndices[elevenCardIndices.index([cardInds[0],cardInds[1],cardInds[2],cardInds[3],cardInds[4],cardInds[5],cardInds[6],cardInds[7]])],8)
                c += 1
    if c > 0:
        return validInds[0:c]
    else:
        return -1
    