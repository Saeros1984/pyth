import random
import modules.actives as actives
import modules.data as data

class network: # abstact class for networks
    name=""
    
    synmax=1.0
    synmin=-1.0
    networks=[]
    norm=0
    innlayer=0
    outlayer=0
    def __init__ (self, name="", activation="sigmoid"):
        self.networks.append(self)
        if (name==""):
            self.name="network "+str(len(self.networks)+1)
        else:
            self.name=name
        self.activation=activation
        self.layers=[]
        return
    def processData(self, path, params={"roles":[]}):
        d=data.dataparser.excelXMLparser(params["roles"], path)
        d.normtableGen()
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
            print("Normalized data missing!")
            return
        lay=enterLayer(self)
        for val in self.norm.columns:
            m=[]
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
            for arr in val.cells[0]:
                n=lay.addNeuron("outNeuron");
                m.append(n)
            lay.out[self.norm.answers.index(val)]=m
        self.layers.append(lay)
        self.outlayer=lay
    def setInput(self, index): #fills input layer neuron outputs with normalized data by it'r index
        if (self.norm==0):
            print("Normalized data missing!")
            return
        if (len(self.norm.columns[0].cells)-1<index):
            print ("Data index out of range!")
            return
        for col in self.norm.columns:
            for neu in self.innlayer.inn[self.norm.columns.index(col)]:
                neuIndex=self.innlayer.inn[self.norm.columns.index(col)].index(neu)
                neu.out=col.cells[index][neuIndex]
    def compareOutput(self, ansIndex):#compares net output with answers in data
        for ans in self.norm.answers:
            i=0
            for neu in self.outlayer.out[self.norm.answers.index(ans)]:
                #neuIn=self.outlayer.out[self.norm.answers.index(ans)].index(neu)
                self.outlayer.out[self.norm.answers.index(ans)][i].mistake=ans.cells[ansIndex][i]-self.outlayer.out[self.norm.answers.index(ans)][i]
            i+=1
        

class layer: # abstract for layers
    typ="layer"
    def __init__ (self, network):
        self.network=network
        self.activation=self.network.activation
        self.neurons=[]
    def addNeuron(self, clName="neuron"):
            n=classesNeurons[clName](self)
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
        for neu in self.neurons:
            neu.getsum()
            neu.getout()
class enterLayer(layer): #entering layer of network
    typ="enterLayer"
    inn={} #holds arrays of neurons, each for one data point

class outLayer(layer):#outlayer of network
    typ="outlayer"
    out={} #holds arrays of neurons, each for one data answer
    
class neuron: # abstract class for neurons
    summ=0.0 # sum of all previous layer outputs
    out=0.0 # current neuron output
    q=0 # current computed misatke
    def __init__ (self, layer):
        self.layer=layer
        self.outneurons=[]
        self.sinapses=[]
    def connectToNeu(self, neur): # connect to neuron from previous layer
        sinaps(self, neur).weight=random.uniform(self.layer.network.synmax, self.layer.network.synmin)
    def getsum (self): #getting weigh sum of all previous neurons outputs
        for sin in self.sinapses:
            self.summ+=sin.weight*sin.prevneuron.out
    def getout (self):
        if hasattr(self, "activation"):
            self.out=actives.activ[activation].activate(self.summ)
        else:
            self.out=actives.activ[self.layer.activation].activate(self.summ)
        
class outNeuron (neuron):
    compareRes=0;

class neuronOwnActivator (neuron):
    "Has personal activation function, instead of using layer parametr"
    activation="sigmoid"

class sinaps (): #container with information for sinapses
    weight=0.0
    def __init__(self, owner, prevneuron):
        self.owner=owner
        self.prevneuron=prevneuron
        owner.sinapses.append(self)
        prevneuron.outneurons.append(owner)
        
        
        

classesNeurons={"neuron":neuron,"neuronOwnActivator":neuronOwnActivator, \
                "outNeuron":outNeuron}
classesLayers={"layer":layer, "enterLayer":enterLayer, "outLayer":outLayer}     
    
    
