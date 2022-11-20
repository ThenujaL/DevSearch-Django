from email import message
from multiprocessing import context
import profile
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Profile
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.contrib import messages
#user creation form impot
from .forms import CustomUserCreationForm

# Create your views here.

def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'users/developers.html', context)

def developer(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkill = profile.skills_set.exclude(description="")
    otherSkill = profile.skills_set.filter(description="")
    context = {'profile': profile, 'topSkill': topSkill, 'otherSkill': otherSkill}
    return render(request, 'users/user-profile.html', context)

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print(f"################# FORM {form}")
        if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                messages.success(request, 'Acconnt successfully registered')
                login(request, user)
                return redirect('profiles')
        else:
            messages.error(request, "An error occured. Please try again.")

    context = {'page': page, 'form': form}
    return render(request, 'users/login-register.html', context=context)

#logout funtionality
def logoutUser(request):
    logout(request)
    messages.success(request, 'User logged out')
    return redirect('login')

#login
def loginUser(request):
    page = 'login'
    context = {'page': page}

    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']


        #checks if user exists
        try:
            user = User.objects.get(username=username)
        except:
            print('User not found')
            print(username)
            messages.error(request, 'Username not found')


        else:
            #queries data for user if user exists
            user = authenticate(request, username=username, password=password)

            if user is not None:
                print('User exists')
                login(request, user)
                return redirect('profiles')
            else:
                print('Username and password does not match')
                messages.error(request, 'Username and password does not match')


    return render(request, 'users/login-register.html', context=context)