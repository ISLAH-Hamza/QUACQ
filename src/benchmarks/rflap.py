from QUACQ.core import *
import random

class Model:
    """
    A class to represent the Radio Link Frequency Assignment Problem (RFLAP) benchmark model.
    This model assigns frequencies (channels) to a set of 25 radio links (variables) with a domain of [0, 32].
    It enforces interference constraints to ensure that no two variables in the same group have the same value,
    and applies additional constraints between groups to model realistic frequency assignment requirements.
    """
    def __init__(self) -> None:
        
        self.domain=[0,32]
        self.variables=[Variable(f'{i}',self.domain) for i in range(25)]
        random.shuffle(self.variables)
        self.language={
            '==':Relation('==',2,False),
            '!=':Relation('!=',2,False),
            '||>1':Relation('||>val',2,False,1),
            '||>2':Relation('||>val',2,False,2),
            '||>3':Relation('||>val',2,False,3),
            }
        
        self.bais=Bais(Language=self.language.values(),variables=self.variables)


        self.constraints=set()

              
        self.click(self.variables[0:5],relation=self.language['!=']) 
        self.click(self.variables[5:10],relation=self.language['!=']) 
        self.click(self.variables[10:15],relation=self.language['!=']) 
        self.click(self.variables[15:20],relation=self.language['!=']) 
        self.click(self.variables[20:25],relation=self.language['!=']) 
        self.specific(self.variables[0:5],self.variables[5:10])
        self.specific(self.variables[5:10],self.variables[10:15])
        self.specific(self.variables[15:20],self.variables[20:25])
      
    
    def click(self,variables,relation):
        for i in range(len(variables)):
            for j in range(i+1,len(variables)):
                self.constraints.add(Constraints(scope=[variables[i],variables[j]],relation=relation))

    def specific(self,l1,l2):
        for i in l1:
            for j in l2:
                self.constraints.add(
                    Constraints(scope=[i,j],relation=self.language['||>2'])
                )