import unittest
import json
from scheduler.schedalgo.schedule import sched

class TestScheduler(unittest.TestCase):

    # Setup the courses and rooms
    def setUp(self):
        with open("test_data/test_no_room_available.json") as f:
            json_no_room = json.load(f)
        self.json_str_no_room_available = json.dumps(json_no_room)
        with open("test_data/test_same_capacity.json") as f:
            json_same_capacity = json.load(f)
        self.json_str_same_capacity = json.dumps(json_same_capacity)
        with open("test_data/test_room_available.json") as f: 
            self.josn_room_available = json.load(f)
        self.json_str_room_available = json.dumps(self.josn_room_available)

    def test_course_with_no_room_available(self):
        sched_result = sched(self.json_str_no_room_available)
        sched_dict = json.loads(sched_result)
        unsched = sched_dict['unscheduled']

        self.assertEqual(len(unsched), 3)

    def test_course_and_room_with_same_capacity(self):
        sched_result = sched(self.json_str_same_capacity)
        sched_dict = json.loads(sched_result)
        unsched = sched_dict['unscheduled']

        self.assertEqual(len(unsched), 0)

    def test_courses_with_rooms_available_scheduled(self):
        courses_cnt = len(self.josn_room_available['consumers'])
        sched_result = sched(self.json_str_room_available)
        sched_dict = json.loads(sched_result)
        sched_courses = sched_dict['scheduled']

        self.assertEqual(len(sched_courses), courses_cnt)

if __name__ == '__main__':
	unittest.main()
