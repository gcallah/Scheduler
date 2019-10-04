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

if __name__ == '__main__':
            main()