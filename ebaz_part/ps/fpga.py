from pynq import Overlay,allocate
from pynq.lib import AxiGPIO
import time
import numpy as np
import sys
path_overlay = "./pl/test.bit"

class FPGA:
    def __init__(self):
        self.overlay = Overlay(path_overlay)
        self.pl_data_port1 = self.overlay.data1()
        self.pl_data_port2 = self.overlay.data2()
        self.pl_data_port3 = self.overlay.data3()

    def return_data_1(self):
        data = self.pl_data_port1.read()
        return data

    def return_data_2(self):
        data = self.pl_data_port2.read()
        return data

    def return_data_3(self):
        data = self.pl_data_port3.read()
        return data