from .memory import Memory
from .process import Process
#from .dispatcher import Dispatcher

#Scheduler irá implementar apenas a política escolha do próximo processo, mas sem efetivamente realizar alterações
class Scheduler:
    def __init__(self):
        pass
    
    def getAvaliableIO (self, printers, disks):
        avaliablePrinters = len([printer for printer in printers if printer.avaliable])
        avaliableDisks = len([disk for disk in disks if disk.avaliable])
        return [avaliablePrinters, avaliableDisks]

    def checkProcessIO(self, process, printers, disks):
        avaliablePrinters, avaliableDisks = self.getAvaliableIO(printers, disks)
        if (avaliablePrinters >= process.printers and avaliableDisks >= process.disk):
            return True
        return False

    def admitProcess(self, process, system):
        system.memory.criticalProcesses.append(process) if process.priority == 0 else system.memory.rq0.append(process)
    
    def chooseNext(self, memory):
        if( memory.criticalProcesses ): return memory.criticalProcesses[0]
        elif( memory.rq0 ): return memory.rq0[0]
        elif( memory.rq1 ): return memory.rq1[0]
        elif( memory.rq2 ): return memory.rq2[0]

    def checkFinished(self, system, dispatcher):
        for cpu in system.CPUs:
            if (not cpu.empty and (cpu.currentProcess.remainingTime == 0)):
                if (cpu.currentProcess.priority == 1):
                    self.freeResources(cpu.currentProcess, system.printers, system.disks)   
                dispatcher.finishProcess(cpu)
            
    def getProcessQueue(self, id, memory):
        for i in range (len(memory.rq)):
                for process in memory.rq[i]:
                    if process.id == id:
                        return i

    def manageReadyQueues(self, system, dispatcher):
        #checar ready queues até encaixar o máximo possível de processos de usuário
        avaliableCPUIndex = self.checkAvaliableCPUS(system.CPUs, False)
        while (avaliableCPUIndex != None):
            nextProcess = self.chooseNext(system.memory)
            if not nextProcess:
                return
            nextProcessQueue = self.getProcessQueue(nextProcess.id, system.memory)
            if (self.checkProcessIO(nextProcess, system.printers, system.disks)):
                dispatcher.dispatchProcess(system.CPUs[avaliableCPUIndex], system.memory, nextProcessQueue)
                self.allocateResources(nextProcess, system.printers, system.disks)
            else:
                dispatcher.blockProcess(system.memory, nextProcessQueue)
            avaliableCPUIndex = self.checkAvaliableCPUS(system.CPUs, False)
    
    def manageBlockedQueue(self, system, dispatcher):
        #t minimo para ser suspenso: 5 unidades de tempo
        avaliablePrinters, avaliableDisks = self.getAvaliableIO(system.printers, system.disks)
        originalBlockedLength = len(system.memory.blockedProcesses)
        for i in range(originalBlockedLength):
            process = system.memory.blockedProcesses[0]
            if (process.printers <= avaliablePrinters and process.disk <= avaliableDisks):
                avaliablePrinters -= process.printers
                avaliableDisks -= process.disk
                dispatcher.unblockProcess(system.memory, process)
            
            if (avaliablePrinters == 0 and avaliableDisks == 0):
                return

    def allocateResources(self, process, printers, disks):
        n_printers = 0
        n_disks = 0

        for i in range(2):
            if  n_printers < process.printers and printers[i].avaliable:
                printers[i].avaliable = False
                n_printers += 1

            if n_disks < process.disk and disks[i].avaliable:
                disks[i].avaliable = False
                n_disks += 1
    
    def freeResources(self, process, printers, disks):
        n_printers = 0
        n_disks = 0

        for i in range(2):
            if  n_printers < process.printers and not printers[i].avaliable:
                printers[i].avaliable = True
                n_printers += 1
                
            if n_disks < process.disk and not disks[i].avaliable:
                disks[i].avaliable = True
                n_disks += 1
                
    def checkAvaliableCPUS(self, cpus, userProcessesIncluded): #userProcessesIncluded = True p/ Processos Críticos
        userProcessCPU = None
        for i in range(len(cpus)):
            if cpus[i].empty:
                return i
            if userProcessesIncluded and cpus[i].currentProcess.priority == 1:
                userProcessCPU = i
        if (userProcessesIncluded):
            return userProcessCPU #priorizar a busca por CPUs vazias. Caso não haja nenhuma vazia, retornar cpu com processo de usuário

    def manageCriticalProcesses(self, system, dispatcher):
        if not (system.memory.criticalProcesses):
            return
        
        for i in range(4): #NO MÁXIMO, HAVERÃO 4 CPUs DISPONÍVEIS (como a checagem é por clock, não é necessário checar mais do que 4 vezes)
            if not system.memory.criticalProcesses:
                return
            criticalProcess = system.memory.criticalProcesses[0]
            avaliableCPUIndex = self.checkAvaliableCPUS(system.CPUs, True)
            if avaliableCPUIndex == None:
                return #Nesse caso, não há CPU com processo de usuário nem vaga
            if (not system.CPUs[avaliableCPUIndex].empty):  #CPU executando processo de usuário
                self.freeResources(system.CPUs[avaliableCPUIndex].currentProcess, system.printers, system.disks)
                dispatcher.interruptProcess(system.CPUs[avaliableCPUIndex], system.memory, self)
            #inserir criticalProcess na CPU
            dispatcher.dispatchProcess(system.CPUs[avaliableCPUIndex], system.memory, None)
                                
    def checkEntries(self, jobList, currentTime, dispatcher, system): #OK
            while (jobList and jobList[0]['arrivalTime'] == currentTime):
                processInput = jobList.pop(0)
                newProcess = dispatcher.createProcess(processInput['arrivalTime'], processInput['priority'], processInput['serviceTime'], processInput['size'], processInput['printers'], processInput['disk'], system.memory)
                self.admitProcess(newProcess, system)

    def checkQuantum(self, system, currentTime, dispatcher): #necessário passar o sistema como param, pois existem os processos bloqueados, suspensos, etc.
        cpus = system.CPUs
        avaliableCPU = self.checkAvaliableCPUS(cpus, False)
        if avaliableCPU: #se houver CPU disponível, não é necessário realizar preempção no processo
            return
        for cpu in cpus:
            if (cpu.currentProcess and cpu.currentProcess.priority == 1 and cpu.currentProcess.currentStatusTime % 2 == 0):
                nextProcess = self.chooseNext(system.memory)
                if (nextProcess):
                    #ADICIONAR LIBERACAO DE RECURSO
                    self.freeResources(cpu.currentProcess, system.printers, system.disks)
                    dispatcher.interruptProcess(cpu, system.memory, self) 
                    self.allocateResources(nextProcess, system.printers, system.disks)
                    dispatcher.dispatchProcess(cpu, system.memory, self.getProcessQueue(nextProcess.id, system.memory))
                    

