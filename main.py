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
    i= 0
    while i<30: #loop deve ser executado até que último processo seja finalizado - TIMER AINDA NÃO IMPLEMENTADO

        #PERCORRER CPUS PARA CHECAR TÉRMINO DE PROCESSOS
        scheduler.checkFinished(system.CPUs, dispatcher)

        #checar se há processo crítico -> Scheduler
        scheduler.searchCriticalProcesses(system.memory, system.CPUs, dispatcher)

        #checar se existem novos processos p/serem admitidos no sistema (currentTime ainda não foi implementado)
        scheduler.checkEntries(sort_p, i, dispatcher, system.memory)

        #checar processos em execução para realizar preempcao, se necessário (apenas em processos de user)
        scheduler.checkQuantum(system, i, dispatcher)

        print('-------------------------------------')
        print('t =', i)
        print('RQ0', system.memory.rq0)
        print('RQ1', system.memory.rq1)
        print('RQ2', system.memory.rq2)
        print('CPs', system.memory.criticalProcesses)
        print('CPU0', system.CPUs[0].currentProcess)
        print('CPU1', system.CPUs[1].currentProcess)
        print('CPU2', system.CPUs[2].currentProcess)
        print('CPU3', system.CPUs[3].currentProcess)

        #ATUALIZAÇÕES DE STATUS (CONTADORES DE EXECUCAO, ATUALIZACAO DE PROCESSOS BLOQUEADOS, SUSPENSOS ETC.)
        
        i+=1

        #ATUALIZAR TEMPO DE EXECUCAO
        
        for cpu in system.CPUs:
            if (cpu.currentProcess != None):
                cpu.currentProcess.currentStatusTime += 1

        #ATUALIZAR TEMPO DE ESPERA DOS PROCESSOS NA MP
        
        for rqi in system.memory.rq:
            for process in rqi:
                print('p_id:', process.id)
                print('p_st:', process.currentStatusTime)
                

main()