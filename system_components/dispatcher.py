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

    def admitProcess(self, process, memory):
        memory.criticalProcesses.append(process) if process.priority == 0 else memory.rq0.append(process)

    def dispatchProcess(self, cpu, memory, queue):

        if (0<=queue<=2):
            process = memory.rq[queue].pop(0)
        else:
            process= memory.criticalProcesses.pop(0)

        process.currentStatus = ProcessState.RUNNING
        process.currentStatusTime = 0
        cpu.currentProcess = process
        cpu.lastQueueIndex = queue
        cpu.empty = False

    def finishProcess(self, cpu):
        cpu.currentProcess.currentStatus = ProcessState.FINISHED
        cpu.reset()
        
    def interruptProcess(self, cpu, memory, scheduler):
        cpu.currentProcess.currentStatus = ProcessState.READY
        cpu.currentProcess.currentStatusTime = 0
        processQueueIndex = scheduler.getProcessQueue(cpu.currentProcess.id, memory) #só vale para processos de usuário, que podem ser interrompidos
        targetQueue = cpu.lastQueueIndex
        if (targetQueue == 2):
            targetQueue = 0
        else:
            targetQueue +=1
        memory.rq[targetQueue].append(cpu.currentProcess)
        #devolver a fila de prontos seguinte a anterior. se processo estava na ultima fila, voltará para fila inicial
        cpu.reset()