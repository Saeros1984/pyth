import math
import random
import modules.actives as actives
import modules.classes as classes
import modules.algorithms as algs


net=classes.network()
net.processData("C:/Users/USER/Desktop/xor.xml", {"roles":[2]})
net.innlayerGen()
net.connectToPrev()
net.addLayer().addNeurons(5)
net.connectToPrev()
net.outlayerGen()
net.connectToPrev()

