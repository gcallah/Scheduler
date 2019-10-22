import copy
import random

"""
classes CSP and minConflicts below define
& solve a constraint satisfaction problem
"""


class CSP(object):
    def __init__(self):
        self.nodes = []
        # describes the domain of values assignable to the node
        self.node_domains = {}
        # constraints depending only on a singular node,
        # 0,1 depending on node value
        self.unary_constraints = {}
        # binary constraints depending on node pair,
        # 0,1 or 2 depending on node values
        self.binary_constraints = {}

    def add_node(self, node, domain):
        """Adds a node and its list of domains (rooms, hours) to the node domains.

        Arguments:
            node {tuple} -- A tuple of (course, professor).
            domain {list} -- A list of domains (rooms, hours) for the node.
        """
        if node in self.nodes:
            return
        self.nodes.append(node)
        self.node_domains[node] = domain

    def add_unary_constraint(self, node, constraint_func):
        """Adds an unary constraint to an existing node.

        Arguments:
            node {tuple} -- A tuple of (course, professor).
            constraint_func {function} -- A constraint function.

        Raises:
            ValueError: Raises ValueError if node has not been added yet.
        """
        if node not in self.nodes:
            raise ValueError(node, "was not added.")
        domain = self.node_domains[node]
        factor = {val: constraint_func(val) for val in domain}
        # case where no constraints existed
        if node not in self.unary_constraints.keys():
            self.unary_constraints[node] = factor
        else:
            self.unary_constraints[node] = ({val: self.unary_constraints[node][val]
                                            * factor[val] for val in domain})

    def add_binary_constraint(self, node1, node2, constraint_func):
        """Adds a binary constraint to two existing nodes.

        Arguments:
            node1 {tuple} -- A tuple of (course, professor).
            node2 {tuple} -- A tuple of (course, professor).
            constraint_func {function} -- A constraint function.

        Raises:
            ValueError: Raises ValueError if either node has not been added yet.
        """
        # make sure both nodes have been added
        if node1 not in self.nodes or node2 not in self.nodes:
            raise ValueError("{} or {} were not added.".format(node1, node2))
        domain1 = self.node_domains[node1]
        domain2 = self.node_domains[node2]
        table_factor1 = {val1: {val2: constraint_func(val1, val2)
                                for val2 in domain2} for val1 in domain1}
        table_factor2 = {val2: {val1: constraint_func(val1, val2)
                                for val1 in domain1} for val2 in domain2}
        self.update_binary_constraint_table(node1, node2, table_factor1)
        self.update_binary_constraint_table(node2, node1, table_factor2)

    def update_binary_constraint_table(self, node_a, node_b, table_factor):
        if node_a not in self.binary_constraints.keys():
            self.binary_constraints[node_a] = {}
            self.binary_constraints[node_a][node_b] = table_factor
            return
        if node_b not in self.binary_constraints[node_a].keys():
            self.binary_constraints[node_a][node_b] = table_factor
            return
        current_table = self.binary_constraints[node_a][node_b]
        for i in table_factor:
            for j in table_factor[i]:
                assert i in current_table and j in current_table[i]
                current_table[i][j] *= table_factor[i][j]


class minConflicts(object):
    def __init__(self, csp):
        self.csp = csp

    # assigns each variable a random domain value
    def initial_var_assignment(self):
        assignments = {}
        nodes = self.csp.nodes
        domains = self.csp.node_domains
        for n in nodes:
            val_rand = random.choice(domains[n])
            assignments[n] = val_rand
        return assignments

    # returns list of conflicted node assignments i.e. which evaluate to zero
    def conflicted(self, assignments):
        conflicted = []
        csp = self.csp
        for n in assignments:
            if n in conflicted:
                continue
            val = assignments[n]
            # make sure no KeyError on unary and binary constraints
            try:
                if csp.unary_constraints[n][val] == 0:
                    conflicted.append(n)
            except KeyError:
                pass
            try:
                neighbors = set(csp.binary_constraints[n].keys())
            except KeyError:
                continue
            for m in neighbors:
                val_neigh = assignments[m]
                if csp.binary_constraints[n][m][val][val_neigh] == 0:
                    conflicted += [n, m]
        return set(conflicted)

    # returns list of node neighbors that conflict with it
    def conflicted_neighbors(self, assignments, n):
        conflicted = []
        val = assignments[n]
        csp = self.csp
        soft_weight = 1
        # proportional to number of soft-constraints satisfied
        # checks for missing keys on unary constraints
        try:
            if csp.unary_constraints[n][val] == 0:
                conflicted.append(n)
        except BaseException:
            pass
        # checks on binary constraints
        try:
            neighbors = set(csp.binary_constraints[n].keys())
        except BaseException:
            return (set(conflicted), soft_weight)
        for m in neighbors:
            val_neigh = assignments[m]
            w = csp.binary_constraints[n][m][val][val_neigh]
            if w == 0:
                conflicted += [n, m]
            else:
                soft_weight *= w
        return (set(conflicted), soft_weight)

    # choose a random conflicted variable
    def rand_conflict_var(self, conflicted, assignments):
        node = random.choice(list(conflicted))
        val = assignments[node]
        domain = self.csp.node_domains[node]
        random.shuffle(domain)
        return domain, val, node

    def solve(self, max_iters=100):
        assignments = self.initial_var_assignment()
        for _ in range(max_iters):
            conflicted = self.conflicted(assignments)
            if not conflicted:
                return assignments
            domain, val, node = self.rand_conflict_var(conflicted, assignments)
            c0, w0 = self.conflicted_neighbors(assignments, node)
            min_conflicted = len(c0)
            for each_domain in domain:
                if each_domain == val:
                    continue
                assignments_cpy = copy.deepcopy(assignments)
                assignments_cpy[node] = each_domain
                conflict, w = self.conflicted_neighbors(assignments_cpy, node)
                if len(conflict) < min_conflicted:
                    assignments = assignments_cpy
                    min_conflicted = len(conflict)
                    w0 = w
                elif len(conflict) == min_conflicted:
                    # choose equally conflicted node by
                    # random weighted on soft-constraint
                    r = random.random()
                    if r < w / (w + w0):
                        w0 = w
                        assignments = assignments_cpy

        return False  # process failed
