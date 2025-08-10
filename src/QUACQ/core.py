import itertools



class Variable:
    def __init__(self, name, domain) -> None:
        
        assert isinstance(domain, list), "The domain of a variable should be a list"
        assert isinstance(name, str), "The identifier should be a string"
        
        self.name = name
        self.domain = domain
        
    def __str__(self) -> str:
            return f"name:{self.name} | domain:{self.domain}"
        



class Relation:

    def __init__(self, operator, arity, directed, parameter=None) -> None:
      
        self.operator = operator
        self.arity = arity
        self.directed = directed
        self.parameter = parameter

    def __eq__(self, rel):
            return (self.operator, self.parameter) == (rel.operator, rel.parameter)
    
    def __hash__(self):
        return hash((self.operator, self.parameter))
       
    def __str__(self) -> str:
        if self.parameter==None:
            return f"relation: {self.operator}"
        else:
            return f"relation: {self.operator} | params: {self.parameter} "





class Constraints:

    def __init__(self, scope, relation) -> None:

        self.scope = scope
        self.relation = relation


    def __eq__(self, C) -> bool:
        if self.relation.directed:
            return (self.relation, self.scope)==(C.relation, C.scope)
        else:
            return (self.relation, frozenset(self.scope))==(C.relation, frozenset(C.scope))


    def __hash__(self) -> int:
        if self.relation.directed:
            return hash((self.relation, tuple(self.scope)))
        else:
            return hash((self.relation, frozenset(self.scope)))

    def __str__(self) -> str:
        scope=' && '.join([v.__str__() for v in self.scope])
        return f"{self.relation.__str__()} ## {scope}" 

    def check(self, example):
        ## chek if the scope of the constraint is in the dictionary
        if all(v.name in example.keys() for v in self.scope):
            
            if self.relation.arity==1:
                rel=self.relation.operator.replace('val','')
                return eval(f"{example[self.scope[0].name]} {rel} {self.relation.parameter}")
            
            elif self.relation.arity==2:
                v1,v2=self.scope
                if all( item in self.relation.operator for item in ['||','val']): 
                    rel=self.relation.operator.replace('val','').replace('||','')
                    return eval(f"abs({example[v1.name]} - {example[v2.name]}) {rel} {self.relation.parameter} ")
                elif self.relation.operator in ['==', '!=' ,'>=' , '<=' , '>' , '<']:   
                    return eval(f"{example[v1.name]} {self.relation.operator} {example[v2.name]}")
        
                else: raise ValueError("sorry  we cant handle the constraint that you provide !!")

            else:
                raise ValueError("sorry  we cant handle the constraint that you provide !!")



def Bais(Language, variables):
    constraints = set()

    for relation in Language:
        if relation.arity == 1:  # Unary constraints
            for var in variables:
                constraints.add(Constraints(scope=[var],relation=relation))
        
        elif relation.arity == 2:  # Binary constraints
            if relation.directed:
                # For directed relations, order matters
                for var1, var2 in itertools.permutations(variables, 2):
                    constraints.add(Constraints(scope=[var1, var2],relation=relation))
            else:
                # For undirected relations, order doesn't matter
                for var1, var2 in itertools.combinations(variables, 2):
                    constraints.add(Constraints(scope=[var1, var2],relation=relation))

    return constraints



class Target_Network:
 
    def __init__(self, constraints=None, mode="default") -> None:
        self.constraints = constraints
        self.ask_counter = 0
        self.mode = mode
        if mode == "default":
            if constraints is None:
                raise ValueError("Please provide constraints for the default mode")

    def ask(self, example):
        self.ask_counter += 1
        if self.mode == "human":
            print("Is the example valid? (yes/no):")
            print(f"Example: {example}")
            return input().strip().lower() == "yes"
        else:
            return all(c.check(example)!= False for c in self.constraints)

    def __str__(self) -> str:
        return  f"Total constraints: {len(self.constraints)}\nTotal asks: {self.ask_counter}"
