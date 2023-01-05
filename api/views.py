from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from projects.models import Project, Review
from .serializers import ProjectSerializer

@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'GET' : '/api/projects'},
        {'GET' : '/api/projects/id'},
        {'POST' : '/api/projects/id/vote'},

        {'POST' : '/api/users/token'},
        {'POST' : '/api/user/token/refresh'}
    ]

    return Response(routes)


@api_view(['GET'])
def projects(request):
    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
def project(request, pk):
    if request.method == 'GET':
        project = Project.objects.get(id=pk)
        serializer = ProjectSerializer(project, many=False)
        return Response(serializer.data)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile
    data = request.data
    print(f'DATA: {data}')


    #update review and vote
    review, isCreated = Review.objects.get_or_create(
        project = project,
        owner = user
    )
    # users can only post one review per project
    if isCreated:
        review.value = data['value']
        review.save()
        project.get_voteCount

    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)