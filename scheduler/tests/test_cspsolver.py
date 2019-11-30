"""
This is the test suite for cspsolver.py.
"""
import os, sys, random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest import TestCase, main, skip
from cspsolver import CSP, minConflicts


def create_csp1():
    csp = CSP()
    csp.add_node(("physics", "John Smith"), [("648", (5, 60), "physics")])
    return csp


def create_csp2():
    csp = CSP()
    csp.add_node("class1", ["domain1"])
    csp.add_node("class2", ["domain2", "domain3", "domain4"])
    csp.add_node("class3", ["domain5", "domain6"])
    return csp


def create_user_data():
    courses = ["physics", "chemistry"]
    professors = ['John Smith', 'Lisa Jones', 'Mike Williams']
    rooms = ["648", "649"]
    room_capacities = {'648': 30, '649': 40}
    course_no_students = {'physics': 35, 'chemistry': 26}
    course_mins = {'physics': 60, 'chemistry': 90}
    course_no_sections = {'physics': 2, 'chemistry': 2}
    course_days_weekly = {'physics': 3, 'chemistry': 2}
    prof_info = {'John Smith': {'courses': ['physics', 'chemistry'], 'start_time': 8, 'end_time': 17},
                 'Lisa Jones': {'courses': ['physics'], 'start_time': 9, 'end_time': 18},
                 'Mike Williams': {'courses': ['biology 1'], 'start_time': 9, 'end_time': 15}}
    user_data = professors, prof_info, rooms, room_capacities, courses, \
                course_no_students, course_no_sections, course_mins, course_days_weekly
    return user_data


class CspTestCase(TestCase):
    def setUp(self):
        self.csp = create_csp1()
        self.data = create_user_data()

    def tearDown(self):
        self.csp = None

    def test_nodes(self):
        self.assertEqual(self.csp.nodes[0], ("physics", "John Smith"))
        self.assertEqual(self.csp.node_domains[("physics", "John Smith")], [("648", (5, 60), "physics")])

    def test_add(self):
        """
        Test if add node to CSP work.
        """
        self.assertFalse(self.csp.add_node(("physics", "John Smith"), [("648", (5, 60), "physics")]))
        self.assertFalse(self.csp.add_node(("physics", "John Smith"), ["domain2"]))
        self.assertEqual(len(self.csp.nodes), 1)
        self.csp.add_node("class2", ["domain2"])
        self.assertEqual(len(self.csp.nodes), 2)

    def room_has_capacity(self, val, course):
        """
            Constraint function for unary
        """
        room = val[0]
        no_students = self.data[5][course]
        return bool(self.data[3][room] >= no_students)

    def test_unary_constraint(self):
        """
            Test unary constraint function
        """
        result = self.room_has_capacity(("648", (5, 60)), "physics")
        self.assertFalse(result)
        result = self.room_has_capacity(("649", (5, 60)), "physics")
        self.assertTrue(result)

    def test_add_unary_constraint(self):
        """
        Test if add unary constraint work.
        """
        self.assertRaises(ValueError, lambda: self.csp.add_unary_constraint
        ("class2", constraint_func=1))
        node = ("physics", "John Smith")
        domain = self.csp.node_domains[node]
        course = node[0]
        factor = {val: self.room_has_capacity(val, course) for val in domain}
        self.csp.add_unary_constraint(node, self.room_has_capacity)
        constraint = self.csp.unary_constraints[node]
        self.assertEqual(constraint, factor)
        self.csp.add_unary_constraint(node, self.room_has_capacity)
        constraint = self.csp.unary_constraints[node]
        factor = {val: self.csp.unary_constraints[node][val] * factor[val] for val in domain}
        self.assertEqual(constraint, factor)

    def no_class_overlap(self, val1, val2, course1, course2):
        """
            Class constraint function for binary
        """
        course_min = self.data[5]
        hours1, mins1 = val1[1]
        hours2, mins2 = val2[1]
        course_start1 = hours1 * 6 + mins1 // 10
        course_end1 = course_start1 + \
                      course_min[course1] // 10
        course_start2 = hours2 * 6 + mins2 // 10
        course_end2 = course_start2 + \
                      course_min[course2] // 10
        # conditions to check if one class starts during other
        if course_start1 <= course_start2 < course_end1:
            return bool(False)
        if course_start2 <= course_start1 < course_end2:
            return bool(False)
        # soft constraint: non-sequential classes
        # get higher weight
        if course_start1 == course_end2 or course_start2 == course_end1:
            return 2
        return bool(True)

    def test_binary_class(self):
        """
        Test if binary constraint of class work.
        """
        val1 = ["648", (5, 60), "physics"]
        val2 = ["648", (5, 60), "chemistry"]
        self.assertFalse(self.no_class_overlap(val1, val2, val1[2], val2[2]))
        val1[1] = (6, 10)
        self.assertFalse(self.no_class_overlap(val1, val2, val1[2], val2[2]))
        val1[1] = (6, 60)
        self.assertTrue(self.no_class_overlap(val1, val2, val1[2], val2[2]))
        val1[1] = (6, 20)
        self.assertEqual(2, self.no_class_overlap(val1, val2, val1[2], val2[2]))

    def no_time_clash(self, val1, val2, course, dummy):
        """
            Class constraint function for binary
        """
        course_min = self.data[5]
        room1, time1 = val1[0], val1[1]
        room2, time2 = val2[0], val2[1]
        if room1 != room2:
            return bool(True)
        hours1, mins1 = time1
        hours2, mins2 = time2
        start_time1 = hours1 * 6 + mins1 // 10
        end_time1 = start_time1 + course_min[course] // 10
        start_time2 = hours2 * 6 + mins2 // 10
        if start_time1 <= start_time2 < end_time1:
            return bool(False)
        return bool(True)

    def test_binary_time(self):
        """
        Test if binary constraint of time work.
        """
        val1 = ["648", (5, 60), "physics"]
        val2 = ["649", (5, 60), "physics"]
        self.assertTrue(self.no_time_clash(val1, val2, val1[2], val2[2]))
        val1[0] = "649"
        self.assertFalse(self.no_time_clash(val1, val2, val1[2], val2[2]))
        val2[1] = (3, 60)
        self.assertTrue(self.no_time_clash(val1, val2, val1[2], val2[2]))

    def test_update_binary_constraint(self):
        self.csp.add_node(("chemistry", "John Smith"), [("649", (5, 60), "chemistry")])
        node1 = ("physics", "John Smith")
        node2 = ("chemistry", "John Smith")
        node3 = ("physics", "Lisa Jones")
        factor1 = {"factor1": {"factor2": True}}
        factor2 = {"factor3": {"factor4": True}}
        binary_constraint = self.csp.binary_constraints
        self.assertEqual(binary_constraint, {})
        self.csp.update_binary_constraint_table(node1, node2, factor1)
        self.assertEqual(binary_constraint[node1], {node2: factor1})
        self.csp.update_binary_constraint_table(node1, node3, factor2)
        self.assertEqual(binary_constraint[node1], {node2: factor1, node3: factor2})
        self.csp.update_binary_constraint_table(node1, node2, factor1)
        self.assertEqual(binary_constraint[node1][node2], {"factor1": {"factor2": 1}})
        self.assertEqual(binary_constraint[node1][node3], factor2)

    def test_add_binary_constraint(self):
        """
        Test if add binary constraint work.
        """
        self.assertRaises(ValueError, lambda: self.csp.add_binary_constraint
        ("class2", "class1", constraint_func=1))
        self.csp.add_node(("chemistry", "John Smith"), [("649", (5, 60), "chemistry")])
        node1 = ("physics", "John Smith")
        node2 = ("chemistry", "John Smith")
        course1 = node1[0]
        course2 = node2[0]
        domain1 = self.csp.node_domains[node1]
        domain2 = self.csp.node_domains[node2]
        factor1 = {val1: {val2: self.no_time_clash(val1, val2, course1, course2) for val2 in domain2} for val1 in
                   domain1}
        factor2 = {val2: {val1: self.no_time_clash(val1, val2, course1, course2) for val1 in domain1} for val2 in
                   domain2}
        self.csp.add_binary_constraint(node1, node2, self.no_time_clash)
        binary_constraint = self.csp.binary_constraints
        self.assertEqual(binary_constraint[node1][node2], factor1)
        self.assertEqual(binary_constraint[node2][node1], factor2)


class MinConflictsTestCase(TestCase):
    def setUp(self):
        csp = create_csp2()
        self.minC = minConflicts(csp)

    def tearDown(self):
        self.minC.csp = None
        self.minC = None

    def test_initial_var_assign(self):
        assignment = self.minC.initial_var_assignment()
        self.assertTrue(assignment["class1"] == "domain1")
        self.assertTrue(assignment["class2"] in ["domain2", "domain3", "domain4"])
        self.assertFalse(assignment["class3"] == "domain10")

    def test_conflicted(self):
        self.minC.csp.node_domains['class2'] = ['domain2']
        self.minC.csp.node_domains['class3'] = ['domain3']
        assignment = self.minC.initial_var_assignment()
        conflict = self.minC.conflicted(assignment)
        self.assertEqual(conflict, set())
        self.minC.csp.unary_constraints = {"class1": {"domain1": 0}, 'class2': {}, 'class3': {}}
        conflict = self.minC.conflicted(assignment)
        self.assertTrue('class1' in conflict)
        self.minC.csp.unary_constraints['class2'] = {"domain2": 0}
        conflict = self.minC.conflicted(assignment)
        self.assertTrue('class2' in conflict)
        self.assertFalse('class3' in conflict)
        self.minC.csp.unary_constraints['class2'] = {"domain2": 1}
        conflict = self.minC.conflicted(assignment)
        self.assertFalse('class2' in conflict)
        self.minC.csp.binary_constraints = {'class3': {'class2': {'domain3': {'domain2': 0}}}}
        conflict = self.minC.conflicted(assignment)
        self.assertTrue('class2' in conflict)
        self.assertTrue('class3' in conflict)
        self.minC.csp.binary_constraints['class3'] = {'class1': {'domain3': {'domain1': 0}}}
        conflict = self.minC.conflicted(assignment)
        self.assertFalse('class2' in conflict)
        self.assertTrue('class3' in conflict)
        self.minC.csp.binary_constraints['class3']['class1']['domain3']['domain1'] = 1
        conflict = self.minC.conflicted(assignment)
        self.assertFalse('class3' in conflict)

    def test_conflicted_neighbors(self):
        self.minC.csp.node_domains['class2'] = ['domain2']
        self.minC.csp.node_domains['class3'] = ['domain3']
        assignment = self.minC.initial_var_assignment()
        self.assertRaises(KeyError, lambda: self.minC.conflicted_neighbors(assignment, "class1"))
        self.minC.csp.unary_constraints = {"class1": {"domain1": 0}, 'class2': {'domain2': 1}, 'class3': {"domain3": 1}}
        conflict = self.minC.conflicted_neighbors(assignment, "class1")
        self.assertTrue('class1' in conflict[0])
        self.assertEqual(conflict[1], 1)
        conflict = self.minC.conflicted_neighbors(assignment, "class2")
        self.assertFalse('class2' in conflict[0])
        self.assertEqual(conflict[0], set())
        self.minC.csp.binary_constraints = {'class3': {'class2': {'domain1': {'domain2': 0}}}}
        self.assertRaises(KeyError, lambda: self.minC.conflicted_neighbors(assignment, "class3"))
        self.minC.csp.binary_constraints['class3']['class2'] = {'domain3': {'domain1': 0}}
        self.assertRaises(KeyError, lambda: self.minC.conflicted_neighbors(assignment, "class3"))
        self.minC.csp.binary_constraints['class3']['class2'] = {'domain3': {'domain2': 0}}
        conflict = self.minC.conflicted_neighbors(assignment, "class3")
        self.assertFalse('class1' in conflict[0])
        self.assertTrue('class2' in conflict[0])
        self.assertTrue('class3' in conflict[0])
        self.assertEqual(conflict[1], 1)
        self.minC.csp.binary_constraints['class3']['class2']['domain3']['domain2'] = 2
        conflict = self.minC.conflicted_neighbors(assignment, "class3")
        self.assertEqual(conflict[1], 2)

    def test_rand_conflict_var(self):
        self.minC.csp.node_domains['class2'] = ['domain2']
        self.minC.csp.node_domains['class3'] = ['domain3']
        self.minC.csp.unary_constraints = {"class1": {"domain1": 0}, 'class2': {'domain2': 1}, 'class3': {"domain3": 1}}
        assignment = self.minC.initial_var_assignment()
        conflict = self.minC.conflicted(assignment)
        result = self.minC.rand_conflict_var(conflict, assignment)
        self.assertFalse(result[2] == 'class3')
        self.assertTrue(result[2] in conflict)
        self.assertTrue(result[1] in result[0])
        self.minC.csp.binary_constraints = {'class3': {'class2': {'domain3': {'domain2': 0}}}}
        assignment = self.minC.initial_var_assignment()
        conflict = self.minC.conflicted(assignment)
        result = self.minC.rand_conflict_var(conflict, assignment)
        self.assertTrue(result[2] in conflict)
        self.assertTrue(result[1] in result[0])


    def test_solve(self):
        result = self.minC.solve(100)
        self.assertEqual(result["class1"], "domain1")
        self.assertTrue(result["class2"] in ["domain2", "domain3", "domain4"])
        self.assertNotEqual(result["class3"], "domin5")


if __name__ == '__main__':
    main()
