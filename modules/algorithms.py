#learning algorithms here
import modules.actives as activ
import modules.lossfunctions as loss

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
        backPropagation.getOutMistake(network.outlayer)
        backPropagation.getAllMistake(network.layers)
        backPropagation.weightCorrect(network.layers)
    def epoch(network): #one epoch
        i=0
        for row in network.norm.columns[0].cells:
            backPropagation.step(network, i)
            i+=1
        network.stats["epochs"]+=1
    def start (network):
        while (True):
            backPropagation.epoch(network)
            loss.lossFunctions[network.params["lossFunction"]](network, True)
            loss.lossFunctions[network.params["lossFunction"]](network, False)
            res=network.conditionsCheck()
            if (res):
                print (res)
                network.learning=False
                network.debug(2, "learning Finished", network.stats)
                break
            
            

algs={"backPropagation":backPropagation}
