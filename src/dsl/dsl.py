from ast import Num
import numpy as np
import copy

class Node:
    def __init__(self):       
        self.size = 1
        self.number_children = 0
        self.current_child = 0
        
        self.local = 'locals'
        self.intname = 'int'
        self.intname64 = 'int64'
        self.listname = 'list'
        self.tuplename = 'tuple'
        self.statename = 'state'
        
        self.allowed_types = set()
        self.allowed_types.add(self.local)
        self.allowed_types.add(self.intname)
        self.allowed_types.add(self.intname64)
        self.allowed_types.add(self.listname)
        self.allowed_types.add(self.tuplename)
        self.allowed_types.add(self.statename)
        
        self.children = []

    @staticmethod
    def is_terminal():
        return False
    
    def add_child(self, child):            
        if len(self.children) + 1 > self.number_children:
            raise Exception('Unsupported number of children')
        
        self.children.append(child)
        self.current_child += 1
        
        if child is None or not isinstance(child, Node):
            self.size += 1
        else:
            self.size += child.size
    
    def interpret_local_variables(self, env, x):
        
        if type(x).__name__ not in self.allowed_types:
            raise Exception('Type not allowed in local list: ', type(x).__name__)
                    
        if self.local not in env:
            env[self.local] = {}
        
        if type(x).__name__ == self.tuplename:
            x = list(x)
        
        env[self.local][type(x).__name__] = x
                
        return self.interpret(env) 

 

    @staticmethod
    def leftmost_hole(node):
        
        for i in range(node.number_children):
                        
            if node.current_child == i:
                return node, i
            
            if isinstance(node.children[i], Node):
                
                incomplete_node, child_id = Node.leftmost_hole(node.children[i])
            
                if incomplete_node is not None:
                    return incomplete_node, child_id
        return None, None
    
    @classmethod
    def class_name(cls):
        return cls.__name__

    @classmethod
    def accepted_initial_rules(cls):
        return cls.accepted_types

    @classmethod
    def accepted_rules(cls, child):
        return cls.accepted_types[child] 

    @staticmethod
    def factory(classname):               
        if classname not in globals():           
            return classname
        
        return globals()[classname]()

    @staticmethod
    def restore_original_production_rules():

        VarListSliceFront.accepted_nodes_list = set([LocalList.class_name(),
                                                VarList.class_name()])
        VarListSliceFront.accepted_nodes_index = set([NumericConstant.class_name()])
        VarListSliceFront.accepted_types = [VarListSliceFront.accepted_nodes_list, VarListSliceFront.accepted_nodes_index]

        VarListSliceEnd.accepted_nodes_list = set([LocalList.class_name(),
                                                VarList.class_name()])
        VarListSliceEnd.accepted_nodes_index = set([NumericConstant.class_name()])
        VarListSliceEnd.accepted_types = [VarListSliceEnd.accepted_nodes_list, VarListSliceEnd.accepted_nodes_index]

        Times.accepted_nodes = set([VarScalar.class_name(), 
                              NumericConstant.class_name(),
                              Plus.class_name(),
                              Times.class_name(),
                              Abs.class_name(),
                              LocalInt.class_name()])
        
        Times.accepted_types = [Times.accepted_nodes, Times.accepted_nodes]
        
        Minus.accepted_nodes = set([VarScalar.class_name(), 
                  NumericConstant.class_name(),
                 Plus.class_name(),
                  Times.class_name(),
                 Minus.class_name(),
                 Sum.class_name(),
                  Abs.class_name(),
                  VarListSliceFront.class_name(),
                  VarListSliceEnd.class_name(),
                  LocalInt.class_name()])

        #Minus.accepted_nodes = set([VarListSliceFront.class_name(),
         #         VarListSliceEnd.class_name()])
        
        Minus.accepted_types = [Minus.accepted_nodes, Minus.accepted_nodes]
        
        Plus.accepted_nodes = set([ITE.class_name(),
                              Sum.class_name()])
        
        Plus.accepted_types = [Plus.accepted_nodes, Plus.accepted_nodes]
        
        Function.accepted_nodes = set([ITE.class_name(),
                                   Plus.class_name(), 
                                   Times.class_name(),
                                   Abs.class_name()])

        #Function.accepted_nodes = set([ITE.class_name()])
        Function.accepted_types = [Function.accepted_nodes]

        VarScalarFromArray.accepted_nodes_array = set([VarList.class_name()])
        VarScalarFromArray.accepted_nodes_index = set([NumericConstant.class_name()])
        VarScalarFromArray.accepted_types = [VarScalarFromArray.accepted_nodes_array, VarScalarFromArray.accepted_nodes_index]
        
        ITE.accepted_nodes_bool = set([LT.class_name()])
        ITE.accepted_nodes_block = set([NumericConstant.class_name()])
        ITE.accepted_types = [ITE.accepted_nodes_bool, ITE.accepted_nodes_block, ITE.accepted_nodes_block]
                
        LT.accepted_nodes = set([NumericConstant.class_name(),
                      VarScalarFromArray.class_name(),
                      VarScalar.class_name(),
                      Abs.class_name()])
        
        LT.accepted_types = [LT.accepted_nodes, LT.accepted_nodes]

        Abs.accepted_nodes = set([LocalInt.class_name()])
        
        Abs.accepted_types = [Abs.accepted_nodes]
        
        Sum.accepted_nodes = set([Map.class_name(), VarList.class_name(), LocalList.class_name()])
        #Sum.accepted_nodes = set([Map.class_name()])
        Sum.accepted_types = [Sum.accepted_nodes]
        
        Map.accepted_nodes_function = set([Function.class_name()])
        Map.accepted_nodes_list = set([Minus.class_name(), VarList.class_name(), LocalList.class_name()])
        Map.accepted_nodes_list = set([Minus.class_name()])
        Map.accepted_types = [Map.accepted_nodes_function, Map.accepted_nodes_list]
        
        Node.accepted_types = [set([Sum.class_name(), Plus.class_name(), Times.class_name(), ITE.class_name()])]
   
    @staticmethod
    def all_rules():
        list = []
        
        
        list.append(VarScalarFromArray)
        list.append(VarListSliceFront)
        list.append(VarListSliceEnd)
        list.append(NumericConstant)
        list.append(Times)
        list.append(Plus)
        list.append(Minus)
        list.append(Sum)
        list.append(Abs)
        list.append(LT)
        list.append(ITE)
        list.append(Map)
        
        list.append(VarScalar)
        list.append(Function)
        return list


    @staticmethod
    def filter_production_rules(operations,
                                numeric_constant_values,
                                variables_scalar,
                                variables_list):
        rules = set()
        for op in operations:
            rules.add(op.class_name())
        
        if len(numeric_constant_values) > 0:
            rules.add(NumericConstant.class_name())
            
        if len(variables_scalar) > 0:
            rules.add(VarScalar.class_name())
            
        if len(variables_list) > 0:
            rules.add(VarList.class_name())
            
        rules.add(None)
        rules.add(LocalInt.class_name())
        # rules.add(LocalList.class_name())
        
        list_all_productions = [Node,
                                ITE, 
                                LT, 
                                Abs, 
                                VarListSliceEnd, 
                                VarListSliceFront,
                                Sum, 
                                Map, 
                                Function, 
                                Plus, 
                                Times, 
                                Minus]
        
        for op in list_all_productions:
            
            op_to_remove = []
            
            for types in op.accepted_types:
                for op in types:                    
                    if op not in rules:
                        op_to_remove.append(op)
                                        
                for op in op_to_remove:
                    if op in types:
                        types.remove(op)

    def get_current_child(self):
        return self.current_child
    
    def get_number_children(self):
        return self.number_children
    
    def get_size(self):
        return self.size
    
    def set_size(self, size):
        self.size = size
        
    def replace_child(self, child, i):
        
        if len(self.children) < i + 1:
            self.add_child(child)
        else:
            if isinstance(self.children[i], Node):
                self.size -= self.children[i].size
            else:
                self.size -= 1
            
            if isinstance(child, Node):
                self.size += child.size
            else:
                self.size += 1
            
            self.children[i] = child
    
    def to_string(self):
        raise Exception('Unimplemented method: to_string')
    
    def interpret(self):
        raise Exception('Unimplemented method: interpret')

class LocalInt(Node):
    def __init__(self):
        super(LocalInt, self).__init__()
        self.number_children = 0
        self.size = 0
        
    @classmethod
    def new(cls):
        inst = cls()
        
        return inst
    @staticmethod
    def is_terminal():
        return True

    def to_string(self):
        return 'LocalInt'
    
    def interpret(self, env):
        if self.local not in env:
            raise Exception('LocalInt not inserted in environment.')
        
        if self.intname64 not in env[self.local]:
            raise Exception('LocalInt not inserted in environment.')

        # print('LocalInt: ', env[self.local][self.intname64])

        return env[self.local][self.intname64]

class VarList(Node):        
    
    def __init__(self):
        super(VarList, self).__init__()
        self.number_children = 1
        self.size = 0
        
    @classmethod
    def new(cls, var):
        inst = cls()
        inst.add_child(var)
        
        return inst

    @staticmethod
    def is_terminal():
        return True

    def to_string(self):
        if len(self.children) == 0:
            raise Exception('VarList: Incomplete Program')
        
        return self.children[0]
    
    def interpret(self, env):
        if len(self.children) == 0:
            raise Exception('VarList: Incomplete Program')
        
        return env[self.children[0]]

class VarScalarFromArray(Node):        
    
    def __init__(self):
        super(VarScalarFromArray, self).__init__()
        self.number_children = 2
        self.size = 0
        
    @classmethod
    def new(cls, var, index):
        inst = cls()
        inst.add_child(var)
        inst.add_child(index)
        
        return inst
        
    def to_string(self):
        if len(self.children) == 0:
            raise Exception('VarListSliceFront: Incomplete Program')
   
        return self.children[0].to_string() + '[' + self.children[1].to_string() + ']' 
    
    def interpret(self, env):
        if len(self.children) == 0:
            raise Exception('VarScalarFromArray: Incomplete Program')

        return self.children[0].interpret(env)[self.children[1].interpret(env)]

class VarListSliceFront(Node):        
    
    def __init__(self):
        super(VarListSliceFront, self).__init__()
        self.number_children = 2
        self.size = 0
        
    @classmethod
    def new(cls, var, index):
        inst = cls()
        inst.add_child(var)
        inst.add_child(index)
        
        return inst
        
    def to_string(self):
        if len(self.children) == 0:
            raise Exception('VarListSliceFront: Incomplete Program')
   
        return self.children[0].to_string() + '[' + self.children[1].to_string() + ':]' 
    
    def interpret(self, env):
        if len(self.children) == 0:
            raise Exception('VarListSliceFront: Incomplete Program')

        return self.children[0].interpret(env)[self.children[1].interpret(env):]

class VarListSliceEnd(Node):        
    
    def __init__(self):
        super(VarListSliceEnd, self).__init__()
        self.number_children = 2
        self.size = 0
        
    @classmethod
    def new(cls, var, index):
        inst = cls()
        inst.add_child(var)
        inst.add_child(index)
        
        return inst
        
    def to_string(self):
        if len(self.children) == 0:
            raise Exception('VarListSliceEnd: Incomplete Program')
        
        return self.children[0].to_string() + '[:' + self.children[1].to_string() + ']'
    
    def interpret(self, env):
        if len(self.children) == 0:
            raise Exception('VarListSliceEnd: Incomplete Program')

        return self.children[0].interpret(env)[:self.children[1].interpret(env)]


class VarScalar(Node):
    
    def __init__(self):
        super(VarScalar, self).__init__()
        self.number_children = 1
        self.size = 0
        
    @classmethod
    def new(cls, var):
        inst = cls()
        inst.add_child(var)
        
        return inst
    
    @staticmethod
    def is_terminal():
        return True

    def to_string(self):
        if len(self.children) == 0:
            raise Exception('VarScalar: Incomplete Program')
        
        return self.children[0]
    
    def interpret(self, env):
        if len(self.children) == 0:
            raise Exception('VarScalar: Incomplete Program')
        
        return env[self.children[0]]

class NumericConstant(Node):
    
    def __init__(self):
        super(NumericConstant, self).__init__()
        self.number_children = 1
        self.size = 0
        
    @classmethod
    def new(cls, var):
        inst = cls()
        inst.add_child(var)
        
        return inst

    @staticmethod
    def is_terminal():
        return True

    def to_string(self):
        if len(self.children) == 0:
            raise Exception('VarScalar: Incomplete Program')
        
        return str(self.children[0])
        
    def interpret(self, env):
        if len(self.children) == 0:
            raise Exception('VarScalar: Incomplete Program')
        
        return self.children[0]

class Times(Node):
    def __init__(self):
        super(Times, self).__init__()

        self.number_children = 2
        
    @classmethod
    def new(cls, left, right):
        inst = cls()
        inst.add_child(left)
        inst.add_child(right)
        
        return inst
        
    def to_string(self):
        if len(self.children) < 2:
            raise Exception('Times: Incomplete Program')
        
        return "(" + self.children[0].to_string() + " * " + self.children[1].to_string() + ")"
    
    def interpret(self, env):
        if len(self.children) < 2:
            raise Exception('Times: Incomplete Program')
        
        return self.children[0].interpret(env) * self.children[1].interpret(env)

class Plus(Node):
    def __init__(self):
        super(Plus, self).__init__()
        
        self.number_children = 2
        
    @classmethod
    def new(cls, left, right):
        inst = cls()
        inst.add_child(left)
        inst.add_child(right)
        
        return inst
        
    def to_string(self):
        return "(" + self.children[0].to_string() + " + " + self.children[1].to_string() + ")"
    
    def interpret(self, env):
        return self.children[0].interpret(env) + self.children[1].interpret(env)
    
class Minus(Node):   
    def __init__(self):
        super(Minus, self).__init__()
        
        self.number_children = 2
    
    @classmethod
    def new(cls, left, right):
        inst = cls()
        inst.add_child(left)
        inst.add_child(right)
        
        return inst
    
    def to_string(self):
        return "(" + self.children[0].to_string() + " - " + self.children[1].to_string() + ")"
    
    def interpret(self, env):
        return self.children[0].interpret(env) - self.children[1].interpret(env)   

class Function(Node):
    def __init__(self):
        super(Function, self).__init__()
        self.number_children = 1
        
    @classmethod
    def new(cls, var):
        inst = cls()
        inst.add_child(var)
        
        return inst
        
    def to_string(self):
        return "(lambda x : " + self.children[0].to_string() + ")"
    
    def interpret(self, env):
        return lambda x : self.children[0].interpret_local_variables(env, x)   

class Argmax(Node):
    def __init__(self):
        super(Argmax, self).__init__()

        self.number_children = 1
        
    @classmethod
    def new(cls, var):
        inst = cls()
        inst.add_child(var)
        
        return inst
        
    def to_string(self):       
        return 'argmax(' + self.children[0].to_string() + ")"
    
    def interpret(self, env):
        return np.argmax(self.children[0].interpret(env)) 

class Sum(Node):
    def __init__(self):
        super(Sum, self).__init__()

        self.number_children = 1
        
    @classmethod
    def new(cls, var):
        inst = cls()
        inst.add_child(var)
        
        return inst
        
    def to_string(self):
        return 'sum(' + self.children[0].to_string() + ")"
    
    def interpret(self, env):       
        return np.sum(self.children[0].interpret(env)) 

class Abs(Node):
    def __init__(self):
        super(Abs, self).__init__()
        self.number_children = 1
        
    @classmethod
    def new(cls, expression):
        inst = cls()
        inst.add_child(expression)
        
        return inst
        
    def to_string(self):
        return 'abs(' + self.children[0].to_string() + ") "
    
    def interpret(self, env):       
        return abs(self.children[0].interpret(env))

class LT(Node):
    def __init__(self):
        super(LT, self).__init__()
        self.number_children = 2
        
    @classmethod
    def new(cls, left, right):
        inst = cls()
        inst.add_child(left)
        inst.add_child(right)
        
        return inst
        
    def to_string(self):
        return self.children[0].to_string() + " < " + self.children[1].to_string()
    
    def interpret(self, env):       
        return self.children[0].interpret(env) < self.children[1].interpret(env)
    

class ITE(Node):
    def __init__(self):
        super(ITE, self).__init__()

        self.number_children = 3
        
    @classmethod
    def new(cls, bool_expression, true_block, false_block):
        inst = cls()
        inst.add_child(bool_expression)
        inst.add_child(true_block)
        inst.add_child(false_block)
        
        return inst
        
    def to_string(self):
        return 'if ' + self.children[0].to_string() + ' then: ' + self.children[1].to_string() + ' else: ' + self.children[2].to_string() 
    
    def interpret(self, env):        
        if self.children[0].interpret(env):
            return self.children[1].interpret(env)
        else:
            return self.children[2].interpret(env)

class Map(Node):
    def __init__(self):
        super(Map, self).__init__()
        self.exception_threshold = 100
        self.number_children = 2
        
    @classmethod
    def new(cls, func, l):
        inst = cls()
        inst.add_child(func)
        inst.add_child(l)
        
        return inst
        
    def to_string(self):
        if self.children[1] is None:
            return 'map(' + self.children[0].to_string() + ", None)"
        return 'map(' + self.children[0].to_string() + ", " + self.children[1].to_string() + ")"
    
    def interpret(self, env):          
        # if list is None, then it tries to retrieve from local variables from a lambda function
        if self.children[1] is None:
            list_var = env[self.local][self.listname]
    
            return list(map(self.children[0].interpret(env), list_var))
        list_var = self.children[1].interpret(env)
        
        v = list(map(self.children[0].interpret(env), list_var)) 

        # removing local variables from the context so they can't be used elsewhere
        # not sure this works with multiple chained map functions. 
        env[self.local].pop(self.intname64)
        env.pop(self.local)

        return v

class LocalList(Node):
    def __init__(self):
        super(LocalList, self).__init__()
        self.size = 0
    
    @classmethod
    def new(cls):
        inst = cls()
        return inst
    
    @staticmethod
    def is_terminal():
        return True

    def to_string(self):
        return 'local_list' 
        
    def interpret(self, env):
        return env[self.local][self.listname] 

Node.restore_original_production_rules()