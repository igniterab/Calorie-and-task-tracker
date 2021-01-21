
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
   
    path('', index , name = 'index'),
    path('signup', signup , name = 'signup'),
    path('signin', signin , name = 'signin'),
    path('profile', profile , name = 'profile'),
    path('tasks', tasks , name = 'tasks'),
    path('calorie-mapper', calorie , name = 'calorie'),
    path('leaderboard', leaderboard , name = 'leaderboard'),
    path('edit/<int:id>/<str:user>/',edit,name="edit"),
    path('delete/<int:id>/<str:user>/',delete,name="delete"),
    path('check/<int:id>/<str:user>/',check,name="check"),
    path('edit/save/<int:obj>/',edit_save,name="edit_save"),
    path('get_data/',get_data,name="get_data"),





    path('logout', logout , name = 'logout'),






]
