#here functions for error calculation
#calculate middle error, calculate max error if mid=False

import math

def fabs (network, dataid, mid=True): #sum of modules differences on each output neuron
    err=0
    if (mid):
        for n in network.outlayer.neurons:
            err+=abs(n.mistake)
            network.debug(5, abs(n.mistake))
        err=err/len(network.outlayer.neurons)
        network.norm.mistakes[dataid]=err
        network.debug(4, network.norm.mistakes[dataid], abs(n.mistake))
        return err
    else:
        for n in network.outlayer.neurons:
            if (abs(n.mistake)>err):
                err=abs(n.mistake)
        network.norm.mistakes[dataid]=err    
        return err

def square (network, dataid, mid=True): #square sum
    err=0
    if (mid):
        for n in network.outlayer.neurons:
            err+=abs(n.mistake)*abs(n.mistake)
        network.norm.mistakes[dataid]=err
        return err
    else:
        for n in network.outlayer.neurons:
            sqr=abs(n.mistake)*abs(n.mistake)
            if (sqr>err):
                err=sqr
        network.norm.mistakes[dataid]=err
        return err
                
def meansquare (network, dataid, mid=True): #mid only!
    if (not mid):
        return square(network, dataid, mid)
    err=0
    for n in network.outlayer.neurons:
            err+=math.fabs(n.mistake)*math.fabs(n.mistake)
    err=err/len(network.outlayer.neurons)
    network.norm.mistakes[dataid]=err
    return err


lossFunctions={"fabs":fabs, "square":square}
