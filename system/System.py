import CPU.py
import Disk.py
import Printer.py
import Memory.py

class System:
    def __init__(self):
        self.CPUs = [CPU(), CPU(), CPU(), CPU()]
        self.printers = [Printer(), Printer()]
        self.disks = [Disk(), Disk()]
        self.memory = Memory()