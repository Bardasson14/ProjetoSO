from random import choice
from string import ascii_letters
from . import Process

class Dispatcher:
    def __init__(self):
        pass

    def createProcess(arrivalTime, priority, serviceTime, size, printers, disk, memory):
        id = ''.join(choice(ascii_letters) for i in range(10))
        if ((priority == 1 and size<=512) or (priority==0)) and (memory.avaliableMemory >= process.size):
            memory.avaliableMemory -= process.size
        return Process(id, arrivalTime, priority, serviceTime, size, printers, disk)

    def addNewToQueue(process, memory):
        memory.criticalProcesses.append(newProcess) if newProcess.priority == 0 else memory.rq0.append(newProcess) #adicionando à fila apropriada

    def dispatchProcess(cpu, queue):
        process = queue.pop(0)
        process.currentStatus = ProcessState.RUNNING
        cpu.currentProcess = process

    def finishProcess(cpu):
        cpu.currentProcess.currentStatus = ProcessState.FINISHED
        cpu.currentProcess = None

    def stopProcess(cpu):
        #adicionar atributo de 'lastqueue' para poder devolver processo a fila posterior (rqi+1) à última, seguindo a política de feedback
        pass
