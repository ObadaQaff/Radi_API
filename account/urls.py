from django.urls import path
from .views import *
from . import views
urlpatterns = [
   # path('oldest-player/', OldestPlayerView.as_view(), name='oldest-player'),
    path('register/', views.register, name='login'),
  
]
