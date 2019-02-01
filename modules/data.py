#classes for working with data
import re
import modules.actives as actives

class data():
    cellnumber=0
    length=0
    def __init__(self, network):
        self.columns=[]
        self.celltypes=[] #type of content cell contain (string, bool, etc)
        self.roles=[] #true - cells is answer-data
        self.normtype=[] #type of used normalization
        self.normtable=normalizationTable(network.normtableParams)
        self.alphaParams=[] #parameters of alpha for numeric normalization
    def normtableGen(self, normtypes=[], numEnclude=False):#numEnclude will allow to generate prepared norms for numeric data
        if (len(self.normtable.table)<1):
            print ("Data not parsed!")
            return
        if (normtypes==[]):
            normtypes=self.celltypes
        if (len(normtypes)!=len(self.columns)):
            self.network.errorMes ("wrong normalization types argument number!")
            return
        self.normtable.types=normtypes
        self.normtable.roles=self.roles
        self.normtable.alphaParams=self.alphaParams
        i=0
        for di in self.normtable.table:
            if (normtypes[i]=="numeric"):
                self.normtable.table[i]="numeric"
                i+=1
                continue
            else:
                self.normtable.table[i].append([])                
            j=0
            #for val in self.normtable.table[i][0]:
            while (j<len(self.normtable.table[i][0])):
                if (self.normtable.table[i]=="numeric"):
                    j+=1
                    break
                if (j>100):
                    break
                val=self.normtable.table[i][0][j]
                if (self.roles[i]):
                    self.normtable.params[normtypes[i]]["role"]=True
                else:
                    self.normtable.params[normtypes[i]]["role"]=False
                if (normtypes[i]=="numeric"):
                    self.normtable.params[normtypes[i]]["alpha"]=self.alphaParams[i]
                self.normtable.table[i][1].append(normalizeTypes[normtypes[i]](self.normtable.table[i][0], val, self.normtable.params[normtypes[i]]))
                j+=1

            i+=1
    def generateNormalizedDataset(self):
        if (len(self.normtable.table)==0):
            self.errorMes("Normalization table missing!")
            return
        norm=normalizedData()
        norm.length=self.length
        norm.celltypes=self.celltypes
        norm.roles=self.roles
        norm.normtype=self.normtable.types
        norm.normtable=self.normtable
        norm.alphaParams=self.alphaParams
        for col in self.columns:
            norm.columns.append(datacolumn())
        i=0
        for ro in range(self.length):
            j=0
            norm.mistakes.append(1)
            norm.recognize.append([])
            for col in self.columns:
                if (self.normtable.table[j]=="numeric"):
                    j+=1
                    continue
                res=self.normtable.table[j][0].index(self.columns[j].cells[i])
                norm.columns[j].cells.append(self.normtable.table[j][1][res])
                j+=1
            i+=1
        i=0
        for col in self.columns:
            if (self.normtable.table[i]=="numeric"):
                norm.columns[i].cells=[normalizeTypes[self.normtable.types[i]](self.normtable.table[i][0], j, {"normtype":"linear", "alpha":self.alphaParams[i]}) for j in self.columns[i].cells]
            i+=1
        i=0
        for t in range(len(norm.normtable.table)):
            if (norm.normtable.roles[i]==True):
                z=norm.normtable.table.pop(i)
                norm.normtable.answers.append(z)
                z=norm.normtable.alphaParams.pop(i)
                norm.normtable.answersAlphas.append(z)
                z=norm.normtable.types.pop(i)
                norm.normtable.answersTypes.append(z)
            i+=1
        i=0
        for col in self.columns:
            if (norm.normtable.roles[i]):
                z=norm.columns[i]
                norm.answers.append(z)
                norm.columns.remove(z)
            i+=1
        return norm
    def visual(self):
        s="columns\n"
        for c in self.columns:
            s+="["
            i=0
            for a in c.cells:
                s+=str(c.cells[i])+" "
                i+=1
            s+="\n"
        print(s)
class normalizedData():
    def __init__(self):
        self.length=0
        self.columns=[]
        self.answers=[]
        self.celltypes=[] #type of content cell contain (string, bool, etc)
        self.roles=[] #true - cells is answer-data
        self.normtype=[] #type of used normalization
        self.ansNormtype=[]
        self.ansAlpha=[]
        self.mistakes=[] #mistakes for each data row
        self.recognize=[] #is recognized
        self.normtable=0
    def visual(self):
        s="columns\n"
        for c in self.columns:
            s+="["
            i=0
            for a in c.cells:
                s+=str(c.cells[i])+" "
                i+=1
            s+="\n"
        s+="answers\n"
        for c in self.answers:
            s+="["
            i=0
            for a in c.cells:
                s+=str(c.cells[i])+" "
                i+=1
            s+="\n"
        print(s)

class datacolumn():
    def __init__(self):
        self.cells=[]

class normalizationTable():
    def __init__(self, params):
        self.table=[]
        self.answers=[]
        self.alphasParams=[]
        self.answersAlphas=[]
        self.types=[]
        self.answersTypes=[]
        self.params=params
    def visual(self):
        s="columns\n"
        for c in self.table:
            s+="["
            i=0
            for a in c:
                s+=str(c[i])+" "
                i+=1
            s+="\n"
        s+="answers\n"
        for c in self.answers:
            s+="["
            i=0
            for a in c:
                s+=str(c[i])+" "
                i+=1
            s+="\n"
        print(s)

class dataparser():
    def delDuples(lis):
        arr=lis.copy()
        i=0
        while (True):
            if (i>=len(arr)):
                break
            ch=arr[i]
            j=i+1
            while (True):
                if (j>=len(arr)):
                        break
                if (ch==arr[j]):
                    arr.remove(arr[j])
                else:
                    j+=1
            
            i+=1
        return arr
    def excelXMLparser(network, roles=[], path="C:/Users/USER/Desktop/xor.xml"):
        "parsing data from Excel table saved as XML2003"
        try:
            dat=data(network)
            file=open(path, "r")
            rawdata=file.read()
            file.close()
        except:
            network.errorMes("Data file reading mistake")
            return
        cellanalyze=re.findall('<data.*?>(.*?)</data>', re.search('<row.*?>(.*?)</row>', rawdata, re.DOTALL|re.I).group(0), re.DOTALL|re.I)#get first row of data for analyze
        z=0
        for i in cellanalyze:
            dat.columns.append(datacolumn())
            dat.normtable.table.append([])
            dat.celltypes.append("none")
            dat.roles.append(False)
            dat.alphaParams.append(1)
            for ro in roles:
                if (z==ro):
                    dat.roles[z]=True
            z+=1
        dat.cellnumber=len(cellanalyze)
        for row in re.findall('<row.*?>(.*?)</row>', rawdata, re.DOTALL|re.I):
            cells=re.findall('<data.*?>(.*?)</data>', row, re.DOTALL|re.I)
            i=0
            for cell in cells:
                dat.columns[i].cells.append(cells[i])
                i+=1
            
        #here we going to analyze data types in our table
        j=0
        dat.length=len(dat.columns[0].cells)
        for column in dat.columns:
            #dist=dataparser.delDuples(dat.columns[j].cells)
            dist=sorted(list(set(dat.columns[j].cells)))
            dat.normtable.table[j].append(dist)
            distinctnum=len(dist)
            if (distinctnum==1):
                dat.celltypes[j]="uno"
            elif (distinctnum==2):
                dat.celltypes[j]="boolean"
            elif (distinctnum==3):
                dat.celltypes[j]="triple"
            elif (distinctnum>3):
                try:
                    i = float(dat.normtable.table[j][0][0])
                    dist=[float(i) for i in dist]
                    dat.columns[j].cells=[float(i) for i in dat.columns[j].cells]
                    dat.celltypes[j]="numeric"
                    dat.normtable.table[j]="numeric"
                    
                    maxx=max(dist)
                    minn=min(dist)
                    dat.alphaParams[j]=1/(maxx-minn)
                except ValueError:
                    dat.celltypes[j]="diff"
            j+=1
        return dat

class normalize():
    def uno(distmass, value, params):
        return [0]
    def boolean(distmass, value, params):
        if (not params["role"]):
            if (distmass.index(value)==1):
                return [1]
            if (distmass.index(value)==0):
                return [-1]
        else:
            if (distmass.index(value)==0):
                return [params["one"]]
            if (distmass.index(value)==1):
                return [params["zero"]]
    def triple(distmass, value, params):
        if (params["activtype"]==1):
            if (distmass.index(value)==0):
                return [1, 0, 0]
            if (distmass.index(value)==1):
                return [0, 1, 0]
            if (distmass.index(value)==2):
                return [0, 0, 1]
        if (params["activtype"]==2):
            if (distmass.index(value)==0):
                return [1, 0]
            if (distmass.index(value)==1):
                return [0, 1]
            if (distmass.index(value)==2):
                return [-1, -1]
    def diff (distmass, value, params):
        i=0
        res=[]
        for item in distmass:
            if (distmass.index(value)==i):
                res.append(1)
            else:
                res.append(0)
            i+=1
        return res
    def numeric(distmass, value, params):
        return [actives.activ[params["normtype"]].normalize(value, params["alpha"])]

normalizeTypes={"uno":normalize.uno, "boolean":normalize.boolean, \
                "triple":normalize.triple, "diff":normalize.diff \
                ,"numeric":normalize.numeric}
