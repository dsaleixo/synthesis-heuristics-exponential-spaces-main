import numpy as np
from dsl.dsl import *
from evaluation import EvalBaseHeuristicPK

def heuristic_value_pancake(state):
    r = 0

    for i in range(len(state) - 1):
        d = state[i] - state[i + 1]
        if d < -1 or d > 1:
            r += 1

    d = state[-1] - len(state)
    if d < -1 or d > 1:
        r += 1
    return r

# int getHeuristic(PKState& state)
# 		{
# 			int size = PKState::size;
# 			int * m = state.getPermutation();

# 			int r = 0 ;
# 			for (int i = 0; i < size - 1; i++) 
# 			{
# 				int d = m[i] - m[i + 1];
# 				if (d < -1 || d > 1)
# 				{
# 					r++ ;
# 				}
# 			}

# 			int d = m[size - 1] - size;

# 			if (d < -1 || d > 1)
# 			{
# 				r++ ;
# 			}

# 			return (int) ( w * r ) ;
# 		}
# };


def heuristic_value(state, width, size):
    h = 0
    
    for i in range(0, size):
        if state[i] == 0:
            continue     
        h = h + abs((state[i] % width) - (i % width)) + abs(int((state[i] / width)) - int((i / width)))

    return h

state = [1, 3, 2, 0, 4, 6, 5, 7, 8]
goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]

width = 3
size = 9
r_map = map(lambda x : abs((x[0] % width) - (x[1] % width)) + abs((x[0] // width) - (x[1] // width)) if x[1] != 0 else 0, enumerate(state))

print('Functional MD: ', sum(list(r_map)))
h = heuristic_value(state, 3, 9)
print('Regular MD: ', h)

state_pk = [3, 2, 5, 1, 6, 7, 4]
r_map = sum(list(map(lambda x : 1 if abs(x) > 1 else 0, np.array(state_pk[1:]) - np.array(state_pk[:-1])))) + (1 if state_pk[-1] < len(state_pk) else 0)
print('Regular GAP: ', heuristic_value_pancake(state_pk))
print('Functional GAP: ', r_map)

print(state_pk[1:])
print(state_pk[:-2])
print(np.array(state_pk[1:]) - np.array(state_pk[:-1]))


env = {}
env['state'] = np.array(state_pk)
env['length'] = len(state_pk)
env['statediff1'] = np.array(state_pk[1:])
env['statediff2'] = np.array(state_pk[:-1])
v = VarList.new('state')
print(v.interpret(env))

eval = EvalBaseHeuristicPK(100, 10)
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

#(sum(map((lambda x : if 1 < abs(LocalInt)  then: 1 else: 0), (state[1:] - state[:-1]))) + if length < abs(LocalInt)  then: -1 else: 1)
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
print(eval.eval(program), program.to_string())
print(eval.eval(program1), program1.to_string())
# r = program.interpret(env)
# print(r)


