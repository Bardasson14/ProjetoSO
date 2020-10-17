#adicionar imports
QUANTUM = 2

def main():
    system = System()
    p = []
    
    #leitura dos processos no arquivo
    with open('../processes.txt') as reader:
        for line in reader.readlines():
            p.append(line.split(', '))
            #inputInfo[0] -> arrivalTime
            #inputInfo[1] -> priority 
            #inputInfo[2] -> CPU time
            #inputInfo[3] -> MBytes
            #inputInfo[4] -> printers
            #inputInfo[5] -> disk
    sort_p = p.sort(key = lambda x: x[0]) #adicionar a vetor auxiliar ordenado p/ ordem de chegada do processo
    loop(system.memory, sort_p)
            
def loop(memory, sort_p):
    #scheduler = Scheduler()
    #dispatcher = Dispatcher()
    
    while True: #loop deve ser executado até que último processo seja finalizado
            
        #checar se há processo crítico -> Scheduler
        #Dispatcher fará alterações necessárias
        #checar se há novos processos / fazer swapping se (currentTime%quantum==0) -> Scheduler
            