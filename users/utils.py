from .models import Profile, Skill
from django.db.models import Q 
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateProfiles(request, profiles, results):
    page = request.GET.get('page')
    paginator = Paginator(profiles, results)
    try:
        profiles = paginator.page(page)    
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)   
    except EmptyPage:
        # if user enters a page not in index, send user to last page
        page = paginator.num_pages
        profiles = paginator.page(page)
    
    leftIndex = int(page) - 4
    if leftIndex < 1:
        leftIndex = 1
    
    rightIndex = int(page) + 4
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages

    page_range = range(leftIndex, rightIndex + 1)
    
    return profiles, page_range, paginator

def searchProfiles(request):
    search_query = ''
    if request.GET.get('q'):
        search_query = request.GET.get('q')
        skills = Skill.objects.filter(name__icontains=search_query)
        profiles = Profile.objects.filter(Q(first_name__icontains=search_query) | 
                                          Q(short_intro__icontains=search_query) |
                                          Q(skill__in=skills)).distinct()
    else:
        profiles = Profile.objects.all()

    return profiles, search_query