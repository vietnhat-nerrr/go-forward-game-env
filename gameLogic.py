import numpy as np

def shuffle(array):
    """
    xáo trộn array => để xáo trộn bài
    """
    i=0
    j=0
    temp = 0
    
    for i in range(array.size-1,0,-1):
        j = int(np.floor(np.random.random()*(i+1)))
        temp = array[i]
        array[i] = array[j]
        array[j] = temp
    return array

def isPair(hand):
    if hand.size != 2:
        return 0
    if np.ceil(hand[0]/4) == np.ceil(hand[1]/4):
        return 1
    else:
        return 0

def isThreeOfAKind(hand):
    if hand.size != 3:
        return 0
    if (np.ceil(hand[0]/4)==np.ceil(hand[1]/4)) and (np.ceil(hand[1]/4)==np.ceil(hand[2]/4)):
        return 1
    else:
        return 0

def isFourOfAKind(hand):
    if hand.size != 4:
        return 0
    if (np.ceil(hand[0]/4)==np.ceil(hand[1]/4)) and (np.ceil(hand[1]/4)==np.ceil(hand[2]/4)) and (np.ceil(hand[2]/4)==np.ceil(hand[3]/4)):
        return 1
    else:
        return 0
def isThreePines(hand):
    if hand.size != 6:
        return 0
    hand.sort()
    if(isPair(hand[0:2]) and isPair(hand[2:4]) and isPair(hand[4:6]) and np.ceil(hand[1]/4)+1==np.ceil(hand[2]/4) and np.ceil(hand[3]/4)+1==np.ceil(hand[4]/4)):
        return 1
    else: return 0

def isFourPines(hand):
    if hand.size != 8:
        return 0
    hand.sort()
    if(isPair(hand[0:2]) and isPair(hand[2:4]) and isPair(hand[4:6]) and isPair(hand[6:8])and np.ceil(hand[1]/4)+1==np.ceil(hand[2]/4) and np.ceil(hand[3]/4)+1==np.ceil(hand[4]/4) and np.ceil(hand[5]/4)+1==np.ceil(hand[6]/4)):
        return 1
    else: return 0

def isFivePines(hand):
    if hand.size != 10:
        return 0
    hand.sort()
    if(isPair(hand[0:2]) and isPair(hand[2:4]) and isPair(hand[4:6]) and isPair(hand[6:8]) and isPair(hand[8:10])and np.ceil(hand[1]/4)+1==np.ceil(hand[2]/4) and np.ceil(hand[3]/4)+1==np.ceil(hand[4]/4) and np.ceil(hand[5]/4)+1==np.ceil(hand[6]/4) and np.ceil(hand[7]/4)+1==np.ceil(hand[8]/4)):
        return 1
    else: return 0
def isStraightThree(hand): # maybe dont need
    if hand.size != 3:
        return 0
    hand.sort()
    if  np.ceil(hand[0]/4)+2==np.ceil(hand[1]/4)+1 == np.ceil(hand[2]/4):
        return 1
    else: return 0
def isStraightFour(hand): #  maybe dont need
    if hand.size != 4:
        return 0
    hand.sort()
    if  np.ceil(hand[0]/4)+3==np.ceil(hand[1]/4) +2 == np.ceil(hand[2]/4) +1 == np.ceil(hand[3]/4):
        return 1
    else: return 0
def isStraightFive(hand): # maybe dont need
    if hand.size != 5:
        return 0
    hand.sort()
    if  np.ceil(hand[0]/4)+4==np.ceil(hand[1]/4) +3 == np.ceil(hand[2]/4) +2 == np.ceil(hand[3]/4)+1 == np.ceil(hand[4]/4):
        return 1
    else: return 0
def isStraightSix(hand): # not complete
    if hand.size != 6:
        return 0
    hand.sort()
    if  np.ceil(hand[0]/4)+4==np.ceil(hand[1]/4) +3 == np.ceil(hand[2]/4) +2 == np.ceil(hand[3]/4)+1 == np.ceil(hand[4]/4):
        return 1
    else: return 0
def isStraight(hand):
    if hand.size < 3 or hand.size>13:
        return (False,)
    for i in range(hand.size):
        if(np.ceil(hand[i]/4) + (hand.size - i - 1)!= np.ceil(hand[-1]/4)):
            return (False,)
    return (True,hand.size,hand[0],hand[-1])
    



def isRealHand(hand):
    if (hand.size > 13) or (hand.size < 1):
        return 0
    if hand.size==1:
        return 1
    if hand.size==2:
        if isPair(hand):
            return 1
        else:
            return 0
    if hand.size==3:
        if isStraight(hand):
            return 1
        if isThreeOfAKind(hand):
            return 1
        else:
            return 0
    if hand.size==4:
        if isStraight(hand):
            return 1
        elif isFourOfAKind(hand):
            return 1
        else:
            return 0
    if hand.size==5:
        if isStraight(hand):
            return 1
        else: return 0
    if hand.size >= 6:
        if isStraight(hand):
            return 1
        if isThreePines(hand):
            return 1
        if isFourPines(hand):
            return 1
        if isFivePines(hand):
            return 1
        else: return 0

#function to convert hand in text form into number form.
def convertHand(hand):
    # Spades < Clubs  < Diamonds < Hearts
    #takes a list in the form ["3","KD",...] etc and converts it into numbers
    output = np.zeros(len(hand))
    counter = 0
    for card in hand:
        if card[0] == "2":
            base = 13
        elif card[0] == "A":
            base = 12
        elif card[0] == "K":
            base = 11
        elif card[0] == "Q":
            base = 10
        elif card[0] == "J":
            base = 9
        elif card[0] == "1":
            base = 8
            card = card.replace("0","")
        else:
            base = int(card[0])-2
        
        if card[1] == "S":
            suit = 1
        elif card[1] == "C":
            suit = 2
        elif card[1] == "D":
            suit = 3
        elif card[1] == "H":
            suit = 4
            
        output[counter] = int((base-1)*4 + suit)
        counter += 1
    return output

def cardValue(num):
    return np.ceil(num/4)    
class card:
    def __init__(self, number, i):
        self.suit = number % 4 #4 - Heart , 3 - Diamond, 2- Club , 1 - Spade
        self.value = np.ceil(number/4) #from 1 to 13.
        self.indexInHand = i #index within current hand (from 0 to 12)
        self.inPair = 0
        self.inThreeOfAKind = 0
        self.inFourOfAKind = 0
        self.inThreePines = 0
        self.inFourPines = 0
        self.inStraight = np.zeros(11,dtype=np.uint8) 
        ###self.straightIndex = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1] #index of which straight this card is in and length straight
        ###self.threePinesIndex = -1
        ###self.fourPinesIndex = -1
    

    def __repr__(self):
        if self.value < 8:
            string1 = str(self.value+2)
            string1 = string1[0]
        elif self.value == 8:
            string1 = "10"
        elif self.value == 9:
            string1 = "J"
        elif self.value == 10:
            string1 = "Q"
        elif self.value == 11:
            string1 = "K"
        elif self.value == 12:
            string1 = "A"
        elif self.value == 13:
            string1 = "2"
        if self.suit == 1:
            string2 = "S"
        elif self.suit == 2:
            string2 = "C"
        elif self.suit == 3:
            string2 = "D"
        else:
            string2 = "H"
        cardString = string1 + string2
        return "<card. %s inPair: %d, inThreeOfKind: %d,inFourOfAKind:%d, inStraight: %d, inThreePines: %d, inFourPines: %d>" % (cardString, self.inPair, self.inThreeOfAKind, self.inFourOfAKind,self.inStraight, self.inThreePines,self.inFourPines)
        

class handsAvailable:
    """
    nC : not understand maybe "number card rest"
    """
    def __init__(self, currentHand, nC=0):
        self.cHand =  np.sort(currentHand).astype(int)
        self.handLength = currentHand.size
        self.cards = {}
        self.setValueCurrentHand = list(set(self.convertAllToValue(currentHand))^set([13])) #loại heo ra để tìm straight dể dàng hơn
        self.cardsValue = self.convertAllToValue(currentHand)
        for i in range(self.cHand.size):
            self.cards[self.cHand[i]] = card(self.cHand[i],i)
        self.pairs = []
        self.threeOfAKinds = []
        self.fourOfAKinds = []
        self.straights = [[],[],[],[],[],[],[],[],[],[],[]] # không phải index mà chứa tên card 
        self.threePines = []
        self.fourPines = []
        self.nPairs = 0
        self.nThreeOfAKinds = 0
        self.nFourOfAKinds = 0
        self.nStraights = [0,0,0,0,0,0,0,0,0,0,0] #3-13 chứa 11 giá trị
        self.nThreePines = 0
        self.nFourPines = 0
        self.nDistinctPairs = 0
        if nC == 2:
            self.fillPairs()
        elif nC == 3:
            self.fillPairs()
            self.fillThreeOfAKinds()
            self.fillStraights()
        elif nC == 4:
            self.fillFourOfAKinds()
            self.fillPairs()
            self.fillStraights()
            self.fillThreeOfAKinds()
        else:
            self.fillPairs()
            self.fillThreeOfAKinds()
            self.fillFourOfAKinds()
            self.fillThreePines()
            self.fillFourPines()
            self.fillStraights()
    def convertAllToValue(self,currentHand):
        arrValue = []
        for i in currentHand:
            arrValue.append(np.ceil(i/4))
        return arrValue
    def findWhereInArray(self,listValueCard,number):
        arrArgWhere = []
        for i in range(len(listValueCard)):
            if number == listValueCard[i]:
                arrArgWhere.append(i)
        return arrArgWhere
    def handStraight(self,arrValue,listNumber):
        arrArg = {}
        index = 0
        totalHands = 1
        for i in range(len(listNumber)):
            arrArg[i] = self.findWhereInArray(arrValue, listNumber[i])
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


                
    def fillThreePines(self):
        for c_1 in range(8): # 0->11
            n_1 = min(c_1+4,9)
            for c_2 in range(c_1+1,n_1): # 0->12
                n_2 = min(c_2+3,10)
                for c_3 in range(c_2+1,n_2):
                    n_3 = min(c_3+4,11)
                    for c_4 in range(c_3+1,n_3):
                        n_4 = min(c_4+3,12)
                        for c_5 in range(c_4+1,n_4):
                            n_5 = min(c_5+4,13)
                            for c_6 in range(c_5+1,n_5):
                                if c_6 >=self.handLength:
                                    continue
                                if self.cHand[c_6] != 52 or  self.cHand[c_6] != 51 or self.cHand[c_6] != 50 or self.cHand[c_6] != 49:
                                    if isThreePines(np.array([self.cHand[c_1], self.cHand[c_2], self.cHand[c_3],self.cHand[c_4],self.cHand[c_5],self.cHand[c_6]])):
                                        self.threePines.append([self.cHand[c_1], self.cHand[c_2], self.cHand[c_3],self.cHand[c_4],self.cHand[c_5],self.cHand[c_6]])
                                        self.nThreePines += 1
                                        self.cards[self.cHand[c_1]].inThreePines = 1
                                        self.cards[self.cHand[c_2]].inThreePines = 1
                                        self.cards[self.cHand[c_3]].inThreePines = 1
                                        self.cards[self.cHand[c_4]].inThreePines = 1
                                        self.cards[self.cHand[c_5]].inThreePines = 1
                                        self.cards[self.cHand[c_6]].inThreePines = 1

    def fillFourPines(self):
        for c_1 in range(6): # 0->11
            n_1 = min(c_1+4,7)
            for c_2 in range(c_1+1,n_1): # 0->12
                n_2 = min(c_2+3,8)
                for c_3 in range(c_2+1,n_2):
                    n_3 = min(c_3+4,9)
                    for c_4 in range(c_3+1,n_3):
                        n_4 = min(c_4+3,10)
                        for c_5 in range(c_4+1,n_4):
                            n_5 = min(c_5+4,11)
                            for c_6 in range(c_5+1,n_5):
                                n_6 = min(c_6+3,12)
                                for c_7 in range(c_6+1,n_6):
                                    n_7 = min(c_7+4,13)
                                    for c_8 in range(c_7+1,n_7):
                                        if c_8 >=self.handLength:
                                            continue
                                        if self.cHand[c_8] != 52 or  self.cHand[c_8] != 51 or self.cHand[c_8] != 50 or self.cHand[c_8] != 49:
                                            if isFourPines(np.array([self.cHand[c_1], self.cHand[c_2], self.cHand[c_3],self.cHand[c_4],self.cHand[c_5],self.cHand[c_6],self.cHand[c_7],self.cHand[c_8]])):
                                                self.fourPines.append([self.cHand[c_1], self.cHand[c_2], self.cHand[c_3],self.cHand[c_4],self.cHand[c_5],self.cHand[c_6],self.cHand[c_7],self.cHand[c_8]])
                                                self.nfourPines += 1
                                                self.cards[self.cHand[c_1]].inFourPines = 1
                                                self.cards[self.cHand[c_2]].inFourPines = 1
                                                self.cards[self.cHand[c_3]].inFourPines = 1
                                                self.cards[self.cHand[c_4]].inFourPines = 1
                                                self.cards[self.cHand[c_5]].inFourPines = 1
                                                self.cards[self.cHand[c_6]].inFourPines = 1
                                                self.cards[self.cHand[c_7]].inFourPines = 1
                                                self.cards[self.cHand[c_8]].inFourPines = 1
    def fillStraights(self):
        streak = 0
        cInd = 0
        sInd = 0
        countLoop = 0
        while cInd < self.setValueCurrentHand.size - 1:
            countLoop += 1
            cVal = self.cards[self.setValueCurrentHand[cInd]].value
            nVal = self.cards[self.setValueCurrentHand[cInd+1]].value
            if nVal == cVal + 1:
                streak += 1
                cInd += 1
            if nVal == cVal:
                cInd += 1
            if streak >= 2:
                straightIndex =  self.handStraight(self.cardsValue,self.setValueCurrentHand[sInd:cInd+1])
                for straight in straightIndex:
                    lstAppend = []
                    for j in straight:
                        self.cards[self.cHand[j]].inStraight[streak+1] = 1
                        lstAppend.append(self.cHand[j])
                    self.straights[streak+1].append(lstAppend.append(self.cHand[j]))
                    self.nStraights[streak+1] += 1
            if countLoop != streak:
                streak = 0
                countLoop = 0
                cInd = sInd + 1
                sInd = cInd
                
    def fillPairs(self):
        cVal = -1
        nDistinct = 0
        for i in range(self.handLength-1):
            for j in range(i+1,i+4):
                if j>=self.handLength:
                    continue
                if isPair(np.array([self.cHand[i], self.cHand[j]])):
                    nVal = cardValue(self.cHand[i])
                    if nVal != cVal:
                        nDistinct += 1
                        cVal = nVal
                    self.pairs.append([self.cHand[i], self.cHand[j]])
                    self.nPairs += 1
                    self.nDistinctPairs = nDistinct
                    self.cards[self.cHand[i]].inPair = 1
                    self.cards[self.cHand[j]].inPair = 1    
    def fillThreeOfAKinds(self):
        for i in range(self.handLength-2):
            for j in range(i+1,i+3):
                if (j+1)>=self.handLength:
                    continue
                if isThreeOfAKind(np.array([self.cHand[i], self.cHand[j], self.cHand[j+1]])):
                    self.threeOfAKinds.append([self.cHand[i], self.cHand[j], self.cHand[j+1]])
                    self.nThreeOfAKinds += 1
                    self.cards[self.cHand[i]].inThreeOfAKind = 1
                    self.cards[self.cHand[j]].inThreeOfAKind = 1
                    self.cards[self.cHand[j+1]].inThreeOfAKind = 1
                    
    def fillFourOfAKinds(self):
        for i in range(self.handLength-3):
            if self.cards[self.cHand[i]].suit==1:
                if np.ceil(self.cHand[i]/4) == np.ceil(self.cHand[i+1]/4):
                    if np.ceil(self.cHand[i]/4) == np.ceil(self.cHand[i+2]/4):
                        if np.ceil(self.cHand[i]/4) == np.ceil(self.cHand[i+3]/4):
                            self.fourOfAKinds.append([self.cHand[i], self.cHand[i+1], self.cHand[i+2], self.cHand[i+3]])
                            self.cards[self.cHand[i]].inFourOfAKind = 1
                            self.cards[self.cHand[i+1]].inFourOfAKind = 1
                            self.cards[self.cHand[i+2]].inFourOfAKind = 1
                            self.cards[self.cHand[i+3]].inFourOfAKind = 1            
        
        