from django.test import TestCase

class ViewsTest(TestCase):

    def test_index(self):
        response = self.client.get('/scheduler/index')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
