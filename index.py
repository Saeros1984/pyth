import math
import random
import modules.actives as actives
import modules.classes as classes
import modules.algorithms as algs


net=classes.network("fff", "linear")
net.params["alpha"]=1
#net.processData("C:/Users/USER/Desktop/xor.xml", {"roles":[2]})
#net.processData("C:/Users/USER/Desktop/mult.xml", {"roles":[1]})
net.processData("C:/Users/USER/Desktop/sqrt.xml", {"roles":[1]})
net.innlayerGen()
net.connectToPrev()
net.addLayer().addNeurons(5)
net.connectToPrev()
net.outlayerGen()
net.connectToPrev()

net.params["speed"]=0.1
net.params["additNeurons"]=0
net.params["impulse"]=0
net.conditions["maxmistake"]=0.001

net.startLearning("backPropagation")

