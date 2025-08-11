from QUACQ.core import *
import random


class Model:
    def __init__(self) -> None:
        
        self.domain=[0,4]
        self.variables=[Variable(f'{i}',self.domain) for i in range(20)]
        random.shuffle(self.variables)
        self.language={
            '==':Relation('==',2,False),
            '!=':Relation('!=',2,False),
            '>=':Relation('>=',2,True),
            '<=':Relation('<=',2,True),
            }
        self.bais=Bais(Language=self.language.values(),variables=self.variables)


        self.constraints={
            Constraints(scope=[self.variables[15],self.variables[1]],relation=self.language['==']),
            Constraints(scope=[self.variables[12],self.variables[16]],relation=self.language['==']),
            Constraints(scope=[self.variables[8],self.variables[13]],relation=self.language['==']),
            Constraints(scope=[self.variables[18],self.variables[11]],relation=self.language['==']),
            Constraints(scope=[self.variables[0],self.variables[9]],relation=self.language['==']),
        }
            
        self.click(self.variables[0:5],relation=self.language['!=']) 
        self.click(self.variables[5:10],relation=self.language['!=']) 
        self.click(self.variables[10:15],relation=self.language['!=']) 
        self.click(self.variables[15:20],relation=self.language['!=']) 
      
    
    def click(self,variables,relation):
        for i in range(len(variables)):
            for j in range(i+1,len(variables)):
                self.constraints.add(Constraints(scope=[variables[i],variables[j]],relation=relation))
