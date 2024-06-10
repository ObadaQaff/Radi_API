# tickets/urls.py
from django.urls import path
from .views import *
from . import views
urlpatterns = [
   # path('oldest-player/', OldestPlayerView.as_view(), name='oldest-player'),
    path('get-all-orders/',views.GetAllOrdersView, name='get-all-orders'),
    path('get-all-customers/', GetAllcustomers.as_view(), name='get-all-customers'),
    path('Get_Totle_Incoming/', GetTotleIncoming.as_view(), name='Get_Totle_Incoming'),   
    path('Get-Orders-With-DateFiltering/<int:days>',GetIncomingWithfilter.as_view(),name='Get-Orders-With-DateFiltering'),
    path('Get-Top-Branches/<int:days>',GetTopBranches.as_view(),name='Get-Top-Branches')

]
