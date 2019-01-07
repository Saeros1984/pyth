import math
import random
import time
import modules.actives as actives
import modules.classes as classes
import modules.algorithms as algs
import modules.multiproc as pr

p=classes.networkPool()

net=classes.network(p, False, "fff", "sigmoid")
net.params["alpha"]=1
net.processData("C:/Users/USER/Desktop/xor.xml", {"roles":[2]})
#net.processData("C:/Users/USER/Desktop/mult.xml", {"roles":[1]})
#net.processData("C:/Users/USER/Desktop/sqrt.xml", {"roles":[1]})


net.params["speed"]=2
net.conditions["epochs"]=10000
net.params["additNeurons"]=1
net.params["impulse"]=0.9
net.conditions["maxmistake"]=0.1000
net.conditions["middlemistake"]=0.0000

net.innlayerGen()
net.addLayer().addNeurons(5)
net.connectToPrev()
net.outlayerGen()
net.connectToPrev()


#net.setInput(0)
#net.getAnswer()
#print (net.pool.outputs)
#for q in net.pool.pool:
#    print ("pool "+str(q.output))
#time.sleep(20)
t=time.time()
net.startLearning("Coshi")

net.setInput(0)
net.getAnswer()
print(net.outlayer.neurons[0].out)
#print(net.outlayer.neurons[0].out+net.norm.mistakes[0])

net.setInput(1)
net.getAnswer()
print(net.outlayer.neurons[0].out)
#print(net.outlayer.neurons[0].out+net.norm.mistakes[1])

net.setInput(2)
net.getAnswer()
print(net.outlayer.neurons[0].out)
#print(net.outlayer.neurons[0].out+net.norm.mistakes[2])

net.setInput(3)
net.getAnswer()
print(net.outlayer.neurons[0].out)
#print(net.outlayer.neurons[0].out+net.norm.mistakes[3])
print(net.norm.mistakes)
