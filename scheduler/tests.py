from django.test import TestCase, Client
from django.contrib.auth.models import User
from scheduler.models import Course, Room
from scheduler.schedule import make_schedule, get_unscheduled_course


class AlgorithmTestCase(TestCase):

    # Setup the courses and rooms
    def setUp(self):
        courses = {
            "Course15": 15,
            "Course50": 50,
            "Course100": 100,
            "Course5000": 5000
        }

        rooms = {
            "Room20": 20,
            "Room50": 50,
            "Room75": 75,
            "Room150": 150
        }
        self.username = 'schedulerTests'
        self.password = 'valid_password'
        self.client = Client()
        self.user = User.objects.create_user(self.username,
                                             'fake@email.com',
                                             self.password)

        for key in courses.keys():
            Course.objects.create(
                cname=key,
                capacity=courses[key])

        for key in rooms:
            Room.objects.create(
                rname=key,
                capacity=rooms[key])

    def test_course_with_no_room_available(self):
        all_courses = Course.objects.all()
        all_rooms = Room.objects.all()
        all_courses_list = list(all_courses)

        returned_scheduled = make_schedule(all_courses, all_rooms, all_courses_list)
        returned_unscheduled = get_unscheduled_course(
           all_courses, returned_scheduled, all_courses_list)

        self.assertEqual(len(returned_unscheduled), 1)

    def test_courses_with_rooms_available_scheduled(self):
        all_courses = Course.objects.filter(capacity__lt=150)
        all_rooms = Room.objects.all()
        all_courses_list = list(all_courses)

        returned_unscheduled = make_schedule(
            all_courses, all_rooms, all_courses_list)

        self.assertEqual(len(returned_unscheduled), all_courses.count())

    def test_course_and_room_with_same_capacity(self):
        course50 = Course.objects.filter(capacity=50)
        room50 = Room.objects.filter(capacity=50)
        course50_list = list(course50)

        returned_schedule = make_schedule(course50, room50, course50_list)

        self.assertEqual(len(returned_schedule), 1)
