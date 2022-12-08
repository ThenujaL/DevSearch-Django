from django.db.models import Q 
from .models import Project, Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateProjects(request, projects, results):
    page = request.GET.get('page')
    paginator = Paginator(projects, results)
    try:
        projects = paginator.page(page)    
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)   
    except EmptyPage:
        # if user enters a page not in index, send user to last page
        page = paginator.num_pages
        projects = paginator.page(page)
    
    leftIndex = int(page) - 4
    if leftIndex < 1:
        leftIndex = 1
    
    rightIndex = int(page) + 4
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages

    page_range = range(leftIndex, rightIndex + 1)
    
    return projects, page_range, paginator

def searchProjects(request):
    if request.GET.get('q'):
        search_query = request.GET.get('q')
        tags = Tag.objects.filter(name__icontains=search_query)
        projects = Project.objects.filter(Q(title__icontains=search_query)|
                                          Q(tags__in=tags)|
                                          Q(owner__first_name__icontains=search_query)).distinct()
    else:
        search_query = ''
        projects = Project.objects.all()

    return projects, search_query