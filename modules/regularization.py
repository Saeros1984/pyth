#learning algorithms here

def forfeit(network, weight, value):
    summ=weight+value
    abbs=abs(summ)
    if (abbs<=network.regularization["top"] or abs(weight)>abbs):
        return value+weight
    res=network.regularization["top"]+(abbs-network.regularization["top"])*network.regularization["forfeit"]
    if (summ>=0):
        return res
    else:
        return -res

regs={"forfeit":forfeit}
