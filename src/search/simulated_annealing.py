from os.path import join
import os
import random
import sys
import time
from dsl.dsl import *

class SimulatedAnnealing:

    def __init__(self, log_file, program_file):
        ncpus = int(os.environ.get('SLURM_CPUS_PER_TASK', default = 1))
        
        self.log_folder = 'logs/'
        self.program_folder = 'programs/'
        self.binary_programs = 'binary_programs/'
        
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)
            
        if not os.path.exists(self.program_folder):
            os.makedirs(self.program_folder)
            
        if not os.path.exists(self.binary_programs):
            os.makedirs(self.binary_programs)
        
        self.log_file = 'sa-' + str(ncpus) + '-cpus-' + log_file
        self.program_file = 'sa-' + str(ncpus) + '-cpus-' + program_file
        self.binary_program_file = self.binary_programs + 'sa-' + str(ncpus) + '-cpus-' + program_file + '.pkl'

    def return_terminal_child(self, p, types):
        terminal_types = []
        
        for t in types:
            child = p.factory(t)
            
            if child.get_number_children() == 0 or child.is_terminal():
                terminal_types.append(child)
        
        if len(terminal_types) == 0:
            for t in types:
                child = p.factory(t)
             
                if child.get_number_children() == 1:
                    terminal_types.append(child)
        
        if len(terminal_types) > 0:
            return terminal_types[random.randrange(len(terminal_types))]

        return p.factory(list(types)[random.randrange(len(types))])


    def fill_random_program(self, p, depth, max_depth):

        size = p.get_size()
        
        for i in range(p.get_number_children()):
            types = p.accepted_rules(i)
            
            if p.is_terminal():
                child = list(types)[random.randrange(len(types))]
                p.add_child(child)
                
                size += 1
            elif depth >= max_depth:                              
                child = self.return_terminal_child(p, types)
                p.add_child(child)
                child_size = self.fill_random_program(child, depth + 1, max_depth)
                
                size += child_size
            else:
                child = p.factory(list(types)[random.randrange(len(types))])
                p.add_child(child)

                child_size = self.fill_random_program(child, depth + 1, max_depth)
                
                size += child_size
        
        p.set_size(size)
        return size

    def mutate_inner_nodes_ast(self, p, index):
        self.processed += 1
        
        if not isinstance(p, Node):
            return False
        
        for i in range(p.get_number_children()):
            
            if index == self.processed:
                # Accepted rules for the i-th child
                types = p.accepted_rules(i)
                
                # Generate instance of a random accepted rule
                child = Node.factory(list(types)[random.randrange(len(types))])
                
                # Randomly generate the child
                if isinstance(child, Node):
                    self.fill_random_program(child, 0, 4)
                
                # Replacing previous child with the randomly generated one
                p.replace_child(child, i)
                return True
            
            mutated = self.mutate_inner_nodes_ast(p.children[i], index)
            
            if mutated:
                
                # Fixing the size of all nodes in the AST along the modified branch 
                modified_size = 1
                for j in range(p.get_number_children()):
                    if isinstance(p.children[j], Node):
                        modified_size += p.children[j].get_size()
                    else:
                        modified_size += 1
                p.set_size(modified_size)
                
                return True
            
        return False
        

    def mutate(self, p):        
        index = random.randrange(p.get_size())
        
        # Mutating the root of the AST
        if index == 0:
            
            initial_types = Node.accepted_rules(0)
            p = Node.factory(list(initial_types)[random.randrange(len(initial_types))])

            self.fill_random_program(p, self.initial_depth_ast, self.max_mutation_depth)
                
            return p

        self.processed = 0
        self.mutate_inner_nodes_ast(p, index)
        
        return p

    def random_program(self):
        initial_types = list(Node.accepted_initial_rules()[0])
        p = Node.factory(initial_types[random.randrange(len(initial_types))])

        self.fill_random_program(p, self.initial_depth_ast, self.max_mutation_depth)
                
        return p
    
    def accept_function(self, current_score, next_score):
        if next_score < current_score:
            return 1.0

        try:
            v = np.exp(self.beta * (current_score - next_score)/self.current_temperature)
        except Exception:
            return 0.0

        return v
    
    def decrease_temperature(self, i):
        self.current_temperature = self.initial_temperature / (1 + self.alpha * (i))
        
    def search(self,
               operations,
               numeric_constant_values,
               variables_scalar,
               variables_list, 
               eval_function,
               initial_temperature,
               alpha,
               beta,
               time_limit,
               initial_program=None):
        
        time_start = time.time()

        Node.filter_production_rules(operations, 
                                numeric_constant_values,
                                variables_scalar, 
                                variables_list)
        
        self.max_mutation_depth = 4
        self.initial_depth_ast = 0
        self.initial_temperature = initial_temperature
        self.alpha = alpha
        self.beta = beta
        self.slack_time = 600
        
        NumericConstant.accepted_types = [set(numeric_constant_values)]
        VarList.accepted_types = [set(variables_list)]
        VarScalar.accepted_types = [set(variables_scalar)]
        
        self.numeric_constant_values = numeric_constant_values
        self.variables_list = variables_list
        self.eval_function = eval_function        
        
        best_score = sys.maxsize
        print('Max size: ', sys.maxsize)
        best_program = None
        
        id_log = 1
        number_states_evaluated = 0

        if initial_program is not None:
            current_program = copy.deepcopy(initial_program)
        else:
            current_program = self.random_program()
            
        while True:
            self.current_temperature = self.initial_temperature
            
            current_score, number_states = self.eval_function.eval(current_program)
            number_states_evaluated += number_states
            
            iteration_number = 1
        
            if best_program is None or current_score < best_score:
                best_score = current_score
                best_program = current_program
                
                
                with open(join(self.log_folder + self.log_file), 'a') as results_file:
                    results_file.write(("{:d}, {:f}, {:d}, {:f} \n".format(id_log, 
                                                                            best_score, 
                                                                            number_states_evaluated,
                                                                            time.time() - time_start)))
                    
                with open(join(self.program_folder + self.program_file), 'a') as results_file:
                    results_file.write(("{:d} \n".format(id_log)))
                    results_file.write(best_program.to_string())
                    results_file.write('\n')
                
                id_log += 1
            
            while self.current_temperature > 1:
                                
                time_end = time.time()
                
                if time_end - time_start > time_limit - self.slack_time:
                    with open(join(self.log_folder + self.log_file), 'a') as results_file:
                        results_file.write(("{:d}, {:f}, {:d}, {:f} \n".format(id_log, 
                                                                                best_score, 
                                                                                number_states_evaluated,
                                                                                time_end - time_start)))                    
                    return best_score, best_program
                
                copy_program = copy.deepcopy(current_program)

                # print('Current: ')
                # print(current_program.to_string())    
                mutation = self.mutate(copy_program)
                # print('Mutated: ')
                # print(mutation.to_string())
                # print()
                
                next_score, number_states = self.eval_function.eval(mutation)
                
                number_states_evaluated += number_states
                                
                if best_program is None or next_score < best_score:
                    
                    best_score = next_score
                    best_program = mutation
                    
                    with open(join(self.log_folder + self.log_file), 'a') as results_file:
                        results_file.write(("{:d}, {:f}, {:d}, {:f} \n".format(id_log, 
                                                                                best_score, 
                                                                                number_states_evaluated,
                                                                                time_end - time_start)))
                        
                    with open(join(self.program_folder + self.program_file), 'a') as results_file:
                        results_file.write(("{:d} \n".format(id_log)))
                        results_file.write(best_program.to_string())
                        results_file.write('\n')
                    
                    id_log += 1
                
                prob_accept = min(1, self.accept_function(current_score, next_score))
                
                prob = random.uniform(0, 1)
                if prob < prob_accept:                    
                    current_program = mutation
                    current_score = next_score
                
                iteration_number += 1
                
                self.decrease_temperature(iteration_number)
                # print('Current Temp: ', self.current_temperature)

            if initial_program is not None:
                current_program = copy.deepcopy(initial_program)
            else:
                if best_score == sys.maxsize:
                    current_program = self.random_program()
                else:
                    current_program = copy.deepcopy(best_program)