#from django.contrib.auth.decorators import login_required
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
            user = form.save()
            login(request, user)
            messages.success(request, 'User creado exitosamente.')
            return redirect('index')
        print(form.errors.as_json())
        messages.error(request, f'Por favor, corrija los errores en el formulario:\n {json.loads(form.errors.as_json())['password2'][0]['message']}')
        return render(request, 'register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = User.authenticate(request, username=username, password=password)
        if user is not None:
            user.set_login(request)
            return redirect('index')
        else:
            return render(request, 'login', {'error': 'Credenciales inválidas'})

class LogoutView(View):
    def get(self, request):
        User.logout(request)
        return redirect('index')

class IndexView(View):
    def get(self, request):
        projects = Project.objects.all()
        return render(request, 'projects/index.html', {'projects': projects})
        #return render(request, 'projects/index.html')

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
                proyecto.image_url = f'http://127.0.0.1:8000/media/images/{str(proyecto.image).replace(' ','_')}'
                proyecto.video_url = f'http://127.0.0.1:8000/media/videos/{str(proyecto.image).replace(' ','_')}'
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

#def CreateProject(request):
#    if request.method == 'POST':
#        form = ProjectForm(request.POST, request.FILES)
#        if form.is_valid():
#            proyecto = form.save(commit=False)
#            proyecto.userID = request.user 
#            proyecto.save()
#            messages.success(request, 'Proyecto creado exitosamente.')
#            return redirect('projects/index.html')
#        else:
#            messages.error(request, 'Por favor, corrija los errores en el formulario.')
#    else:
#        form = ProjectForm()
#        return render(request, 'projects/Form_create.html',{'form':form})

class PanelUser(View):
    def get(self, request):
        #if not request.user.is_authenticated:
        #    return redirect('index')
        try:
            user = User.objects.get(userID=request.user.userID)
            proyectos = user.get_proyectos() 
            return render(request, 'projects/panel.html', {'proyectos': proyectos})
        except Exception as err:
            return render(request, 'projects/panel.html', {'proyectos': []})

    def post(self, request):
        _json = json.loads(request.body)
        print(_json)
        return JsonResponse({
            'msg': f'{_json}'
        })

class EditProject(View):
    def get(self, request):
        form = ProjectForm()
        return render(request, 'projects/Form_edit.html', {'form': form})

    def post(self, request):
        form = forms.ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
        return render(request, 'projects/Form_edit.html', {'form': form})

class DeleteProject(View):
    def get(self, request):
        return render(request, 'projects/delete_project.html')

    def post(self, request, project_id):
        project = Project.objects.get(id=project_id)
        project.delete()
        return redirect('index')

class ProjectDetail(View):
    def get(self, request, project_id):
        project = Project.objects.get(id=project_id)
        return render(request, 'projects/project_detail.html', {'project': project})