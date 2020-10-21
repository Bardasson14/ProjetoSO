import Memory.py
import Process.py

#Scheduler irá implementar apenas a política escolha do próximo processo, mas sem efetivamente realizar alterações

class Scheduler:
    def __init__(self):
        pass

    def chooseNext(memory):
        return memory.criticalProcesses[0] if memory.criticalProcesses
        return memory.rq0[0] if memory.rq0
        return memory.rq1[0] if memory.rq1
        return memory.rq2[0] if memory.rq2

    def checkFinished (cpus):
        pass    #checar em todas as cpus se processo foi finalizado

    
    