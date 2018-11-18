from django.test import TestCase, Client
from django.contrib.auth.models import User
from scheduler.models import Course, Room


class AlgorithmTestCase(TestCase):

    # Setup the courses and rooms
    def setUp(self):
        courses = {
            "Intro": 15,
            "DevOps": 50,
            "Algo": 100,
            "TooBig": 5000
        }

        rooms = {
            "Room1": 20,
            "Room2": 50,
            "Room3": 75,
            "Room4": 150
        }
        self.username = 'schedulerTests'
        self.password = 'valid_password'
        self.client = Client()
        self.user = User.objects.create_user(self.username,
                                             'fake@email.com',
                                             self.password)

        for key, value in courses:
            Course.objects.create(
                cname=key,
                capacity=value)

        for key, value in rooms:
            Room.objects.create(
                rname=key,
                capacity=value)
