from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        if user is not None:
            login(request, user)
            return redirect('sections')
        return redirect('login')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')
