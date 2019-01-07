import multiprocessing as pr
import time
import modules.classes as classes

class procpool():
    def __init__(self, i):
        self.pool=[]
        self.outputs=[]
        for z in range(i):
            p1, p2=pr.Pipe()
            p=pr.Process(target=inputHandler, args=(p1,))
            p.input=p1
            p.output=p2
            self.pool.append(p)
            self.outputs.append(p2)
    def startall(self):
        for p in self.pool:
            p.start()
    def closall(self):
        for p in self.pool:
            p.terminate()
    def responseHandler(self, func):
        summ=0
        for p in self.outputs:
            while(p.poll()):
                func(p.recv())
                summ+=1
        return summ
def inputHandler(p1):
    inn=p1
    while (True):
        resp=inn.recv() #[object, function, output, outtype]
        if (resp=="END"):
            break
        #if outtype=true, returns object, else returns res
        assert len(resp)==4
        res=getattr(resp[0], resp[1])()
        if (resp[2]!=False):
            res=getattr(resp[0], resp[2])()
        if (resp[3]):
            inn.send(resp[0])
        else:
            inn.send([res, resp[0].number])
            
            
