from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from aft.views import *

urlpatterns = [
    path('login/', LoginView.as_view(template_name='aft/registration.html'), name='login'),
    path('signup/', register, name='reg'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('profile', get_profile, name='profile'),
]