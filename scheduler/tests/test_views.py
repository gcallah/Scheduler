from django.test import TestCase 
from unittest import mock
import json

class ViewsTest(TestCase):

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

    @mock.patch('scheduler.views.organize', mock_organize)
    @mock.patch('scheduler.views.sched', mock_sched)
    def test_schedule(self):
        response = self.client.post('/scheduler/schedule', {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'schedule.html')



