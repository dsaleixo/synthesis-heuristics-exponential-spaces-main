import itertools
from dsl import dsl

class VarList(dsl.VarList):
    def __init__(self):
        super().__init__()
   
class VarScalar(dsl.VarScalar):
    def __init__(self):
        super().__init__()
    
class NumericConstant(dsl.NumericConstant):
    def __init__(self):
        super().__init__()

class LocalList(dsl.LocalList):
    def __init__(self):
        super().__init__()

class LocalInt(dsl.LocalInt):
    def __init__(self):
        super().__init__()

class Times(dsl.Times):
    def __init__(self):
        super().__init__()
    
    @staticmethod
    def grow(plist, size):       
        new_programs = []
        
        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(1, size - 1), repeat=2))

        for c in combinations:           
            # skip if the cost combination exceeds the limit
            if c[0] + c[1] + 1 != size:
                continue
                    
            # retrive bank of programs with costs c[0], c[1], and c[2]
            program_set1 = plist.get_programs(c[0])
            program_set2 = plist.get_programs(c[1])
                
            for t1, programs1 in program_set1.items():                
                # skip if t1 isn't a node accepted by Lt
                if t1 not in Times.accepted_rules(0):
                    continue
                
                for p1 in programs1:                       

                    for t2, programs2 in program_set2.items():                
                        # skip if t1 isn't a node accepted by Lt
                        if t2 not in Times.accepted_rules(1):
                            continue
                        
                        for p2 in programs2:
    
                            times = Times()
                            times.add_child(p1)
                            times.add_child(p2)
                            new_programs.append(times)
            
                            yield times
        return new_programs  

class Minus(dsl.Minus):
    def __init__(self):
        super().__init__()
    
    @staticmethod
    def grow(plist, size):               
        new_programs = []

        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(1, size - 1), repeat=2))
 
        for c in combinations:                       
            # skip if the cost combination exceeds the limit
            if c[0] + c[1] + 1 != size:
                continue
                 
            # retrive bank of programs with costs c[0], c[1], and c[2]
            program_set1 = plist.get_programs(c[0])
            program_set2 = plist.get_programs(c[1])
                 
            for t1, programs1 in program_set1.items():                
                # skip if t1 isn't a node accepted by Lt
                if t1 not in Minus.accepted_rules(0):
                    continue
                 
                for p1 in programs1:                       
 
                    for t2, programs2 in program_set2.items():                
                        # skip if t1 isn't a node accepted by Lt
                        if t2 not in Minus.accepted_rules(1):
                            continue
                         
                        for p2 in programs2:
     
                            minus = Minus()
                            minus.add_child(p1)
                            minus.add_child(p2)
                            new_programs.append(minus)
             
                            yield minus
        return new_programs  
 
class Plus(dsl.Plus):
    def __init__(self):
        super().__init__()
    
    @staticmethod
    def grow(plist, size):               
        new_programs = []         
        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(1, size - 1), repeat=2))
 
        for c in combinations:                       
            # skip if the cost combination exceeds the limit
            if c[0] + c[1] + 1 != size:
                continue
                 
            # retrive bank of programs with costs c[0], c[1], and c[2]
            program_set1 = plist.get_programs(c[0])
            program_set2 = plist.get_programs(c[1])
                 
            for t1, programs1 in program_set1.items():                
                # skip if t1 isn't a node accepted by Lt
                if t1 not in Plus.accepted_rules(0):
                    continue
                 
                for p1 in programs1:                       
 
                    for t2, programs2 in program_set2.items():                
                        # skip if t1 isn't a node accepted by Lt
                        if t2 not in Plus.accepted_rules(0):
                            continue
                         
                        for p2 in programs2:
     
                            plus = Plus()
                            plus.add_child(p1)
                            plus.add_child(p2)
                            new_programs.append(plus)
             
                            yield plus
        return new_programs  
     

class Abs(dsl.Abs):
    def __init__(self):
        super().__init__() 
    
    @staticmethod
    def grow(plist, size):
        new_programs = []
          
        program_set = plist.get_programs(size - 1)
                     
        for t1, programs1 in program_set.items():                
            # skip if t1 isn't a node accepted by Lt
            if t1 not in Abs.accepted_rules(0):
                continue
             
            for p1 in programs1:                       
 
                abs = Abs()
                abs.add_child(p1)
                new_programs.append(abs)
         
                yield abs
        return new_programs

class Function(dsl.Function):
    def __init__(self):
        super().__init__() 
    
    @staticmethod
    def grow(plist, size):
        new_programs = []
          
        program_set = plist.get_programs(size - 1)
                     
        for t1, programs1 in program_set.items():                
            # skip if t1 isn't a node accepted by Lt
            if t1 not in Function.accepted_rules(0):
                continue
             
            for p1 in programs1:                       
 
                func = Function()
                func.add_child(p1)
                new_programs.append(func)
         
                yield func
        return new_programs
    
class ITE(dsl.ITE):
    def __init__(self):
        super().__init__()
    
    @staticmethod
    def grow(plist, size):               
        new_programs = []
        
        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(0, size), repeat=3))
 
        for c in combinations:                       
            # skip if the cost combination exceeds the limit
            if c[0] + c[1] + c[2] + 1 != size:
                continue
                 
            # retrive bank of programs with costs c[0], c[1], and c[2]
            program_set1 = plist.get_programs(c[0])
            program_set2 = plist.get_programs(c[1])
            program_set3 = plist.get_programs(c[2])
                 
            for t1, programs1 in program_set1.items():                

                if t1 not in ITE.accepted_rules(0):
                    continue
                 
                for p1 in programs1:                       
 
                    for t2, programs2 in program_set2.items():                

                        if t2 not in ITE.accepted_rules(1):
                            continue
                         
                        for p2 in programs2:
                            
                            for t3, programs3 in program_set3.items():                

                                if t3 not in ITE.accepted_rules(2):
                                    continue
                                 
                                for p3 in programs3:
     
                                    ite = ITE()
                                    ite.add_child(p1)
                                    ite.add_child(p2)
                                    ite.add_child(p3)
                                    new_programs.append(ite)
                     
                                    yield ite
        return new_programs  

class VarListSliceFront(dsl.VarListSliceFront):
    def __init__(self):
        super().__init__()
    
    @staticmethod
    def grow(plist, size):               
        new_programs = []
                 
        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(0, size), repeat=2))
 
        for c in combinations:                       
            # skip if the cost combination exceeds the limit
            if c[0] + c[1] + 1 != size:
                continue
                 
            # retrive bank of programs with costs c[0], c[1], and c[2]
            program_set1 = plist.get_programs(c[0])
            program_set2 = plist.get_programs(c[1])
                 
            for t1, programs1 in program_set1.items():                
                # skip if t1 isn't a node accepted by Lt
                if t1 not in VarListSliceFront.accepted_rules(0):
                    continue
                 
                for p1 in programs1:                       
 
                    for t2, programs2 in program_set2.items():                
                        # skip if t1 isn't a node accepted by Lt
                        if t2 not in VarListSliceFront.accepted_rules(1):
                            continue
                         
                        for p2 in programs2:
     
                            slice_front = VarListSliceFront()
                            slice_front.add_child(p1)
                            slice_front.add_child(p2)
                            new_programs.append(slice_front)
             
                            yield slice_front
        return new_programs  

class VarListSliceEnd(dsl.VarListSliceEnd):
    def __init__(self):
        super().__init__()
    
    @staticmethod
    def grow(plist, size):               
        new_programs = []
                 
        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(0, size), repeat=2))
 
        for c in combinations:                       
            # skip if the cost combination exceeds the limit
            if c[0] + c[1] + 1 != size:
                continue
                 
            # retrive bank of programs with costs c[0], c[1], and c[2]
            program_set1 = plist.get_programs(c[0])
            program_set2 = plist.get_programs(c[1])
                 
            for t1, programs1 in program_set1.items():                
                # skip if t1 isn't a node accepted by Lt
                if t1 not in VarListSliceEnd.accepted_rules(0):
                    continue
                 
                for p1 in programs1:                       
 
                    for t2, programs2 in program_set2.items():                
                        # skip if t1 isn't a node accepted by Lt
                        if t2 not in VarListSliceEnd.accepted_rules(1):
                            continue
                         
                        for p2 in programs2:
     
                            slice_end = VarListSliceEnd()
                            slice_end.add_child(p1)
                            slice_end.add_child(p2)
                            new_programs.append(slice_end)
             
                            yield slice_end
        return new_programs  

class VarScalarFromArray(dsl.VarScalarFromArray):
    def __init__(self):
        super().__init__()
    
    @staticmethod
    def grow(plist, size):               
        new_programs = []
                 
        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(0, size), repeat=2))
 
        for c in combinations:                       
            # skip if the cost combination exceeds the limit
            if c[0] + c[1] + 1 != size:
                continue
                 
            # retrive bank of programs with costs c[0], c[1], and c[2]
            program_set1 = plist.get_programs(c[0])
            program_set2 = plist.get_programs(c[1])
                 
            for t1, programs1 in program_set1.items():                
                # skip if t1 isn't a node accepted by Lt
                if t1 not in VarScalarFromArray.accepted_rules(0):
                    continue
                 
                for p1 in programs1:                       
 
                    for t2, programs2 in program_set2.items():                
                        # skip if t1 isn't a node accepted by Lt
                        if t2 not in VarScalarFromArray.accepted_rules(1):
                            continue
                         
                        for p2 in programs2:
     
                            scalar = VarScalarFromArray()
                            scalar.add_child(p1)
                            scalar.add_child(p2)
                            new_programs.append(scalar)
             
                            yield scalar
        return new_programs  

class LT(dsl.LT):
    def __init__(self):
        super().__init__()
    
    @staticmethod
    def grow(plist, size):               
        new_programs = []
                 
        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(0, size), repeat=2))
 
        for c in combinations:                       
            # skip if the cost combination exceeds the limit
            if c[0] + c[1] + 1 != size:
                continue
                 
            # retrive bank of programs with costs c[0], c[1], and c[2]
            program_set1 = plist.get_programs(c[0])
            program_set2 = plist.get_programs(c[1])
                 
            for t1, programs1 in program_set1.items():                
                # skip if t1 isn't a node accepted by Lt
                if t1 not in LT.accepted_rules(0):
                    continue
                 
                for p1 in programs1:                       
 
                    for t2, programs2 in program_set2.items():                
                        # skip if t1 isn't a node accepted by Lt
                        if t2 not in LT.accepted_rules(1):
                            continue
                         
                        for p2 in programs2:
     
                            lt = LT()
                            lt.add_child(p1)
                            lt.add_child(p2)
                            new_programs.append(lt)
             
                            yield lt
        return new_programs  
 
class Sum(dsl.Sum):
    def __init__(self):
        super().__init__()
    
    @staticmethod
    def grow(plist, size):       
        new_programs = []
        # defines which nodes are accepted in the AST
        program_set = plist.get_programs(size - 1)
                     
        for t1, programs1 in program_set.items():                
            # skip if t1 isn't a node accepted by Lt
            print('Sum Accepted Rules: ', Sum.accepted_rules(0))
            if t1 not in Sum.accepted_rules(0):
                continue
             
            for p1 in programs1:                       
 
                sum_p = Sum()
                sum_p.add_child(p1)
                new_programs.append(sum_p)
         
                yield sum_p
        return new_programs
 
class Map(dsl.Map):
    def __init__(self):
        super().__init__()
    
    @staticmethod
    def grow(plist, size):  
        new_programs = []
                 
        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(0, size), repeat=2))
         
        for c in combinations:         
            # skip if the cost combination exceeds the limit
            if c[0] + c[1] + 1 != size:
                continue
                     
            # retrive bank of programs with costs c[0], c[1], and c[2]
            program_set1 = plist.get_programs(c[0])
            program_set2 = plist.get_programs(c[1])
             
#             if c[1] == 0:
#                 if VarList.className() not in program_set2:
#                     program_set2[VarList.className()] = []
#                 program_set2[VarList.className()].append(None)
                 
            for t1, programs1 in program_set1.items():                
                # skip if t1 isn't a node accepted by Lt
                if t1 not in Map.accepted_rules(0):
                    continue
                 
                for p1 in programs1:                       
     
                    for t2, programs2 in program_set2.items():
                                    
                        # skip if t2 isn't a node accepted by Map
                        if t2 not in Map.accepted_rules(1):
                            continue
                         
                        for p2 in programs2:
     
                            m = Map()
                            m.add_child(p1)
                            m.add_child(p2)
                            new_programs.append(m)
             
                            yield m
        return new_programs 

