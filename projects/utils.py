from django.db.models import Q 
from .models import Project, Tag

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