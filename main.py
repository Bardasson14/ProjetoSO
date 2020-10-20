#adicionar imports
QUANTUM = 2

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
    sort_p = p.sort(key = lambda x: x['arrivalTime']) #adicionar a vetor auxiliar ordenado p/ ordem de chegada do processo
    loop(system.memory, sort_p)
            
def loop(memory, sort_p):
    scheduler = Scheduler()
    dispatcher = Dispatcher()
    memory = system.memory
    
    while True: #loop deve ser executado até que último processo seja finalizado - TIMER AINDA NÃO IMPLEMENTADO

        #checar se há processo crítico -> Scheduler
        if (memory.criticalProcesses[0].state != RUNNING):  #alteracoes necessárias para mudar estado do processo corrente
            memory.criticalProcesses[0].state = RUNNING
            for rq in memory.rq:
                if (rq[0]): #caso a fila não esteja vazia
                    rq[0].state = ProcessState.READY
                    #mover o processo corrente de fila?

        #chegada de processo no sistema
        if (sort_p[0].arrivalTime == """current_time"""):
            #priority = 0 -> critical
            #prority = 1 -> user
            processInput = sort_p.pop(0)
            newProcess = dispatcher.createProcess(processInput['arrivalTime'], processInput['priority'], processInput['serviceTime'], processInput['size'], processInput['printers'], processInput['disk'])
            dispatcher.addNewToQueue(newProcess, memory)

        if not ("""current_time""" % QUANTUM):
            #realizar swapping de processos