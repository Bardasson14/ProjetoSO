from . import Memory
from . import Process
from . import Dispatcher

#Scheduler irá implementar apenas a política escolha do próximo processo, mas sem efetivamente realizar alterações

class Scheduler:
    def __init__(self):
        pass

    def chooseNext(memory):
        if( memory.criticalProcesses ): return memory.criticalProcesses[0]
        elif( memory.rq0 ): return memory.rq0[0]
        elif( memory.rq1 ): return memory.rq1[0]
        elif( memory.rq2 ): return memory.rq2[0]

    def checkFinished(cpus, dispatcher):
        for cpu in cpus:
            currentProcess = cpu.currentProcess
            if( currentProcess.currentStatusTime == currentProcess.serviceTime ): #tempo de servico = tempo de execucao atual
                dispatcher.finishProcess(cpu, currentProcess)

    def searchCriticalProcesses(memory, cpus, dispatcher):

        for i in range(4): #NO MÁXIMO, HAVERÃO 4 CPUs DISPONÍVEIS (como a checagem é por clock, não é necessário checar mais do que 4 vezes)
            if (memory.criticalProcesses[0]): #processo crítico na fila
                criticalProcess = memory.criticalProcesses[0]
                for cpu in cpus:
                    avaliableCPUFound = False
                    if (cpu.currentProcess.priority == 1): #processo corrente é de usuário? se sim, esse pode ser facilmente removido
                        #devolver processo de user para a MP

                        #[FAZER]

                        #inserir criticalProcess na CPU
                        dispatcher.dispatchProcess(cpu, queue)
                        avaliableCPUFound = True

                    if (avaliableCPUFound):
                        break #DESCULPA, VANESSA (KKKKKKKKKKKK)
            else:
                return #fila de processos críticos está vazia

    def checkEntries(jobList, currentTime, dispatcher):
        while (jobList[0].arrivalTime == currentTime):
            processInput = jobList.pop(0)
            newProcess = dispatcher.createProcess(processInput['arrivalTime'], processInput['priority'], processInput['serviceTime'], processInput['size'], processInput['printers'], processInput['disk'])
            dispatcher.addNewToQueue(newProcess, memory)

    def checkQuantum(system, currentTime, dispatcher): #necessário passar o sistema como param, pois existem os processos bloqueados, suspensos, etc.
        memory = system.memory
        cpus = system.CPUs

        for cpu in cpus:
            if (cpu.currentProcess.currentStatusTime % 2 == 0):
                #preempcao
                dispatcher.stopProcess(cpu) #método ainda não implementado
                #trocar processo atual por processo a ser escolhido


