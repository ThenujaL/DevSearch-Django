from contextlib import redirect_stdout
from email import message
from multiprocessing import context
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import searchProjects, paginateProjects
from .models import Project, Tag
from django.http import HttpResponse
from .forms import ProjectForm, ReviewForm
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.

def projects(request):
    projects, search_query = searchProjects(request)
    itemsPerPage = 5
    projects, page_range, paginator = paginateProjects(request, projects, itemsPerPage)

    context = {'projects': projects,
                'search_query' : search_query,
                'paginator' : paginator,
                'page_range' : page_range}
    return render(request, 'projects/projects.html', context)

    

def project(request, pk):  
    projectObj = Project.objects.get(id=pk)
    # getting upvote count and ratio - property decoratore used
    projectObj.get_voteCount
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.project = projectObj
            review.owner = request.user.profile
            review.save()

            

            messages.success(request, "Review submitted!")
            return redirect('project', pk=projectObj.id)

    context = {'project': projectObj,
                'form' : ReviewForm()
                }
    return render(request, 'projects/single-project.html', context)

#sends user to login page if not authenticated
@login_required(login_url='login')
def projectForm(request):
    form = ProjectForm()
    owner = request.user.profile

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = owner
            project.save()
            return redirect('projects')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)   

@login_required(login_url='login')
def UpdateProjectForm(request, pk):
    owner = request.user.profile
    project = owner.project_set.get(id=pk)
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
    owner = request.user.profile
    project = owner.project_set.get(id=pk)
    context = {'object': project}

    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted!')
        return redirect('account')

    return render(request, 'delete_template.html', context)
    

