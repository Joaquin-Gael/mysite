from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth import login
from django.shortcuts import (render, redirect)
from django.views import View
from django.http import JsonResponse
from django.contrib import messages
from projects.forms import *
from projects.models import *
import json

class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, f'¡Usuario creado con éxito! Bienvenido {user.username}.')
                return redirect('index')
            except Exception as e:
                print('Error: {}\nData: {}'.format(e.__class__, e.args))
                messages.error(request, f'Error al crear el usuario: {e}', extra_tags='error')
                return render(request, 'register.html', {'form': form})

        messages.error(request, f'Error de validación. Detalles: {form.errors.as_json()}', extra_tags='validation')
        return render(request, 'register.html', {'form': form})
    
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        try:
            username = request.POST['username']
            password = request.POST['password']
            user = User.authenticate(request, username=username, password=password)
            if user is not None:
                user.set_login(request)
                return redirect('index')
            else:
                return render(request, 'login.html', {'error': 'Credenciales inválidas'})
        except Exception as e:
            print('Error: {}\nData: {}'.format(e.__class__, e.args))
            messages.error(request, f'Error al autenticar el usuario.')
            return render(request, 'login.html', {'error': 'Ocurrió un error inesperado.'})

class LogoutView(View):
    def get(self, request):
        User.logout(request)
        return redirect('index')

class IndexView(View):
    def get(self, request):
        projects = Project.objects.all()
        return render(request, 'projects/index.html', {'projects': projects})
    
    def post(self, request):
        projects = Project.objects.filter(title__icontains=request.POST['search_query'])
        print(projects)
        return render(request, 'projects/index.html', {'projects': projects})

class CreateProject(View):
    def get(self, request):
        form = ProjectForm()
        return render(request, 'projects/Form_create.html',{'form':form})
    
    def post(self, request):
        try:
            form = ProjectForm(request.POST, request.FILES)
            if form.is_valid():
                print(form.data)
                proyecto = form.save(commit=False)
                print(proyecto)
                proyecto.userID = request.user
                proyecto.image_url = 'http://127.0.0.1:8000/media/images/{}'.format(str(proyecto.image).replace(' ', '_'))
                proyecto.video_url = 'http://127.0.0.1:8000/media/videos/{}'.format(str(proyecto.image).replace(' ','_'))
                proyecto.save()
                messages.success(request, 'Proyecto creado exitosamente.')
            else:
                error_mesages = [value for key, value in form.errors.as_json()]
                print(error_mesages)
                messages.error(request, f'Por favor, corrija los errores en el formulario')
            return redirect('index')
        except Exception as err:
            print(err)
            return redirect('project_create')

class PanelUser(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('index')
        try:
            user = User.objects.get(userID=request.user.userID)
            proyectos = user.get_proyectos() 
            medias = MediaContent.objects.all()
            return render(request, 'projects/panel.html', {'proyectos': proyectos, 'medias': medias})
        except Exception as err:
            return render(request, 'projects/panel.html', {'proyectos': [], 'medias': []})

    def post(self, request):
        _json = json.loads(request.body)
        print(_json)
        return JsonResponse({
            'msg': f'{_json}'
        })

class EditProject(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/Form_edit.html'
    context_object_name = 'form'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        # Aquí puedes realizar acciones adicionales si es necesario
        return super().form_valid(form)

class DeleteProject(DeleteView):
    model = Project
    success_url = reverse_lazy('index')
    template_name = 'projects/project_confirm_delete.html'

    def get_object(self, queryset=None):
        """ Devuelve el objeto que se eliminará. """
        obj = super().get_object(queryset)
        return obj

class ProjectDetail(View):
    def get(self, request, project_id):
        project = Project.objects.get(id=project_id)
        return render(request, 'projects/project_detail.html', {'project': project})

class CreateMedia(View):
    def get(self, request):
        form = MediaContentForm()
        return render(request, 'projects/upload_media.html',{'form':form})
    
    def post(self, request):
        form = MediaContentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contenido creado exitosamente.')
            return redirect('index')
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
        return render(request, 'projects/upload_media.html',{'form':form})

class MediaGalery(View):
    def get(self, request):
        images = MediaContent.objects.filter(content__icontains='.png')
        videos = MediaContent.objects.filter(content__icontains='.mp4')
        print(images)
        return render(request, 'projects/media_gallery.html', {'images': images, 'videos': videos})

class DeleteMedia(DeleteView):
    model = MediaContent
    success_url = reverse_lazy('media_galery')
    template_name = 'projects/media_confirm_delete.html'

    def get_object(self, queryset=None):
        """ Devuelve el objeto que se eliminará. """
        obj = super().get_object(queryset)
        return obj