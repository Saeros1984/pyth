import math
import random
import time
import modules.actives as actives
import modules.classes as classes
import modules.algorithms as algs
import modules.multiproc as pr
import modules.testing as test

"""p=test.testpool()
z=test.testParametr(p, "params", "learning")
z.setParam("backPropagation", 30)
z=test.testParametr(p, "params", "speed")
z.setParam(1)
z=test.testParametr(p, "CoshiParams", "CoshiCoeff")
z.setParam(0.5)
z=test.testParametr(p, "conditions", "epochs")
z.setParam(2000)
z=test.testParametr(p, "activation")
z.setParam("sigmoid")
z=test.testParametr(p, "CoshiParams", "randomReset")
z.setParam(False)
z=test.testParametr(p, "CoshiParams", "T0")
z.setParam(100)
p.start()
"""

p=classes.networkPool()

net=classes.network(p, False, "", "tanh")
net.processData("C:/Users/USER/Desktop/test.xml", {"roles":[0]})
#net.processData("C:/Users/USER/Desktop/xor.xml", {"roles":[2]})
net.innlayerGen()
net.addLayer().addNeurons(20)
net.connectToPrev()
net.addLayer().addNeurons(20)
net.connectToPrev()
net.outlayerGen()
net.connectToPrev()

print(len(net.norm.columns[0].cells))
net.startLearning("backPropagation")
