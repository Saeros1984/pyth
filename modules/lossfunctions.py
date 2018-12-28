#here functions for error calculation
#calculate middle error, calculate max error if mid=False

import math

def fabs (network, mid=True): #sum of modules differences on each output neuron
    err=0
    if (mid):
        for n in network.outlayer.neurons:
            err+=abs(n.mistake)
        network.stats["middlemistake"]=err
        return err
    else:
        for n in network.outlayer.neurons:
            if (abs(n.mistake)>err):
                err=abs(n.mistake)
        network.stats["maxmistake"]=err    
        return err

def square (network, mid=True): #square sum
    err=0
    if (mid):
        for n in network.outlayer.neurons:
            err+=abs(n.mistake)*abs(n.mistake)
        network.stats["middlemistake"]=err
        return err
    else:
        for n in network.outlayer.neurons:
            sqr=abs(n.mistake)*abs(n.mistake)
            if (sqr>err):
                err=sqr
        network.stats["maxmistake"]=err
        return err
                
def meansquare (network, mid=True): #mid only!
    if (not mid):
        return square(network, mid)
    err=0
    for n in network.outlayer.neurons:
            err+=math.fabs(n.mistake)*math.fabs(n.mistake)
    err=err/len(network.outlayer.neurons)
    return err


lossFunctions={"fabs":fabs, "square":square}
