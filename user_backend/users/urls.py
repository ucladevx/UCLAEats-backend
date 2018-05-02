from django.urls import path, re_path
from users import views
from rest_framework.authtoken import views as rest_framework_views

urlpatterns = [
    re_path(r'^data/', views.UserService.as_view()),
    re_path(r'^sign_up/', views.UserSignup.as_view()),
]

# Sign up/Create
# Update
# Delete
# Login
