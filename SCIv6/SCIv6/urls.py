from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from schedule import views

urlpatterns = [
    path('', views.index),
    path('schedule/', include('schedule.urls',namespace='schedule')),
    path('accounts/', include('accounts.urls' , namespace='accounts')),
    path('server/', include('server.urls' , namespace='server')),
    path('admin/', admin.site.urls, name='admin'),
]

urlpatterns += staticfiles_urlpatterns()