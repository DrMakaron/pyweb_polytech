from django.views import View
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .forms import CustomUserCreationForm

# Create your views here.


class LoginView(View):

    def get(self, request):
        return render(request, 'index1.html')

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('store:shop')
        return render(request, "index1.html",
                      context={'errors': {'msg': form.errors['__all__']}})


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('login')


class CreateAccountView(View):
    def get(self, request):
        return render(request, "create_account.html")

    def post(self, request):
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            return redirect('store:shop')

        return render(request, "create_account.html",
                      context={'errors': form.errors})

