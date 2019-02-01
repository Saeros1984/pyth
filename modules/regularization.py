#regularization functions here

def forfeit(network, weight, value):
    summ=weight+value
    abbs=abs(summ)
    if (abbs<=network.CoshiParams["top"] or abs(weight)>abbs):
        return value
    res=network.CoshiParams["top"]+(abbs-network.CoshiParams["top"])*network.CoshiParams["forfeit"]
    if (summ>=0):
        return res
    else:
        return -res

regs={"forfeit":forfeit}
