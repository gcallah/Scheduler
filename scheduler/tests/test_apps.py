from django.apps import apps
from django.test import TestCase
from scheduler.apps import SchedulerConfig

class SchedulerConfigTest(TestCase): 

    def test_apps(self): 
        self.assertEquals(SchedulerConfig.name, 'scheduler')
        self.assertEquals(apps.get_app_config('scheduler').name, 'scheduler')