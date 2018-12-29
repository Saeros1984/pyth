import multiprocessing as pr
import os

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f(name):
    info('function f')
    for i in range(20000):
        print('hello', name)

if __name__ == '__main__':
    pr.set_start_method('spawn')
    p = pr.Process(target=f, args=('bob',))
    p.start()
    p.join()
    print("fff")
