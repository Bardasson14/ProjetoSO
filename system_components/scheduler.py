from .memory import Memory
from .process import Process
#from .dispatcher import Dispatcher

#Scheduler irá implementar apenas a política escolha do próximo processo, mas sem efetivamente realizar alterações
class Scheduler:
    def __init__(self):
        pass

    def chooseNext(self, memory):
        if( memory.criticalProcesses ): return memory.criticalProcesses[0]
        elif( memory.rq0 ): return memory.rq0[0]
        elif( memory.rq1 ): return memory.rq1[0]
        elif( memory.rq2 ): return memory.rq2[0]

    def checkFinished(self, cpus, dispatcher):
        for cpu in cpus:
            currentProcess = cpu.currentProcess
            if ((currentProcess != None) and (currentProcess.currentStatusTime == currentProcess.serviceTime)):
                dispatcher.finishProcess(cpu, currentProcess)
                
    def searchCriticalProcesses(self, memory, cpus, dispatcher):

        for i in range(4): #NO MÁXIMO, HAVERÃO 4 CPUs DISPONÍVEIS (como a checagem é por clock, não é necessário checar mais do que 4 vezes)
            if (memory.criticalProcesses): #processo crítico na fila
                criticalProcess = memory.criticalProcesses[0]
                for cpu in cpus:
                    avaliableCPUFound = False
                    if (cpu.currentProcess == None or cpu.currentProcess.priority == 1): 
                        #CPU possui processo de usuário ou está vaga?

                        if (cpu.currentProcess != None):
                            #devolver processo de user para a MP
                            #[FAZER]    
                            pass

                        #inserir criticalProcess na CPU
                        dispatcher.dispatchProcess(cpu, memory.criticalProcesses)
                        avaliableCPUFound = True
                    
                    if (avaliableCPUFound):
                        break #DESCULPA, VANESSA (KKKKKKKKKKKK)
            
    def checkEntries(self, jobList, currentTime, dispatcher, memory): #OK
            while (jobList and jobList[0]['arrivalTime'] == currentTime):
                processInput = jobList.pop(0)
                newProcess = dispatcher.createProcess(processInput['arrivalTime'], processInput['priority'], processInput['serviceTime'], processInput['size'], processInput['printers'], processInput['disk'], memory)
                dispatcher.addNewToQueue(newProcess, memory)

    def checkQuantum(self, system, currentTime, dispatcher): #necessário passar o sistema como param, pois existem os processos bloqueados, suspensos, etc.
        memory = system.memory
        cpus = system.CPUs

        for cpu in cpus:
            if (cpu.currentProcess and cpu.currentProcess.currentStatusTime % 2 == 0):
                dispatcher.interruptProcess(cpu) #método ainda não implementado
                #preempcao
                #trocar processo atual por processo a ser escolhido pela funcao chooseNext


