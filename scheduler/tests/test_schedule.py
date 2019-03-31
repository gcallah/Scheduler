import unittest, json, os
from scheduler.schedalgo.schedule import sched
from ddt import ddt, file_data, unpack

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@ddt
class TestScheduler(unittest.TestCase):

    def setUp(self):
        pass

    @file_data(os.path.join(ROOT_DIR, "test_data/test_schedule_data.json"))
    def test_sched_classes(self, data, expect_sched, expect_unsched):
        json_str_no_room_available = json.dumps(data)
        sched_result = sched(json_str_no_room_available)
        sched_dict = json.loads(sched_result)
        unsched = sched_dict['unscheduled']
        scheded = sched_dict['scheduled']

        self.assertEqual(len(unsched), expect_unsched)
        self.assertEqual(len(scheded), expect_sched)


if __name__ == '__main__':
	unittest.main()
