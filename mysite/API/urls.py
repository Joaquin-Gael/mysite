from django.urls import path,include
from rest_framework import routers
from API import views

router = routers.DefaultRouter()
router.register(r'users',views.UserViewSet)
router.register(r'projects',views.ProjectViewSet)

urlpatterns = [
    path('', include(router.urls))
]