"""
This is the test suite for cspsolver.py.
"""
import os, sys
import collections

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest import TestCase, main, skip

from teachercourse_csp import pref_handler, assign_days_for_course, maps_day_to_class, hours_for_prof, profs_for_courses, add_nodes, assigner, compute_course_start_end, add_unary_constraint, add_binary_constraint
from cspsolver import CSP


def create_csp():
    csp = CSP()
    csp.add_node(("physics", "John Smith"), [("648", (5, 60), "physics")])
    return csp

def create_user_data1():
    rooms = ['655', '666', '745a', '745b', '433', '201', '115a', '115b']
    room_capacities = {
        '655': 30,
        '666': 30,
        '745a': 22,
        '745b': 40,
        '433': 31,
        '201': 28,
        '115a': 35,
        '115b': 40
    }

    # Course details
    courses = ['physics', 'chemistry', 'biochemistry', 'biology 1', 'biology 2',
               'molecular biology', 'calculus 1', 'calculus 4', 'astrophysics']
    course_no_students = {
        'physics': 35,
        'chemistry': 26,
        'biochemistry': 22,
        'molecular biology': 20,
        'biology 1': 38,
        'biology 2': 25,
        'calculus 1': 34,
        'calculus 4': 21,
        'astrophysics': 15,
    }
    course_mins = {
        'physics': 60,
        'chemistry': 90,
        'biochemistry': 90,
        'biology 1': 90,
        'biology 2': 60,
        'molecular biology': 60,
        'calculus 1': 60,
        'calculus 4': 60,
        'astrophysics': 60
    }

    course_no_sections = {
        'physics': 2,
        'chemistry': 2,
        'biochemistry': 1,
        'biology 1': 2,
        'biology 2': 1,
        'molecular biology': 1,
        'calculus 1': 2,
        'calculus 4': 1,
        'astrophysics': 1
    }

    course_days_weekly = {
        'physics': 3,
        'chemistry': 2,
        'biochemistry': 2,
        'biology 1': 2,
        'biology 2': 3,
        'molecular biology': 1,
        'calculus 1': 3,
        'calculus 4': 2,
        'astrophysics': 1
    }

    # Info about professors
    professors = ['John Smith', 'Lisa Jones', 'Mike Williams',
                  'Tim Simpson', 'Rachel Smith', 'Gregg Woods',
                  'Simon Valinski', 'Chu Yen', 'Peter Parker',
                  'Lisa Mullen', 'Elizabeth Walker', 'Brian K. Dickson',
                  'Jamir Abdullah']
    prof_info = {
        'John Smith': {
            'courses': ['physics', 'chemistry'],
            'start_time': 8,
            'end_time': 17
        },
        'Lisa Jones': {
            'courses': ['physics'],
            'start_time': 9,
            'end_time': 18
        },
        'Mike Williams': {
            'courses': ['biology 1'],
            'start_time': 9,
            'end_time': 15
        },
        'Tim Simpson': {
            'courses': ['calculus 1', 'calculus 4'],
            'start_time': 9,
            'end_time': 18
        },
        'Rachel Smith': {
            'courses': ['calculus 4', 'biology 2'],
            'start_time': 9,
            'end_time': 18
        },
        'Gregg Woods': {
            'courses': ['chemistry', 'biochemistry'],
            'start_time': 8,
            'end_time': 17
        },
        'Simon Valinski': {
            'courses': ['calculus 1', 'physics', 'astrophysics'],
            'start_time': 8,
            'end_time': 17
        },
        'Chu Yen': {
            'courses': ['calculus 1', 'calculus 4',
                        'physics', 'astrophysics'],
            'start_time': 10,
            'end_time': 18
        },
        'Peter Parker': {
            'courses': ['biology 1', 'biology 2', 'biochemistry',
                        'chemistry', 'molecular biology'],
            'start_time': 8,
            'end_time': 14
        },
        'Lisa Mullen': {
            'courses': ['calculus 1', 'calculus 4'],
            'start_time': 9,
            'end_time': 13
        },
        'Elizabeth Walker': {
            'courses': ['calculus 1', 'calculus 4'],
            'start_time': 9,
            'end_time': 18
        },
        'Brian K. Dickson': {
            'courses': ['calculus 4', 'physics'],
            'start_time': 9,
            'end_time': 18
        },
        'Jamir Abdullah': {
            'courses': ['chemistry', 'calculus 4'],
            'start_time': 10,
            'end_time': 18
        }
    }
    user_data = professors, prof_info, rooms, room_capacities, courses, \
                course_no_students, course_mins, course_days_weekly
    return user_data


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
                course_no_students, course_mins, course_days_weekly
    return user_data


class Teachercourse_Csp_TestCase(TestCase):
    def setUp(self):
        self.csp = create_csp()
        self.data = create_user_data()

    def tearDown(self):
        self.csp = None
        self.data = None

    def room_has_capacity(self, val, course):
        room = val[0]
        hour_and_min = val[1]
        no_students = self.data[5][course]
        return self.data[3][room] >= no_students

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

    def test_pref_handler(self):
        self.assertRaises(ValueError, lambda: pref_handler("sun"))
        result = pref_handler("tues")
        self.assertEqual(result, ["mon", "wed", "thur", "fri"])
        result = pref_handler("mon")
        self.assertFalse("mon" in result)
        self.assertEqual(result, ["wed"] + ["tues", "wed", "thur", "fri"])
        result = pref_handler("fri")
        self.assertFalse("fri" in result)
        self.assertEqual(result, ["thur"] + ["mon", "tues", "wed", "thur"])

    def test_assign_days_for_course(self):
        result1 = assign_days_for_course(1)
        self.assertEqual(len(result1), 1)
        self.assertTrue(result1[0] in ["mon", "tues", "wed", "thur", "fri"])
        result2 = assign_days_for_course(2)
        self.assertEqual(len(result2), 2)
        result3 = assign_days_for_course(3)
        self.assertEqual(len(result3), 3)
        result4 = assign_days_for_course(4)
        self.assertEqual(len(result4), 4)
        result5 = assign_days_for_course(5)
        self.assertEqual(len(result5), 5)
        self.assertEqual(result5, ["mon", "tues", "wed", "thur", "fri"])

    def test_maps_day_to_class(self):
        course = ["physics", "chemistry", "japanese"]
        course_days = {"physics": 3, "chemistry": 1, "japanese": 5}
        result = maps_day_to_class(course_days, course)
        count_physics = 0
        count_chemistry = 0
        count_japanese = 0
        for key in result.keys():
            if "physics" in result[key]:
                count_physics += 1
            if "chemistry" in result[key]:
                count_chemistry += 1
            if "japanese" in result[key]:
                count_japanese += 1
        self.assertEqual(count_japanese, 5)
        self.assertEqual(count_chemistry, 1)
        self.assertEqual(count_physics, 3)

    def test_hours_for_prof(self):
        prof_info = {'John Smith': {'courses': ['physics', 'chemistry'], 'start_time': 17, 'end_time': 17}}
        prof = "John Smith"
        self.assertEqual(hours_for_prof(prof_info, prof), set())
        prof_info[prof]["start_time"] = 16
        self.assertFalse(len(hours_for_prof(prof_info, prof)) > 2)
        self.assertEqual(len(hours_for_prof(prof_info, prof)), 2)
        prof_info[prof]["start_time"] = 15
        self.assertFalse(len(hours_for_prof(prof_info, prof)) > 4)
        self.assertEqual(len(hours_for_prof(prof_info, prof)), 4)
        prof_info[prof]["start_time"] = 8
        self.assertFalse(len(hours_for_prof(prof_info, prof)) > 18)
        self.assertEqual(len(hours_for_prof(prof_info, prof)), 18)

    def test_profs_for_course(self):
        prof_info = {'John Smith': {'courses': [], 'start_time': 15, 'end_time': 17}}
        courses = ["physics", "chemistry"]
        profs = ['John Smith']
        self.assertEqual(profs_for_courses(courses, profs, prof_info), {})
        prof_info["John Smith"]["courses"].append("physics")
        self.assertFalse("chemistry" in profs_for_courses(courses, profs, prof_info).keys())
        self.assertTrue("physics" in profs_for_courses(courses, profs, prof_info).keys())
        self.assertEqual(profs_for_courses(courses, profs, prof_info)["physics"], "John Smith")
        prof_info["John Smith"]["courses"].append("chemistry")
        self.assertFalse("biology" in profs_for_courses(courses, profs, prof_info).keys())
        self.assertTrue("physics" in profs_for_courses(courses, profs, prof_info).keys())
        self.assertTrue("chemistry" in profs_for_courses(courses, profs, prof_info).keys())
        self.assertEqual(profs_for_courses(courses, profs, prof_info)["physics"], "John Smith")
        self.assertEqual(profs_for_courses(courses, profs, prof_info)["chemistry"], "John Smith")
        prof_info = {'John Smith': {'courses': ["chemistry"], 'start_time': 15, 'end_time': 17},
                     'Lisa Jones': {'courses': ['physics'], 'start_time': 9, 'end_time': 18}}
        profs.append("Lisa Jones")
        self.assertFalse(profs_for_courses(courses, profs, prof_info)["physics"] == "John Smith")
        self.assertTrue(profs_for_courses(courses, profs, prof_info)["chemistry"] == "John Smith")
        self.assertFalse(profs_for_courses(courses, profs, prof_info)["chemistry"] == "Lisa Jones")
        self.assertTrue(profs_for_courses(courses, profs, prof_info)["physics"] == "Lisa Jones")

    def test_add_node(self):
        courses = ["physics", "chemistry"]
        profs = ['John Smith', "Lisa Jones"]
        prof_info = {'John Smith': {'courses': ["chemistry"], 'start_time': 16, 'end_time': 17},
                     'Lisa Jones': {'courses': ['physics'], 'start_time': 9, 'end_time': 10}}
        prof_assign = profs_for_courses(courses, profs, prof_info)
        room_chosen = {}
        rooms = ["648"]
        add_nodes(courses, rooms, room_chosen, prof_assign, prof_info, self.csp)
        nodes = []
        for i in range(len(courses)):
            nodes.append((courses[i], prof_assign[courses[i]]))
        self.assertFalse(("Bob") in self.csp.node_domains.keys())
        self.assertTrue(nodes[0] in self.csp.node_domains.keys())
        self.assertTrue(nodes[1] in self.csp.node_domains.keys())
        self.assertEqual(rooms[0], self.csp.node_domains[nodes[0]][0][0])
        self.assertEqual(rooms[0], self.csp.node_domains[nodes[1]][0][0])

    def test_compute_course_start_end(self):
        hour = 5
        min = 0
        duration = {"physics": 30}
        course = "physics"
        result = compute_course_start_end(hour, min, duration, course)
        self.assertTrue(len(result) == 2)
        self.assertEqual(result, (5 * 6, 5 * 6 + 30))
        min = 50
        result = compute_course_start_end(hour, min, duration, course)
        self.assertEqual(result, (5 * 6 + 5, 5 * 6 + 5 + 30))

    def test_add_unary(self):
        self.assertTrue(self.csp.unary_constraints == {})
        add_unary_constraint(self.csp, self.room_has_capacity)
        self.assertFalse(self.csp.unary_constraints == {})
        self.assertTrue(('physics', 'John Smith') in self.csp.unary_constraints)

    def test_binary(self):
        self.csp.add_node(("chemistry", "John Smith"), [("649", (5, 60), "chemistry")])
        self.assertTrue(self.csp.binary_constraints == {})
        course_map = {}
        add_binary_constraint(self.csp, course_map, self.no_class_overlap, self.no_time_clash)
        self.assertFalse(self.csp.binary_constraints == {})
        self.assertTrue(('physics', 'John Smith') in self.csp.binary_constraints)

    def test_assigner(self):
        user_data = create_user_data()
        solution = assigner(user_data)
        self.assertFalse(len(solution) == 0)
        self.assertEqual(type(solution), type(collections.defaultdict(lambda: None)))
        user_data = create_user_data1()
        solution = assigner(user_data)
        self.assertFalse(len(solution) == 0)
        self.assertEqual(type(solution), type(collections.defaultdict(lambda: None)))
