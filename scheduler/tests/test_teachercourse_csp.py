"""
This is the test suite for cspsolver.py.
"""
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest import TestCase, main, skip

from teachercourse_csp import pref_handler, assign_days_for_course, maps_day_to_class, hours_for_prof, profs_for_courses, add_nodes, assigner
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
