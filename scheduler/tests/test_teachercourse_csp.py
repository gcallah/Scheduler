"""
This is the test suite for cspsolver.py.
"""
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest import TestCase, main, skip

from teachercourse_csp import pref_handler, assign_days_for_course, maps_day_to_class, hours_for_prof, profs_for_courses, add_nodes, assigner, compute_course_start_end
from cspsolver import CSP, minConflicts

def create_csp():
    csp = CSP()
    csp.add_node("class1", ["domain1"])
    return csp

def create_user_data():
    courses = ["physics"]
    professors = ['John Smith']
    rooms = ["648"]
    room_capacities = {'648': 30,}
    course_no_students = {'physics': 35}
    course_mins = {'physics': 60}
    course_no_sections = {'physics': 2}
    course_days_weekly = {'physics': 3}
    prof_info = {'John Smith': {'courses': ['physics', 'chemistry'],'start_time': 8,'end_time': 17}}
    user_data = professors, prof_info, rooms, room_capacities, courses, \
                    course_no_students, course_mins, course_days_weekly
    return user_data

class Teachercourse_Csp_TestCase(TestCase):
    def setUp(self):
        self.csp = CSP()
        self.room_chosen = {}
        self.assigner = assigner(user_data=create_user_data())

    def tearDown(self):
        self.csp = None

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
        self.assertTrue(result1[0] in ["mon", "tues","wed", "thur", "fri"])
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
        duration = {"physics" : 30}
        course = "physics"
        result = compute_course_start_end(hour, min, duration, course)
        self.assertTrue(len(result) == 2)
        self.assertEqual(result, (5*6, 5*6+30))
        min = 50
        result = compute_course_start_end(hour, min, duration, course)
        self.assertEqual(result, (5*6+5, 5*6+5+30))