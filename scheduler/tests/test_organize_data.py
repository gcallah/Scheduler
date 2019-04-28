from django.test import TestCase 
from ddt import ddt, file_data
from scheduler.organize_data import organize_courses, organize_rooms, organize_course_time, organize_room_time, organize_timeslots
from scheduler.models import Course, Room, Time, Day
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

    def setup_time_and_day(self, times, days): 
        Time.objects.all().delete()
        Day.objects.all().delete()
        for time in times:
            Time.objects.create(times=time)
        for day in days:
            Day.objects.create(days=day)

    @file_data(os.path.join(ROOT_DIR, "test_data/test_org_ctime_data.json"))
    def test_organize_course_time(self, times_list, days_list, duration, expected): 
        self.setup_time_and_day(times_list, days_list)
        day_times_list = organize_course_time(Time.objects.all(), Day.objects.all(), duration)
        self.assertEqual(day_times_list, expected)

    @file_data(os.path.join(ROOT_DIR, "test_data/test_org_rtime_data.json"))
    def test_organize_room_time(self, times_list, days_list, expected): 
        self.setup_time_and_day(times_list, days_list)
        day_time_dict = organize_room_time(Time.objects.all(), Day.objects.all())
        self.assertEqual(day_time_dict, expected)

    @file_data(os.path.join(ROOT_DIR, "test_data/test_org_timeslots_data.json"))
    def test_organize_timeslots(self, times, expected): 
        timeslots = organize_timeslots(times)
        self.assertEqual(timeslots, expected)



