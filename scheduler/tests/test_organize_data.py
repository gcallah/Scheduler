from django.test import TestCase 
from ddt import ddt, file_data
from scheduler.organize_data import organize_courses, organize_rooms
from scheduler.models import Course, Room
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@ddt
class OrganizeDataTest(TestCase):

    def setup_courses(self, courses):
        Course.objects.all().delete()
        for key in courses: 
            Course.objects.create(cname=key, capacity=courses[key])
    
    @file_data(os.path.join(ROOT_DIR, "test_data/test_org_course_data.json"))
    def test_organize_courses(self, courses_from, all_courses, expected):
        self.setup_courses(all_courses)
        organized_courses = organize_courses(courses_from, Course.objects.all())
        self.assertEqual(organized_courses, expected)

    def setup_rooms(self, rooms):
        Room.objects.all().delete()
        for key in rooms:
            Room.objects.create(rname=key, capacity=rooms[key])

    @file_data(os.path.join(ROOT_DIR, "test_data/test_org_room_data.json"))
    def test_organize_rooms(self, all_rooms, expected): 
        self.setup_rooms(all_rooms)
        organized_rooms = organize_rooms(Room.objects.all())
        self.assertEqual(organized_rooms, expected)

