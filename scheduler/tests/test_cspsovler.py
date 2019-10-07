"""
This is the test suite for cspsolver.py.
"""

from unittest import TestCase, main, skip

from cspsolver import CSP, minConflicts

class Cspsolve_TestCase(TestCase):
    def setUp(self):
        self.sech = CSP()

    def tearDown(self):
        self.sech = None

    def test_add(self):
        """
        Test if add node to CSP work.
        """
        self.sech.add_node("class1", "domain1")
        self.assertTrue(len(self.sech.nodes) == 1)
        old_len = len(self.sech.nodes)
        self.assertFalse(self.sech.add_node("class1","domain1"))
        self.assertTrue(old_len == len(self.sech.nodes))
        self.assertTrue(self.sech.nodeDomains["class1"] == "domain1")


class MinConflicts_TestCase(TestCase):
    def setUp(self):
        csp = CSP()
        self.minC = minConflicts(csp)

    def tearDown(self):
        self.minC.csp = None
        self.minC = None

    def test_assigner(self):
        self.minC.csp.add_node("class1", ["domain1"])
        self.minC.csp.add_node("class2", ["domain2", "domain3", "domain4"])
        self.minC.csp.add_node("class3", ["domain5", "domain6"])
        self.assertTrue(self.minC.initial_var_assignment()["class1"] == "domain1")
        self.assertTrue(self.minC.initial_var_assignment()["class2"] in ["domain2", "domain3", "domain4"])
        self.assertFalse(self.minC.initial_var_assignment()["class3"] == "domain10")


if __name__ == '__main__':
            main()