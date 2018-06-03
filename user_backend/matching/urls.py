from django.urls import path, re_path
from matching import views

urlpatterns = [
    path('new/', views.MatchingService.as_view()),
    path('data/', views.WaitingService.as_view()),
]
