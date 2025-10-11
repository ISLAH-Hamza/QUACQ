import itertools
from QUACQ.core import *
from ortools.sat.python import cp_model
from tqdm import tqdm

def Constraint2CPModel(c,model,variables) -> None:
    """
        Convert a constraint to a ortools CP model.
        args:
            c         : The constraint to convert.
            model     : The CP model to add the constraint to.
            variables : The mapping of variable names to CP variables.
    """
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
    """
        associate a constraint with a boolean variable, if the constraint will be satisfied the boolean variable will be true.
        otherwise, the boolean variable will be false.
        This is useful for assuring the number of constraint satisfied by the problem is bounded by specific number
        see generate_query to see the application
        args:
            c         : The constraint to convert.
            b         : The boolean variable to associate with the constraint.
            model     : The CP model to add the constraint to.
            variables : The mapping of variable names to CP variables.
    """
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




def Solve(L,vars,logger=None):
    """
        Solve the constraints in L using the given variables in cp_model from ortools.
        args:
            L       : The list of constraints to solve.
            vars    : The list of variables to use in the constraints.
            logger  : An optional logger to log information.
    """
    if logger: logger.info('solve constraints from L')
    m=cp_model.CpModel()
    variables={v.name:m.NewIntVar(*v.domain,v.name) for v in vars}

    for conj in L:
        for c in conj:
             Constraint2CPModel(c,m,variables=variables)

    solver = cp_model.CpSolver()
    status = solver.Solve(m)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        sol={i: solver.Value(variables[i])for i in variables.keys()}
        if logger:logger.info(f'solution:\n{sol}')
        return sol




# ===========================  quacq function & it's procedures =================
def GenerateExample(B,L,vars,logger=None):
    """
        Generate an example that satisfies the constraints in L while rejecting at least one constraint in B.
        args:
            B       : The Basis represent all possible constraint that could be used to model the problem.
            L       : The list of constraints to satisfy.
            vars    : The list of variables to use in the constraints.
            logger  : An optional logger to log information.
    """
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
    """
        a recursive process to find the scope of variables in example that make the answer of the user negative see more information in the original paper.
        args:
            example         : The example to analyze.
            R               : The set of relevant variables.
            Y               : The set of variables to consider.
            B               : The Bais.
            target_network  : The target network (which model the user's oracle/answers).
            logger          : An optional logger to log information.
    """
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
    """
        helper subprosess that will be used with findC, it checks if a conjunction of constraints is satisfiable.
        args:
            s : The conjunction of constraints to check.
    """
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
    """
        the join operation used in findC procedure see more information in the original paper.
        it will join to list of constraints S and S' and return a new list of constraints.
        args:
            S       : The first list of constraints.
            S_prime : The second list of constraints.
    """
    Output=[]
    for s1,s2 in  itertools.product(S,S_prime):
        s=s1|s2
        if s not in Output and checkConj(s)==True: Output.append(s)

    return Output





def FindEprime(L,Y,Delta,vars) -> dict: 
    """
        find an example that satisfy the constraints in L and reject at least one conjunction in Delta.
        args:
            L      : The list of constraints to satisfy.
            Y      : The set of variables to consider.
            Delta  : set of candidate constraints.
            vars   : The set of all variables.
    """
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

    





def findC(example,Y,L,B,target_network,variables,logger=None):

    """
        find the conjunction of constraints that make the example negative see more information in the original paper.
        args:
            example         : The (negative)example to analyze.
            Y               : The set of variables to consider.
            L               : The list of constraints to satisfy.
            B               : The Bais.
            target_network  : The target network (which model the user's oracle/answers).
            variables       : The set of all variables.
            logger          : An optional logger to log information.
    """
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
    """
        The main QuAcq algorithm to learn the target network using the basis B and the given variables.
        args:
            B               : The Basis represent all possible constraint that could be used to model the problem.
            variables       : The set of all variables.
            target_network  : The target network (which model the user's oracle/answers).
            logger          : An optional logger to log information.
    """
    if logger:
        logger.info('start Quacq learning:')
        logger.info(f'initial bais contains:{len(B)}')

    L = []
    B_initial_size = len(B)
    pbar = tqdm(total=len(B), desc="Size of B", unit="constraints")
    
    
    
    while True:
       
        example = GenerateExample(B, L, variables,logger)
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

