#!/usr/bin/python3
# CMPT310 A2
#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
"""
num_hours_i_spent_on_this_assignment = 
"""
#
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
"""
<Your feedback goes here>


"""
#####################################################
#####################################################
import sys, getopt
import copy
import random
import time
import numpy as np
sys.setrecursionlimit(10000)

class SatInstance:
    def __init__(self):
        pass

    def from_file(self, inputfile):
        self.clauses = list()
        self.VARS = set()
        self.p = 0
        self.cnf = 0
        with open(inputfile, "r") as input_file:
            self.clauses.append(list())
            maxvar = 0
            for line in input_file:
                tokens = line.split()
                if len(tokens) != 0 and tokens[0] not in ("p", "c"):
                    for tok in tokens:
                        lit = int(tok)
                        maxvar = max(maxvar, abs(lit))
                        if lit == 0:
                            self.clauses.append(list())
                        else:
                            self.clauses[-1].append(lit)
                if tokens[0] == "p":
                    self.p = int(tokens[2])
                    self.cnf = int(tokens[3])
            assert len(self.clauses[-1]) == 0
            self.clauses.pop()
            if (maxvar > self.p):
                print("Non-standard CNF encoding!")
                sys.exit(5)
        # Variables are numbered from 1 to p
        for i in range(1, self.p + 1):
            self.VARS.add(i)

    def __str__(self):
        s = ""
        for clause in self.clauses:
            s += str(clause)
            s += "\n"
        return s


def main(argv):
    inputfile = ''
    verbosity = False
    inputflag = False
    try:
        opts, args = getopt.getopt(argv, "hi:v", ["ifile="])
    except getopt.GetoptError:
        print('DPLLsat.py -i <inputCNFfile> [-v] ')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('DPLLsat.py -i <inputCNFfile> [-v]')
            sys.exit()
        ##-v sets the verbosity of informational output
        ## (set to true for output veriable assignments, defaults to false)
        elif opt == '-v':
            verbosity = True
        elif opt in ("-i", "--ifile"):
            inputfile = arg
            inputflag = True
    if inputflag:
        instance = SatInstance()
        instance.from_file(inputfile)
        start_time = time.time()
        solve_dpll(instance, verbosity)
        print("--- %s seconds ---" % (time.time() - start_time))

    else:
        print("You must have an input file!")
        print('DPLLsat.py -i <inputCNFfile> [-v]')
def Unit_Propogation(clauses, variables, model):
    ret_value = 0
    for each_clause in clauses:
        if len(each_clause) == 1:
            if each_clause[0] not in model.keys():
                ret_value = each_clause[0]
                #print("Unit clause found: ", ret_value)
                return ret_value
    return False

def Pure_Elim(clauses, variables, model):

    #print("Entering pure elimination: ", clauses, model)    
    
    #################################
    '''
    unassigned = []
    ret_value = 0
    for each_num in variables:
        if each_num not in model.keys():
            unassigned.append(each_num)
            test = each_num * -1
            unassigned.append(test)
            
    pure_found = False

    for each_num in unassigned:
        ret_value = each_num
        pure_found = True
        for each_clause in clauses:
            if (each_num * -1) in each_clause:
                pure_found = False
                break
        if pure_found:
            break
    if pure_found:
        return ret_value
    return False
    '''
    unassigned = []
    ret_value = 0
    for each_num in variables:
        if each_num not in model.keys():
            unassigned.append(each_num)
            test = each_num * -1
            unassigned.append(test)
            
    pure_found = False
    for each_num in unassigned:
        ret_value = each_num
        num_counterpart = each_num * -1
        pure_found = True
        for each_clause in clauses:
            if (num_counterpart in each_clause):
                pure_found = False
                break

        if pure_found:
            #print("Found a positive pure.")
            break
        
        if (not pure_found):
            ret_value = num_counterpart
            pure_found = True 
            for each_clause in clauses:
                if (each_num in each_clause):
                    pure_found = False
                    break

            if pure_found:
                break
          
    if pure_found:
        #print("Pure found: ", ret_value)
        return ret_value
        
    return False
    


def DPLL(clauses, variables, model):

    # Basecases
    if (clauses == []):
        #print("Success: ", model)
        return model
    if ([] in clauses):
        #print("This method won't work.")
        return False

    get_varz = False
    for varz in variables:
        if varz not in model.keys():
            get_varz = varz
            break
    #print("Unassigned first var: ", get_varz)
    if get_varz:
        # Set get_varz to true   
        ####################################
        
        get_pure = Pure_Elim(clauses, variables, model)
        if get_pure:
            #print(get_pure)
            pure_clauses = []
            pure_model = copy.deepcopy(model)

            for each_clause in clauses:
                if get_pure not in each_clause:
                    pure_clauses.append(list(each_clause))
            for each_clause in pure_clauses:
                for e_var in each_clause:
                    if (-1 * get_pure) == e_var:
                        each_clause.remove(e_var)
            if (get_pure > 0):
                pure_model[get_pure] = True
            if (get_pure < 0):
                negative_unit = get_pure * -1
                pure_model[negative_unit] = False
            return DPLL(pure_clauses, variables, pure_model)
        
        ####################################
        get_unit = Unit_Propogation(clauses, variables, model)
        if get_unit:
            unit_clauses = []
            unit_model = copy.deepcopy(model)
            
            for each_clause in clauses:
                #print("EACH CLAUSE", each_clause)
                if get_unit not in each_clause:
                    unit_clauses.append(list(each_clause))
                    #print("UNTI CLAUSES: ", unit_clauses)
            for each_clause in unit_clauses:
                for e_var in each_clause:
                    if (-1 * get_unit) == e_var:
                        each_clause.remove(e_var)
            if (get_unit > 0):
                unit_model[get_unit] = True
            if (get_unit < 0):
                neg_unit = get_unit * -1
                unit_model[neg_unit] = False
            #print("Unit clauses: ", unit_clauses)
            #print("Unit model: ", unit_model)
            return DPLL(unit_clauses, variables, unit_model)
            
        
        ####################################
        positive_clauses = []
        positive_model = copy.deepcopy(model)
        for each_clause in clauses:
            if get_varz not in each_clause:
                test_clause = list(each_clause)
                the_complement = get_varz * -1
                if (the_complement in test_clause):
                    test_clause.remove(the_complement)
                positive_clauses.append(list(test_clause))
        #print(positive_clauses)
        '''
        for each_clause in positive_clauses:
            for e_var in each_clause: # careful - this may not pass test.
                if (-1 * get_varz) == e_var:
                    each_clause.remove(e_var)
        '''
        '''
        #print("Clauses: ", clauses)
        # Set get_varz to false
        for each_clause in clauses:
            if (get_varz * -1) not in each_clause:
                negative_clauses.append(list(each_clause))
        for each_clause in negative_clauses:
            for e_var in each_clause:
                # This will not index correctly.
                if get_varz == e_var:
                    each_clause.remove(e_var)
        '''
        positive_model[get_varz] = True
        #print("Model: ", positive_model)
        #print("Positive_clauses: ", positive_clauses)
        #print("Negative_clauses: ", negative_clauses)
            
        result = DPLL(positive_clauses, variables, positive_model)

        if result:
            return result
        else:
            negative_clauses = []
            negative_model = copy.deepcopy(model)
            #print("Clauses: ", clauses)
            # Set get_varz to false
            '''
            for each_clause in clauses:
                if (get_varz * -1) not in each_clause:
                    test_clause = list(each_clause)       
                    if (get_varz in test_clause):
                        test_clause.remove(get_varz)
                    negative_clauses.append(list(each_clause))
            '''
            
            for each_clause in clauses:
                if (get_varz * -1) not in each_clause:
                    negative_clauses.append(list(each_clause))
            for each_clause in negative_clauses:
                for e_var in each_clause:
                    # This will not index correctly.
                    if get_varz == e_var:
                        each_clause.remove(e_var)
            
            #print("Going the negative route.")
            #print("Negative clauses: ", negative_clauses)
            negative_model[get_varz] = False
            #print("Negative model going into recursion: ", negative_model)
            result = DPLL(negative_clauses, variables, negative_model)
            if result:
                return result
            else:
                return False 
 
# Finds a satisfying assignment to a SAT instance,
# using the DPLL algorithm.
# Input: a SAT instance and verbosity flag
# Output: print "UNSAT" or
#    "SAT"
#    list of true literals (if verbosity == True)
#
#  You will need to define your own
#  DPLLsat(), DPLL(), pure-elim(), propagate-units(), and
#  any other auxiliary functions
def solve_dpll(instance, verbosity):
    #print(instance)
    # instance.VARS goes 1 to N in a dict
    # print(instance.VARS)
    #print(verbosity)
    ###########################################
    # Start your code
    clauses = instance.clauses
    variables = instance.VARS
    model = {}
    #print("Original clauses: ",clauses)
    #print("Original variables: ", variables)

    result = DPLL(clauses, variables, model)
    #print("Result of DPLL: ", result)
    if (result == False):
        print("UNSAT")
        return
    true_vars = []
    if verbosity:
        for key in result:
            if result[key] == True:
                true_vars.append(key)
        print("SAT"+ str(true_vars))
    else:
        print("SAT")
            
    ###########################################


if __name__ == "__main__":
    main(sys.argv[1:])
