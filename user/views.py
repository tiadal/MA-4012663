from django.shortcuts import render, redirect, reverse
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from app.models import *
from django.db.models import Avg, Count, Min, Sum
from datetime import date

from app.views import *

#error pages
def error_404(request, exception):
    return render(request, 'app/error.html')

def error_500(request):
    return render(request, 'app/error.html')


#    path('register/', user_views.register, name="register"),
def register(request):
    print("init")
    if request.user.is_authenticated:
        return redirect('profile')
    print("not auth")
    if request.method == 'POST':
        print("request.method == POST")
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            print("form.is_valid")
            form.save()
            print("form saved")
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})

#    path('accounts/profile/', user_views.profile_redirect, name="profile_redirect"),
@login_required
def profile_redirect(request):
    return redirect('app:test-create')

#    path('profile/', user_views.profile, name="profile"),
@login_required
def profile(request):
    return redirect('app:test-create')

#    path('imprint/', user_views.imprint, name="imprint"),
def imprint(request):
    return render(request, 'app/imprint.html')


