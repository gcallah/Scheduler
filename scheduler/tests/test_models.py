from django.test import TestCase
from scheduler.models import Room, Course, Time, Day
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

@ddt
class TimeTest(TestCase):

    def create_time(self, times):
        return Time.objects.create(times=times)
    
    @file_data(os.path.join(ROOT_DIR, "test_data/test_time_data.json"))
    def test_time_creation(self, times, expected_times):
        t = self.create_time(times)
        self.assertTrue(isinstance(t, Time))
        self.assertEqual(t.__str__(), expected_times)

@ddt
class DayTest(TestCase):

    def create_day(self, days):
        return Day.objects.create(days=days)

    @file_data(os.path.join(ROOT_DIR, "test_data/test_day_data.json"))
    def test_day_creation(self, days, expected_days):
        d = self.create_day(days)
        self.assertTrue(isinstance(d, Day))
        self.assertEqual(d.__str__(), expected_days)
    
    def test_day_default_creation(self):
        day = Day.objects.create()
        self.assertTrue(isinstance(day, Day))
        self.assertEqual(day.__str__(), "Monday")

