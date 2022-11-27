from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('project/<str:pk>', views.project, name='project'),
    path('add-project/', views.projectForm, name='project-form'),
    path('edit-project/<str:pk>', views.UpdateProjectForm, name='update-project'),
    path('delete-project/<str:pk>', views.DeleteProject, name='delete-project' ),
]