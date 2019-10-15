"""
This is the test suite for cspsolver.py.
"""
import sys 
sys.path.append('..')

from unittest import TestCase, main, skip
from cspsolver import CSP, minConflicts


def create_csp1():
    csp = CSP()
    csp.add_node("class1", ["domain1"])
    return csp


def create_csp2():
    csp = CSP()
    csp.add_node("class1", ["domain1"])
    csp.add_node("class2", ["domain2", "domain3", "domain4"])
    csp.add_node("class3", ["domain5", "domain6"])
    return csp


class CSP_TestCase(TestCase):
    def setUp(self):
        self.csp = CSP()

    def tearDown(self):
        self.csp = None

    def test_nodes(self):
        self.csp = create_csp1()
        self.assertEqual(self.csp.nodes[0], "class1")
        self.assertEqual(self.csp.node_domains["class1"][0], "domain1")

    def test_add(self):
        """
        Test if add node to CSP work.
        """
        self.assertFalse(self.csp.add_node("class1", ["domain1"]))
        self.assertFalse(self.csp.add_node("class1", ["domain2"]))
        self.assertEqual(len(self.csp.nodes), 1)
        self.csp.add_node("class2", ["domain2"])
        self.assertEqual(len(self.csp.nodes), 2)

    def test_add_unary_constraint(self):
        """
        Test if add unary constraint work.
        """
        self.assertFalse(self.csp.add_unary_constraint("class2", constraint_func="1"))


class MinConflicts_TestCase(TestCase):
    def setUp(self):
        csp = create_csp2()
        self.minC = minConflicts(csp)

    def tearDown(self):
        self.minC.csp = None
        self.minC = None

    def test_assigner(self):
        assignment = self.minC.initial_var_assignment()
        self.assertTrue(assignment["class1"] == "domain1")
        self.assertTrue(assignment["class2"] in ["domain2", "domain3", "domain4"])
        self.assertFalse(assignment["class3"] == "domain10")

    def test_solve(self):
        result = self.minC.solve(100)
        self.assertEqual(result["class1"], "domain1")
        self.assertTrue(result["class2"] in ["domain2", "domain3", "domain4"])
        self.assertNotEqual(result["class3"], "domin5")

if __name__ == '__main__':
    main()
