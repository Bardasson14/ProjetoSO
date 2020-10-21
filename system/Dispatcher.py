from random import choice
from string import ascii_lowercase
import Process.py

class Dispatcher:
    def __init__(self):
        pass

    def createProcess(arrivalTime, priority, serviceTime, size, printers, disk):
        id = ''.join(choice(ascii_lowercase) for i in range(10)) #incremental (?)
        return Process(id, arrivalTime, priority, serviceTime, size, printers, disk, memory)

    def addNewToQueue(process, memory):
        memory.criticalProcesses.append(newProcess) if newProcess.priority == 0 else memory.rq0.append(newProcess) #adicionando a fila apropriada
