# big 2 class
# tiến lên miền Nam
import enumerateOptions
import gameLogic
import numpy as np
import random
import math
from multiprocessing import Process, Pipe


def convertAvailableActions(availAcs):
    # convert from (1,0,0,1,1...) to (0, -math.inf, -math.inf, 0,0...) etc
    availAcs[np.nonzero(availAcs == 0)] = -math.inf
    availAcs[np.nonzero(availAcs == 1)] = 0
    return availAcs


class handPlayed:  # return type hand card played by player
    def __init__(self, hand, player):
        self.hand = hand
        self.player = player
        self.nCards = len(hand)
        if self.nCards <= 1:
            self.type = 0
        elif self.nCards == 2:
            self.type = 1
        elif self.nCards == 3:
            if gameLogic.isThreeOfAKind(hand):
                self.type = 2
            else:
                self.type = 6
        elif self.nCards == 4:
            if gameLogic.isFourOfAKind(hand):
                self.type = 3
            else:
                self.type = 6
        elif self.nCards == 5:
            self.type = 6
        elif self.nCards == 6:
            if gameLogic.isThreePines(hand):
                self.type = 4
            else:
                self.type = 6
        elif self.nCards == 8:
            if gameLogic.isFourPines(hand):
                self.type = 5
            else:
                self.type = 6
        else:
            self.type = 6


class big2Game:
    def __init__(self):
        self.reset()

    def reset(self):
        shuffledDeck = np.random.permutation(52) + 1  # sáo bài
        # hand out cards to each player
        self.currentHands = {}
        self.currentHands[1] = np.sort(shuffledDeck[0:13])
        self.currentHands[2] = np.sort(shuffledDeck[13:26])
        self.currentHands[3] = np.sort(shuffledDeck[26:39])
        self.currentHands[4] = np.sort(shuffledDeck[39:52])
        self.cardsPlayed = np.zeros((4, 52), dtype=int)
        self.firstStep = True
        self.firstAction = False
        # who has 3D - this gets played H -> D -> C -> S
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
        #self.currentHands[whoHas3D] = self.currentHands[whoHas3D][1:]
        #self.cardsPlayed[whoHas3D-1][0] = 1
        self.goIndex = 1  # sử dụng trong handsPlayed
        self.handsPlayed = {}  # đây là dictionary
        #self.handsPlayed[self.goIndex] = handPlayed([1],whoHas3D)
        #self.goIndex += 1
        self.playersGo = whoHas3D
        #print(self.currentHands[self.playersGo])
        # self.playersGo = whoHas3D + 1 # người chơi tiếp theo
        # if self.playersGo == 5:
        #    self.playersGo = 1
        self.passCount = 0  # dont understand maybe đếm số lần bỏ lượt
        self.control = 0  # 1 player có thể có quyền kiểm soát
        self.noTurn = {0: False, 1: False, 2: False, 3: False,
                       4: False}  # 0 chèn vào để bắt đầu từ 1->4
        self.playerFinish = {0: False, 1: False, 2: False, 3: False, 4: False}
        self.numberOfOutput = {}
        self.neuralNetworkInputs = {}  # các A.I. player
        # pair, thereofkine, fourofkind, theepines, fouroines , threeStraight , four.., five..., sex...
        self.numberOfOutput[2] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.numberOfOutput[3] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.numberOfOutput[4] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        # số sảnh bải từng đánh gồm 2->13
        self.numberOfOutput[1] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        # np.zeros((412,)) 1 vector đầu vào của mạng netron
        self.neuralNetworkInputs[1] = np.zeros((732,), dtype=int)
        self.neuralNetworkInputs[2] = np.zeros((732,), dtype=int)
        self.neuralNetworkInputs[3] = np.zeros((732,), dtype=int)
        self.neuralNetworkInputs[4] = np.zeros((732,), dtype=int)
        nPlayerInd = 33*13
        nnPlayerInd = nPlayerInd + 71
        nnnPlayerInd = nnPlayerInd + 71
        """
        chưa hiểu đoạn này nó viết cái gì nữa
        """
        # initialize number of cards
        for i in range(1, 5):  # 1,2,3,4
            self.neuralNetworkInputs[i][nPlayerInd+13] = 1
            self.neuralNetworkInputs[i][nnPlayerInd+13] = 1
            self.neuralNetworkInputs[i][nnnPlayerInd+13] = 1
        self.fillNeuralNetworkHand(1)
        self.fillNeuralNetworkHand(2)
        self.fillNeuralNetworkHand(3)
        self.fillNeuralNetworkHand(4)
        # self.updateNeuralNetworkInputs(np.array([1]),whoHas3D)
        self.gameOver = 0
        self.positionFinish = np.zeros((4,))
        self.rewards = np.zeros((4,))
        self.goCounter = 0  # đếm số bước đi

    def resetCanPlay(self):
        self.canPlay[1] = True
        self.canPlay[2] = True
        self.canPlay[3] = True
        self.canPlay[4] = True

    def fillNeuralNetworkHand(self, player):  # table 1
        handOptions = gameLogic.handsAvailable(self.currentHands[player])
        sInd = 0
        self.neuralNetworkInputs[player][sInd:33*13] = 0
        for i in range(len(self.currentHands[player])):
            card = handOptions.cards[self.currentHands[player][i]]
            value = card.value
            suit = card.suit
            self.neuralNetworkInputs[player][sInd+int(value)-1] = 1
            if suit == 1:
                self.neuralNetworkInputs[player][sInd+13] = 1
            elif suit == 2:
                self.neuralNetworkInputs[player][sInd+14] = 1
            elif suit == 3:
                self.neuralNetworkInputs[player][sInd+15] = 1
            else:
                self.neuralNetworkInputs[player][sInd+16] = 1
            if card.inPair:
                self.neuralNetworkInputs[player][sInd+17] = 1
            if card.inThreeOfAKind:
                self.neuralNetworkInputs[player][sInd+18] = 1
            if card.inFourOfAKind:
                self.neuralNetworkInputs[player][sInd+19] = 1
            if card.inThreePines:
                self.neuralNetworkInputs[player][sInd+20] = 1
            if card.inFourPines:
                self.neuralNetworkInputs[player][sInd+21] = 1
            for i in range(len(card.inStraight)):
                if card.inStraight[i]:
                    self.neuralNetworkInputs[player][sInd+22+i] = 1
            sInd += 33

    def updateTurnAndFinish(self, cPlayer):
        phInd = 33*13 + 71 + 71 + 71 + 44
        nPlayer = cPlayer-1
        if nPlayer == 0:
            nPlayer = 4
        nnPlayer = nPlayer - 1
        if nnPlayer == 0:
            nnPlayer = 4
        nnnPlayer = nnPlayer - 1
        if nnnPlayer == 0:
            nnnPlayer = 4
        for i in [nPlayer, nnPlayer, nnnPlayer, cPlayer]:
            if self.noTurn[i] == True:
                self.neuralNetworkInputs[i][phInd+38] = 1
            if self.noTurn[i] == False:
                self.neuralNetworkInputs[i][phInd+38] = 0
            if self.playerFinish[i] == True:
                self.neuralNetworkInputs[i][phInd+42] = 1
            if self.playerFinish[i] == False:
                self.neuralNetworkInputs[i][phInd+42] = 0
            ni = i + 1
            if ni == 5:
                ni = 1
            if self.noTurn[ni] == True:
                self.neuralNetworkInputs[i][phInd+39] = 1
            if self.noTurn[ni] == False:
                self.neuralNetworkInputs[i][phInd+39] = 0
            if self.playerFinish[ni] == True:
                self.neuralNetworkInputs[i][phInd+43] = 1
            if self.playerFinish[ni] == False:
                self.neuralNetworkInputs[i][phInd+43] = 0
            nni = ni + 1
            if nni == 5:
                nni = 1
            if self.noTurn[nni] == True:
                self.neuralNetworkInputs[i][phInd+40] = 1
            if self.noTurn[nni] == False:
                self.neuralNetworkInputs[i][phInd+40] = 0
            if self.playerFinish[nni] == True:
                self.neuralNetworkInputs[i][phInd+44] = 1
            if self.playerFinish[nni] == False:
                self.neuralNetworkInputs[i][phInd+44] = 0
            nnni = nni + 1
            if nnni == 5:
                nnni = 1
            if self.noTurn[nnni] == True:
                self.neuralNetworkInputs[i][phInd+41] = 1
            if self.noTurn[nnni] == False:
                self.neuralNetworkInputs[i][phInd+41] = 0
            if self.playerFinish[nnni] == True:
                self.neuralNetworkInputs[i][phInd+45] = 1
            if self.playerFinish[nnni] == False:
                self.neuralNetworkInputs[i][phInd+45] = 0

    def updateNeuralNetworkPass(self, cPlayer):
        # this is a bit of a mess tbh, some things are unnecessary.
        phInd = 33*13 + 71 + 71 + 71 + 44
        nPlayer = cPlayer-1
        if nPlayer == 0:
            nPlayer = 4
        nnPlayer = nPlayer - 1
        if nnPlayer == 0:
            nnPlayer = 4
        nnnPlayer = nnPlayer - 1
        if nnnPlayer == 0:
            nnnPlayer = 4
        if self.passCount < 2:
            # no control - prev hands remain same
            self.neuralNetworkInputs[nPlayer][phInd+35:] = 0
            self.neuralNetworkInputs[nnPlayer][phInd+35:] = 0
            self.neuralNetworkInputs[nnnPlayer][phInd+35:] = 0
            if self.passCount == 0:
                self.neuralNetworkInputs[nPlayer][phInd+36] = 1
                self.neuralNetworkInputs[nnPlayer][phInd+36] = 1
                self.neuralNetworkInputs[nnnPlayer][phInd+36] = 1
            else:
                self.neuralNetworkInputs[nPlayer][phInd+37] = 1
                self.neuralNetworkInputs[nnPlayer][phInd+37] = 1
                self.neuralNetworkInputs[nnnPlayer][phInd+37] = 1
        else:  # passCount == 3            #next player is gaining control.
            self.neuralNetworkInputs[nPlayer][phInd:] = 0
            self.neuralNetworkInputs[nnPlayer][phInd:] = 0
            self.neuralNetworkInputs[nnnPlayer][phInd:] = 0
            self.neuralNetworkInputs[nnnPlayer][phInd+34] = 1  # maybe control

    def updateNeuralNetworkInputs(self, prevHand, cPlayer):
        """
        cPlayer mean current player, table 2 and table 4, update info
        """
        self.fillNeuralNetworkHand(
            cPlayer)  # có vẽ không cập nhật bảng 3 của current player
        nPlayer = cPlayer-1  # đi theo chiều dảm dần
        if nPlayer == 0:
            nPlayer = 4
        nnPlayer = nPlayer - 1
        if nnPlayer == 0:
            nnPlayer = 4
        nnnPlayer = nnPlayer - 1
        if nnnPlayer == 0:
            nnnPlayer = 4
        nCards = self.currentHands[cPlayer].size
        cardsOfNote = np.intersect1d(prevHand, np.arange(29, 53))  # 10 đến heo
        nPlayerInd = 33*13
        nnPlayerInd = nPlayerInd + 71
        nnnPlayerInd = nnPlayerInd + 71
        # next player
        self.neuralNetworkInputs[nPlayer][nPlayerInd:(nPlayerInd+13)] = 0
        self.neuralNetworkInputs[nPlayer][nPlayerInd +
                                          nCards-1] = 1  # number of cards
        # next next player
        self.neuralNetworkInputs[nnPlayer][nnPlayerInd:(nnPlayerInd+13)] = 0
        self.neuralNetworkInputs[nnPlayer][nnPlayerInd + nCards-1] = 1
        # next next next player
        self.neuralNetworkInputs[nnnPlayer][nnnPlayerInd:(nnnPlayerInd+13)] = 0
        self.neuralNetworkInputs[nnnPlayer][nnnPlayerInd + nCards-1] = 1
        for val in cardsOfNote:
            self.neuralNetworkInputs[nPlayer][nPlayerInd+13+(val-29)] = 1
            self.neuralNetworkInputs[nnPlayer][nnPlayerInd+13+(val-29)] = 1
            self.neuralNetworkInputs[nnnPlayer][nnnPlayerInd+13+(val-29)] = 1
        # prevHand table 2 and table 3
        phInd = nnnPlayerInd + 71 + 44
        self.neuralNetworkInputs[nPlayer][phInd:] = 0
        self.neuralNetworkInputs[nnPlayer][phInd:] = 0
        self.neuralNetworkInputs[nnnPlayer][phInd:] = 0
        self.neuralNetworkInputs[cPlayer][phInd:] = 0
        nCards = prevHand.size
        if nCards == 2:
            self.numberOfOutput[cPlayer][nCards-2] += 1
            self.neuralNetworkInputs[nPlayer][nPlayerInd+37:nPlayerInd+43] = 0
            self.neuralNetworkInputs[nnPlayer][nnPlayerInd +
                                               37:nPlayerInd+43] = 0
            self.neuralNetworkInputs[nnnPlayer][nnnPlayerInd +
                                                37:nPlayerInd+43] = 0
            self.neuralNetworkInputs[nPlayer][nPlayerInd +
                                              37+self.numberOfOutput[cPlayer][nCards-2]-1] = 1
            self.neuralNetworkInputs[nnPlayer][nnPlayerInd +
                                               37+self.numberOfOutput[cPlayer][nCards-2]-1] = 1
            self.neuralNetworkInputs[nnnPlayer][nnnPlayerInd +
                                                37+self.numberOfOutput[cPlayer][nCards-2]-1] = 1
            value = int(gameLogic.cardValue(prevHand[1]))
            suit = prevHand[1] % 4
            # pair
            self.neuralNetworkInputs[nPlayer][phInd+18] = 1
            self.neuralNetworkInputs[nnPlayer][phInd+18] = 1
            self.neuralNetworkInputs[nnnPlayer][phInd+18] = 1
        elif nCards == 3:
            if gameLogic.isThreeOfAKind(prevHand):
                self.numberOfOutput[cPlayer][nCards-2] += 1
                self.neuralNetworkInputs[nPlayer][nPlayerInd +
                                                  43:nPlayerInd+47] = 0
                self.neuralNetworkInputs[nnPlayer][nnPlayerInd +
                                                   43:nPlayerInd+47] = 0
                self.neuralNetworkInputs[nnnPlayer][nnnPlayerInd +
                                                    43:nPlayerInd+47] = 0
                self.neuralNetworkInputs[nPlayer][nPlayerInd +
                                                  43+self.numberOfOutput[cPlayer][nCards-2]-1] = 1
                self.neuralNetworkInputs[nnPlayer][nnPlayerInd +
                                                   43+self.numberOfOutput[cPlayer][nCards-2]-1] = 1
                self.neuralNetworkInputs[nnnPlayer][nnnPlayerInd +
                                                    43+self.numberOfOutput[cPlayer][nCards-2]-1] = 1
                value = int(gameLogic.cardValue(prevHand[2]))
                suit = prevHand[2] % 4
                self.neuralNetworkInputs[nPlayer][phInd+19] = 1
                self.neuralNetworkInputs[nnPlayer][phInd+19] = 1
                self.neuralNetworkInputs[nnnPlayer][phInd+19] = 1
            else:  # three straight
                self.numberOfOutput[cPlayer][nCards+2] += 1
                self.neuralNetworkInputs[nPlayer][nPlayerInd +
                                                  53:nPlayerInd+57] = 0
                self.neuralNetworkInputs[nnPlayer][nnPlayerInd +
                                                   53:nPlayerInd+57] = 0
                self.neuralNetworkInputs[nnnPlayer][nnnPlayerInd +
                                                    53:nPlayerInd+57] = 0
                self.neuralNetworkInputs[nPlayer][nPlayerInd +
                                                  53+self.numberOfOutput[cPlayer][nCards+2]-1] = 1
                self.neuralNetworkInputs[nnPlayer][nnPlayerInd +
                                                   53+self.numberOfOutput[cPlayer][nCards+2]-1] = 1
                self.neuralNetworkInputs[nnnPlayer][nnnPlayerInd +
                                                    53+self.numberOfOutput[cPlayer][nCards+2]-1] = 1
                value = int(gameLogic.cardValue(prevHand[2]))
                suit = prevHand[2] % 4
                self.neuralNetworkInputs[nPlayer][phInd+23] = 1
                self.neuralNetworkInputs[nnPlayer][phInd+23] = 1
                self.neuralNetworkInputs[nnnPlayer][phInd+23] = 1
        elif nCards == 4:
            if gameLogic.isFourOfAKind(prevHand):
                self.numberOfOutput[cPlayer][nCards-2] += 1
                self.neuralNetworkInputs[nPlayer][nPlayerInd +
                                                  47:nPlayerInd+50] = 0
                self.neuralNetworkInputs[nnPlayer][nnPlayerInd +
                                                   47:nPlayerInd+50] = 0
                self.neuralNetworkInputs[nnnPlayer][nnnPlayerInd +
                                                    47:nPlayerInd+50] = 0
                self.neuralNetworkInputs[nPlayer][nPlayerInd +
                                                  47+self.numberOfOutput[cPlayer][nCards-2]-1] = 1
                self.neuralNetworkInputs[nnPlayer][nnPlayerInd +
                                                   47+self.numberOfOutput[cPlayer][nCards-2]-1] = 1
                self.neuralNetworkInputs[nnnPlayer][nnnPlayerInd +
                                                    47+self.numberOfOutput[cPlayer][nCards-2]-1] = 1
                value = int(gameLogic.cardValue(prevHand[3]))
                suit = prevHand[3] % 4
                self.neuralNetworkInputs[nPlayer][phInd+20] = 1
                self.neuralNetworkInputs[nnPlayer][phInd+20] = 1
                self.neuralNetworkInputs[nnnPlayer][phInd+20] = 1
            else:  # four straight
                self.numberOfOutput[cPlayer][nCards+2] += 1
                self.neuralNetworkInputs[nPlayer][nPlayerInd +
                                                  57:nPlayerInd+60] = 0
                self.neuralNetworkInputs[nnPlayer][nnPlayerInd +
                                                   57:nPlayerInd+60] = 0
                self.neuralNetworkInputs[nnnPlayer][nnnPlayerInd +
                                                    57:nPlayerInd+60] = 0
                self.neuralNetworkInputs[nPlayer][nPlayerInd +
                                                  57+self.numberOfOutput[cPlayer][nCards+2]-1] = 1
                self.neuralNetworkInputs[nnPlayer][nnPlayerInd +
                                                   57+self.numberOfOutput[cPlayer][nCards+2]-1] = 1
                self.neuralNetworkInputs[nnnPlayer][nnnPlayerInd +
                                                    57+self.numberOfOutput[cPlayer][nCards+2]-1] = 1
                value = int(gameLogic.cardValue(prevHand[3]))
                suit = prevHand[3] % 4
                self.neuralNetworkInputs[nPlayer][phInd+24] = 1
                self.neuralNetworkInputs[nnPlayer][phInd+24] = 1
                self.neuralNetworkInputs[nnnPlayer][phInd+24] = 1
        elif nCards == 5:
            self.numberOfOutput[cPlayer][nCards+2] += 1
            self.neuralNetworkInputs[nPlayer][nPlayerInd+60:nPlayerInd+62] = 0
            self.neuralNetworkInputs[nnPlayer][nnPlayerInd +
                                               60:nPlayerInd+62] = 0
            self.neuralNetworkInputs[nnnPlayer][nnnPlayerInd +
                                                60:nPlayerInd+62] = 0
            self.neuralNetworkInputs[nPlayer][nPlayerInd +
                                              62+self.numberOfOutput[cPlayer][nCards+2]-1] = 1
            self.neuralNetworkInputs[nnPlayer][nnPlayerInd +
                                               62+self.numberOfOutput[cPlayer][nCards+2]-1] = 1
            self.neuralNetworkInputs[nnnPlayer][nnnPlayerInd +
                                                62+self.numberOfOutput[cPlayer][nCards+2]-1] = 1
            value = int(gameLogic.cardValue(prevHand[4]))
            suit = prevHand[4] % 4
            self.neuralNetworkInputs[nPlayer][phInd+25] = 1
            self.neuralNetworkInputs[nnPlayer][phInd+25] = 1
            self.neuralNetworkInputs[nnnPlayer][phInd+25] = 1
        elif nCards == 6:
            if gameLogic.isThreePines(prevHand):
                self.numberOfOutput[cPlayer][nCards-2] += 1
                self.neuralNetworkInputs[nPlayer][nPlayerInd +
                                                  50:nPlayerInd+52] = 0
                self.neuralNetworkInputs[nnPlayer][nnPlayerInd +
                                                   50:nPlayerInd+52] = 0
                self.neuralNetworkInputs[nnnPlayer][nnnPlayerInd +
                                                    50:nPlayerInd+52] = 0
                self.neuralNetworkInputs[nPlayer][nPlayerInd +
                                                  50+self.numberOfOutput[cPlayer][nCards-2]-1] = 1
                self.neuralNetworkInputs[nnPlayer][nnPlayerInd +
                                                   50+self.numberOfOutput[cPlayer][nCards-2]-1] = 1
                self.neuralNetworkInputs[nnnPlayer][nnnPlayerInd +
                                                    50+self.numberOfOutput[cPlayer][nCards-2]-1] = 1
                value = int(gameLogic.cardValue(prevHand[5]))
                suit = prevHand[5] % 4
                self.neuralNetworkInputs[nPlayer][phInd+21] = 1
                self.neuralNetworkInputs[nnPlayer][phInd+21] = 1
                self.neuralNetworkInputs[nnnPlayer][phInd+21] = 1
            else:  # six straight
                self.numberOfOutput[cPlayer][nCards+2] += 1
                self.neuralNetworkInputs[nPlayer][nPlayerInd +
                                                  62:nPlayerInd+64] = 0
                self.neuralNetworkInputs[nnPlayer][nnPlayerInd +
                                                   62:nPlayerInd+64] = 0
                self.neuralNetworkInputs[nnnPlayer][nnnPlayerInd +
                                                    62:nPlayerInd+64] = 0
                self.neuralNetworkInputs[nPlayer][nPlayerInd +
                                                  62+self.numberOfOutput[cPlayer][nCards+2]-1] = 1
                self.neuralNetworkInputs[nnPlayer][nnPlayerInd +
                                                   62+self.numberOfOutput[cPlayer][nCards+2]-1] = 1
                self.neuralNetworkInputs[nnnPlayer][nnnPlayerInd +
                                                    62+self.numberOfOutput[cPlayer][nCards+2]-1] = 1
                value = int(gameLogic.cardValue(prevHand[3]))
                suit = prevHand[3] % 4
                self.neuralNetworkInputs[nPlayer][phInd+26] = 1
                self.neuralNetworkInputs[nnPlayer][phInd+26] = 1
                self.neuralNetworkInputs[nnnPlayer][phInd+26] = 1
        elif nCards == 7:
            self.neuralNetworkInputs[nPlayer][nPlayerInd+64] = 1
            self.neuralNetworkInputs[nnPlayer][nnPlayerInd+64] = 1
            self.neuralNetworkInputs[nnnPlayer][nnnPlayerInd+64] = 1
            value = int(gameLogic.cardValue(prevHand[7]))
            suit = prevHand[7] % 4
            self.neuralNetworkInputs[nPlayer][phInd+27] = 1
            self.neuralNetworkInputs[nnPlayer][phInd+27] = 1
            self.neuralNetworkInputs[nnnPlayer][phInd+27] = 1
        elif nCards == 8:
            if gameLogic.isFourPines(prevHand):
                self.numberOfOutput[cPlayer][nCards-2] += 1
                self.neuralNetworkInputs[nPlayer][nPlayerInd+52] = 0
                self.neuralNetworkInputs[nnPlayer][nnPlayerInd+52] = 0
                self.neuralNetworkInputs[nnnPlayer][nnnPlayerInd+52] = 0
                self.neuralNetworkInputs[nPlayer][nPlayerInd+52] = 1
                self.neuralNetworkInputs[nnPlayer][nnPlayerInd+52] = 1
                self.neuralNetworkInputs[nnnPlayer][nnnPlayerInd+52] = 1
                value = int(gameLogic.cardValue(prevHand[7]))
                suit = prevHand[7] % 4
                self.neuralNetworkInputs[nPlayer][phInd+22] = 1
                self.neuralNetworkInputs[nnPlayer][phInd+22] = 1
                self.neuralNetworkInputs[nnnPlayer][phInd+22] = 1
            else:  # four straight
                self.neuralNetworkInputs[nPlayer][nPlayerInd+43] = 1
                self.neuralNetworkInputs[nnPlayer][nnPlayerInd+43] = 1
                self.neuralNetworkInputs[nnnPlayer][nnnPlayerInd+43] = 1
                value = int(gameLogic.cardValue(prevHand[7]))
                suit = prevHand[7] % 4
                self.neuralNetworkInputs[nPlayer][phInd+28] = 1
                self.neuralNetworkInputs[nnPlayer][phInd+28] = 1
                self.neuralNetworkInputs[nnnPlayer][phInd+28] = 1
        elif nCards > 8:
            plus = nCards - 8
            self.neuralNetworkInputs[nPlayer][nPlayerInd+64+plus] = 1
            self.neuralNetworkInputs[nnPlayer][nnPlayerInd+64+plus] = 1
            self.neuralNetworkInputs[nnnPlayer][nnnPlayerInd+64+plus] = 1
            value = int(gameLogic.cardValue(prevHand[nCards-1]))
            suit = prevHand[nCards-1] % 4
            self.neuralNetworkInputs[nPlayer][phInd+27+plus] = 1
            self.neuralNetworkInputs[nnPlayer][phInd+27+plus] = 1
            self.neuralNetworkInputs[nnnPlayer][phInd+27+plus] = 1
        else:
            value = int(gameLogic.cardValue(prevHand[0]))
            suit = prevHand[0] % 4
            self.neuralNetworkInputs[nPlayer][phInd+17] = 1
            self.neuralNetworkInputs[nnPlayer][phInd+17] = 1
            self.neuralNetworkInputs[nnnPlayer][phInd+17] = 1
        self.neuralNetworkInputs[nPlayer][phInd+value-1] = 1
        self.neuralNetworkInputs[nnPlayer][phInd+value-1] = 1
        self.neuralNetworkInputs[nnnPlayer][phInd+value-1] = 1
        if suit == 1:
            self.neuralNetworkInputs[nPlayer][phInd+13] = 1
            self.neuralNetworkInputs[nnPlayer][phInd+13] = 1
            self.neuralNetworkInputs[nnnPlayer][phInd+13] = 1
        elif suit == 2:
            self.neuralNetworkInputs[nPlayer][phInd+14] = 1
            self.neuralNetworkInputs[nnPlayer][phInd+14] = 1
            self.neuralNetworkInputs[nnnPlayer][phInd+14] = 1
        elif suit == 3:
            self.neuralNetworkInputs[nPlayer][phInd+15] = 1
            self.neuralNetworkInputs[nnPlayer][phInd+15] = 1
            self.neuralNetworkInputs[nnnPlayer][phInd+15] = 1
        elif suit == 0:
            self.neuralNetworkInputs[nPlayer][phInd+16] = 1
            self.neuralNetworkInputs[nnPlayer][phInd+16] = 1
            self.neuralNetworkInputs[nnnPlayer][phInd+16] = 1
        # update turn and finish
        self.updateTurnAndFinish(cPlayer)
        # general - common to all hands.
        cardsRecord = np.intersect1d(prevHand, np.arange(37, 53))
        endInd = nnnPlayerInd + 71
        for val in cardsRecord:
            self.neuralNetworkInputs[1][endInd+(val-37)] = 1
            self.neuralNetworkInputs[2][endInd+(val-37)] = 1
            self.neuralNetworkInputs[3][endInd+(val-37)] = 1
            self.neuralNetworkInputs[4][endInd+(val-37)] = 1
        # no passes.
        self.neuralNetworkInputs[nPlayer][phInd+35] = 1
        self.neuralNetworkInputs[nnPlayer][phInd+35] = 1
        self.neuralNetworkInputs[nnnPlayer][phInd+35] = 1
        self.neuralNetworkInputs[nPlayer][phInd+36:] = 0
        self.neuralNetworkInputs[nnPlayer][phInd+36:] = 0
        self.neuralNetworkInputs[nnnPlayer][phInd+36:] = 0

    def updateGame(self, option, nCards=0):
        self.goCounter += 1
        self.firstStep = False
        if option == -1 or option == -2 or option == -3:
            # cPlayer pass
            cPlayer = self.playersGo
            self.updateNeuralNetworkPass(cPlayer)
            for i in range(0, 4):
                self.playersGo += 1
                if self.playersGo == 5:
                    self.playersGo = 1
                if self.noTurn[self.playersGo] == False:
                    break
                if self.playerFinish[self.playersGo] == False:
                    break
            self.passCount += 1
            self.noTurn[cPlayer] = True
            if self.passCount == 3:
                self.control = 1
                self.resetCanPlay()
                self.passCount = 0
            self.updateTurnAndFinish(cPlayer)
            return
        self.passCount = 0
        # handToPlay mean : nhưng lá bài được chơi
        if nCards == 1:
            handToPlay = np.array([self.currentHands[self.playersGo][option]])
        elif nCards == 2:
            handToPlay = self.currentHands[self.playersGo][enumerateOptions.inverseTwoCardIndices[option]]
        elif nCards == 3:
            handToPlay = self.currentHands[self.playersGo][enumerateOptions.inverseThreeCardIndices[option]]
        elif nCards == 4:
            handToPlay = self.currentHands[self.playersGo][enumerateOptions.inverseFourCardIndices[option]]
        elif nCards == 5:
            handToPlay = self.currentHands[self.playersGo][enumerateOptions.inverseFiveCardIndices[option]]
        elif nCards == 6:
            handToPlay = self.currentHands[self.playersGo][enumerateOptions.inverseSixCardIndices[option]]
        elif nCards == 7:
            handToPlay = self.currentHands[self.playersGo][np.array(
                enumerateOptions.sevenCardIndices[option])]
        elif nCards == 8:
            handToPlay = self.currentHands[self.playersGo][np.array(
                enumerateOptions.eightCardIndices[option])]
        elif nCards == 9:
            handToPlay = self.currentHands[self.playersGo][np.array(
                enumerateOptions.nineCardIndices[option])]
        elif nCards == 10:
            handToPlay = self.currentHands[self.playersGo][np.array(
                enumerateOptions.tenCardIndices[option])]
        elif nCards == 11:
            handToPlay = self.currentHands[self.playersGo][np.array(
                enumerateOptions.elevenCardIndices[option])]
        elif nCards == 12:
            handToPlay = self.currentHands[self.playersGo][np.array(
                enumerateOptions.twelveCardIndices[option])]
        else:
            handToPlay = self.currentHands[self.playersGo][np.array(
                enumerateOptions.thirTeenCardIndices[option])]
        for i in handToPlay:
            self.cardsPlayed[self.playersGo-1][i-1] = 1
        #print(handToPlay)
        self.handsPlayed[self.goIndex] = handPlayed(
            handToPlay, self.playersGo)  # hand là chuổi các cards
        self.control = 0
        self.goIndex += 1
        self.currentHands[self.playersGo] = np.setdiff1d(
            self.currentHands[self.playersGo], handToPlay)
        """
        most important set how to end game
        """
        if self.currentHands[self.playersGo].size == 0:
            self.assignRewards()
            if self.gameOver == 1:
                return
        self.updateNeuralNetworkInputs(handToPlay, self.playersGo)
        for i in range(0, 4):
            self.playersGo += 1
            if self.playersGo == 5:
                self.playersGo = 1
            if self.noTurn[self.playersGo] == False:
                break
            if self.playerFinish[self.playersGo] == False:
                break

    def assignRewards(self):
        numberDone = 4
        for i in self.positionFinish:
            if i != 0:
                numberDone += 1
        if(numberDone == 4):
            self.gameOver = 1
        self.positionFinish[self.playersGo] = numberDone + 1
        if self.gameOver == 1:
            for i in range(self.positionFinish.size):
                if self.positionFinish[i] == 1:
                    self.rewards[i] == 20
                elif self.positionFinish[i] == 2:
                    self.rewards[i] == 10
                elif self.positionFinish[i] == 3:
                    self.rewards[i] == -10
                elif self.positionFinish[i] == 4:
                    self.rewards[i] == -20

    def returnAvailableActions(self):
        if self.firstStep ==True and self.firstAction == False:
            currHand = self.currentHands[self.playersGo]
            handOptions = gameLogic.handsAvailable(currHand)
            availableActions = np.zeros(
                (enumerateOptions.nActions[-1]+1,))  # +1 pass
            options = enumerateOptions.firstPlayerOptions(currHand,handOptions)
            if isinstance(options, int):  # no options - must pass
                if self.firstStep != False: # khÓ xảy ra
                    return availableActions
            for option in options:
                availableActions[option] = 1
            return availableActions
        else:
            currHand = self.currentHands[self.playersGo]
            handOptions = gameLogic.handsAvailable(currHand)
            # +1 pass +2 noTurn +3 doneFinsh
            availableActions = np.zeros((enumerateOptions.nActions[-1]+1,))
            if self.control == 0:
                # allow pass action
                availableActions[enumerateOptions.passInd] = 1

                # goIndex có lưu pass không
                prevHand = self.handsPlayed[self.goIndex-1].hand
                nCardsToBeat = len(prevHand)

                if nCardsToBeat > 1:
                    handOptions = gameLogic.handsAvailable(currHand)

                if nCardsToBeat == 1:
                    options = enumerateOptions.oneCardOptions(
                        currHand, handOptions, prevHand, 1)
                elif nCardsToBeat == 2:
                    options = enumerateOptions.twoCardOptions(
                        handOptions, prevHand, 1)
                elif nCardsToBeat == 3:
                    if gameLogic.isStraight(prevHand)[0]:
                        options = enumerateOptions.threeCardOptions(
                            handOptions, prevHand, 1)
                    if gameLogic.isThreeOfAKind(prevHand):
                        options = enumerateOptions.threeCardOptions(
                            handOptions, prevHand, 2)
                elif nCardsToBeat == 4:
                    if gameLogic.isStraight(prevHand)[0]:
                        options = enumerateOptions.fourCardOptions(
                            handOptions, prevHand, 1)
                    if gameLogic.isFourOfAKind(prevHand):
                        options = enumerateOptions.fourCardOptions(
                            handOptions, prevHand, 2)
                elif nCardsToBeat == 5:
                    options = enumerateOptions.fiveCardOptions(
                        handOptions, prevHand, 1)
                elif nCardsToBeat == 6:
                    if gameLogic.isStraight(prevHand)[0]:
                        options = enumerateOptions.sixCardOptions(
                            handOptions, prevHand, 1)
                    if gameLogic.isThreePines(prevHand):
                        options = enumerateOptions.sixCardOptions(
                            handOptions, prevHand, 2)
                else:
                    if gameLogic.isStraight(prevHand)[0]:
                        options = enumerateOptions.greaterSixCardOptions(
                            handOptions, prevHand, 1)
                    if gameLogic.isFourPines(prevHand):
                        options = enumerateOptions.greaterSixCardOptions(
                            handOptions, prevHand, 2)

                if isinstance(options, int):  # no options - must pass
                    return availableActions

                for option in options:
                    # index = enumerateOptions.getIndex(option, nCardsToBeat)
                    availableActions[option] = 1

                return availableActions

            else:  # player has control.
                handOptions = gameLogic.handsAvailable(currHand)
                oneCardOptions = enumerateOptions.oneCardOptions(
                    currHand, handOptions)
                twoCardOptions = enumerateOptions.twoCardOptions(handOptions)
                threeCardOptions = enumerateOptions.threeCardOptions(
                    handOptions)
                fourCardOptions = enumerateOptions.fourCardOptions(handOptions)
                fiveCardOptions = enumerateOptions.fiveCardOptions(handOptions)
                sixCardOptions = enumerateOptions.sixCardOptions(handOptions)
                greaterSixCardOptions = enumerateOptions.greaterSixCardOptions(
                    handOptions)

                for option in oneCardOptions:
                    availableActions[option] = 1

                if not isinstance(twoCardOptions, int):
                    for option in twoCardOptions:
                        availableActions[option] = 1

                if not isinstance(threeCardOptions, int):
                    for option in threeCardOptions:
                        availableActions[option] = 1

                if not isinstance(fourCardOptions, int):
                    for option in fourCardOptions:
                        availableActions[option] = 1

                if not isinstance(fiveCardOptions, int):
                    for option in fiveCardOptions:
                        availableActions[option] = 1
                if not isinstance(sixCardOptions, int):
                    for option in fiveCardOptions:
                        availableActions[option] = 1
                if not isinstance(greaterSixCardOptions, int):
                    for option in fiveCardOptions:
                        availableActions[option] = 1

                return availableActions

    def step(self, action):
        opt, nC = enumerateOptions.getOptionNC(action)
        self.updateGame(opt, nC)
        """
        opt mean options
        nC mean number Cards
        getOptionNC được sử dụng ngược với hàm index
        """
        if self.gameOver == 0:
            reward = None
            done = False
            info = {}
            info['Position result'] = self.positionFinish

        else:
            reward = self.rewards
            done = True
            info = {}
            info['numTurns'] = self.goCounter
            info['rewards'] = self.rewards
            # what else is worth monitoring?
            self.reset()
        return reward, done, info

    def getCurrentState(self):
        #return self.playersGo, self.neuralNetworkInputs[self.playersGo].reshape(1, 732), convertAvailableActions(self.returnAvailableActions()).reshape(1,8032)
        return self.playersGo, self.neuralNetworkInputs[self.playersGo].reshape(1, 732), self.returnAvailableActions().reshape(1,8032)


# now create a vectorized environment
def worker(remote, parent_remote):
    parent_remote.close()
    game = big2Game()
    while True:
        cmd, data = remote.recv()
        if cmd == 'step':
            reward, done, info = game.step(data)
            remote.send((reward, done, info))
        elif cmd == 'reset':
            game.reset()
            pGo, cState, availAcs = game.getCurrentState()
            remote.send((pGo, cState))
        elif cmd == 'getCurrState':
            pGo, cState, availAcs = game.getCurrentState()
            remote.send((pGo, cState, availAcs))
        elif cmd == 'close':
            remote.close()
            break
        else:
            print("Invalid command sent by remote")
            break


class vectorizedBig2Games(object):
    def __init__(self, nGames):

        self.waiting = False
        self.closed = False
        self.remotes, self.work_remotes = zip(*[Pipe() for _ in range(nGames)])
        self.ps = [Process(target=worker, args=(work_remote, remote)) for (
            work_remote, remote) in zip(self.work_remotes, self.remotes)]

        for p in self.ps:
            p.daemon = True
            p.start()
        for remote in self.work_remotes:
            remote.close()

    def step_async(self, actions):
        for remote, action in zip(self.remotes, actions):
            remote.send(('step', action))
        self.waiting = True

    def step_wait(self):
        results = [remote.recv() for remote in self.remotes]
        self.waiting = False
        rewards, dones, infos = zip(*results)
        return rewards, dones, infos

    def step(self, actions):
        self.step_async(actions)
        return self.step_wait()

    def currStates_async(self):
        for remote in self.remotes:
            remote.send(('getCurrState', None))
        self.waiting = True

    def currStates_wait(self):
        results = [remote.recv() for remote in self.remotes]
        self.waiting = False
        pGos, currStates, currAvailAcs = zip(*results)
        return np.stack(pGos), np.stack(currStates), np.stack(currAvailAcs)

    def getCurrStates(self):
        self.currStates_async()
        return self.currStates_wait()

    def showInfo(self):
        pGos, currStates, currAvailAcs = self.getCurrStates()
        string = ""
        actions = []
        count = 0
        for i in range(0, 13*33, 33):
            countLoop = i
            string = string + str(i) + "["
            for j in range(countLoop, countLoop+13):
                if(currStates[j] == 1):
                    string = string + str(j-countLoop+3)
            for j in range(countLoop+13, countLoop+17):
                if(j == countLoop + 13):
                    string = string + str("S")
                elif(j == countLoop + 14):
                    string = string + str("C")
                elif(j == countLoop + 13):
                    string = string + str("D")
                elif(j == countLoop + 13):
                    string = string + str("H")
            count += 1
            string += "] "
        for i in range(currAvailAcs[:-1].size):
            if currAvailAcs[i] != 1:
                option, nC = enumerateOptions.getOptionNC(i)
                if nC == 1:
                    actions.append([option])
                elif nC == 2:
                    actions.append(
                        enumerateOptions.inverseTwoCardIndices[option])
                elif nC == 3:
                    actions.append(
                        enumerateOptions.inverseThreeCardIndices[option])
                elif nC == 4:
                    actions.append(
                        enumerateOptions.inverseFourCardIndices[option])
                elif nC == 5:
                    actions.append(
                        enumerateOptions.inverseFiveCardIndices[option])
                elif nC == 6:
                    actions.append(
                        enumerateOptions.inverseSixCardIndices[option])
                elif nC == 7:
                    actions.append(
                        np.array(enumerateOptions.sevenCardIndices[option]))
                elif nC == 8:
                    actions.append(
                        np.array(enumerateOptions.eightCardIndices[option]))
                elif nC == 9:
                    actions.append(
                        np.array(enumerateOptions.nineCardIndices[option]))
                elif nC == 10:
                    actions.append(
                        np.array(enumerateOptions.tenCardIndices[option]))
                elif nC == 11:
                    actions.append(
                        np.array(enumerateOptions.elevenCardIndices[option]))
                elif nC == 12:
                    actions.append(
                        np.array(enumerateOptions.twelveCardIndices[option]))
                else:
                    actions.append(
                        np.array(enumerateOptions.thirTeenCardIndices[option]))
        if currAvailAcs[-1] == 1:
            actions.append("Pass")

        return (pGos, string, actions)

    def close(self):
        if self.closed:
            return
        if self.waiting:
            for remote in self.remotes:
                remote.recv()
        for remote in self.remotes:
            remote.send(('close', None))
        for p in self.ps:
            p.join()
        self.closed = True


class vectorizedBig2GamesTest():
    def __init__(self):
        self.goForward = big2Game()
    def reset(self):
        self.goForward.reset()
    def step(self,action):
        a,b,c =  self.goForward.step(action)
        return a,b,c
    def getCurrentState(self):
        a,b,c =  self.goForward.getCurrentState()
        #print(self.goForward.getCurrentState())
        return a,b,c
    def info(self):
        pGos, currStates, currAvailAcs = self.goForward.getCurrentState()
        string = ""
        actions = []
        count = 0
        listAction = []
        for i in range(0, 13*33, 33):
            countLoop = i
            string = string + str(count) + "["
            for j in range(countLoop, countLoop+13):
                if(currStates[0][j] == 1):
                    string = string + str(j-countLoop+3)
            j = countLoop+13
            if(currStates[0][j]==1):
                string = string + str("S")
            elif(currStates[0][j+1]==1):
                string = string + str("C")
            elif(currStates[0][j+2]==1):
                string = string + str("D")
            elif(currStates[0][j+3]==1):
                string = string + str("H")
            count += 1
            string += "] "
        for i in range(currAvailAcs[0][:-1].size):
            if currAvailAcs[0][i] == 1:
                option, nC = enumerateOptions.getOptionNC(i)
                listAction.append(i)
                if nC == 1:
                    actions.append([option])
                elif nC == 2:
                    actions.append(
                        enumerateOptions.inverseTwoCardIndices[option])
                elif nC == 3:
                    actions.append(
                        enumerateOptions.inverseThreeCardIndices[option])
                elif nC == 4:
                    actions.append(
                        enumerateOptions.inverseFourCardIndices[option])
                elif nC == 5:
                    actions.append(
                        enumerateOptions.inverseFiveCardIndices[option])
                elif nC == 6:
                    actions.append(
                        enumerateOptions.inverseSixCardIndices[option])
                elif nC == 7:
                    actions.append(
                        np.array(enumerateOptions.sevenCardIndices[option]))
                elif nC == 8:
                    actions.append(
                        np.array(enumerateOptions.eightCardIndices[option]))
                elif nC == 9:
                    actions.append(
                        np.array(enumerateOptions.nineCardIndices[option]))
                elif nC == 10:
                    actions.append(
                        np.array(enumerateOptions.tenCardIndices[option]))
                elif nC == 11:
                    actions.append(
                        np.array(enumerateOptions.elevenCardIndices[option]))
                elif nC == 12:
                    actions.append(
                        np.array(enumerateOptions.twelveCardIndices[option]))
                else:
                    actions.append(
                        np.array(enumerateOptions.thirTeenCardIndices[option]))
        if currAvailAcs[0][-1] == 1:
            actions.append("Pass")
            listAction.append(currAvailAcs.size - 1)
        #print(pGos)
        #print("______")
        #print(string)
        #print("______")
        #print(actions)
        return (pGos, string, actions,listAction)