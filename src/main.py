from evaluation import EvalBaseHeuristicPK, EvalTrueDistance
from dsl.dsl import *
from search.bottom_up_search import BottomUpSearch
from search.simulated_annealing import SimulatedAnnealing

program = Sum.new(
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
)


def run_bus():
        from dsl.dsl_bus import ITE, \
                                LT, \
                                Sum, \
                                Map, \
                                Function, \
                                Plus, \
                                Times, \
                                Minus, \
                                LocalList, \
                                Abs, \
                                VarListSliceFront, \
                                VarScalarFromArray, \
                                VarListSliceEnd
        
        eval = EvalTrueDistance("./instance/pacanke")
        # eval = EvalBaseHeuristicPK(100, 10)
       
        bus = BottomUpSearch('log_file', 'program_file')

        bus.search(22, 
                [ITE, 
                LT, 
                Sum,
                Map, 
                Plus,
                Function, 
                Minus,
                VarScalarFromArray,
                Abs,
                VarListSliceFront,
                VarListSliceEnd], [-1, 0, 1], ['length'], ['state'], eval, 1000)

def run_sa():
    eval = EvalBaseHeuristicPK(100, 10)
    sa = SimulatedAnnealing('log_file', 'program_file')

    print('Target: ', eval.eval(program))
    print(program.to_string())

    sa.search([ITE, 
                LT, 
                Sum,
                Map, 
                Function, 
                Minus,
                Abs,
                VarScalarFromArray,
                VarListSliceFront,
                VarListSliceEnd], [-1, 0, 1], [], ['state'], eval, 100, 0.9, 200, 1000, None)


def main():
        run_bus()
        # eval = EvalBaseHeuristicPK(100, 10)
        # v = eval.eval(program)
        # print(program.to_string(), v)
if __name__ == "__main__":
    main()