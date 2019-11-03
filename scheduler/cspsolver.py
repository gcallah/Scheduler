import copy
import random

"""
classes CSP and minConflicts below define
& solve a constraint satisfaction problem
"""


class CSP(object):
    def __init__(self):
        """Constraint Satisfaction Problem class.

        Attributes:
            nodes {list} -- A list of nodes (course, professor).
            node_domains {dict} -- Maps each node to its domain (rooms, hours).
            unary_constraints {dict} -- Maps each node to its
                                        unary constraints
            binary_constraints {dict} -- Maps each node to its
                                         binary constraints
        """
        self.nodes = []
        self.node_domains = {}
        self.unary_constraints = {}
        self.binary_constraints = {}

    def add_node(self, node, domain):
        """Adds a node and its list of domains (rooms, hours) to the node domains.

        Arguments:
            node {tuple} -- A tuple of (course, professor).
            domain {list} -- A list of domains (rooms, hours) for the node.
        """
        if node not in self.nodes: 
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
        node_domain = self.node_domains[node]
        factor = {domain: constraint_func(domain) for domain in node_domain}
        if node not in self.unary_constraints:
            self.unary_constraints[node] = factor
        else:
            self.unary_constraints[node] = ({val: self.unary_constraints[node][val]
                                            * factor[val] for val in node_domain})

    def add_binary_constraint(self, node1, node2, constraint_func):
        """Adds a binary constraint to two existing nodes.

        Arguments:
            node1 {tuple} -- A tuple of (course, professor).
            node2 {tuple} -- A tuple of (course, professor).
            constraint_func {function} -- A constraint function.

        Raises:
            ValueError: Raises ValueError if either node has not been added yet
        """
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
            self.binary_constraints[node_a] = {node_b:table_factor}
        elif node_b not in self.binary_constraints[node_a].keys():
            self.binary_constraints[node_a][node_b] = table_factor
        else:
            current_table = self.binary_constraints[node_a][node_b]
            for i in table_factor:
                for j in table_factor[i]:
                    assert i in current_table and j in current_table[i]
                    current_table[i][j] *= table_factor[i][j]


class minConflicts(object):
    def __init__(self, csp):
        self.csp = csp

    def initial_var_assignment(self):
        """Assigns each node a random domain value.

        Returns:
            dict -- Random domain assignment of each node.
        """
        return {node:random.choice(self.csp.node_domains[node]) for node in self.csp.nodes}

    def conflicted(self, assignments):
        """Finds a set of conflicted nodes (which evaluate to zero).

        Arguments:
            assignments {dict} -- Random domain assignment of each node.

        Returns:
            set -- A set of conflicted nodes.
        """
        conflicted = set()
        for node in assignments:
            if node in conflicted:
                continue
            assigned_domain = assignments[node]
            if self.csp.unary_constraints[node][assigned_domain] == 0:
                conflicted.add(node)
            if node in self.csp.binary_constraints: 
                neighbors = set(self.csp.binary_constraints[node].keys())
                for neighbor in neighbors:
                    val_neigh = assignments[neighbor]
                    if self.csp.binary_constraints[node][neighbor][assigned_domain][val_neigh] == 0:
                        conflicted.add(node)
                        conflicted.add(neighbor)
        return conflicted

    def conflicted_neighbors(self, assignments, node):
        """Returns a list of neighbors that conflict with the node.

        Arguments:
            assignments {dict} -- Random domain assignment of each node.
            node {tuple} -- A tuple of (course, professor).

        Returns:
            list -- A list of neighbors that conflict with the node.
        """
        conflicted = set()
        domain = assignments[node]
        soft_weight = 1
        # proportional to number of soft-constraints satisfied
        # checks for missing keys on unary constraints
        if self.csp.unary_constraints[node][domain] == 0:
            conflicted.add(node)
        if node in self.csp.binary_constraints: 
            neighbors = self.csp.binary_constraints[node].keys()
            for neigh in neighbors:
                neigh_domain = assignments[neigh]
                weight = self.csp.binary_constraints[node][neigh][domain][neigh_domain]
                if weight == 0:
                    conflicted.add(node) 
                    conflicted.add(neigh)
                else:
                    soft_weight *= weight
        return (conflicted, soft_weight)

    def rand_conflict_var(self, conflicted, assignments):
        """Chooses a random conflicted variable.

        Arguments:
            conflicted {set} -- A set of conflicted nodes.
            assignments {dict} -- Random domain assignment of each node.

        Returns:
            tuple -- A tuple of (rooms, hours), assigned values, and node.
        """
        node = random.choice(tuple(conflicted))
        val = assignments[node]
        domain = self.csp.node_domains[node]
        random.shuffle(domain)
        return domain, val, node

    def solve(self, max_iters=100):
        """Attempts to map node to its domain
        in a manner that satisfies the constraints.

        Keyword Arguments:
            max_iters {int} -- Max number of trials allowed (default: {100}).

        Returns:
             dict -- Final domain assignment of each node.
        """
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