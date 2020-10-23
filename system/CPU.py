from .Resource import Resource

class CPU(Resource):

    def __init__(self, currentProcess):
        self.currentProcess = currentProcess
        self.empty = currentProcess == None
