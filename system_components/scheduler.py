from .memory import Memory
from .process import Process
#from .dispatcher import Dispatcher

#Scheduler irá implementar apenas a política escolha do próximo processo, mas sem efetivamente realizar alterações
class Scheduler:
    def __init__(self):
        pass
    
    def checkProcessIO(self, process, printers, disks):
        avaliablePrinters = len([x for x in printers if x.avaliable])
        avaliableDisks = len([x for x in disks if x.avaliable])
        if (avaliablePrinters >= process.printers and avaliableDisks >= process.disk):
            return True
        return False


    def admitProcess(self, process, system):
        if (self.checkProcessIO(process, system.printers, system.disks)):
            system.memory.criticalProcesses.append(process) if process.priority == 0 else system.memory.rq0.append(process)
        else:
            system.memory.blockedProcesses.append(process)

    def chooseNext(self, memory):
        if( memory.criticalProcesses ): return memory.criticalProcesses[0]
        elif( memory.rq0 ): return memory.rq0[0]
        elif( memory.rq1 ): return memory.rq1[0]
        elif( memory.rq2 ): return memory.rq2[0]

    def checkFinished(self, cpus, dispatcher):
        for cpu in cpus:
            if (not cpu.empty and (cpu.currentProcess.serviceTimeLeft == 0)):
                dispatcher.finishProcess(cpu)
            
    def getProcessQueue(self, id, memory):
        for i in range (len(memory.rq)):
                for process in memory.rq[i]:
                    if process.id == id:
                        return i

    def manageReadyQueues(self, memory, cpus, dispatcher):
        #checar ready queues até encaixar o máximo possível de processos de usuário
        _avaliableCPUIndex = self.checkAvaliableCPUS(cpus, False)
        while (_avaliableCPUIndex != None):
            nextProcess = self.chooseNext(memory)
            if not nextProcess:
                return
            nextProcessQueue = self.getProcessQueue(nextProcess.id, memory)
            dispatcher.dispatchProcess(cpus[_avaliableCPUIndex], memory, nextProcessQueue)
            _avaliableCPUIndex = self.checkAvaliableCPUS(cpus, False)
    
    def manageBlockedQueue(self):
        #t minimo para ser suspenso: 5 unidades de tempo
        pass
                
    def checkAvaliableCPUS(self, cpus, userProcessesIncluded):
        #retorna primeira CPU disponível. Caso não haja nenhuma, retorna None (caso processos de usuário sejam incluidos, seu indice é retornado)
        userProcessCPU = None
        for i in range(len(cpus)):
            if cpus[i].empty:
                return i
            if cpus[i].currentProcess.priority == 1:
                userProcessCPU = i
        if (userProcessesIncluded):
            return userProcessCPU #priorizar a busca por CPUs vazias. Caso não haja nenhuma vazia, retornar cpu com processo de usuário


    def manageCriticalProcesses(self, memory, cpus, dispatcher):
        if not (memory.criticalProcesses):
            return
        
        for i in range(4): #NO MÁXIMO, HAVERÃO 4 CPUs DISPONÍVEIS (como a checagem é por clock, não é necessário checar mais do que 4 vezes)
            if not memory.criticalProcesses:
                return
            criticalProcess = memory.criticalProcesses[0]
            avaliableCPUIndex = self.checkAvaliableCPUS(cpus, True)
            if avaliableCPUIndex == None:
                return #Nesse caso, não há CPU com processo de usuário nem vaga
            if (not cpus[avaliableCPUIndex].empty):  #CPU executando processo de usuário
                dispatcher.interruptProcess(cpus[avaliableCPUIndex], memory, self)
            #inserir criticalProcess na CPU
            dispatcher.dispatchProcess(cpus[avaliableCPUIndex], memory, 4)
                    
            
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
                    dispatcher.interruptProcess(cpu, system.memory, self) 
                    dispatcher.dispatchProcess(cpu, system.memory, self.getProcessQueue(nextProcess.id, system.memory))

