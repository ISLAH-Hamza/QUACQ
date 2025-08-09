import itertools
from QUACQ.core import *
from ortools.sat.python import cp_model
from tqdm import tqdm

def Constraint2CPModel(c,model,variables) -> None:

    if c.relation.arity==1:
        i=c.scope[0].name
    else:
        i,j,*k=[v.name for v in c.scope]

    parameter=c.relation.parameter
    op=c.relation.operator

    if   op == "==val"    : model.Add(variables[i]==parameter)
    elif op == "!=val"    : model.Add(variables[i]!=parameter)
    elif op == "<=val"    : model.Add(variables[i]<=parameter)
    elif op == "<val"     : model.Add(variables[i]<parameter)
    elif op == ">=val"    : model.Add(variables[i]>=parameter)
    elif op == ">val"     : model.Add(variables[i]>parameter)
    elif op == "=="       : model.Add(variables[i]==variables[j])
    elif op == "!="       : model.Add(variables[i]!=variables[j])
    elif op == "<="       : model.Add(variables[i]<=variables[j])
    elif op == "<"        : model.Add(variables[i]<variables[j])
    elif op == ">="       : model.Add(variables[i]>=variables[j])
    elif op == ">"        : model.Add(variables[i]>variables[j])
    elif op == "||==val"  : model.AddAbsEquality(parameter, variables[i] - variables[j])
    elif op == "||!=val"  :
            temp_variable=model.NewIntVar(0, max(variables[i].Proto().domain[1],variables[j].Proto().domain[1]), f"abs_{i}_{j}")
            model.AddAbsEquality(temp_variable, variables[i] - variables[j])
            model.Add(temp_variable != parameter)
    elif op== "||>val"   :
            temp_variable=model.NewIntVar(0, max(variables[i].Proto().domain[1],variables[j].Proto().domain[1]), f"abs_{i}_{j}")
            model.AddAbsEquality(temp_variable, variables[i] - variables[j])
            model.Add(temp_variable > parameter)
    elif op== "||>=val"  :
            temp_variable=model.NewIntVar(0, max(variables[i].Proto().domain[1],variables[j].Proto().domain[1]), f"abs_{i}_{j}")
            model.AddAbsEquality(temp_variable, variables[i] - variables[j])
            model.Add(temp_variable >= parameter)
    elif op== "||<val"   :
            temp_variable=model.NewIntVar(0, max(variables[i].Proto().domain[1],variables[j].Proto().domain[1]), f"abs_{i}_{j}")
            model.AddAbsEquality(temp_variable, variables[i] - variables[j])
            model.Add(temp_variable < parameter)
    elif op== "||<=val"  :
            temp_variable=model.NewIntVar(0, max(variables[i].Proto().domain[1],variables[j].Proto().domain[1]), f"abs_{i}_{j}")
            model.AddAbsEquality(temp_variable, variables[i] - variables[j])
            model.Add(temp_variable <= parameter)


def Constraint2Boolean(c,b,model,variables)->None:

    if c.relation.arity==1:
        i=c.scope[0].name
    else:
        i,j,*k=[v.name for v in c.scope]

    parameter=c.relation.parameter

    op= c.relation.operator
    if op == "==":
            model.Add(variables[i] == variables[j]).OnlyEnforceIf(b)
            model.Add(variables[i] != variables[j]).OnlyEnforceIf(b.Not())
    elif op == "!=":
            model.Add(variables[i] != variables[j]).OnlyEnforceIf(b)
            model.Add(variables[i] == variables[j]).OnlyEnforceIf(b.Not())
    elif op == ">=":
            model.Add(variables[i] >= variables[j]).OnlyEnforceIf(b)
            model.Add(variables[i] < variables[j]).OnlyEnforceIf(b.Not())
    elif op == ">":
            model.Add(variables[i] > variables[j]).OnlyEnforceIf(b)
            model.Add(variables[i] <= variables[j]).OnlyEnforceIf(b.Not())
        
    elif op == "<=":
            model.Add(variables[i] <= variables[j]).OnlyEnforceIf(b)
            model.Add(variables[i] > variables[j]).OnlyEnforceIf(b.Not())
        
    elif op == "<":
            model.Add(variables[i] < variables[j]).OnlyEnforceIf(b)
            model.Add(variables[i] >= variables[j]).OnlyEnforceIf(b.Not())


    elif '||' in c.relation.operator and 'val' in c.relation.operator:
            max_domain = max(variables[i].Proto().domain[1], variables[j].Proto().domain[1])
            temp_variable = model.NewIntVar(0, max_domain, f"boolean_abs_{i}_{j}")
            model.AddAbsEquality(temp_variable, variables[i] - variables[j])
            
            op = c.relation.operator.split('||')[1].split('val')[0]
            if op == "==":
                model.Add(temp_variable == parameter).OnlyEnforceIf(b)
                model.Add(temp_variable != parameter).OnlyEnforceIf(b.Not())
            elif op == "!=":
                model.Add(temp_variable != parameter).OnlyEnforceIf(b)
                model.Add(temp_variable == parameter).OnlyEnforceIf(b.Not())
            
            elif op == ">=":
                model.Add(temp_variable >= parameter).OnlyEnforceIf(b)
                model.Add(temp_variable < parameter).OnlyEnforceIf(b.Not())
            
            elif op == ">":
                model.Add(temp_variable > parameter).OnlyEnforceIf(b)
                model.Add(temp_variable <= parameter).OnlyEnforceIf(b.Not())
            
            elif op == "<":
                model.Add(temp_variable < parameter).OnlyEnforceIf(b)
                model.Add(temp_variable >= parameter).OnlyEnforceIf(b.Not())
            
            elif op == "<=":
                model.Add(temp_variable <= parameter).OnlyEnforceIf(b)
                model.Add(temp_variable > parameter).OnlyEnforceIf(b.Not())


def GeneratExample(B,L,vars,logger=None):
 
    if logger: logger.info('start generating example')
    m=cp_model.CpModel()
    bools=[]
    variables={v.name:m.NewIntVar(*v.domain,v.name) for v in vars}

    for conj in L:
        for c in conj:
             Constraint2CPModel(c,m,variables=variables)

    for c in B:
        bools.append(m.NewBoolVar(f'b{len(bools)}'))
        Constraint2Boolean(c,bools[-1],m,variables)
    

    m.Add(sum(bools) != len(B))
    m.Add(sum(bools) > 0)

    solver = cp_model.CpSolver()
    status = solver.Solve(m)


    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        sol={i: solver.Value(variables[i])for i in variables.keys()}
        if logger:logger.info(f'the function succesfly generate solution:\n{sol}')
        return sol


def findScope(example,R,Y,B,target_network,logger=None):
   
    if logger:logger.info('looking for scope that make the example nagative')
    e_R={key:val for key,val in example.items() if key in R }
    K_B=set(c for c in B if c.check(e_R)==False)

    if len(K_B)>0:
        if target_network.ask(e_R): B.difference_update(K_B)
        else: return set()
    
    if len(Y)==1: return Y
    n=len(Y)//2
    Y1,Y2=set(list(Y)[:n]),set(list(Y)[n:])
    e_R_Y1={key:val for key,val in example.items() if key in set(R)|Y1}
    e_R_Y={key:val for key,val in example.items() if key in set(R)|Y}
    
    if set(c for c in B if c.check(e_R_Y1)==False)==set(c for c in B if c.check(e_R_Y)==False):
        S1=set()
    else:
        S1=findScope(example,set(R)|Y1,Y2,B,target_network)

    e_R_S1={key:val for key,val in example.items() if key in set(R)|S1}
    if set(c for c in B if c.check(e_R_S1)==False)==set(c for c in B if c.check(e_R_Y)==False):
        S2=set()
    else:
        S2=findScope(example,set(R)|S1,Y1,B,target_network)

    return S1|S2


def checkConj(s):
 
    s=list(s)

    if len(s)==0:
        return False 
    
    elif any(i.scope != s[0].scope for i in s):
        return False
    
    else:
        names=[v.name for v in s[0].scope]
        for c in s:
            if set(v.name for v in c.scope)!=set(names) :
                return False
        
        m=cp_model.CpModel()
        variables=dict()

        ### Creating Cp model variables and constraints
        for c in s:
            for v in c.scope:
                if v.name not in variables.keys():
                    variables[v.name]=m.NewIntVar(*v.domain,name=v.name)

        for c in s: Constraint2CPModel(c,m,variables)
        
        sovler=cp_model.CpSolver()
        status=sovler.Solve(m)
        
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            return True
        
        else: return False


def join_operation(S,S_prime):
    Output=[]
    for s1,s2 in  itertools.product(S,S_prime):
        s=s1|s2
        if s not in Output and checkConj(s)==True: Output.append(s)

    return Output





def FindEprime(L,Y,Delta,vars) -> dict:
    
    
    m=cp_model.CpModel()

    ### creating ortools variables
    variables={v.name:m.NewIntVar(v.domain[0],v.domain[1],name=v.name) for v in vars}
    
    for conj in L:
        for c in conj:
            if all(v.name in Y for v in c.scope):
                Constraint2CPModel(c,m,variables)

    solver=cp_model.CpSolver()
    while True:
        status=solver.Solve(m)

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            solution={v:solver.Value(variables[v]) for v in Y}
            K_Delta=[conj for conj in Delta  if any(c.check(solution)==False for c in conj) ]
            if len(K_Delta)<len(Delta) and len(K_Delta)>0:
                return solution
            else:
                m.AddForbiddenAssignments([variables[v] for v in solution.keys()],
                                          [tuple(solution.values())]
                                          )
        else: return 

    





def findC(example,Y,L,B,target_network,variables,logger=None) -> None:

    if logger:logger.info('looking for the constraint that make the example negative')
    B_Y=set([c for c in B if all(v.name in Y for v in c.scope)])
    
    Delta=[{item} for item in B_Y]
    K_Delta=[conj for conj in Delta  if any(c.check(example)==False for c in conj) ]
    Delta=join_operation(Delta,K_Delta)
    if not Delta:
        return 
    
    while True:
        eprime=FindEprime(L,Y,Delta,variables)
        if eprime==None:
            L.append((Delta[0]))
            B.difference_update(B_Y)
            return 
        else:
            K_DeltaEprime=[conj for conj in Delta  if any(c.check(eprime)==False for c in conj)]
            if target_network.ask(eprime)==True:
                Delta=[conj for conj in Delta if conj not in K_DeltaEprime]
                B.difference_update(set(c for c in B if c.check(eprime)==False))
              
            else:
                S=findScope(eprime,set(),Y,B,target_network)
                if all(i in Y for i in S) and len(S)<len(Y):
                    findC(eprime,S,L,B,target_network,variables)
                else:
                    Delta=join_operation(Delta,K_DeltaEprime)





def QuAcq(B, variables, target_network,logger=None):
   
    if logger:
        logger.info('start Quacq learning:')
        logger.info(f'initial bais contains:{len(B)}')

    L = []
    B_initial_size = len(B)
    pbar = tqdm(total=len(B), desc="Size of B", unit="constraints")
    
    
    
    while True:
       
        example = GeneratExample(B, L, variables,logger)
        if example is None:
            if logger:
                logger.info('the learning is end')
                logger.info(f'L contain: {len(L)}')
            pbar.n = B_initial_size - len(B)
            pbar.refresh()
            pbar.close()
            return L

        if target_network.ask(example):
            K_B = {c for c in B if not c.check(example)}
            B.difference_update(K_B)
        else:
            scope = findScope(example, set(), {v.name for v in variables}, B, target_network,logger)
            findC(example, scope, L, B, target_network, variables,logger)

        pbar.n = B_initial_size - len(B)
        pbar.refresh()