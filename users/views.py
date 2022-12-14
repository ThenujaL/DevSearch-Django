from email import message
from multiprocessing import context
import profile
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import IntegrityError
from .models import Profile, Skill, Message
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
#user creation form impot
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import searchProfiles, paginateProfiles

# Create your views here.

def profiles(request):
    profiles, search_query = searchProfiles(request)
    itemsPerPage = 5
    profiles, page_range, paginator = paginateProfiles(request, profiles, itemsPerPage)
    context = {'profiles': profiles, 
               'search_query' : search_query,
               'page_range' : page_range}
               
    return render(request, 'users/developers.html', context)

def developer(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkill = profile.skill_set.exclude(description="")
    otherSkill = profile.skill_set.filter(description="")
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
                # check is user already exists
                try:
                    User.objects.get(username=user.username)
                    messages.error(request, 'Username already exists!')
                except User.DoesNotExist:
                    user.save()
                    messages.success(request, 'Acconnt successfully registered')
                    login(request, user)
                    return redirect('edit-account')   
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

        username = request.POST['username'].lower()
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
                return redirect(request.GET['next'] if 'next' in request.GET else 'account')
            else:
                print('Username and password does not match')
                messages.error(request, 'Username and password does not match')


    return render(request, 'users/login-register.html', context=context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
 
    context = {'profile' : profile, 'skills' : skills, 'projects' : projects}
    return render(request, 'users/account.html', context=context)

@login_required(login_url='login')
def editAccount(request):
    
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    context = {'form' : form}
    
    if request.method == 'POST':
        print('IS VALID')
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form' : form}
    return render(request, 'users/profile_form.html', context)    

@login_required(login_url='login')
def createSkill(request):
    form = SkillForm()
    profile = request.user.profile

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            return redirect('account')

    context = {'form' : form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def updateSkill(request, pk):
    
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill) #if instance is passed, the existing instance will be edited. Else a new instance is crteated
        if form.is_valid():
            skill.save()
            return redirect('account')

    context = {'form' : form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill deleted!')
        return redirect('account')

    context = {'object' : skill}
    return render(request, 'delete_template.html', context)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequest = profile.messages.all()
    unreadCount = messageRequest.filter(is_read=False).count()
    context = {'messageRequest': messageRequest,'unreadCount' : unreadCount}
    return render(request, 'users/inbox.html', context)

@login_required(login_url='login')
def single_message(request, pk):
    profile = request.user.profile
    messageRequest = profile.messages.get(id=pk)
    print(messageRequest)

    # set is_read to true if requested
    if not messageRequest.is_read:
        messageRequest.is_read = True
        messageRequest.save()

    context = {'messageRequest' : messageRequest}
    return render(request, 'users/message.html', context)

def sendMessage(request, pk):
    form = MessageForm()
    receipient = Profile.objects.get(id=pk)

    if request.user.is_authenticated:
        sender = request.user.profile
    else:
        sender = None
        

    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            messageInstance = form.save(commit=False)
            messageInstance.sender = sender
            messageInstance.recipient = receipient
            if sender is not None:
                messageInstance.name = f'{sender.first_name} {sender.last_name}'
                messageInstance.email = sender.email
            messageInstance.save()
            messages.success(request, 'Message sent!')
        else:
            messages.error(request, 'Message not sent!')
        
        return redirect('profile', pk=pk)

    context = {'form' : form, 'receipient' : receipient}
    return render(request, 'users/message_form.html', context)

