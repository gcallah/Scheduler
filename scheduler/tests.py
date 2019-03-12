import unittest, json
from schedule import sched, make_sched, get_unsched

class TestScheduler(unittest.TestCase):

    # Setup the courses and rooms
    def setUp(self):
        json_data = {
            "consumers": [{
                "name": "Algorithms",
                "type": ["rooms"],
                "attributes": [{
                    "name": "capacity",
                    "value": 60
                }]
            }, {
                "name": "Algorithms",
                "type": ["rooms"],
                "attributes": [{
                    "name": "capacity",
                    "value": 60
                }]
            }, {
                "name": "Algorithms",
                "type": ["rooms"],
                "attributes": [{
                    "name": "capacity",
                    "value": 60
                }]
            }, {
                "name": "DevOps",
                "type": ["rooms"],
                "attributes": [{
                    "name": "capacity",
                    "value": 120
                }]
            }, {
                "name": "DevOps",
                "type": ["rooms"],
                "attributes": [{
                    "name": "capacity",
                    "value": 120
                }]
            }],
            "resources": {
                "rooms": [{
                    "name": "Small Room",
                    "attributes": [{
                        "name": "capacity",
                        "value": 30
                    }]
                }, {
                    "name": "Medium Room",
                    "attributes": [{
                        "name": "capacity",
                        "value": 70
                    }]
                }, {
                    "name": "Big Room",
                    "attributes": [{
                        "name": "capacity",
                        "value": 150
                    }]
                }]
            }
        }
        self.json_str = json.dumps(json_data)

    def test_course_with_no_room_available(self):
        sched_result = sched(self.json_str)
        print(sched_result)
        sched_dict = json.loads(sched_result)
        unsched = sched_dict['unscheduled']

        self.assertEqual(len(unsched), 3)

    # def test_courses_with_rooms_available_scheduled(self):
    #     all_courses = Course.objects.filter(capacity__lt=150)
    #     all_rooms = Room.objects.all()
    #     all_courses_total = [d.cname for d in all_courses]

    #     returned_unscheduled = make_schedule(all_courses, all_rooms,
    #                                          all_courses_total)
    #     self.assertEqual(len(returned_unscheduled), all_courses.count())

    # def test_course_and_room_with_same_capacity(self):
    #     course50 = Course.objects.filter(capacity=50)
    #     room50 = Room.objects.filter(capacity=50)
    #     course50_list = list(course50)

    #     returned_schedule = make_schedule(course50, room50, course50_list)

    #     self.assertEqual(len(returned_schedule), 1)

suite = unittest.TestLoader().loadTestsFromTestCase(TestScheduler)
unittest.TextTestRunner(verbosity=2).run(suite)
