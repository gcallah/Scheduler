from django.test import TestCase, Client
from django.contrib.auth.models import User
from scheduler.models import Course, Room
from scheduler.views import make_schedule, get_unscheduled_course


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

# Lines commented out for flake8 compliance (unused local variable errors)
#        returned_schedule = make_schedule(all_courses, all_rooms, all_courses)
        returned_unscheduled = get_unscheduled_course(
#            all_courses, returned_scheduled, all_courses)

        self.assertEqual(returned_unscheduled.size(), 1)

    def test_courses_with_rooms_available_scheduled(self):
        all_courses = Course.objects.filter(capacity < 150)
        all_rooms = Room.objects.all()

        returned_unscheduled = make_schedule(
            all_courses, all_rooms, all_courses)

        assertEqual(returned_unscheduled.size(), all_courses.size())

    def test_course_and_room_with_same_capacity(self):
        course50 = Course.objects.filter(capacity=50)
        room50 = Room.objects.filter(capacity=50)

        returned_schedule=make_schedule(course50, room50, course50)

        assertEqual(returned_schedule.size(), 1)
