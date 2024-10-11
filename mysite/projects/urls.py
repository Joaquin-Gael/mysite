from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('projects/panel/', views.PanelUser.as_view(), name='panel_user'),
    path('projects/<int:project_id>/', views.ProjectDetail.as_view(), name='project_detail'),
    path('projects/create/', views.CreateProject.as_view(), name='project_create'),
    path('projects/<int:pk>/update/', views.EditProject.as_view(), name='project_update'),
    path('projects/<int:pk>/delete/', views.DeleteProject.as_view(), name='project_delete'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('media/create/', views.CreateMedia.as_view(), name='media_create'),
    path('media/galery/', views.MediaGalery.as_view(), name='media_galery'),
    path('media/<int:pk>/delete/', views.DeleteMedia.as_view(), name='media_delete'),
]