import sys
sys.path.append("../")
from guide import Guide
from  dsl.dsl import *

list_all_productions = [ITE, 
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

def test0():
    guide = Guide(list_all_productions)
    guide.printer()

def test1():
    guide0 = Guide(list_all_productions)
    guide1 = Guide(list_all_productions)
    guide1.conf0();
    print("guide0 <= guide1 ",guide0.accept(guide1))
    print("guide1 <= guide0 ",guide1.accept(guide0))

if __name__ == "__main__":
    
    test1()