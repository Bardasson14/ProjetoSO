#adicionar imports
from system import System, Dispatcher, Scheduler

def main():
    system = System()
    p = []
    
    #leitura dos processos no arquivo
    with open('../processes.txt') as reader:
        for line in reader.readlines():
            arrivalTime, priority, serviceTime, size, printers, disk = line.split(', ')
            newInput = {
                "arrivalTime": arrivalTime,
                "priority": priority,
                "serviceTime": serviceTime,
                "size": size,
                "printers": printers,
                "disk": disk
            }
            p.append(newInput)
    sort_p = p.sort(key = lambda x: x['arrivalTime']) 
    #adicionar a vetor auxiliar ordenado p/ ordem de chegada do processo
    loop(system, sort_p)

           
def loop(system, sort_p):
    memory = system.memory
    cpus = system.CPUs
    scheduler = Scheduler()
    dispatcher = Dispatcher()

    
    while True: #loop deve ser executado até que último processo seja finalizado - TIMER AINDA NÃO IMPLEMENTADO

        #PERCORRER CPUS PARA CHECAR TÉRMINO DE PROCESSOS
        scheduler.checkFinished(cpus)

        #checar se há processo crítico -> Scheduler
        scheduler.searchCriticalProcesses(memory, cpus, dispatcher)

        #checar se existem novos processos p/serem admitidos no sistema (currentTime ainda não foi implementado)
        scheduler.checkEntries(sort_p, currentTime, dispatcher)

        #checar processos em execução para realizar preempcao, se necessário (apenas em processos de user)
        scheduler.checkQuantum(system, currentTime, dispatcher)

        #ATUALIZAÇÕES DE STATUS (CONTADORES DE EXECUCAO, ATUALIZACAO DE PROCESSOS BLOQUEADOS, SUSPENSOS ETC.)