#here functions for error calculation

import modules.actives as activ
import math
class fabs():
    def do (network, dataid, of=""): #sum of modules differences on each output neuron
        if(of==""):
            of=network.norm
        maxerr=0
        err=0
        for n in network.outlayer.neurons:
            n.calculatedMistake=abs(n.mistake)
            err+=n.calculatedMistake
            if (n.calculatedMistake>maxerr):
                maxerr=n.calculatedMistake
        err/=len(network.outlayer.neurons)
        of.mistakes[dataid]=maxerr
        return maxerr
    def outDerivative(network):
        for n in network.outlayer.neurons:
            n.q=n.mistake*activ.activ[n.getactiv()].derivative(n)*network.params["speed"]
        return n.q

class meansquare():                
    def do (network, dataid, of=""): #mid only!
        if(of==""):
            of=network.norm
        err=0
        maxerr=0
        for n in network.outlayer.neurons:
            n.calculatedMistake=n.mistake*n.mistake
            err+=n.calculatedMistake
            if (n.calculatedMistake>maxerr):
                maxerr=n.calculatedMistake
        err=err/len(network.outlayer.neurons)
        of.mistakes[dataid]=err
        return err
    def outDerivative(network):
        for n in network.outlayer.neurons:
            n.q=n.mistake*activ.activ[n.getactiv()].derivative(n)*network.params["speed"]
        return n.q

class crossEntropy():                
    def do (network, dataid):
        err=0
        maxerr=0
        for n in network.outlayer.neurons:
            ut=1-n.out+0.000000000001
            n.calculatedMistake=n.rightValue*math.log(n.out)+(1-n.rightValue)*math.log(ut)
            err+=n.calculatedMistake
            if (n.calculatedMistake>maxerr):
                maxerr=n.calculatedMistake
        err*=-(1/len(network.outlayer.neurons))
        network.norm.mistakes[dataid]=err
        return err
    def outDerivative(network):
        for n in network.outlayer.neurons:
            n.q=activ.activ[n.getactiv()].derivative(n)*(-1*(n.rightValue*(1/n.out)+(1-n.rightValue)*(1/(1-n.out))))
        return n.q



lossFunctions={"fabs":fabs, "meansquare":meansquare, "crossEntropy":crossEntropy}
