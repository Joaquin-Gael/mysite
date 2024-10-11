from django import forms
from .models import (Project, User, MediaContent)
from django.contrib.auth.forms import UserCreationForm

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title', 'subtitle', 'image_url', 'image', 'video', 'video_url',
            'description', 'objective', 'goals', 'content', 'teachers', 'course',
            'students', 'subject'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del proyecto'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subtítulo del proyecto'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'URL de la imagen', 'value': 'http://127.0.0.1:8000/media/images/default.jpg'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'URL del video', 'value': 'http://127.0.0.1:8000/media/videos/default.mp4'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción del proyecto', 'rows': 5}),
            'objective': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Objetivo del proyecto', 'rows': 3}),
            'goals': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Metas del proyecto', 'rows': 3}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Contenido del proyecto', 'rows': 5}),
            'teachers': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Profesores', 'rows': 3}),
            'course': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Curso'}),
            'students': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Estudiantes', 'rows': 3}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Materia'}),
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'password1','password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirma tu contraseña'}),
        }


class MediaContentForm(forms.ModelForm):
    class Meta:
        model = MediaContent
        fields = ['title', 'description', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del contenido'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descripción del contenido...'}),
            'content': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }