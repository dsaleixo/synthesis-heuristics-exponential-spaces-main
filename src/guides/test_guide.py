import sys
sys.path.append("../")
from guide import Guide
from  dsl.dsl import *



def test0():
    guide = Guide(Node.all_rules())
    guide.printer()

def test1():
    guide0 = Guide(Node.all_rules())
    guide0.conf1()
    guide0.printer()


    
def getProg0():
    program = Plus.new(
                    Sum.new(
                        Map.new(
                                Function.new(
                                            ITE.new(
                                                    LT.new(NumericConstant.new(1), Abs.new(LocalInt.new())), 
                                                    NumericConstant.new(1), 
                                                    NumericConstant.new(0)
                                                    )
                                            ), 
                                Minus.new(VarListSliceFront.new(VarList.new('state'), NumericConstant.new(1)), 
                                        VarListSliceEnd.new(VarList.new('state'), NumericConstant.new(-1)))
                            )
                        ), ITE.new(
                                    LT.new(
                                        VarScalarFromArray.new(VarList.new('state'), NumericConstant.new(-1)),
                                        VarScalar.new('length')
                                    ),
                                    NumericConstant.new(1),
                                    NumericConstant.new(0))
                    )
    return program

def getProg1():
    program1 = Plus.new(
                    Sum.new(
                        Map.new(
                                Function.new(
                                            ITE.new(
                                                    LT.new(NumericConstant.new(1), Abs.new(LocalInt.new())), 
                                                    NumericConstant.new(1), 
                                                    NumericConstant.new(0)
                                                    )
                                            ), 
                                Minus.new(VarListSliceFront.new(VarList.new('state'), NumericConstant.new(1)), 
                                        VarListSliceEnd.new(VarList.new('state'), NumericConstant.new(-1)))
                            )
                        ), ITE.new(
                                    LT.new(
                                        VarScalar.new('length'), Abs.new(LocalInt.new())
                                    ),
                                    NumericConstant.new(-1),
                                    NumericConstant.new(1))
                    )
    return program1


def test2():

  
    guide0 = Guide(Node.all_rules())
    guide0.conf0()
    guide1 = Guide(Node.all_rules())
    guide1.conf1()
    print(guide0.accept(guide1))
    print(guide1.accept(guide0))

def test3():
    p = getProg1()
    guide0 = Guide(Node.all_rules())
    guide0.countRules(p)
    guide0.printer()

def test4():
    guide0 = Guide(Node.all_rules())
    guide0.confAlet()
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    print(guide0.tostring())
    guide1= guide0.clone()
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    guide1.printer()
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    guide1.mutation()
    guide1.printer()

if __name__ == "__main__":
    
    test4()