from django.conf.urls import url
from . import views

app_name = 'scheduler'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^scheduler/about/*$', views.about, name='about'),
    url(r'^scheduler/feedback/*$', views.feedback, name='feedback'),
    url(r'^scheduler/schedule/*$', views.schedule, name='schedule'),
    url(r'^scheduler/addCourse/*$', views.addCourse, name='addCourse'),
]
