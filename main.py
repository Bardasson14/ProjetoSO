#!/usr/bin/env python3
# the line above allow us to run this file as './main.py' in *nix systems
# don't worry, the rest of the systems will only see it as a normal comment :)

#adicionar imports
from system_components import dispatcher as dispatcherModule, scheduler as schedulerModule, system as systemModule
import csv

def main():
    sys = systemModule.System()
    p = []

    #leitura dos processos no arquivo
    with open('./processes.txt') as file:
        #reader = csv.DictReader(file)
        reader = file.readlines()
        for row in reader:
            #p.append(row)
            parsed_row  = list(map(int, row.split(', ')))
            p.append({'arrivalTime': parsed_row[0], 'priority': parsed_row[1], 'serviceTime': parsed_row[2], 'size': parsed_row[3], 'printers': parsed_row[4], 'disk': parsed_row[4]})
    #adicionar a vetor auxiliar ordenado p/ ordem de chegada do processo
    #sort_p = [p.sort(key = lambda x: x['arrivalTime']) for i in range(len(p))]
    
    #p não passou por nenhuma ordenação
    loop(sys, p)

def loop(system, sort_p):
    scheduler = schedulerModule.Scheduler()
    dispatcher = dispatcherModule.Dispatcher()
    currentTime = 0
    while currentTime<30: #loop deve ser executado até que último processo seja finalizado - TIMER AINDA NÃO IMPLEMENTADO

        #AINDA É NECESSÁRIO FAZER A VERIFICAÇÃO PARA POSSÍVEIS EVENTOS BLOQUEANTES
        #USAR FILA DE PROCESSOS BLOQUEADOS

        #CHECAR CHEGADA DE NOVOS PROCESSOS
        scheduler.checkEntries(sort_p, currentTime, dispatcher, system.memory)

        #PERCORRER CPUS PARA CHECAR TÉRMINO DE PROCESSOS
        scheduler.checkFinished(system.CPUs, dispatcher)

        #CHECAR QUANTUM PARA REALIZAR PREEMPÇÃO, SE NECESSÁRIO
        scheduler.checkQuantum(system, currentTime, dispatcher)

        #checar se há processo crítico -> Scheduler
        scheduler.manageCriticalProcesses(system.memory, system.CPUs, dispatcher) #corrigir

        #gerenciar filas de processos de usuário, admitindo para a memória aqueles que possam ser executados, e suspendendo outros
        scheduler.manageReadyQueues(system.memory, system.CPUs, dispatcher)


        print()
        print('-------------------------------------\n')
        print('t =', currentTime, '\n')
        for i in range(len(system.memory.rq)):
            print('RQ',i)
            for process in system.memory.rq[i]:
                print(process.__dict__)
        print('Critical Processes')
        for process in system.memory.criticalProcesses:
            print(process.__dict__)
        for i in range(len(system.CPUs)):
            print('CPU',i)
            if not system.CPUs[i].empty :
                print(system.CPUs[i].currentProcess.__dict__)
            
        
        #ATUALIZAÇÕES DE STATUS (CONTADORES DE EXECUCAO, ATUALIZACAO DE PROCESSOS BLOQUEADOS, SUSPENSOS ETC.)
        
        currentTime+=1

        #ATUALIZAR TEMPO DE EXECUCAO
        
        for cpu in system.CPUs:
            if (cpu.currentProcess != None):
                cpu.currentProcess.currentStatusTime += 1
                cpu.currentProcess.serviceTimeLeft -= 1

        #ATUALIZAR TEMPO DE ESPERA DOS PROCESSOS NA MP
        
        for rqi in system.memory.rq:
            for process in rqi:
                process.currentStatusTime += 1
                

main()