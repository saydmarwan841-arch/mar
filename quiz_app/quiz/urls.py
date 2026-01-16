from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quiz/', views.quiz, name='quiz'),
    path('results/', views.results, name='results'),
    path('manager/login/', views.manager_login, name='manager_login'),
    path('manager/', views.manager, name='manager'),
    path('manager/logout/', views.manager_logout, name='manager_logout'),
]
