
from django.urls import path

from . import views
from django.conf.urls import url
app_name = 'schedule'

urlpatterns = [
    path('', views.index , name='index' ),
    path('createRoom/', views.createRoom , name='createRoom' ),
    path('createExam/', views.createExam , name='createExam' ),
    path('createMasterSchedule/', views.createMasterSchedule , name='createMasterSchedule' ),
    path('updateMasterSchedule/<id>', views.updateMasterSchedule , name='updateMasterSchedule' ),
    path('createSchedule/', views.createSchedule , name='createSchedule' ),
    path('createAdhoc/', views.createAdhoc, name='createAdhoc'),
    path('roomTable/', views.roomTable , name='roomTable' ),
    path('schedule/', views.schedule , name='schedule' ),
    path('SESSIONS/', views.SESSIONSview , name='SESSIONSview' ),

    path('createsExam/', views.createsExam, name='createsExam'),

    url('^calendar', views.calendar, name='calendar'),
    url('^add_event$', views.add_event, name='add_event'),
    url('^update$', views.update, name='update'),
    url('^remove', views.remove, name='remove'),
]
