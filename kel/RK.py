import container as con
import boundary as bound
import rkfunctions as rkf
import numpy as np 


class RK:

    def __init__(self, runVal):
        
        self.runVal = runVal
        self.Alpha = runVal.lim.alphaMin

        self.bound = bound.Boundary(self.run_container.getSet(self.Alpha))
        self.func_value = self.boundary.get()
        self.Alpha_increment = dict()
        self.kRK = dict()
        self.func = dict()

    def doRK(self):

        for iAlpha in range(self.run_container['constants']['nAlpha']):
            self.getIncrement()
             
            self.func['step1'] = rkf.RKFunctions(self.run_container.getSet(self.Alpha_increment['start']), self.func_value)
            self.kRK['step1'] = self.func['step1'].get() 

            self.func['step2'] = rkf.RKFunctions(self.run_container.getSet(self.Alpha_increment['middle']),
                                                    self.func_value + self.const['dAlpha'] * self.kRK['step1'] / 2.0)

            self.kRK['step2'] = self.func['step2'].get()
            
            self.func['step3'] = rkf.RKFunctions(self.run_container.getSet(self.Alpha_increment['middle']),
                                                    self.func_value + self.const['dAlpha'] * self.kRK['step2'] / 2.0)
            self.kRK['step3'] = self.func['step3'].get()
            
            self.func['step4'] = rkf.RKFunctions(self.run_container.getSet(self.Alpha_increment['end']),
                                                    self.func_value + self.const['dAlpha'] * self.kRK['step3'])
            self.kRK['step4'] = self.func['step4'].get()
            
             
            self.kRK['final'] = (self.const['dAlpha'] / 6.0) * (self.kRK['step1'] + 2 * (self.kRK['step2'] + self.kRK['step3']) + self.kRK['step4'])
            self.func_value += self.kRK['final']
            self.Alpha += self.const['dAlpha']

    def getIncrement(self):

        self.Alpha_increment['start'] = self.Alpha
        self.Alpha_increment['middle'] = self.Alpha + self.const['dAlpha'] / 2.0
        self.Alpha_increment['end'] = self.Alpha + self.const['dAlpha']
    
    def getValue(self):

        return self.func_value

