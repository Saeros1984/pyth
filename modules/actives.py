#activation functions here

import math

class activator ():
    def activate (value):
        res=value
        return res
    def derivative (value):
        res=value
        return res

class sigmoid(activator):
    def activate (x):
        return 1 / (1 + math.exp(-x))
    def derivative (x):
        return x*(1-x)
    
activ={"sigmoid":sigmoid}
