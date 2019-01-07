import random
import modules.actives as actives
import modules.data as data
import modules.lossfunctions as loss
import modules.algorithms as algs
import modules.multiproc as pr

class networkPool:
    name=""
    netpools=[]
    def __init__(self, name=""):
        self.nets=[]
        if (name==""):
            self.name="Pool "+str(len(self.netpools)+1)
        else:
            self.name=name

class network: # abstact class for networks
    name=""
    debugLevel=2 #the importsnce of the messages - 1 is the highest   
    synmax=1.3
    synmin=-1.3
    norm=0 #table of normalized data
    innlayer=0
    outlayer=0
    learning=False #shows if learning process executes right now

    stats={"descr":"", \
           "epochs":0, \
           "maxmistake":1.0, \
           "middlemistake":1.0, \
           
           }
    params={"speed":1, \
            "alpha":1, \
            "additNeurons":1, \
            "impulse":0.9, \
            "lossFunction":"fabs", \
            "allowPreserveNumericData":True, \
            "regularization":"forfeit", \
            
            }
    CoshiParams={"T0":300, \
                "T":0, \
                 "Tcoeff":10, \
                 "speed":1, \
                 "randomReset":True, \
                 
                 }
    regularization={"top":8, \
                    "forfeit":0.1, \
                    }
    conditions={"epochs":2000, \
                "maxmistake":0.1, \
                "middlemistake":0.0,\
                

                }
    normtableParams={"uno":{},\
                     "boolean":{"role":False, "zero":1, "one":0}, \
                     "triple":{"role":False, "acrivtype":1}, \
                     "diff":{"role":False}, \
                     "numeric":{"role":False, "normtype":"linear", "alpha":1}}
    def __init__ (self, networkPool, pool=False ,name="", activation="sigmoid"): #pool - gets procpool object
        networkPool.nets.append(self)
        self.networkPool=networkPool
        if (name==""):
            self.name="network "+str(len(self.networkPool)+1)
        else:
            self.name=name
        self.activation=activation
        self.layers=[]
        self.pool=pool
        return
    def errorMes (self, *messages):
        res=""
        for string in messages:
            res+=str(string)+"\n"
        print(res)
    def debug(self, level=1, *messages):
        if (level<=self.debugLevel):
            res=""
            for string in messages:
                res+=str(string)+"\n"
            print(res+"\n")
    def processData(self, path, params={"roles":[]}):
        d=data.dataparser.excelXMLparser(self, params["roles"], path)
        d.normtableGen([], self.params["allowPreserveNumericData"])
        self.norm=d.generateNormalizedDataset()
        
    def addLayer(self, clName="layer"):
        #print(str(clName))
        lay=classesLayers[clName](self)
        self.layers.append(lay)
        return lay
    def connectToPrev(self):
        self.layers[len(self.layers)-1].connectToLayer(self.layers[len(self.layers)-2])
    def getAnswer(self): #getting answer of current incoming data
        i=0
        while (i<=len(self.layers)-1):
            if (self.layers[i].typ!="enterLayer"):
                self.layers[i].getAnswerFromPrev()
            i+=1
    def innlayerGen(self):
        if (self.norm==0):
            self.errorMes("Normalized data missing!")
            return
        lay=enterLayer(self)
        for val in self.norm.columns:
            m=[]
            if (self.norm.normtable.table[self.norm.columns.index(val)][1]=="numeric"):
                n=lay.addNeuron();
                m.append(n)
            else:
                for arr in val.cells[0]:
                    n=lay.addNeuron();
                    m.append(n)
            lay.inn[self.norm.columns.index(val)]=m
        self.layers.append(lay)
        self.innlayer=lay
    def outlayerGen(self):
        if (self.norm==0):
            print("Normalized data missing!")
            return
        lay=outLayer(self)
        for val in self.norm.answers:
            m=[]
            if (self.norm.normtable.table[self.norm.answers.index(val)][1]=="numeric"):
                n=lay.addNeuron("outNeuron");
                m.append(n)
            else:
                for arr in val.cells[0]:
                    n=lay.addNeuron("outNeuron");
                    m.append(n)
            lay.out[self.norm.answers.index(val)]=m
        self.layers.append(lay)
        self.outlayer=lay
    def setInput(self, index): #fills input layer neuron outputs with normalized data by it'r index
        if (self.norm==0):
            self.errorMes("Normalized data missing!")
            return
        for col in self.norm.columns:
            if (len(col.cells)-1<index and self.norm.normtable.table[self.norm.columns.index(col)][1]!="numeric"):
                self.errorMes("Data index out of range!")
                return
            if (self.norm.normtable.table[self.norm.columns.index(col)][1]=="numeric"):
                for neu in self.innlayer.inn[self.norm.columns.index(col)]:
                    neuIndex=self.innlayer.inn[self.norm.columns.index(col)].index(neu)
                    neu.out=actives.activ[self.normtableParams["numeric"]["normtype"]].activate(self.norm.normtable.table[self.norm.columns.index(col)][0][index], self.norm.alphaParams[self.norm.columns.index(col)]) 
            else:
                for neu in self.innlayer.inn[self.norm.columns.index(col)]:
                    neuIndex=self.innlayer.inn[self.norm.columns.index(col)].index(neu)
                    neu.out=col.cells[index][neuIndex]
    def getAnswer(self):
        i=1
        while (i<len(self.layers)):
            self.layers[i].getAnswerFromPrev()
            i+=1
    def giveInput(self, inn): #get array of not normalized data, normalizes it and aet to input layer
        if (type(inn)!=list):
            self.errorMes("Input is not array!")
            return
        if (len(inn)!=len(self.innlayer.inn)):
            self.errorMes(str(len(self.innlayer.inn))+" arguments needed!")
        res=[]
        i=0
        for arg in inn:
            if (self.norm.normtable.normtype[i]=="numeric"):
                try:
                    num=float(inn[i])
                    res.append([actives.activ[self.norm.normtable.params["numeric"]["normtype"]].activate(num, self.norm.alphaParams[i])])
                except ValueError:
                    self.errorMes("Argument "+inn[i]+" is not numeric data!")
                    return
            else:
                try:
                    res.append(self.norm.normtable.table[i][1][self.norm.normtable.table[i][0].index(inn[i])])
                except ValueError:
                    self.errorMes("Cannot fing argument "+inn[i]+" in normalization table!")
                    return
            i+=1
        #adding values to neurons
        i=0
        for r in res:
            j=0
            for neu in self.innlayer.inn[i]:
                self.innlayer.inn[i][j].out=res[i][j]
                j+=1

            i+=1
    def compareOutput(self, ansIndex):#compares net output with answers in data !!!!!!доделать с нормализацией для цифр
        for ans in self.norm.answers:
            i=0
            for neu in self.outlayer.out[self.norm.answers.index(ans)]:
                #neuIn=self.outlayer.out[self.norm.answers.index(ans)].index(neu)
                self.outlayer.out[self.norm.answers.index(ans)][i].mistake=ans.cells[ansIndex][i]-self.outlayer.out[self.norm.answers.index(ans)][i].out
            i+=1
    def denormalize(self): #convert current output to array of denormalized data
        res=[]
        i=0
        for ans in self.norm.answers:
            m=[]
            j=0
            while (j<=len(self.outlayer.out[i])-1):
                if (self.norm.ansNormtype[i]=="numeric"):
                    m.append(self.outlayer.out[i][j].out)
                else:
                    m.append(round(self.outlayer.out[i][j].out))
                j+=1                    
            #denorm result now
            r=0
            z=0
            for rol in self.norm.normtable.roles:
                if (rol):
                    if (i==r):
                        if (self.norm.ansNormtype[i]=="numeric"):
                            self.debug(3, "denorm, normtype", self.norm.alphaParams[r], self.norm.normtable.params["numeric"])
                            res.append(actives.activ[self.norm.normtable.params["numeric"]["normtype"]].denorm(m[0], self.norm.ansAlpha[r]))
                        else:
                            self.debug(3, "from denormalize", self.norm.normtable.table[z][1], m)
                            res.append(self.norm.normtable.table[z][0][self.norm.normtable.table[z][1].index(m)])
                    r+=1
                z+=1
            i+=1
        return res
    def use(self, data): #gets array of not-normalized data and returns array of denormalized answer data
        self.giveInput(data)
        self.getAnswer()
        return self.denormalize()
    def conditionsCheck(self):
        if (self.conditions["epochs"]<=self.stats["epochs"]):
            return "Finished: epochs limit"
        if (self.conditions["middlemistake"]>=self.stats["middlemistake"]):
            return "Finished: middle error"
        if (self.conditions["maxmistake"]>=self.stats["maxmistake"]):
            return "Finished: max error"
        return False
    
    def startLearning(self, algorithm):
        self.learning=True
        algs.algs[algorithm].start(self)

class layer: # abstract for layers
    typ="layer"
    def __init__ (self, network):
        self.network=network
        self.activation=self.network.activation
        self.neurons=[]
        if (self.typ!="outlayer" and self.network.params["additNeurons"]!=0):
            self.addNeuron("additNeuron").out=self.network.params["additNeurons"]
    def addNeuron(self, clName="neuron"):
            n=classesNeurons[clName](self)
            n.number=len(self.neurons)
            self.neurons.append(n)
            return n
    def addNeurons(self, num=5, clName="neuron"):
            while (num>0):
                self.addNeuron(clName)
                num-=1
    def connectToLayer(self, layer):
        for neu in self.neurons:
            for neu2 in layer.neurons:
                neu.connectToNeu(neu2)
    def getAnswerFromPrev(self):
        if (self.network.pool!=False):
            recieves=0 #count of recieves
            procId=0
            for neu in self.neurons:
                neu.number=self.neurons.index(neu)
                self.network.pool.outputs[procId].send([neu, "getsum", "getout", False])
                
                if(procId>=len(self.network.pool.pool)-1):
                    procId=0
                    recieves+=self.network.pool.responseHandler(self.setNeuroOutput)
                else:
                    procId+=1
            while (recieves<len(self.neurons)):
                recieves+=self.network.pool.responseHandler(self.setNeuroOutput)
        else:
            for neu in self.neurons:
                neu.getsum()
                neu.getout()
    def setNeuroOutput(self, output):#for multiprocessind only
        self.neurons[output[1]].out=output[0]
        
class enterLayer(layer): #entering layer of network
    typ="enterLayer"
    inn={} #holds arrays of neurons, each for one data point

class outLayer(layer):#outlayer of network
    typ="outlayer"
    out={} #holds arrays of neurons, each for one data answer
    
class neuron: # abstract class for neurons
    typ="neuron"
    number=0
    summ=0.0 # sum of all previous layer outputs
    out=0.0 # current neuron output
    q=0 # current computed misatke
    def __getstate__(self):
        res={}
        res["typ"]=self.typ
        res["number"]=self.number
        res["out"]=self.layer.network.params["additNeurons"]
        res["summ"]=self.summ
        res["q"]=self.q
        res["alpha"]=self.layer.network.params["alpha"]
        res["sinapses"]=[]
        for sin in self.sinapses:
            res["sinapses"].append({"weight":sin.weight, "out":sin.prevneuron.out})
        res["getsum"]=self.getsumPick
        res["getout"]=self.getoutPick
        if hasattr(self, "activation"):
            res["activation"]=self.activation
        else:
            res["activation"]=self.layer.activation
        if hasattr(self, "mistake"):
            res["mistake"]=self.mistake
        return res
    def __init__ (self, layer):
        self.layer=layer
        self.outneurons=[]
        self.sinapses=[] #sinapses which connect neuron with previous layer
        self.sinapsesOfOut=[] #sinapses which connect neuron with next layer
    def connectToNeu(self, neur): # connect to neuron from previous layer
        if (self.layer.network.params["impulse"]==0):
            sinaps(self, neur).weight=random.uniform(self.layer.network.synmax, self.layer.network.synmin)
        else:
            sinapsImpulse(self, neur).weight=random.uniform(self.layer.network.synmax, self.layer.network.synmin)
    def getsum (self): #getting weigh sum of all previous neurons outputs
        self.summ=0
        for sin in self.sinapses:
            self.summ+=sin.weight*sin.prevneuron.out
    def getsumPick (self): #for picked object only
        self.summ=0
        for sin in self.sinapses:
            self.summ+=sin["weight"]*sin["out"]
    def getactiv(self): #return activation function for current neuron
        return self.layer.activation
    def getout (self):
        if hasattr(self, "activation"):
            self.out=actives.activ[self.activation].activate(self.summ, self.layer.network.params["alpha"])
        else:
            self.out=actives.activ[self.layer.activation].activate(self.summ, self.layer.network.params["alpha"])
        return self.out
    def getoutPick(self): #for picked object only
        if (self.typ=="additNeuron"):
            return self.out
        else:
            self.out=actives.activ[self.activation].activate(self.summ, self.alpha)
        return self.out
class outNeuron (neuron):
    mistake=0;

class neuronOwnActivator (neuron):
    "Has personal activation function, instead of using layer parametr"
    activation="sigmoid"
    def getactiv(self): #return activation function for current neuron
        return self.activation
class additNeuron (neuron):
    typ="additNeuron"
    def getsum(self):
        return 0
    def getout(self):
        return self.layer.network.params["additNeurons"]
    def connectToNeu(self, neur):
        return

class sinaps (): #container with information for sinapses
    weight=0.0
    def __init__(self, owner, prevneuron):
        self.owner=owner
        self.prevneuron=prevneuron
        owner.sinapses.append(self)
        prevneuron.outneurons.append(owner)
        prevneuron.sinapsesOfOut.append(self)
        
class sinapsImpulse (sinaps):
    prevCorr=0.0
        

classesNeurons={"neuron":neuron,"neuronOwnActivator":neuronOwnActivator, \
                "outNeuron":outNeuron, "additNeuron":additNeuron}
classesLayers={"layer":layer, "enterLayer":enterLayer, "outLayer":outLayer}     
    
    
