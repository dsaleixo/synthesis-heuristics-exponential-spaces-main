from  dsl.dsl import *
import random


class Guide:

    def __init__(self,rules):  
        self.rules = {}
        for  key in rules:
            if not key.is_terminal():
                self.rules[key.class_name()]={}
                for acc2 in key.accepted_types:
                    for acc in acc2:
                      
                        self.rules[key.class_name()][acc]=0    


    def valid_program(self,p):
        count = Guide(Node.all_rules())
        count.countRules(p)
        return self.accept(count)
       

    def accept(self,count):
        for key, value in count.rules.items():
            for k,v in value.items():
                if v > self.rules[key][k]:
                    return False
        return True

    def countRules(self,p):


        for c in p.children:
            if isinstance(c, Node) :
                self.countRule(p,c)
                self.countRules(c)


    def countRule(self,p,f):
        if not p.class_name() in self.rules:
            self.rules[p.class_name()][f.class_name()]=0
            return
        if not f.class_name() in self.rules[p.class_name()]:
            self.rules[p.class_name()][f.class_name()]=0
            return
        self.rules[p.class_name()][f.class_name()]+=1
        
    def removeV(self,vertice):
        for key, value in self.rules.items():
            for k,v in value.items():
                if key in vertice or k in vertice:
                    self.rules[key][k] = 0

    def tostring2(self):
        s=''     
        for key, value in self.rules.items():
            for k,v in value.items():
                if v==0:
                    s+="0"
                elif v==1:
                    s+="1"
                else:
                    s+="2"
        s+="\n"
        return s


    def tostring(self):
        s=''     
        for key, value in self.rules.items():
            s+=str(key)+'\n'
            for k,v in value.items():
                s+=("\t==>%3d %s"% (v,k))+"\n"
            s+="\n"
        return s



    def printer(self):
        for key, value in self.rules.items():
            print("%s" % (key))
            for k,v in value.items():
                print("\t==>%3d %s"% (v,k))
            print()
    
  
    def conf0(self):
        self.rules[VarScalarFromArray.class_name()][VarList.class_name()] =1
        self.rules[VarScalarFromArray.class_name()][NumericConstant.class_name()] =1


        self.rules[Function.class_name()][Plus.class_name()] =0
        self.rules[Function.class_name()][Times.class_name()] =0
        self.rules[Function.class_name()][ITE.class_name()] =1
        self.rules[Function.class_name()][ Abs.class_name()] =0


        self.rules[VarListSliceEnd.class_name()][LocalList.class_name()] =0
        self.rules[VarListSliceEnd.class_name()][VarList.class_name()] =1
        self.rules[VarListSliceEnd.class_name()][NumericConstant.class_name()] =1


        self.rules[ITE.class_name()][NumericConstant.class_name()] =4
        self.rules[ITE.class_name()][LT.class_name()] =2

        self.rules[VarListSliceFront.class_name()][LocalList.class_name()] =0
        self.rules[VarListSliceFront.class_name()][VarList.class_name()] =1
        self.rules[VarListSliceFront.class_name()][NumericConstant.class_name()] =1

        self.rules[Sum.class_name()][LocalList.class_name()] =0
        self.rules[Sum.class_name()][VarList.class_name()] =0
        self.rules[Sum.class_name()][Map.class_name()] =1


        self.rules[Minus.class_name()][LocalInt.class_name()] =0
        self.rules[Minus.class_name()][Plus.class_name()] =0
        self.rules[Minus.class_name()][VarScalar.class_name()] =0
        self.rules[Minus.class_name()][VarListSliceEnd.class_name()] =1
        self.rules[Minus.class_name()][NumericConstant.class_name()] =0
        self.rules[Minus.class_name()][VarListSliceFront.class_name()] =1
        self.rules[Minus.class_name()][Abs.class_name()] =0
        self.rules[Minus.class_name()][Times.class_name()] =0
        self.rules[Minus.class_name()][Sum.class_name()] = 0
        self.rules[Minus.class_name()][Minus.class_name()] = 0

        self.rules[Plus.class_name()][Sum.class_name()] = 1
        self.rules[Plus.class_name()][ITE.class_name()] = 1


        self.rules[Map.class_name()][Function.class_name()] = 1
        self.rules[Map.class_name()][Minus.class_name()] = 1 

        self.rules[Abs.class_name()][LocalInt.class_name()] = 1

        #self.rules[Argmax.class_name()][Plus.class_name()] = 0
        #self.rules[Argmax.class_name()][Times.class_name()] = 0
        #self.rules[Argmax.class_name()][ITE.class_name()] = 0
        #self.rules[Argmax.class_name()][Sum.class_name()] = 0


        self.rules[Times.class_name()][LocalInt.class_name()] = 0
        self.rules[Times.class_name()][Plus.class_name()] = 0
        self.rules[Times.class_name()][VarScalar.class_name()] = 0
        self.rules[Times.class_name()][Abs.class_name()] = 0
        self.rules[Times.class_name()][Times.class_name()] = 0
        self.rules[Times.class_name()][NumericConstant.class_name()] = 0

        self.rules[LT.class_name()][VarScalarFromArray.class_name()] = 1
        self.rules[LT.class_name()][VarScalar.class_name()] = 1
        self.rules[LT.class_name()][Abs.class_name()] = 1
        self.rules[LT.class_name()][NumericConstant.class_name()] = 1

    def conf2(self):



       
        self.rules[Function.class_name()][Plus.class_name()] =0
        self.rules[Function.class_name()][Times.class_name()] =0
        self.rules[Function.class_name()][ITE.class_name()] =1
        self.rules[Function.class_name()][ Abs.class_name()] =0
        self.rules[VarListSliceEnd.class_name()][LocalList.class_name()] =0
        self.rules[VarListSliceEnd.class_name()][VarList.class_name()] =1
        self.rules[VarListSliceEnd.class_name()][NumericConstant.class_name()] =1
        self.rules[ITE.class_name()][NumericConstant.class_name()] =1000
        self.rules[ITE.class_name()][LT.class_name()] =2
        self.rules[VarListSliceFront.class_name()][LocalList.class_name()] =0
        self.rules[VarListSliceFront.class_name()][VarList.class_name()] =1
        self.rules[VarListSliceFront.class_name()][NumericConstant.class_name()] =1
        self.rules[Sum.class_name()][LocalList.class_name()] =0
        self.rules[Sum.class_name()][VarList.class_name()] =0
        self.rules[Sum.class_name()][Map.class_name()] =1
        self.rules[Minus.class_name()][LocalInt.class_name()] =0
        self.rules[Minus.class_name()][Plus.class_name()] =0
        self.rules[Minus.class_name()][VarScalar.class_name()] =0
        self.rules[Minus.class_name()][VarListSliceEnd.class_name()] =1
        self.rules[Minus.class_name()][NumericConstant.class_name()] =0
        self.rules[Minus.class_name()][VarListSliceFront.class_name()] =1
        self.rules[Minus.class_name()][Abs.class_name()] =0
        self.rules[Minus.class_name()][Times.class_name()] =0
        self.rules[Minus.class_name()][Sum.class_name()] = 0
        self.rules[Minus.class_name()][Minus.class_name()] = 0
        self.rules[Plus.class_name()][Sum.class_name()] = 1
        self.rules[Plus.class_name()][ITE.class_name()] = 1
        self.rules[Map.class_name()][Function.class_name()] = 1
        self.rules[Map.class_name()][Minus.class_name()] = 1 
        self.rules[Abs.class_name()][LocalInt.class_name()] = 1
     


        self.rules[Times.class_name()][LocalInt.class_name()] = 0
        self.rules[Times.class_name()][Plus.class_name()] = 0
        self.rules[Times.class_name()][VarScalar.class_name()] = 0
        self.rules[Times.class_name()][Abs.class_name()] = 0
        self.rules[Times.class_name()][Times.class_name()] = 0
        self.rules[Times.class_name()][NumericConstant.class_name()] = 0

        self.rules[LT.class_name()][VarScalarFromArray.class_name()] = 1
        self.rules[LT.class_name()][VarScalar.class_name()] = 1
        self.rules[LT.class_name()][Abs.class_name()] = 1
        self.rules[LT.class_name()][NumericConstant.class_name()] = 1

        for key, value in self.rules.items():
            for k,v in value.items():
                if v>0:
                    self.rules[key][k] = 1000

    
    def clone(self):
        clone = Guide(Node.all_rules())
        for key, value in self.rules.items():
            for k,v in value.items():
                clone.rules[key][k]=self.rules[key][k]
        return clone
                
       

    def confAlet(self):
        for key, value in self.rules.items():
            for k,v in value.items():
                aux =random.randint(0,1000)%4
                if  aux<2:
                    self.rules[key][k]=0
                elif aux == 2:
                    self.rules[key][k]=2
                elif aux == 3:
                    self.rules[key][k]=1000


    def mutation(self):
        for i in range(12):
            x=random.randint(0,42)
            cont=0
            for key, value in self.rules.items():
                for k,v in value.items():
                    if cont==x:
                        aux =random.randint(0,1000)%4
                        if  aux<2:
                            self.rules[key][k]=0
                        elif aux == 2:
                            self.rules[key][k]=2
                        elif aux == 3:
                            self.rules[key][k]=1000
                           

                    cont+=1

    def canGrow(self,father_name,child_name):
        if self.rules[father_name][child_name]==0:
            return False
        return True
        







      
       
        