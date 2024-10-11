from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import (login, logout, authenticate)
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
    userID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True)
    last_logout = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def set_login(self, request):
        self.last_login = timezone.now()
        self.save()
        login(request, self)

    def set_logout(self, request):
        self.last_logout = timezone.now()
        self.save()
        logout(request)
    
    @classmethod
    def authenticate(cls, request, username=None, password=None):
        user = cls.objects.filter(name=username).first()
        if user.check_password(password):
            user.set_login(request)
            return user
        return None
    
    @classmethod
    def logout(cls, request) -> bool:
        user = request.user
        if user.is_authenticated:
            user.set_logout(request)
            return True
        return False
    
    def get_proyectos(self):
        return Project.objects.filter(userID=self)

class Project(models.Model):
    userID = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100,blank=True,null=True)
    image_url = models.URLField()
    image = models.ImageField(upload_to='images/', default='800x600.png', null=True)
    video = models.FileField(upload_to='videos/', default='800x600.png', null=True)
    video_url = models.URLField(blank=True, null=True)
    description = models.TextField()
    objective = models.TextField()
    goals = models.TextField()
    content = models.TextField()
    teachers = models.TextField()
    course = models.TextField()
    students = models.TextField()
    subject = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def large_image_url(self):
        return self.image_url.replace('small', 'large')

class MediaContent(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    content = models.FileField(upload_to='content/', default='800x600.png', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title