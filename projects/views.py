from contextlib import redirect_stdout
from email import message
from multiprocessing import context
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Project
from django.http import HttpResponse
from .forms import ProjectForm

# Create your views here.

def projects(request):
    projects = Project.objects.all()
    context = {'projects': projects}
    return render(request, 'projects/projects.html', context)

def project(request, pk):  
    projectObj = Project.objects.get(id=pk)
    return render(request, 'projects/single-project.html', {'project': projectObj})

#sends user to login page if not authenticated
@login_required(login_url='login')
def projectForm(request):
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projects')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)   

@login_required(login_url='login')
def UpdateProjectForm(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)   

@login_required(login_url='login')
def DeleteProject(request, pk):
    project = Project.objects.get(id=pk)
    context = {'project': project}

    if request.method == 'POST':
        project.delete()
        return redirect('projects')

    return render(request, 'projects/delete_template.html', context)
    

