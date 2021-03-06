from django.conf.urls import url
from . import views

app_name = 'scheduler'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^scheduler/about/*$', views.about, name='about'),
    url(r'^scheduler/feedback/*$', views.feedback, name='feedback'),
    url(r'^scheduler/request_history/*$', views.request_history, name='request_history'),
    url(r'^scheduler/resubmit/*$', views.resubmit, name='resubmit'),
    url(r'^scheduler/schedule/*$', views.schedule, name='schedule'),
]
