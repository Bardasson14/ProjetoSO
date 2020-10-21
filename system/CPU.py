import Resource.py

class CPU(Resource):
    
    def __init__(self, id, priority):
        self.id = id #id do processo sendo executado atualmente
        self.priority = priority #prioridade do processo sendo executado