from  dsl.dsl import *



class Guide:

    def __init__(self,rules):  
        self.rules = {}
        for  key in rules:

            self.rules[key.class_name]=0;

    def valid_program(self,p):
        count = Guide()
        p.countRules(count)
        return self.accept(count)

    def accept(self,count):
        for key, value in count.rules.items():
            if value > self.rules[key]:
                return False
        return True;

    def countRule(self,rule):
        if not rule.name() in self.rules:
            self.rules[rule.name()]=0
        self.rules[rule.name()]+=1


    def printer(self):
        for key, value in self.rules.items():
            print("%3d %s" % (value,key))
    
    def conf0(self):
        self.rules={}
        self.rules[ITE.class_name] = 0
        self.rules[LT.class_name] = 0
        self.rules[Abs.class_name] = 0
        self.rules[VarListSliceEnd.class_name] = 0
        self.rules[VarListSliceFront.class_name] = 0
        self.rules[Sum.class_name] = 0
        self.rules[Map.class_name] = 0
        self.rules[Function.class_name] = 0
        self.rules[Plus.class_name] = 0
        self.rules[Times.class_name] = 0
        self.rules[Minus.class_name] = 0
    

    