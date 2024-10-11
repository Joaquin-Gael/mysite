from django.shortcuts import render
from rest_framework import viewsets, permissions, decorators, response, status
from projects.models import User, Project
from .serializers import UserSerializer, ProjectSerializer

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @decorators.action(['GET'], url_path='projects', detail=True)
    def get_projects_by_user(self, request, pk=None):
        try:
            projects = Project.objects.filter(userID=pk)
            list_projects = []
            for project in projects:
                data = {
                    'id': project.id,
                    'title': project.title,
                    'subtitle': project.subtitle,
                    'image_url': project.image_url,
                    'image': project.image.url if project.image else None,
                    'description': project.description,
                    'created_at': project.created_at.isoformat(),
                    'updated_at': project.updated_at.isoformat()
                }
                list_projects.append(data)
                
            return response.Response(list_projects, status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return response.Response({
                'error': str(err)
            }, status=status.HTTP_404_NOT_FOUND)
            
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]