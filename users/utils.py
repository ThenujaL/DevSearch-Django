from .models import Profile, Skill
from django.db.models import Q 


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