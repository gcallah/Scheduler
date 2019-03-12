import unittest, json
from schedule import sched, make_sched, get_unsched

class AlgorithmTestCase(unittest.TestCase):

    # Setup the courses and rooms
    def setUp(self):
        json_data = {
            "resources": {
                "room": [{
                        "name": "room20",
                        "attributes": {
                            "capacity": 20,
                            "video": True
                        }
                    },
                    {
                        "name": "room50",
                        "attributes": {
                            "capacity": 50,
                            "video": False
                        }
                    },
                    {
                        "name": "room75",
                        "attributes": {
                            "capacity": 75,
                            "video": False
                        }
                    },
                    {
                        "name": "room150",
                        "attrubutes": {
                            "capacity": 150,
                            "video": True
                        }
                    }
                ],
                "prof": []
            },
            "consumers": [{
                    "type": [],
                    "name": "course50",
                    "attributes": [
                        {
                            "value": 50
                        },
                        {
                            "video": True
                        }
                    ]
                },
                {
                    "type": [],
                    "name": "course15",
                    "attributes": [
                        {
                            "value": 15
                        },
                        {
                            "video": False
                        }
                    ]
                },
                {
                    "type": [],
                    "name": "course500",
                    "attributes": [
                        {
                            "value": 500
                        },
                        {
                            "value": True
                        }
                    ]
                },
                {
                    "type": [],
                    "name": "course100",
                    "attributes": [
                        {
                            "value": 100
                        },
                        {
                            "value": False
                        }
                    ]
                }
            ]
        }
        self.json_str = json.dumps(json_data)

    def test_course_with_no_room_available(self):
        sched_result = sched(self.json_str)
        print(sched_result)
        sched_dict = json.loads(sched_result)
        unsched = sched_dict['unscheduled']

        self.assertEqual(len(unsched), 1)

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

    if __name__ == '__main__':
        unittest.main()
