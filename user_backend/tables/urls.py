from django.conf.urls import include
from django.urls import path, re_path

from . import views

# see https://docs.google.com/document/d/18LYrT5Ga8waJjVXeNwnG76YZkv_bfovJCedDW9plz90/edit
# Endpoint List:
# list_tables, table, joined_tables, create_table, join_table, leave_table, increment_unread, reset_unread

# For now, use user_id as auth_token - fix with authentication later!
urlpatterns = [
    path('tables/list_tables', views.list_tables),
    re_path(r'^tables/table/(?P<table_id>\w{0,50})/$', views.get_table),
    path('tables/create_table', views.create_table),
    re_path(r'^tables/join_table', views.join_table),
    re_path(r'^tables/leave_table', views.leave_table)
]
