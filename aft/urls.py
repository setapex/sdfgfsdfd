from django.contrib.auth.views import LoginView
from django.urls import path

from aft import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration.html'), name='login'),
    path('signup/', views.register, name='reg'),
]