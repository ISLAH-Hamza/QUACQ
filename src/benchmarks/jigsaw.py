from quacq.core import *
import random



class Model:
    """
        A class to represent the Jigsaw puzzle benchmark model.
        The model consists of 36 variables with a domain of [1,6] and a set of constraints to ensure that no two adjacent pieces have the same value.
        The model also includes additional constraints to ensure that pieces in the same row or column do not share the same value.
    """
    def __init__(self) -> None:
        
        self.domain=[1,6]
        self.variables=[Variable(f'{i}',self.domain) for i in range(36)]
        random.shuffle(self.variables)
        self.language={
            '==':Relation('==',2,False),
            '!=':Relation('!=',2,False),
            '>=':Relation('>=',2,True),
            '<=':Relation('<=',2,True),
            }
        
        self.bais=Bais(Language=self.language.values(),variables=self.variables)


        self.constraints={
            Constraints(scope=[self.variables[1],self.variables[6]],relation=self.language['!=']),
            Constraints(scope=[self.variables[1],self.variables[12]],relation=self.language['!=']),
            Constraints(scope=[self.variables[2],self.variables[6]],relation=self.language['!=']),
            Constraints(scope=[self.variables[2],self.variables[12]],relation=self.language['!=']),
            
            Constraints(scope=[self.variables[3],self.variables[11]],relation=self.language['!=']),
            Constraints(scope=[self.variables[3],self.variables[17]],relation=self.language['!=']),
            Constraints(scope=[self.variables[4],self.variables[11]],relation=self.language['!=']),
            Constraints(scope=[self.variables[4],self.variables[17]],relation=self.language['!=']),
            
            
            Constraints(scope=[self.variables[7],self.variables[14]],relation=self.language['!=']),
            Constraints(scope=[self.variables[7],self.variables[15]],relation=self.language['!=']),
            
            
            Constraints(scope=[self.variables[8],self.variables[16]],relation=self.language['!=']),
            Constraints(scope=[self.variables[8],self.variables[21]],relation=self.language['!=']),
            Constraints(scope=[self.variables[8],self.variables[22]],relation=self.language['!=']),
            Constraints(scope=[self.variables[9],self.variables[16]],relation=self.language['!=']),
            Constraints(scope=[self.variables[9],self.variables[20]],relation=self.language['!=']),
            Constraints(scope=[self.variables[9],self.variables[22]],relation=self.language['!=']),
            Constraints(scope=[self.variables[10],self.variables[20]],relation=self.language['!=']),
            Constraints(scope=[self.variables[10],self.variables[21]],relation=self.language['!=']),
            Constraints(scope=[self.variables[16],self.variables[20]],relation=self.language['!=']),
            Constraints(scope=[self.variables[16],self.variables[21]],relation=self.language['!=']),
            
            Constraints(scope=[self.variables[19],self.variables[26]],relation=self.language['!=']),
            Constraints(scope=[self.variables[19],self.variables[27]],relation=self.language['!=']),
            Constraints(scope=[self.variables[19],self.variables[28]],relation=self.language['!=']),
            
            Constraints(scope=[self.variables[18],self.variables[31]],relation=self.language['!=']),
            Constraints(scope=[self.variables[18],self.variables[32]],relation=self.language['!=']),
            Constraints(scope=[self.variables[24],self.variables[31]],relation=self.language['!=']),
            Constraints(scope=[self.variables[24],self.variables[32]],relation=self.language['!=']),
            
            
            Constraints(scope=[self.variables[23],self.variables[33]],relation=self.language['!=']),
            Constraints(scope=[self.variables[23],self.variables[34]],relation=self.language['!=']),
            Constraints(scope=[self.variables[29],self.variables[33]],relation=self.language['!=']),
            Constraints(scope=[self.variables[29],self.variables[34]],relation=self.language['!=']),
        

        }


        #### add line clicks      
        self.click(0,5) 
        self.click(6,11) 
        self.click(12,17) 
        self.click(18,23) 
        self.click(24,29) 
        self.click(30,35)

        #### add column clicks
        self.click(0,30) 
        self.click(1,31) 
        self.click(2,32) 
        self.click(3,33) 
        self.click(4,34) 
        self.click(5,35) 
        
      
    
    def click(self,start,end):
        step=int((end-start)/5)
        for i in range(start,end,step):
            for j in range(i+step,end+1,step):
                self.constraints.add(
                    Constraints(scope=[self.variables[i],self.variables[j]],relation=self.language['!='])
                )
