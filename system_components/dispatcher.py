from random import choice
from string import ascii_letters
from .process import Process, ProcessState

class Dispatcher:
    def __init__(self):
        pass

    def createProcess(self, arrivalTime, priority, serviceTime, size, printers, disk, memory):
        id = ''.join(choice(ascii_letters) for i in range(10))
        if ((priority == 1 and size<=512) or (priority==0)) and (memory.avaliableMemory >= size):
            memory.avaliableMemory -= size
        return Process(id, arrivalTime, priority, serviceTime, size, printers, disk)

    def addNewToQueue(self, process, memory):
        memory.criticalProcesses.append(process) if process.priority == 0 else memory.rq0.append(process)

    def dispatchProcess(self, cpu, queue):
        process = queue.pop(0)
        process.currentStatus = ProcessState.RUNNING
        cpu.empty = False
        cpu.currentProcess = process

    def finishProcess(self, cpu):
        cpu.currentProcess.currentStatus = ProcessState.FINISHED
        cpu.currentProcess = None

    def interruptProcess(self, cpu):
        #adicionar atributo de 'lastqueue' para poder devolver processo a fila posterior (rqi+1) à última, seguindo a política de feedback
        pass
