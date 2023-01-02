from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerUser, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('', views.profiles, name='profiles'),
    path('developer/<str:pk>', views.developer, name='profile'),
    path('account/', views.userAccount, name='account'),
    path('edit-account/', views.editAccount, name='edit-account'),
    path('add-skill/', views.createSkill, name='add-skill'),
    path('edit-skill/<str:pk>/', views.updateSkill, name='edit-skill'),
    path('delete-skill/<str:pk>/', views.deleteSkill, name='delete-skill'),
    path('inbox/', views.inbox, name='inbox'),
    path('message/<str:pk>/', views.single_message, name='message'),
    path('send-message/<str:pk>/', views.sendMessage, name='send-message')
 

]