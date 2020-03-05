from django.conf.urls import include
from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path(r'^tables/create_table', views.create_table),
    re_path(r'^tables/join_table', views.join_table),
    re_path(r'^tables/leave_table', views.leave_table)
]
