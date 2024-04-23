from django.contrib.auth import login
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from aft.services import AccountService

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            return render(request, 'aft/registration.html', {'error': 'Passwords do not match'})

        user = User.objects.create_user(username=username, password=password1)
        login(request, user)

        return redirect('index')

    return render(request, 'aft/registration.html')


def get_profile(request):
    profile_data = AccountService.get_user_profile(request.user)
    return render(request, 'aft/profile.html', profile_data)