import sys
sys.path.append("../")
from dsl.dsl_bus import *
from b2n.l1Binaria import L1Binaria
from dsl.dsl import Node
import numpy as np
from guides.guide import Guide
from evaluation import EvalBaseHeuristicPK, EvalTrueDistance
from search.bottom_up_search import BottomUpSearch
from math import inf
import time


class SA():

    def __init__(self,nodes,log_file=''):
        self.log_file = log_file
        self.dic = {}
        self.nodes = nodes
        self.vetor = []
        self.l1 = L1Binaria(Node.all_rules())
        for _ in nodes:
            self.vetor.append(0)
        self.exemplos = [[1,1,1,1,1,1,1,1,1,1,1,1],
                         [1,1,1,1,1,1,0,1,1,1,0,1],
                         [1,1,1,1,1,0,0,1,1,1,0,1],
                         [1,1,1,1,1,0,0,0,1,1,0,1]]
                      


    


    def getSeed(self,v):
        listA = []
        listB = set()
        guide = Guide(self.nodes)
        guide.conf2();
        for i in range(len(v)):
            if v[i]==1:
                listA.append(self.nodes[i])
            else:
                listB.add(self.nodes[i].class_name())
        guide.removeV(listB)
        
       
        return listA, guide

    def run(self,eval):

        
        best = inf
        progam = None
        best_v = Guide(Node.all_rules())
        best_v.confAlet()
        
        
        bus = BottomUpSearch(best_v,'log_file', 'program_file')
        best,progam,d,e,f=bus.search(22, self.nodes, [-1, 0, 1], ['length'], ['state'], eval,self.l1)
        cont=0
        arq = open(self.log_file,'w')
        arq.write("Inicial"+"\n")
        
        while True:
            arq = open(self.log_file,'a')
            arq.write("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            arq.write(best_v.tostring2())
            arq.write("Execucao "+str(cont)+"\n")
            if isinstance(progam, Node):
                arq.write("melhor Programa ="+progam.to_string()+"\n")
            else:
                arq.write("melhor Programa ="+"Nenhum"+"\n")
            
            arq.write("melhor REsultado ="+str(best)+"\n")
            

            aux = best_v.clone()
            aux.mutation()
            arq.write("teste ="+aux.tostring2()+"\n")
            arq.close()
            ini = time.time()
            bus = BottomUpSearch(aux,'log_file', 'program_file')
            r,p,d,e,f=bus.search(22, self.nodes, [-1, 0, 1], ['length'], ['state'], eval,self.l1)
            fim = time.time()
            arq = open(self.log_file,'a')
            arq.write("Tempo de Execução : "+ str(fim-ini)+"\n")
            if isinstance(p, Node):
                arq.write("Programa ="+p.to_string()+"\n")
            else:
                arq.write("Programa ="+"Nenhum"+"\n")
            arq.write("Numero de Programa visitados ="+str(e)+"\n")
            arq.write("REsultado ="+str(r)+"\n")
            if r<= best and r>0:
                arq.write("Atualizou")
                progam = p
                best = r
                best_v = aux

            if cont%9==0:
                arq.write(self.l1.to_string())
                
            cont+=1
            arq.close()


        
        



def teste1():
    nodes =[ITE,LT, Sum,Map, Function, Plus, Times, Minus, Abs, VarListSliceFront, 
                                VarScalarFromArray,VarListSliceEnd]
    sa = SA(nodes)
    a,b = sa.getSeed(sa.exemplos[0])
    eval = EvalTrueDistance("../instance/pacanke")
        
       
    bus = BottomUpSearch(b,'log_file', 'program_file')

    r,p, d=bus.search(22, a, [-1, 0, 1], ['length'], ['state'], eval)
    print(r)
    print(p)
    print(d)


def teste2():
    nodes =[ITE,LT, Sum,Map, Function, Plus, Times, Minus, Abs, VarListSliceFront, 
                                VarScalarFromArray,VarListSliceEnd]
    sa = SA(nodes)
    print(len(nodes))

def teste3():
    best_v = Guide(Node.all_rules())
    best_v.confAlet()
    for _ in range(10):
        print(best_v.tostring2())
        best_v = best_v.clone()

if __name__ == "__main__":
    teste3()