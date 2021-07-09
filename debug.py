from gameLogic import handsAvailable
import numpy as np
import enumerateOptions

shuffledDeck = np.random.permutation(52) + 1  # sáo bài
# hand out cards to each player
currentHands = {}
currentHands[1] = np.sort(shuffledDeck[0:13])
currentHands[2] = np.sort(shuffledDeck[13:26])
currentHands[3] = np.sort(shuffledDeck[26:39])
currentHands[4] = np.sort(shuffledDeck[39:52])
for i in range(52):
    if shuffledDeck[i] == 1:
        threeDiamondInd = i
        break
if threeDiamondInd < 13:
    whoHas3D = 1
elif threeDiamondInd < 26:
    whoHas3D = 2
elif threeDiamondInd < 39:
    whoHas3D = 3
else:
    whoHas3D = 4
playersGo = whoHas3D
#print(list(currentHands[playersGo]))
'''
0[3S] 1[4C] 2[5S] 3[6C] 4[6D] 5[6H] 6[10S] 7[10H] 8[11D] 9[12H] 10[13D] 11[14S] 12[15H]
______
[[0], array([0, 1, 2]), array([0, 1, 2, 3]), array([0, 1, 2, 4]), array([0, 1, 2, 5])]
'''
currentHands = np.array([ 1 ,3, 8, 12, 14, 16, 24, 29, 32, 47, 48, 51, 52])
hands = handsAvailable(currentHands)
print("______")
print(hands.setValueCurrentHand)
print(hands.cardsValue)
print(hands.straights[4])
print(hands.pairs)
print(hands.threePines)
print(hands.fourPines)
#print(hands.straights)
prevhand = np.array([5, 8, 9, 11, 13, 14])
ops = enumerateOptions.firstPlayerOptions(currentHands,hands)
print(ops)