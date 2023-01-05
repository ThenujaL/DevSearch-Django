from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('projects/', views.projects),
    path('projects/<str:pk>', views.project),
    path('projects/<str:pk>/vote/', views.projectVote),

    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]