import random
import math
import modules.actives as actives
import modules.data as data
import modules.lossfunctions as loss
import modules.algorithms as algs
import modules.multiproc as pr

class networkPool:
    name=""
    netpools=[]
    def __len__(self):
        return len(self.nets)
    def __init__(self, name=""):
        self.nets=[]
        if (name==""):
            self.name="Pool "+str(len(self.netpools)+1)
        else:
            self.name=name
        networkPool.netpools.append(self)

class network: # abstact class for networks
    name=""
    debugLevel=4 #the importsnce of the messages - 1 is the highest
    activation=""
    synmax=1.3
    synmin=-1.3
    innlayer=0
    outlayer=0
    learning=False #shows if learning process executes right now

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
        self.valid=0 #table of validation data
        self.test=0 #table of testing data
        self.norm=0
        self.stats={"descr":"", \
           "epochs":0, \
           "maxmistake":1.0, \
           "middlemistake":1.0, \
           "currentBatch":0, \
           "ValidMaxMistake":1, \
           "ValiMiddleMistake":1, \
           "TestMaxMistake":1, \
           "TestMiddleMistake":1, \
           "TestRecognition":[], \
           
           }
        self.bestStats=[]
        self.params={"learning":"backPropagation", \
                "speed":0.3, \
                "alpha":1, \
                "additNeurons":1, \
                "impulse":0.9, \
                "lossFunction":"fabs", \
                "allowPreserveNumericData":False, \
                "regularization":False, \
                "batchSize":1, \
                "usedData":100, \
                "validationData":0, \
                "testData":10, \
                "bestResults":1, \
                "testRecognition":True
                
                }
        self.alphas={"linear":1, "sigmoid":1, \
                   "tanh":1, "reLU":[0.01, 0.1], "bipolar":1, \
                   "ELU":[1, 1], "gauss":1}
        self.CoshiParams={"T0":150, \
                    "T":0, \
                     "Tcoeff":1, \
                     "speed":1, \
                     "CoshiReg":True, \
                     "top":1.5, \
                     "forfeit":0.2, \
                     "randomReset":True, \
                     "CoshiCoeff":0.5
                     
                     }
        self.regularization={ \
                        }
        self.conditions={"epochs":500, \
                    "maxmistake":0.1, \
                    "middlemistake":0.0,\
                    "testMaxMistake":0, \
                    "testMiddleMistake":0, \

                    }
        self.normtableParams={"uno":{},\
                         "boolean":{"role":False, "zero":1, "one":0}, \
                         "triple":{"role":False, "activtype":1}, \
                         "diff":{"role":False}, \
                         "numeric":{"role":False, "normtype":"linear", "alpha":1}}
        self.paramsForGen={"layers":1, "neurons":5}
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
    def processData(self, path, params={"roles":[],"activtype":1}):
        d=data.dataparser.excelXMLparser(self, params["roles"], path)
        print("Data parsing finished")
        d.normtableGen([], self.params["allowPreserveNumericData"])
        print("Normtable generated")
        self.norm=d.generateNormalizedDataset()
        print("Data normalized")
        self.generateUsedData()
        self.generateValidData()
        self.generateTestData()
        print("Test data generated")
    def generateUsedData(self): #only left several percents of data to use
        if (self.params["usedData"]>=100):
            return 0
        datanum=math.floor(self.norm.length/100*(100-self.params["usedData"]))
        for i in range(datanum):
            r=random.randint(0, self.norm.length-1)
            del self.norm.mistakes[0]
            del self.norm.recognize[0]
            for j in range(len(self.norm.columns)):
                del self.norm.columns[j].cells[r]
            for j in range(len(self.norm.answers)):
                del self.norm.answers[j].cells[r]
            self.norm.length-=1
    def generateValidData(self):
        if (self.params["validationData"]==0):
            return 0
        validat=data.normalizedData()
        self.valid=validat
        datanum=math.ceil(self.norm.length/100*self.params["validationData"])

        for c in self.norm.columns:
            validat.columns.append(data.datacolumn())
        for c in self.norm.answers:
            validat.answers.append(data.datacolumn())

        for i in range(datanum):
            r=random.randint(0, self.norm.length-1)
            validat.mistakes.append(1)
            validat.recognize.append([])
            del self.norm.mistakes[0]
            del self.norm.recognize[0]
            for j in range(len(self.norm.columns)):
                validat.columns[j].cells.append(self.norm.columns[j].cells.pop(r))
            for j in range(len(self.norm.answers)):
                validat.answers[j].cells.append(self.norm.answers[j].cells.pop(r))
            self.norm.length-=1
            validat.length+=1
    def generateTestData(self):
        if (self.params["testData"]==0):
            return 0
        testdat=data.normalizedData()
        self.test=testdat
        datanum=math.ceil(self.norm.length/100*self.params["testData"])

        for c in self.norm.columns:
            testdat.columns.append(data.datacolumn())
        for c in self.norm.answers:
            testdat.answers.append(data.datacolumn())

        for i in range(datanum):
            r=random.randint(0, self.norm.length-1)
            testdat.mistakes.append(1)
            testdat.recognize.append([])
            del self.norm.mistakes[0]
            del self.norm.recognize[0]
            for j in range(len(self.norm.columns)):
                testdat.columns[j].cells.append(self.norm.columns[j].cells.pop(r))
            for j in range(len(self.norm.answers)):
                testdat.answers[j].cells.append(self.norm.answers[j].cells.pop(r))
            self.norm.length-=1
            testdat.length+=1
    def addLayer(self, clName="layer", activ="inherit"):
        #print(str(clName))
        lay=classesLayers[clName](self, activ)
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
        i=0
        for val in self.norm.normtable.table:
            m=[]
            if (val=="numeric"):
                n=lay.addNeuron();
                m.append(n)
            else:
                for arr in val[1][0]:
                    n=lay.addNeuron();
                    m.append(n)
            lay.inn[i]=m
            i+=1
        self.layers.append(lay)
        self.innlayer=lay
    def outlayerGen(self, activ="inherit"):
        if (self.norm==0):
            print("Normalized data missing!")
            return
        lay=outLayer(self, activ)
        for val in self.norm.normtable.answers:
            m=[]
            if (val=="numeric"):
                n=lay.addNeuron("outNeuron");
                m.append(n)
            else:
                for arr in val[1][0]:
                    n=lay.addNeuron("outNeuron");
                    m.append(n)
            lay.out[self.norm.normtable.answers.index(val)]=m
        self.layers.append(lay)
        self.outlayer=lay
    def setInput(self, index, of=""): #fills input layer neuron outputs with normalized data by it'r index
        if (self.norm==0):
            self.errorMes("Normalized data missing!")
            return
        if (of==""):
            of=self.norm
        for col in of.columns:
            if (len(col.cells)-1<index and self.norm.normtable.table[of.columns.index(col)][1]!="numeric"):
                self.errorMes("Data index out of range!")
                return
            if (self.norm.normtable.table[of.columns.index(col)]=="numeric"):
                for neu in self.innlayer.inn[of.columns.index(col)]:
                    neu.out=col.cells[index][0]
            else:
                for neu in self.innlayer.inn[of.columns.index(col)]:
                    neuIndex=self.innlayer.inn[of.columns.index(col)].index(neu)
                    #neu.out=self.norm.columns.index(col)[index]
                    neu.out=of.columns[of.columns.index(col)].cells[index][neuIndex]
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
    def compareOutput(self, ansIndex, of=""):#compares net output with answers in data !!!!!!доделать с нормализацией для цифр
        if (of==""):
            of=self.norm
        for ans in of.answers:
            i=0
            for neu in self.outlayer.out[of.answers.index(ans)]:
                #neuIn=self.outlayer.out[self.norm.answers.index(ans)].index(neu)
                self.outlayer.out[of.answers.index(ans)][i].mistake=ans.cells[ansIndex][i]-self.outlayer.out[of.answers.index(ans)][i].out
                self.outlayer.out[of.answers.index(ans)][i].rightValue=ans.cells[ansIndex][i]
                i+=1
    def clearAnswer(self, ind, m):
        if (self.norm.normtable.answersTypes[ind]=="triple" or self.norm.normtable.answersTypes[ind]=="diff"):
            maxx=max(m)
            for value in m:
                if (value==maxx):
                    m[m.index(value)]=1
                else:
                    m[m.index(value)]=0
        if (self.norm.normtable.answersTypes[ind]=="boolean"):
            m[0]=round(m[0])
        return m
    def denormalize(self, denorm=True): #convert current output to array of denormalized data
        res=[]
        i=0
        for ans in self.norm.normtable.answers:
            m=[]
            j=0
            while (j<=len(self.outlayer.out[i])-1):
                if (self.norm.normtable.answersTypes[i]=="numeric"):
                    m.append(self.outlayer.out[i][j].out)
                else:
                    m.append(self.outlayer.out[i][j].out)
                j+=1
            m=self.clearAnswer(i, m)
            #denorm result now
            r=0
            z=0
            for rol in self.norm.normtable.answersTypes:
                if (rol):
                    if (i==r):
                        if (self.norm.normtable.answersTypes[i]=="numeric"):
                            self.debug(5, "denorm, normtype", self.norm.normtable.alphaParams[r], self.norm.normtable.params["numeric"])
                            if (denorm):
                                res.append(actives.activ[self.norm.normtable.params["numeric"]["normtype"]].denorm(m[0], self.norm.ansAlpha[r]))
                            else:
                                res.append(m)
                        else:
                            self.debug(5, "from denormalize", self.norm.normtable.answers[z][1], m)
                            if (denorm):
                                try:
                                    res.append(self.norm.normtable.answers[z][0][self.norm.normtable.answers[z][1].index(m)])
                                except:
                                    res.append("no such answer!")
                            else:
                                res.append(m)
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
            return "Finished: train average error"
        if (self.conditions["maxmistake"]>=self.stats["maxmistake"]):
            return "Finished: train max error"
        if (self.conditions["testMaxMistake"]>=self.stats["TestMaxMistake"]):
            return "Finished: test max error"
        if (self.conditions["testMiddleMistake"]>=self.stats["TestMiddleMistake"]):
            return "Finished: test average error"
        return False
    
    def startLearning(self, algorithm=""):
        self.learning=True
        if (algorithm==""):
            algs.algs[self.params["learning"]].start(self)
        else:
            algs.algs[algorithm].start(self)
    def checkResult(self):#checking if current result is the best
        if (self.bestStats==[]):
            self.bestStats.append(self.stats.copy())
            return True
        if (self.stats["TestMiddleMistake"]<self.bestStats[0]["TestMiddleMistake"]):
            self.bestStats.insert(0, self.stats.copy())
            if (len(self.bestStats)>self.params["bestResults"]):
                del self.bestStats[len(self.bestStats)-1]
        return False
    def saveResult(self):#save result into weights
        for l in self.layers:
            for n in l.neurons:
                for s in n.sinapses:
                    if (not hasattr(s, "bestValue")):
                        s.bestValue=[]
                        s.bestValue.append(s.weight)
                        continue
                    s.bestValue=s.weight+s.bestValue
                    if (len(s.bestValue)>self.params["bestResults"]):
                        del s.bestValue[len(self.bestStats)-1]
    def setResult(self, num): #set the chosen best result to this nerwork
        if (num>self.params["bestResults"]-1):
            self.errorMes("no results preserved on this index")
            return
        for l in self.layers:
            for n in l.neurons:
                for s in n.sinapses:
                    s.weight=s.bestValue[num]
        self.stats=self.bestStats[num]
    def visual(self):
        res=""
        sin=""
        i=len(self.layers)-1
        for l in self.layers:
            for n in self.layers[i].neurons:
                res+="O "
                sin+="\n"
                for s in n.sinapses:
                    sin+=str(s.weight)+" "

            i-=1
            res+="\n"
        print (res)
        print (sin)
        
class layer: # abstract for layers
    typ="layer"
    def __init__ (self, network, activation="inherit"):
        self.network=network
        self.activation=activation
        self.alpha="inherit"
        self.alphas=self.network.alphas
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
    def getactiv(self): #return activation function for current layer
        if (self.activation=="inherit"):
            return self.network.activation
        else:
            return self.activation
    def getalpha(self): #return alpha for current layer
        if (self.alpha=="inherit"):
            return self.network.alphas[self.getactiv()]
        else:
            return self.alphas[self.getactiv()]
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
    def visual(self):
        res="OUTS:\n"
        for n in self.neurons:
            res+=str(n.out)+" "
        res+="\nWEIGHTS: \n"
        for n in self.neurons:
            res+="\n"
            for s in n.sinapses:
                res+=str(round(s.weight, 3))+" "
        print(res)
    def setNeuroOutput(self, output):#for multiprocessind only
        self.neurons[output[1]].out=output[0]
        
class enterLayer(layer): #entering layer of network
    typ="enterLayer"
    inn={} #holds arrays of neurons, each for one data point

class outLayer(layer):#outlayer of network
    typ="outlayer"
    out={} #holds arrays of neurons, each for one data answer
    def visual(self):
        res="OUTS:\n"
        for n in self.neurons:
            res+=str(n.out)+" "
        res+="\nMISTAKES: \n"
        for n in self.neurons:
            res+=str(n.mistake)+" "
        res+="\nWEIGHTS: \n"
        for n in self.neurons:
            res+="\n"
            for s in n.sinapses:
                res+=str(round(s.weight, 3))+" "
        print(res)

class radialLayer(layer):
    typ="radialLayer"
    def __init__(self, network, function="gauss"):
        super().__init__(network)
        self.activation=function
        self.neurons[0].c=0
    def addNeuron(self, c, clName="neuronRadial"):
            n=classesNeurons[clName](self)
            n.number=len(self.neurons)
            n.c=c
            self.neurons.append(n)
            return n
    def addNeurons(self, r1, r2, num=5, clName="neuronRadial"):
            num0=num
            while (num>0):
                c=(r2-r1)/num0*num+r1
                self.addNeuron(float(c), clName)
                num-=1
    
class neuron: # abstract class for neurons
    typ="neuron"
    number=0
    summ=0.0 # sum of all previous layer outputs
    out=0.0 # current neuron output
    q=0 # current computed misatke
    batchQ=0
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
        return self.layer.getactiv()
    def getalpha(self): #return alpha for current neuron
            return self.layer.getalpha()
    def getout (self):
        self.out=actives.activ[self.getactiv()].activate(self)
        return self.out
    def getoutPick(self): #for picked object only
        if (self.typ=="additNeuron"):
            return self.out
        else:
            self.out=actives.activ[self.activation].activate(self.summ, self.alpha)
        return self.out
class outNeuron (neuron):
    mistake=0
    rightValue=0
    calculatedMistake=0
    lossDerivative=0

class neuronOwnActivator (neuron):
    "Has personal activation function, instead of using layer parametr"
    activation="sigmoid"
    def getactiv(self): #return activation function for current neuron
        return self.activation
    def getalpha(self): #return alpha for current neuron
        return self.alphas[self.getactiv()]
class neuronRadial(neuronOwnActivator):
    "for rafial activation functions"
    c=0
    activation="gauss"
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
    accumDelta=0
    def __init__(self, owner, prevneuron):
        self.owner=owner
        self.prevneuron=prevneuron
        owner.sinapses.append(self)
        prevneuron.outneurons.append(owner)
        prevneuron.sinapsesOfOut.append(self)
        
class sinapsImpulse (sinaps):
    prevCorr=0.0
        

classesNeurons={"neuron":neuron,"neuronOwnActivator":neuronOwnActivator, \
                "outNeuron":outNeuron, "additNeuron":additNeuron, "neuronRadial":neuronRadial}
classesLayers={"layer":layer, "enterLayer":enterLayer, "outLayer":outLayer, "radialLayer":radialLayer}     
    
    
