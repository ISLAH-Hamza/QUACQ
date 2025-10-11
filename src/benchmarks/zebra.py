from QUACQ.core import *
import random


class Model:
    """
    The Zebra puzzle, also known as "Einstein's Riddle," is a logic puzzle that involves deducing the arrangement of five houses, each with a unique color, nationality, pet, drink, and cigarette brand, based on a set of clues. The objective is to determine who owns the zebra and who drinks water.

    This model encodes the Zebra puzzle as a constraint satisfaction problem (CSP) with:
    - 25 variables, each representing an attribute (nationality, color, drink, pet, cigarette) for each house.
    - Each variable has a domain of [0, 4], corresponding to the five possible values for each attribute.
    - Constraints are defined to enforce the rules and clues of the Zebra puzzle, including uniqueness of attributes per house and relationships between attributes.
    """
    def __init__(self) -> None:
        
        self.domain=[0,4]
        self.variables=[Variable(f'{i}',self.domain) for i in range(25)]
        random.shuffle(self.variables)
        self.indexes={
            'Nor':self.variables[0] ,'En':self.variables[1],'Sp': self.variables[2],'Uk':self.variables[3],'Jp':self.variables[4],
            'blue':self.variables[5] ,'red':self.variables[6],'green': self.variables[7],'yellow':self.variables[8],'Ivre':self.variables[9],
            'cofee':self.variables[10] ,'milk':self.variables[11],'tee': self.variables[12],'jus':self.variables[13],'water':self.variables[14],
            'fox':self.variables[15] ,'dog':self.variables[16],'snail': self.variables[17],'hors':self.variables[18],'zebra':self.variables[19],
            'kool':self.variables[20] ,'parl':self.variables[21],'old': self.variables[22],'luck':self.variables[23],'chest':self.variables[24],
        }
        self.language={
            '==':Relation('==',2,False),
            '!=':Relation('!=',2,False),
            '>':Relation('>=',2,True),
            '==1':Relation('==val',1,False,1),
            '==2':Relation('==val',1,False,2),
            '||==1':Relation('||==val',2,False,1),
            }
        
        self.bais=Bais(Language=self.language.values(),variables=self.variables)


        self.constraints={
            Constraints([self.indexes['Nor']],self.language['==1']),
            Constraints([self.indexes['Nor'],self.indexes['blue']],self.language['||==1']),
            Constraints([self.indexes['milk']],self.language['==2']),
            Constraints([self.indexes['En'],self.indexes['red']],self.language['==']),
            Constraints([self.indexes['cofee'],self.indexes['green']],self.language['==']),
            Constraints([self.indexes['kool'],self.indexes['yellow']],self.language['==']),
            Constraints([self.indexes['Ivre'],self.indexes['green']],self.language['||==1']),
            Constraints([self.indexes['Ivre'],self.indexes['green']],self.language['>']),
            Constraints([self.indexes['Sp'],self.indexes['dog']],self.language['==']),
            Constraints([self.indexes['Uk'],self.indexes['tee']],self.language['==']),
            Constraints([self.indexes['Jp'],self.indexes['parl']],self.language['==']),
            Constraints([self.indexes['old'],self.indexes['snail']],self.language['==']),
            Constraints([self.indexes['luck'],self.indexes['jus']],self.language['==']),
            Constraints([self.indexes['chest'],self.indexes['fox']],self.language['||==1']),
            Constraints([self.indexes['kool'],self.indexes['hors']],self.language['||==1']),
        }

              
        self.click(self.variables[0:5],relation=self.language['!=']) 
        self.click(self.variables[5:10],relation=self.language['!=']) 
        self.click(self.variables[10:15],relation=self.language['!=']) 
        self.click(self.variables[15:20],relation=self.language['!=']) 
        self.click(self.variables[20:25],relation=self.language['!=']) 
      
        
    def click(self,variables,relation):
        for i in range(len(variables)):
            for j in range(i+1,len(variables)):
                self.constraints.add(Constraints(scope=[variables[i],variables[j]],relation=relation))
