#activation functions here

import math

class activator ():
    def activate (value):
        res=value
        return res
    def derivative (value):
        res=value
        return res

class linear(activator):
    def activate (x, alpha):
        return float(x)*alpha
    def derivative (x, alpha):
        return alpha
    def denorm (x, alpha):
        return x/alpha
        

class sigmoid(activator):
    def activate (x, alpha):
        return 1 / (1 + math.exp(-float(x)*alpha))
    def derivative (x, alpha):
        return float(x)*(1-float(x))
    def denorm (x, alpha):
        return 1
    
activ={"linear":linear, "sigmoid":sigmoid}
