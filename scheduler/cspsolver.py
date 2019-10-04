import json
import copy
import random

''' classes CSP and minConflicts below define & solve a constraint satisfaction problem'''
class CSP(object):
        def __init__(self):
                self.nodes = []
                #describes the domain of values assignable to the node
                self.nodeDomains = {}
                #constraints depending only on asingular node 0,1 depending on node value
                self.unary_constraints = {}
                #binary constraints depending on node pair, 0,1 or 2 depending on node values
                self.binary_constraints = {}
                
        def add_node(self,node_name,domain):
                #check that node doesn't already exist
                if node_name in self.nodes:
                        return False
                self.nodes.append(node_name) 
                self.nodeDomains[node_name] = domain

        def add_unary_constraint(self,node,constraintFunc):
                #make sure node has previously been added
                if node not in self.nodes:
                        return False
                domain  = self.nodeDomains[node]
                factor = {val : constraintFunc(val) for val in domain}
                #case where no constraints existed  
                if node not in self.unary_constraints.keys():
                        self.unary_constraints[node] = factor
                        return
                #case where constraints did exist
                self.unary_constraints[node] = {val : self.unary_constraints[node][val] * factor[val] for val in domain}

        def add_binary_constraint(self,node1,node2,constaintFunc):
                #make sure both nodes have been added
                if node1 not in self.nodes or node2 not in self.nodes:
                        return False
                domain1 = self.nodeDomains[node1]
                domain2 = self.nodeDomains[node2]
                tableFactor1 = {val1 : {val2 : constaintFunc(val1,val2) for val2 in domain2} for val1 in domain1}
                tableFactor2 = {val2 : {val1 : constaintFunc(val1,val2) for val1 in domain1} for val2 in domain2}
                self.update_binary_constraint_table(node1,node2,tableFactor1)
                self.update_binary_constraint_table(node2,node1,tableFactor2) 
                   
        def update_binary_constraint_table(self,nodeA,nodeB,tableFactor):
                if nodeA not in self.binary_constraints.keys():
                        self.binary_constraints[nodeA] = {}
                        self.binary_constraints[nodeA][nodeB] = tableFactor
                        return
                if nodeB not in self.binary_constraints[nodeA].keys():
                       self.binary_constraints[nodeA][nodeB] = tableFactor
                       return
                currentTable = self.binary_constraints[nodeA][nodeB]
                for i in tableFactor:
                        for j in tableFactor[i]:
                                assert i in currentTable and j in currentTable[i]
                                currentTable[i][j] *= tableFactor[i][j]
                                
class minConflicts(object):
        def __init__(self,csp):
                self.csp = csp
                
        #assigns each variable a random domain value
        def initial_var_assignment(self):
                assignments = {}
                nodes = self.csp.nodes
                domains = self.csp.nodeDomains
                for n in nodes:
                        val_rand = random.choice(domains[n])
                        assignments[n] = val_rand
                return assignments
        
        #returns list of conflicted node assignments i.e. which evaulate to zero
        def conflicted(self,assignments):
                conflicted = []
                csp = self.csp
                for n in assignments:
                        if n in conflicted: continue 
                        val = assignments[n]
                        #make sure no KeyError on unary and binary constraints
                        try:
                                if csp.unary_constraints[n][val]==0:
                                        conflicted.append(n)
                        except KeyError:
                                pass
                        try:
                                neighbors = set(csp.binary_constraints[n].keys())
                        except KeyError:
                                continue
                        for m in neighbors:
                                val_neigh = assignments[m]
                                if csp.binary_constraints[n][m][val][val_neigh]==0:
                                        conflicted+=[n,m]
                return set(conflicted)
                
        #returns list of node neighbors that conflict with it
        def conflicted_neighbors(self,assignments,n):
                conflicted = []
                val = assignments[n]
                csp = self.csp  
                soft_weight = 1  #proportional to number of soft-constraints satisfied
                #checks for missing keys on unary constraints
                try: 
                        if csp.unary_constraints[n][val] == 0: 
                                conflicted.append(n)
                except:
                        pass
                #checks on binary constraints
                try:    
                        neighbors = set(csp.binary_constraints[n].keys())
                except:
                        return (set(conflicted),soft_weight)
                for m in neighbors:
                        val_neigh = assignments[m]
                        w = csp.binary_constraints[n][m][val][val_neigh]
                        if w==0:
                                conflicted+=[n,m]
                        else:
                                soft_weight*=w
                return (set(conflicted),soft_weight)

        def solve(self,max_iters=100):
                assignments = self.initial_var_assignment()
                csp = self.csp
                for _ in range(max_iters):
                        conflicted = self.conflicted(assignments)
                        if len(conflicted)==0: return assignments
                        #choose a random conflicted variable
                        node = random.choice(list(conflicted))
                        val = assignments[node]
                        c0,w0 = self.conflicted_neighbors(assignments,node)
                        min_conflicted = len(c0)
                        D = csp.nodeDomains[node]
                        random.shuffle(D)
                        for u in D:
                                if u == val: continue
                                assignments_cpy = copy.deepcopy(assignments)
                                assignments_cpy[node] = u
                                c,w = self.conflicted_neighbors(assignments_cpy,node)
                                if len(c) < min_conflicted:
                                        assignments = assignments_cpy 
                                        min_conflicted = len(c)
                                        w0 = w
                                elif len(c) == min_conflicted:
                                        #chooose equally conflicted node by random weighted on soft-constraint
                                        r = random.random()
                                        if r < w/(w+w0):
                                                w0=w
                                                assignments = assignments_cpy
                                        
                return False        #process failed
  