#learning algorithms here
import modules.actives as activ
import modules.regularization as reg
import modules.lossfunctions as loss
import math
import random

class backPropagation():
    def getOutMistake(layer): #Computing mistake for output neurons
        for n in layer.neurons:
            n.q=n.mistake*activ.activ[n.getactiv()].derivative(n.out, layer.network.params["alpha"])*layer.network.params["speed"]
    def getAllMistake(layers): #computing mistake for all neurons, except outs
        i=len(layers)-2
        while (i>=0):
            for neu in layers[i].neurons:
                neu.q=0
                for sin in neu.sinapsesOfOut:
                    neu.q+=sin.owner.q*sin.weight
                neu.q=neu.q*activ.activ[neu.getactiv()].derivative(neu.out, layers[0].network.params["alpha"])*layers[i].network.params["speed"]
            i-=1
    def weightCorrect(layers):#correcting sinapses weights
        i=len(layers)-1
        while (i>0):
            for neu in layers[i].neurons:
                for sin in neu.sinapses:
                    if (layers[0].network.params["regularization"]!=False):
                        corr=neu.q*layers[i].network.params["speed"]*sin.prevneuron.out
                        sin.weight=reg.regs[layers[i].network.params["regularization"]](layers[i].network, sin.weight, corr)
                        if (layers[0].network.params["impulse"]!=0):
                            sin.weight=reg.regs[layers[0].network.params["regularization"]](layers[i].network, sin.weight, sin.prevCorr*layers[0].network.params["impulse"])
                            sin.prevCorr=corr
                    else:
                        corr=neu.q*layers[i].network.params["speed"]*sin.prevneuron.out
                        sin.weight+=corr
                        if (layers[0].network.params["impulse"]!=0):
                            sin.weight+=sin.prevCorr*layers[0].network.params["impulse"]
                            sin.prevCorr=corr
            i-=1
    def step(network, dataindex): #one step of each learning row
        network.setInput(dataindex)
        network.getAnswer()
        network.compareOutput(dataindex)
        loss.lossFunctions[network.params["lossFunction"]](network, dataindex, True)
        network.debug(5, "Step", dataindex, network.outlayer.neurons[0].out)
        backPropagation.getOutMistake(network.outlayer)
        backPropagation.getAllMistake(network.layers)
        backPropagation.weightCorrect(network.layers)
    def mistakeChecker(network, dataindex):
        network.setInput(dataindex)
        network.getAnswer()
        network.compareOutput(dataindex)
        loss.lossFunctions[network.params["lossFunction"]](network, dataindex, True)
    def epoch(network): #one epoch
        i=0
        for row in network.norm.columns[0].cells:
            backPropagation.step(network, i)
            i+=1
        i=0
        for row in network.norm.columns[0].cells:
            backPropagation.mistakeChecker(network, i)
            i+=1
        network.stats["epochs"]+=1
    def start (network):
        while (True):
            backPropagation.epoch(network)
            network.stats["middlemistake"]=sum(network.norm.mistakes)/len(network.norm.mistakes)
            network.stats["maxmistake"]=max(network.norm.mistakes)
            res=network.conditionsCheck()
            if (res):
                network.learning=False
                network.debug(2, "learning Finished", network.stats)
                if (network.pool!=False):
                    for o in network.pool.outputs:
                        o.send("END")
                break
            
class Coshi():
    def epoch (network):
        i=0
        network.CoshiParams["T"]=network.CoshiParams["T0"]/(1+network.stats["epochs"]/network.CoshiParams["Tcoeff"])
        for row in network.norm.columns[0].cells:
            Coshi.step(network, i)
            i+=1
        i=0
        for row in network.norm.columns[0].cells:
            Coshi.mistakeChecker(network, i)
            i+=1
        network.stats["epochs"]+=1
        network.debug(4, network.CoshiParams["T"])
    def step(network, dataindex):
        network.setInput(dataindex)
        network.getAnswer()
        network.compareOutput(dataindex)
        mist=loss.lossFunctions[network.params["lossFunction"]](network, dataindex, True)
        xc=network.CoshiParams["speed"]*network.CoshiParams["T"]
        Coshi.weightCorrect(network, xc)
        network.getAnswer()
        network.compareOutput(dataindex)
        if (network.CoshiParams["randomReset"]):
            P=network.CoshiParams["T"]/network.CoshiParams["T0"]
        else:
            P=False
        if (mist<loss.lossFunctions[network.params["lossFunction"] or network.CoshiParams["randomReset"] and random.uniform(0, 1)==P](network, dataindex, True)):
            Coshi.weightReset(network)
            network.norm.mistakes[dataindex]=mist
    def mistakeChecker(network, dataindex):
        network.setInput(dataindex)
        network.getAnswer()
        network.compareOutput(dataindex)
        loss.lossFunctions[network.params["lossFunction"]](network, dataindex, True)
    def weightCorrect(network, xc):
        for l in network.layers:
            for n in l.neurons:
                for s in n.sinapses:
                    s.weightCoshiPrev=s.weight
                    if (network.params["regularization"]!=False):
                        s.weight=reg.regs[network.params["regularization"]](network, s.weight, xc*math.tanh(random.uniform(1.57, -1.57)))
                    else:
                        s.weight+=xc*math.tanh(random.uniform(1.57, -1.57))
    def weightReset(network):
        for l in network.layers:
            for n in l.neurons:
                for s in n.sinapses:
                    s.weight=s.weightCoshiPrev
    def start (network):
        while (True):
            Coshi.epoch(network)
            network.stats["middlemistake"]=sum(network.norm.mistakes)/len(network.norm.mistakes)
            network.stats["maxmistake"]=max(network.norm.mistakes)
            res=network.conditionsCheck()
            if (res):
                network.learning=False
                network.debug(2, "learning Finished", network.stats)
                if (network.pool!=False):
                    for o in network.pool.outputs:
                        o.send("END")
                break
algs={"backPropagation":backPropagation, "Coshi":Coshi}
