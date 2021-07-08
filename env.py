from big2Game import vectorizedBig2GamesTest

vectorizedGame = vectorizedBig2GamesTest()

vectorizedGame.reset()
a,b,c = vectorizedGame.getCurrentState()
a,b,c,d= vectorizedGame.info()
print(a)
print("______")
print(b)
print("______")
print(c)
print("______")
print(d)
a,b,c= vectorizedGame.step(0)
print("### NEXT PLAYER ###")
