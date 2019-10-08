"""
This is the test suite for cspsolver.py.
"""

from unittest import TestCase, main, skip

from cspsolver import CSP, minConflicts


def create_csp():
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

    def test_add(self):
        """
        Test if add node to CSP work.
        """
        self.csp.add_node("class1", "domain1")
        self.assertTrue(len(self.csp.nodes) == 1)
        old_len = len(self.csp.nodes)
        self.assertFalse(self.csp.add_node("class1", "domain1"))
        self.assertTrue(old_len == len(self.csp.nodes))
        self.assertTrue(self.csp.nodeDomains["class1"] == "domain1")


class MinConflicts_TestCase(TestCase):
    def setUp(self):
        csp = create_csp()
        self.minC = minConflicts(csp)

    def tearDown(self):
        self.minC.csp = None
        self.minC = None

    def test_assigner(self):
        self.assertTrue(self.minC.initial_var_assignment()["class1"] == "domain1")
        self.assertTrue(self.minC.initial_var_assignment()["class2"] in ["domain2", "domain3", "domain4"])
        self.assertFalse(self.minC.initial_var_assignment()["class3"] == "domain10")


if __name__ == '__main__':
    main()
