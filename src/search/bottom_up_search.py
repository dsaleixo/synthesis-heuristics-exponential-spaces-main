from dsl.dsl_bus import *
import time
from os.path import join
from dsl.dsl import Node
from b2n.l1Binaria import L1Binaria
from guides.guide import Guide
from math import inf
import os, psutil 



import numpy as np

class ProgramList():
    
    def __init__(self):
        self.plist = {}
        self.number_programs = 0
    
    def insert(self, program):       
        if program.get_size() not in self.plist:
            self.plist[program.get_size()] = {}
        
        if program.class_name() not in self.plist[program.get_size()]:
            self.plist[program.get_size()][program.class_name()] = []
        
        self.plist[program.get_size()][program.class_name()].append(program)
        self.number_programs += 1
                                                
    def get_programs(self, size):
        
        if size in self.plist: 
            return self.plist[size]
        return {}
    
    def get_number_programs(self):
        return self.number_programs
       

class BottomUpSearch():
    
    def __init__(self,guide, log_file, program_file, log_results=False):
        self.log_results = log_results
        self.guide = Guide(Node.all_rules())
        self.guide=guide
        

        

        if self.log_results:
            self.log_folder = 'logs/'
            self.program_folder = 'programs/'
            
            self.log_file = 'bus-' + log_file
            self.program_file = 'bus-' + program_file
    
    def generate_initial_set_of_programs(self, numeric_constant_values,
                                               variables_scalar,
                                               variables_list):
        set_of_initial_programs = []
        
        for i in variables_scalar:
            p = VarScalar.new(i)
            
            if self.has_equivalent(p)and self.guide.valid_program(p):
                continue
            
            set_of_initial_programs.append(p)
                
        for i in variables_list:
            p = VarList.new(i)
            
            if self.has_equivalent(p)and self.guide.valid_program(p):
                continue
            
            set_of_initial_programs.append(p)

        for i in numeric_constant_values:
            constant = NumericConstant.new(i)
            
            if self.has_equivalent(constant)and self.guide.valid_program(constant):
                continue
            
            set_of_initial_programs.append(constant)

        if self.guide.valid_program(LocalInt.new()):
            set_of_initial_programs.append(LocalInt.new())
        if self.guide.valid_program(LocalList.new()):
            set_of_initial_programs.append(LocalList.new())
            
        return set_of_initial_programs
        
    
    def init_env(self, state):
        env = {}
        env['state'] = state
        env['length'] = len(state)     
        return env
    
    def run_program_on_equivalence_data(self, p):
        outputs = []
        
        for state in self._eval.get_states():
            env = self.init_env(state)
            try:
                out = p.interpret(env)
                
                if isinstance(out, list):
                    if isinstance(out[0], list):
                        out = tuple(tuple(l) for l in out)
                    else:
                        out = tuple(out)
                if isinstance(out, np.ndarray):
                    out = tuple(out)

                outputs.append(out)
            except Exception:
                return None, True
        
        return tuple(outputs), False
    
    def has_equivalent(self, p):
        outputs_p, error = self.run_program_on_equivalence_data(p)
        
        if not error:
            if type(p) not in self.programs_outputs:
                self.programs_outputs[type(p)] = set()

            if outputs_p in self.programs_outputs[type(p)]:

                # print('Has equivalent: ', p.to_string())
                # print(self.programs_outputs[outputs_p])
                # print()
                return True
            else:
                #self.programs_outputs.add(outputs_p)
                self.programs_outputs[type(p)].add(outputs_p)
                return False
        return False
    
    def grow(self, operations, size):
        new_programs = []

        for op in operations:

            # print('Growing operation: ', op)

            for p in op.grow(self.plist, size,self.guide):
                # print('Generated: ', p.to_string())
                if p.to_string() not in self.closed_list and self.guide.valid_program(p):
                    
                    if self.has_equivalent(p):
                        self.closed_list.add(p.to_string())
                        continue
                    
                    self.closed_list.add(p.to_string())
                    new_programs.append(p)
                    yield p
                         
        for p in new_programs:
            self.plist.insert(p)
            
    def get_closed_list(self):
        return self.closed_list

    def search(self, 
               bound, 
               operations,
               numeric_constant_values, 
               variables_scalar,
               variables_list, 
               eval_function,l1): 
        
        

        self._eval = eval_function
        '''
        NumericConstant.accepted_types = [set(numeric_constant_values)]
        VarList.accepted_types = [set(variables_list)]
        VarScalar.accepted_types = [set(variables_scalar)]
        
        Node.filter_production_rules(operations, 
                             numeric_constant_values, 
                             variables_scalar, 
                             variables_list)
        '''
        self.closed_list = set()
        self.programs_outputs = {} #set()
        
        initial_set_of_programs = self.generate_initial_set_of_programs(numeric_constant_values,
                                                                        variables_scalar,
                                                                        variables_list)
        self.plist = ProgramList()
        for p in initial_set_of_programs:
            self.plist.insert(p)
        
        # print('Number of programs: ', self.plist.get_number_programs())

        # for s, programs in self.plist.plist.items():
        #     print(s, programs)
        #     for type, ps in programs.items():
        #         print(type) 
        #         for p in ps:
        #             print(p.to_string())
        
        self._variables_list = variables_list
        
        number_programs_evaluated = 0
        total_number_states_evaluated = 0
        current_size = 0
        id_log = 1
        
        best_loss = None
        best_program = None
       
        while current_size <= bound:
            
            number_evaluations_bound = 0

            print('Current bound: ', current_size)
            #print(psutil.virtual_memory()._asdict()) 
            process = psutil.Process(os.getpid())
            free_m = 23099292672-process.memory_info().rss
            #print("free ",(free_m))
            for p in self.grow(operations, current_size):
                
               # print(p.to_string())
#                 if isinstance(p, ITE):
#                     print(p.to_string())
            
                

                                                                  
                memoria = psutil.virtual_memory()._asdict()['free']- 104857600
                process = psutil.Process(os.getpid())
                free_m = 23099292672-process.memory_info().rss
                if  memoria<0 or free_m<0:
                   
                    if self.log_results:
                        if best_loss == None:
                            best_loss = inf
                        with open(join(self.log_folder + self.log_file), 'a') as results_file:
                            
                            results_file.write(("{:d}, {:f}, {:d}, {:f} \n".format(id_log, 
                                                                                    best_loss, 
                                                                                    total_number_states_evaluated,
                                                                                    45)))                    
                    
                    return best_loss, best_program,current_size, number_programs_evaluated, total_number_states_evaluated
                
                
                number_programs_evaluated += 1
                number_evaluations_bound += 1
                
#                 if number_evaluations_bound % 1000 == 0:
#                     print('Number Eval Bounds: ', number_evaluations_bound)

                loss, number_states = self._eval.eval(p)
                guide_aux = Guide(Node.all_rules())
                guide_aux.countRules(p)
                if loss < inf:
                    l1.update(guide_aux,loss)

                # print(p.to_string(), loss)
                total_number_states_evaluated += number_states                    

                if best_program is None or loss < best_loss:
                    best_loss = loss
                    best_program = p

                    print(best_program.to_string())
                    guide0 = Guide(Node.all_rules())
                    guide0.countRules(best_program)
                    #guide0.printer()
                    print()     

                    if self.log_results:
                        with open(join(self.log_folder + self.log_file), 'a') as results_file:

                            print(id_log, best_loss, total_number_states_evaluated, number_programs_evaluated)
                            results_file.write(("{:d}, {:f}, {:d}, {:f} \n".format(id_log, 
                                                                                    best_loss, 
                                                                                    total_number_states_evaluated,
                                                                                    number_programs_evaluated,
                                                                                    -1 )))
                            
                        with open(join(self.program_folder + self.program_file), 'a') as results_file:
                            results_file.write(("{:d} \n".format(id_log)))
                            results_file.write(best_program.to_string())
                            results_file.write('\n')
                        
                        id_log += 1  
                
            #print('Size: ', current_size, ' Evaluations: ', number_evaluations_bound)
            current_size += 1
        if best_loss == None:
            best_loss = inf
        return best_loss, best_program,current_size, number_programs_evaluated, total_number_states_evaluated

