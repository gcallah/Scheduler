from django.test import TestCase 
from unittest.mock import patch
from scheduler import views
import json, shutil, os

class ViewsTest(TestCase):

    history_data_path_for_test = 'scheduler/history_data_for_test/'
    history_data_path_original = 'scheduler/history_schedule_data/'

    @classmethod
    def setUpClass(self): 
        if not os.path.exists(self.history_data_path_for_test):
            os.mkdir(self.history_data_path_for_test)
        views.history_data_path = self.history_data_path_for_test

    @classmethod
    def tearDownClass(self):
        # clear the temporary dir when it's not empty
        if os.path.exists(self.history_data_path_for_test) and os.listdir(self.history_data_path_for_test): 
            shutil.rmtree(self.history_data_path_for_test)
        views.history_data_path = self.history_data_path_original

    # def setUp(self): 
    #     views.history_data_path = self.history_data_path_for_test

    # def tearDown(self): 
    #     views.history_data_path = self.history_data_path_original

    def test_index(self):
        response = self.client.get('/scheduler/index', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_about(self):
        response = self.client.get('/scheduler/about', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    def test_feedback(self):
        response = self.client.post('/scheduler/feedback', {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feedback.html')

    def mock_organize(self):
        return {}

    def mock_sched(self):
        res = {
            "scheduled": [],
            "unscheduled": []
        }
        return json.dumps(res)

    @patch('scheduler.views.organize', mock_organize)
    @patch('scheduler.views.sched', mock_sched)
    def test_schedule(self):
        response = self.client.post('/scheduler/schedule', {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'schedule.html')

    @patch('scheduler.views.sched', mock_sched)
    def test_schedule_with_reschedule_req(self): 
        with patch('scheduler.views.organize', return_value={}) as mock_org:
            response = self.client.post('/scheduler/schedule', {'reschedule': 'Sort', 'devops_1': 1, 'devops_2': 1})
            self.assertEqual(response.status_code, 200)
            mock_org.assert_called_with({'schedule': 'Sort', 'devops':2})





