from random import choice;
from string import ascii_letters
from .process import Process, ProcessState

#DISPATCHER SE COMUNICA APENAS COM MEMORIA E CPU
class Dispatcher:
    def __init__(self):
        pass

    def createProcess(self, arrivalTime, priority, serviceTime, size, printers, disk, memory):

        id = ''.join(choice(ascii_letters) for i in range(10))

        self.getMemoryForNewProcess(memory, size, priority)

        return Process(id, arrivalTime, priority, serviceTime, size, printers, disk, None)

    def dispatchProcess(self, cpu, memory, queue):

        if (queue != None):
            process = memory.rq[queue].pop(0)
        else:
            process = memory.criticalProcesses.pop(0)
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

    def blockProcess(self, memory, queue):
        process = memory.rq[queue].pop(0) #apenas processos de usuário podem ser bloqueados, já que processos críticos são CPU-bound
        process.currentStatus = ProcessState.BLOCKED
        process.currentStatusTime = 0
        memory.blockedProcesses.append(process)

    def unblockProcess(self, memory, process):
        processIndex = memory.blockedProcesses.index(process)
        del memory.blockedProcesses[processIndex]
        memory.rq0.append(process)
        process.currentStatus = ProcessState.READY
        process.currentStatusTime = 0

    def readySuspendedProcess(self, memory, process, originQueue):

        process.currentStatus = ProcessState.READY_SUSPENDED
        process.currentStatusTime = 0

        memory.readySuspendedProcesses.append(originQueue.pop(originQueue.index(process)))

    def suspendBlockedProcess(self, memory, process):

        process.currentStatus = ProcessState.SUSPENDED_BLOCKED
        process.currentStatusTime = 0

        memory.blockedSuspendedProcesses.append(memory.blockedProcesses.pop(memory.blockedProcesses.index(process)))
        memory.avaliableMemory += process.size

    def activateProcess(self, memory, proc):

        proc.currentStatus = ProcessState.READY
        proc.currentStatusTime = 0

        memory.rq0.append(memory.readySuspendedProcesses.pop(memory.readySuspendedProcesses.index(proc)))

        memory.avaliableMemory -= proc.size

    def getMemoryForNewProcess(self, memory, size, priority):

        # if we have enough memory for the new process, just take space from MP
        if( memory.avaliableMemory >= size ):
            memory.avaliableMemory -= size

        # if we don't have enough space and this is a user process
        else:

            # get more space by suspending blocked processes
            for processIndex in range(len(memory.blockedProcesses)-1, -1, -1):
                self.suspendBlockedProcess(memory, memory.blockedProcesses[processIndex])
                if( memory.avaliableMemory >= size ):
                    break

            # if we still don't have enough memory
            if( memory.avaliableMemory < size ):

                # get more space by sending ready process to ready-suspended queue
                for rq in memory.rq[::-1]:

                    for processIndex in range(len(rq)-1, -1, -1):
                        self.readySuspendedProcess(memory, rq[processIndex], rq)
                        memory.avaliableMemory += rq[processIndex].size
                        if( memory.avaliableMemory >= size ):
                            break
