#learning algorithms here
import modules.actives as activ
import modules.regularization as reg
import modules.lossfunctions as loss
import math
import random

class backPropagation():
    def getOutMistake(layer): #Computing mistake for output neurons
        for n in layer.neurons:
            n.q=loss.lossFunctions[layer.network.params["lossFunction"]].outDerivative(layer.network)
    def getAllMistake(layers): #computing mistake for all neurons, except outs
        i=len(layers)-2
        while (i>=0):
            for neu in layers[i].neurons:
                neu.q=0
                sinapses=0
                for sin in neu.sinapsesOfOut:
                    sinapses+=sin.owner.q*sin.weight
                    neu.q=sinapses*activ.activ[neu.getactiv()].derivative(neu)*layers[i].network.params["speed"]
            i-=1
    def weightAccum(layers, CoshiCoef=1):#accumpulating deltas from batch
        i=len(layers)-1
        while (i>0):
            for neu in layers[i].neurons:
                for sin in neu.sinapses:
                    if (False):
                        corr=neu.q*layers[i].network.params["speed"]*sin.prevneuron.out
                        sin.accumDelta+=reg.regs[layers[i].network.params["regularization"]](layers[i].network, sin.weight, corr)
                    else:
                        corr=neu.q*layers[i].network.params["speed"]*sin.prevneuron.out
                        sin.accumDelta+=corr
            i-=1
    def weightCorrect(layers, CoshiCoef=1):
        i=len(layers)-1
        while (i>0):
            for neu in layers[i].neurons:
                for sin in neu.sinapses:
                    corr=sin.accumDelta
                    sin.weight+=corr
                    sin.accumDelta=0
                    if (layers[0].network.params["impulse"]!=0):
                        sin.weight+=sin.prevCorr*layers[0].network.params["impulse"]
                        sin.prevCorr=corr
            i-=1
    def step(network, dataindex): #one step of each learning row
        backPropagation.mistakeChecker(network, dataindex)
        network.debug(5, "Step", dataindex, network.outlayer.neurons[0].out)
        backPropagation.getOutMistake(network.outlayer)
        backPropagation.getAllMistake(network.layers)
        backPropagation.weightAccum(network.layers)
    def batchEnd(layer):#performed in the end of every batch
        for n in layer.neurons:
            n.batchQ/=layer.network.stats["currentBatch"]
        backPropagation.weightCorrect(layer.network.layers)
        for n in layer.neurons:
            n.batchQ=0
    def mistakeChecker(network, dataindex, of=""):
        if (of==""):
            of=network.norm
        network.setInput(dataindex, of)
        network.getAnswer()
        network.compareOutput(dataindex, of)
        loss.lossFunctions[network.params["lossFunction"]].do(network, dataindex, of)
    def recognitionChecker(network, dataindex, of=""):
        if (of==""):
            of=network.test
        res=network.denormalize(False)
        i=0
        for r in res:
            if (i>len(of.recognize[dataindex])-1):
                of.recognize[dataindex].append(0)
            if (of.answers[i].cells[dataindex]==res[i]):
                of.recognize[dataindex][i]=1
            else:
                of.recognize[dataindex][i]=0
    def epoch(network): #one epoch
        itemsList=list(range(len(network.norm.columns[0].cells)))
        i=0
        for row in network.norm.columns[0].cells:
            item=random.choice(itemsList)
            backPropagation.step(network, item)
            itemsList.remove(item)
            network.stats["currentBatch"]+=1
            if (network.stats["currentBatch"]>=network.params["batchSize"] or len(itemsList)==0):
                backPropagation.batchEnd(network.outlayer)
                network.stats["currentBatch"]=0
            i+=1
        i=0
        for row in network.norm.columns[0].cells:
            backPropagation.mistakeChecker(network, i)
            i+=1
        if (network.params["validationData"]>0):
            i=0
            for row in network.valid.columns[0].cells:
                backPropagation.mistakeChecker(network, i, network.valid)
                i+=1
        if (network.params["testData"]>0):
            i=0
            for row in network.test.columns[0].cells:
                backPropagation.mistakeChecker(network, i, network.test)
                if (network.params["testRecognition"]):
                    backPropagation.recognitionChecker(network, i, network.test)
                i+=1
        if (network.params["testRecognition"]):
            i=0
            for c in network.test.answers:
                if (i>len(network.stats["TestRecognition"])-1):
                    network.stats["TestRecognition"].append([])
                network.stats["TestRecognition"][i]=sum(z[i] for z in network.test.recognize)/len(network.test.recognize)
        network.stats["epochs"]+=1
        network.debug(4, network.stats)
    def start (network):
        while (True):
            backPropagation.epoch(network)
            network.stats["middlemistake"]=sum(network.norm.mistakes)/len(network.norm.mistakes)
            network.stats["maxmistake"]=max(network.norm.mistakes)
            if (network.params["validationData"]>0):
                network.stats["ValidMiddleMistake"]=sum(network.valid.mistakes)/len(network.valid.mistakes)
                network.stats["ValidMaxMistake"]=max(network.valid.mistakes)
            if (network.params["testData"]>0):
                network.stats["TestMiddleMistake"]=sum(network.test.mistakes)/len(network.test.mistakes)
                network.stats["TestMaxMistake"]=max(network.test.mistakes)
            res=network.conditionsCheck()
            if (res):
                network.learning=False
                network.debug(2, "learning Finished", network.stats, network.params)
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
        if (network.params["validationData"]>0):
            i=0
            for row in network.valid.columns[0].cells:
                backPropagation.mistakeChecker(network, i, network.valid)
                i+=1
        if (network.params["testData"]>0):
            i=0
            for row in network.test.columns[0].cells:
                backPropagation.mistakeChecker(network, i, network.test)
                if (network.params["testRecognition"]):
                    backPropagation.recognitionChecker(network, i, network.test)
                i+=1
        if (network.params["bestResults"]>0 and network.checkResult()):
            network.saveResult()
        if (network.params["testRecognition"]):
            i=0
            for c in network.test.answers:
                if (i>len(network.stats["TestRecognition"])-1):
                    network.stats["TestRecognition"].append([])
                network.stats["TestRecognition"][i]=sum(z[i] for z in network.test.recognize)/len(network.test.recognize)
        network.stats["epochs"]+=1
        network.debug(4, network.CoshiParams["T"], network.stats)
    def step(network, dataindex):
        network.setInput(dataindex)
        network.getAnswer()
        network.compareOutput(dataindex)
        mist=loss.lossFunctions[network.params["lossFunction"]].do(network, dataindex)
        xc=network.CoshiParams["speed"]*network.CoshiParams["T"]
        Coshi.weightCorrect(network, xc)
        network.getAnswer()
        network.compareOutput(dataindex)
        if (network.CoshiParams["randomReset"]):
            P=network.CoshiParams["T"]/network.CoshiParams["T0"]
        else:
            P=1
        if (mist<loss.lossFunctions[network.params["lossFunction"] or network.CoshiParams["randomReset"] and random.uniform(0, 1)<=P].do(network, dataindex)):
            Coshi.weightReset(network)
            network.norm.mistakes[dataindex]=mist
    def mistakeChecker(network, dataindex):
        network.setInput(dataindex)
        network.getAnswer()
        network.compareOutput(dataindex)
        loss.lossFunctions[network.params["lossFunction"]].do(network, dataindex)
    def weightCorrect(network, xc, CoshiCoef=1):
        for l in network.layers:
            for n in l.neurons:
                for s in n.sinapses:
                    s.weightCoshiPrev=s.weight
                    if (network.CoshiParams["CoshiReg"]!=False):
                        s.weight=reg.regs["forfeit"](network, s.weight, CoshiCoef*xc*math.tanh(random.uniform(1.57, -1.57)))
                        
                    else:
                        s.weight+=xc*math.tanh(random.uniform(1.57, -1.57))*CoshiCoef
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
            if (network.params["validationData"]>0):
                network.stats["ValidMiddleMistake"]=sum(network.valid.mistakes)/len(network.valid.mistakes)
                network.stats["ValidMaxMistake"]=max(network.valid.mistakes)
            if (network.params["testData"]>0):
                network.stats["TestMiddleMistake"]=sum(network.test.mistakes)/len(network.test.mistakes)
                network.stats["TestMaxMistake"]=max(network.test.mistakes)

            res=network.conditionsCheck()
            if (res):
                network.learning=False
                network.debug(2, "learning Finished", network.stats, network.params, network.CoshiParams)
                if (network.pool!=False):
                    for o in network.pool.outputs:
                        o.send("END")
                break
class backPropagationCoshi():
    def step(network, dataindex): #one step of each learning row
        if (network.CoshiParams["CoshiCoeff"]!=0):
            backPropagation.mistakeChecker(network, dataindex)
            network.debug(5, "Step", dataindex, network.outlayer.neurons[0].out)
            backPropagation.getOutMistake(network.outlayer)
            backPropagation.getAllMistake(network.layers)
            backPropagation.weightAccum(network.layers)
            
        if (network.CoshiParams["CoshiCoeff"]!=1 and network.stats["currentBatch"]==0):
            network.setInput(dataindex)
            network.getAnswer()
            network.compareOutput(dataindex)
            mist=loss.lossFunctions[network.params["lossFunction"]].do(network, dataindex)
            xc=network.CoshiParams["speed"]*network.CoshiParams["T"]
            Coshi.weightCorrect(network, xc, 1-network.CoshiParams["CoshiCoeff"])
            network.getAnswer()
            network.compareOutput(dataindex)
            if (network.CoshiParams["randomReset"]):
                P=network.CoshiParams["T"]/network.CoshiParams["T0"]
            else:
                P=1
            if (mist<loss.lossFunctions[network.params["lossFunction"] or network.CoshiParams["randomReset"] and random.uniform(0, 1)<=P].do(network, dataindex)):
                Coshi.weightReset(network)
                network.norm.mistakes[dataindex]=mist
    def epoch (network):
        network.CoshiParams["T"]=network.CoshiParams["T0"]/(1+network.stats["epochs"]/network.CoshiParams["Tcoeff"])
        itemsList=list(range(len(network.norm.columns[0].cells)))
        i=0
        for row in network.norm.columns[0].cells:
            item=random.choice(itemsList)
            backPropagationCoshi.step(network, item)
            itemsList.remove(item)
            network.stats["currentBatch"]+=1
            if (network.stats["currentBatch"]>=network.params["batchSize"] or len(itemsList)==0):
                backPropagation.batchEnd(network.outlayer)
                network.stats["currentBatch"]=0
            i+=1
        i=0
        for row in network.norm.columns[0].cells:
            Coshi.mistakeChecker(network, i)
            i+=1
        if (network.params["validationData"]>0):
            i=0
            for row in network.valid.columns[0].cells:
                backPropagation.mistakeChecker(network, i, network.valid)
                i+=1
        if (network.params["testData"]>0):
            i=0
            for row in network.test.columns[0].cells:
                backPropagation.mistakeChecker(network, i, network.test)
                if (network.params["testRecognition"]):
                    backPropagation.recognitionChecker(network, i, network.test)
                i+=1
        if (network.params["testRecognition"]):
            i=0
            for c in network.test.answers:
                if (i>len(network.stats["TestRecognition"])-1):
                    network.stats["TestRecognition"].append([])
                network.stats["TestRecognition"][i]=sum(z[i] for z in network.test.recognize)/len(network.test.recognize)
        network.stats["epochs"]+=1
        network.debug(4, network.stats)
        network.debug(4, network.CoshiParams["T"])
    def start (network):
        while (True):
            backPropagationCoshi.epoch(network)
            network.stats["middlemistake"]=sum(network.norm.mistakes)/len(network.norm.mistakes)
            network.stats["maxmistake"]=max(network.norm.mistakes)
            if (network.params["validationData"]>0):
                network.stats["ValidMiddleMistake"]=sum(network.valid.mistakes)/len(network.valid.mistakes)
                network.stats["ValidMaxMistake"]=max(network.valid.mistakes)
            if (network.params["testData"]>0):
                network.stats["TestMiddleMistake"]=sum(network.test.mistakes)/len(network.test.mistakes)
                network.stats["TestMaxMistake"]=max(network.test.mistakes)

            res=network.conditionsCheck()
            if (res):
                network.learning=False
                network.debug(2, "learning Finished", network.stats, network.params, network.CoshiParams)
                if (network.pool!=False):
                    for o in network.pool.outputs:
                        o.send("END")
                break
algs={"backPropagation":backPropagation, \
      "Coshi":Coshi, "backPropagationCoshi":backPropagationCoshi}
