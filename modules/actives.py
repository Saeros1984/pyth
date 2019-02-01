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
    def normalize (x, alpha):
        return float(x)*alpha
    def activate (n):
        return float(n.summ)*n.getalpha()
    def derivative (n):
        return n.getalpha()
    def denorm (x, alpha):
        return x/alpha
        

class sigmoid(activator):
    def normalize (x, alpha):
        return 1 / (1 + math.exp(-float(x)*alpha))
    def activate (n):
        return 1 / (1 + math.exp(-n.summ*n.getalpha()))
    def derivative (n):
        return n.out*(1-float(n.out))
    def denorm (x, alpha):
        return 1

class tanh(activator):
    def normalize (x, alpha):
        return math.tanh(float(x)*float(alpha))
    def activate (n):
        return math.tanh(n.summ*n.getalpha())
    def derivative (n):
        return (1-n.out*n.out)*n.getalpha()
    def denorm (x, alpha):
        return 1

class bipolar(activator):
    def normalize (x, alpha):
        return (1-math.exp(-float(x)*alpha))/(1+math.exp(-float(x)*alpha))
    def activate (n):
        return (1-math.exp(-n.summ*n.getalpha()))/(1+math.exp(-n.summ*n.getalpha()))
    def derivative (n):
        return n.getalpha()/2*(1-n.out*n.out)
    def denorm (x, alpha):
        return 1

class gauss(activator):
    def normalize (x, alpha):
        return math.exp(-(float(x)*float(x)))
    def activate (n):
        return math.exp(-(float(n.summ)-float(n.c))**2)
    def derivative (n):
        return -2*n.summ*math.exp(-(n.summ-n.c)**2)
    def denorm (x, alpha):
        return 1

class ELU(activator):
    def normalize (x, alpha):
        if (x<=0):
            return alpha*(math.exp(x)-1)
        else:
            return x
    def activate (n):
        if (n.summ<=0):
            return n.getalpha()[1]*(math.exp(n.summ)-1)
        else:
            return n.summ*n.getalpha()[0]
            
    def derivative (n):
        if (n.out<=0):
            return n.out+n.getalpha()[1]
        else:
            return 1
        
    def denorm (x, alpha):
        return 1


class reLU(activator):
    def normalize (x, alpha):
        if (x>=0):
            res=float(x)*alpha[1]
        else:
            res=float(x)*alpha[0]
        return res
    def activate (n):
        if (n.summ>=0):
            res=n.summ*n.getalpha()[1]
        else:
            res=n.summ*n.getalpha()[0]
        return res
    def derivative (n):
        if (n.out>=0):
            res=n.getalpha()[1]
        else:
            res=n.getalpha()[0]
        return res
    def denorm (x, alpha):
        if (x>=0):
            res=x/alpha[1]
        else:
            res=x/alpha[0]
        return res
    
activ={"linear":linear, "sigmoid":sigmoid, \
       "tanh":tanh, "reLU":reLU, "bipolar":bipolar, \
       "ELU":ELU, "gauss":gauss}
