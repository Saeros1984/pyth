import multiprocessing as pr
import os
import time
import random

class mother():
    def __init__(self):
        self.children=[]
        self.ind=1
class child():
    ind=2
    def plus(ch):
        ch.ind+=3

m=mother()



for i in range(100):
    m.children.append(child())

def childsum(pipe):
    summ=0
    while 1:
        resp=pipe.recv()
        if (resp=="END"):
            break
        for ch in resp.children:
            summ+=ch.ind
            ch.ind+=1
        resp.ind=summ
        pipe.send(resp)
    

if __name__ == "__main__":
    p1, p2=pr.Pipe()
    proc=pr.Process(target=childsum, args=(p2, ))
    proc.start()
    p1.send(m)
    p1.send("END")
    m=p1.recv()
    print(m.ind)
    proc.join()
    time.sleep(3)
