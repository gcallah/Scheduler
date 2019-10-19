"""
This is the test suite for cspsolver.py.
"""
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest import TestCase, main, skip

from teachercourse_csp import assigner
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


