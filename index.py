import math
import random
import modules.actives as actives
import modules.classes as classes
import modules.algorithms as algs


net=classes.network("fff", "sigmoid")
net.params["alpha"]=1
#net.processData("C:/Users/USER/Desktop/xor.xml", {"roles":[2]})
#net.processData("C:/Users/USER/Desktop/mult.xml", {"roles":[1]})
net.processData("C:/Users/USER/Desktop/sqrt.xml", {"roles":[1]})
net.innlayerGen()
net.connectToPrev()
net.addLayer().addNeurons(6)
net.connectToPrev()
net.outlayerGen()
net.connectToPrev()

net.params["speed"]=1
net.conditions["epochs"]=15000
net.params["additNeurons"]=1
net.params["impulse"]=0.9
net.conditions["maxmistake"]=0.001

net.startLearning("backPropagation")

