import Memory.py
import Process.py

#Scheduler irá implementar apenas a política escolha do próximo processo, mas sem efetivamente realizar alterações

class Scheduler:
    def __init__(self):
        pass

    def chooseNext(memory):
        if (memory.criticalProcesses):
            return memory.criticalProcesses[0]
        
        #checar filas usando política de feedback