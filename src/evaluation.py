from math import inf
import numpy as np
from domains.pancake import Pancake

from solver.ida_star import IDAStar

class EvalBase:
    def eval(self, program):

        loss = 0
        number_states = 0

        for i in range(len(self._states)):
            env = {}
            env['state'] = np.array(self._states[i])
            env['length'] = len(self._states[i])

            # print('state: ', env['state'])
            try:
                h_value = program.interpret(env)
                # print(h_value, type(h_value), isinstance(h_value, np.int64))
                if not isinstance(h_value, int) and not isinstance(h_value, np.int64):
                    return inf, number_states + 1

                loss += (h_value - self._h_values[i])**2

                # print(program.to_string())
                # print('loss: ', loss, h_value, self._h_values[i])

                number_states += 1

            except Exception as e:
                # print(e)
                return inf, number_states
            
        return loss, number_states

class EvalTrueDistance(EvalBase):

  


    def __init__(self, number_states , size):
        self._states = []
        self._h_values = []
        ida = IDAStar()
        for i in range(number_states):
            print("State ",i)
            permutation = np.arange(1, size, 1)
            np.random.shuffle(permutation)
            start_pancake = Pancake(permutation)

            h = ida.search(start_pancake, lambda x : 0)
            
            print(permutation, h)

            self._states.append(permutation)
            self._h_values.append(h)
            print()
    
    def __init__(self, path):
        arq = open(path,'r')
        linhas = arq.readlines()
        size= int(linhas[0])
        self._states = []
        self._h_values = []
        print("Size = ",size)
        for i in range (1,len(linhas)):
            dados= linhas[i].rsplit('\n')[0].split("\t")
            h= int(dados[1])
            permutation = np.arange(1,size,1)
            aux = dados[0].split(";")
            
            for j in range(0,size-1):
                permutation[j]=int(aux[j])
            print(permutation,h)
            self._states.append(permutation)
            self._h_values.append(h)




    def get_states(self):
        return self._states

    def save_state(self,path):
        arquivo = open(path,'w')
        arquivo.write(str(len(self._states[0])+1)+"\n")
        for i in range(len(self._states)):
            for s in self._states[i]:
                arquivo.write(str(s)+';')
            arquivo.write("\t"+str(self._h_values[i])+"\n")

class EvalBaseHeuristicPK(EvalBase):
    def __init__(self, number_states, size):
        self._states = []
        self._h_values = []

        for _ in range(number_states):
            permutation = np.arange(1, size, 1)
            np.random.shuffle(permutation)
            h = self.heuristic_value_pancake(permutation)
            
            self._states.append(permutation)
            self._h_values.append(h)

    def get_states(self):
        return self._states

    def heuristic_value_pancake(self, state):
        r = 0

        for i in range(len(state) - 1):
            d = state[i] - state[i + 1]
            if d < -1 or d > 1:
                r += 1

        d = state[-1] - len(state)
        # if d < -1 or d > 1:
        if d < 0:
            r += 1
        return r


