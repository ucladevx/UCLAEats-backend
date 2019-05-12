from django.urls import path, re_path
from matching import views

urlpatterns = [
    path('new/', views.MatchingService.as_view()),
    path('data/', views.WaitingService.as_view()),
    
    path('requests/status', views.StatusService.as_view()),
    path('requests', views.WaitingService.as_view()),
    path('matches/url', views.MatchByURLService.as_view()),
    path('matches', views.MatchingService.as_view()),
    path('chats', views.ChatsService.as_view()),
    path('report', views.ReportingService.as_view()),
    

    
]
