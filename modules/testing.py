#test algoritms here
import modules.classes as classes
import random

class testpool(classes.networkPool):
    testing=False
    
    

    def __init__(self, name=""):
        self.nets=[]
        self.params=[]
        self.data="C:/Users/USER/Desktop/xor.xml"
        self.dataroles={"roles":[2]}
        self.stats={"maxepochs":0, \
    "minepochs":9999999, \
    "midepochs":0, \
    "success":0, \
    "failed":0, \
                    }
        if (name==""):
            self.name="TestPool "+str(len(self.netpools)+1)
        else:
            self.name=name
        classes.networkPool.netpools.append(self)
    def getParamByName(self, name):
        for p in self.params:
            if (p.paramToChange[0]==name):
                return p
            if (p.paramToChange[1]==name):
                return p
        return False
    def last (self):
        return self.params[len(self.params)-1]
    def start(self):
        self.testing=True
        while (self.testing):
            n=classes.network(self)
            n.processData(self.data, self.dataroles)
            for p in self.params:
                if (len(p.paramToChange)==1):
                    par=p.returnParam()
                    try:
                        a=getattr(n, p.paramToChange[0])
                    except AttributeError:
                        print("No such attribute " + str(p.paramToChange[0]))
                        return
                    setattr(n, p.paramToChange[0], par)
                else:
                    par=p.returnParam()
                    try:
                        a=getattr(n, p.paramToChange[0])
                    except AttributeError:
                        print("No such attribute " + str(p.paramToChange[0]))
                        return
                    a[p.paramToChange[1]]=par
            n.innlayerGen()
            for l in range(n.paramsForGen["layers"]):
                n.addLayer().addNeurons(n.paramsForGen["neurons"])
                n.connectToPrev()
            n.outlayerGen()
            n.connectToPrev()
            n.startLearning()
            if (n.conditions["epochs"]==n.stats["epochs"]):
                self.stats["failed"]+=1
            else:
                self.stats["success"]+=1
                self.stats["midepochs"]+=n.stats["epochs"]
                if (n.stats["epochs"]>self.stats["maxepochs"]):
                    self.stats["maxepochs"]=n.stats["epochs"]
                if (n.stats["epochs"]<self.stats["minepochs"]):
                    self.stats["minepochs"]=n.stats["epochs"]
        self.end()
    def end(self):
        self.testing=False
        self.stats["midepochs"]/=len(self)
        print(self.stats)

class testParametr():
    def __init__(self, pool, *paramtochange):
        self.counter=0
        self.pool=pool
        self.paramToChange=paramtochange
        self.params=[]
        pool.params.append(self)
    def setParam(self, param, tryes=1):
        for i in range(tryes):
            self.params.append(param)
    def finished(self):
        self.counter=0
        if (self.pool.params.index(self)==0):
            self.pool.end()
        else:
            nextpar=self.pool.params[self.pool.params.index(self)-1]
            if (nextpar.counter+1>len(nextpar.params)-1):
                nextpar.finished()
            else:
                nextpar.counter+=1
            

    def returnParam(self):
        res=self.params[self.counter]
        if (self.pool.last()==self):
            self.counter+=1
            if (self.counter>len(self.params)-1):
                self.finished()
                return res
        return res
        
