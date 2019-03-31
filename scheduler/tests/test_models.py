from django.test import TestCase
from scheduler.models import Room, Course
from ddt import ddt, file_data
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@ddt
class RoomTest(TestCase):
    
    def create_room(self, rname, capacity): 
        return Room.objects.create(rname=rname, capacity=capacity)

    @file_data(os.path.join(ROOT_DIR, "test_data/test_room_data.json"))
    def test_room_creation(self, rname, capacity, expected_rname, expected_capacity): 
        r = self.create_room(rname, capacity)
        self.assertTrue(isinstance(r, Room))
        self.assertEqual(r.__str__(), expected_rname)
        self.assertEqual(r.capacity, expected_capacity)

@ddt
class CourseTest(TestCase): 
    
    def create_course(self, cname):
        return Course.objects.create(cname=cname)

    @file_data(os.path.join(ROOT_DIR, "test_data/test_course_data.json"))
    def test_course_creation(self, cname, expected_cname):
        c = self.create_course(cname)
        self.assertTrue(isinstance(c, Course))
        self.assertEqual(c.__str__(), expected_cname)
