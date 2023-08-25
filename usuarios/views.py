from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import logout,authenticate,login as login_django
from django.contrib.auth.decorators 

# Create your views here.

def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        usuario = User.objects.filter(email=email)
        if usuario.exists():
            usuario = authenticate(username=email,password=senha)
            if usuario:
                login_django(request,usuario)
                return redirect(reverse('home'))
            else:
                messages.add_message(request,constants.WARNING,'Email ou senha incorreto!')
                return redirect(reverse('login'))
        else:
            messages.add_message(request,constants.WARNING,'Usuário não cadastrado!')
            return redirect(reverse('cadastro_usuario'))


def cadastro_usuario(request):
    if request.method == 'GET':
        return render(request,'cadastro_usuario.html')
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirma_senha = request.POST.get('confirma_senha')

        if len(nome.strip()) == 0 or len(sobrenome.strip())==0 or len(email.strip())==0:
            messages.add_message(request,constants.WARNING,'Nome ou sobrenome não estão preenchidos!')
            return redirect(reverse('cadastro_usuario'))
        
        if senha != confirma_senha:
            messages.add_message(request,constants.WARNING,'As senhas não são iguais!')
            return redirect(reverse('cadastro_usuario'))
        
        if len(senha)<8 and len(confirma_senha)<8:
            messages.add_message(request,constants.WARNING,'A senha é menor que 8 caracteres!')
            return redirect(reverse('cadastro_usuario'))            

        usuario = User.objects.filter(email=email)

        if usuario.exists():
            messages.add_message(request,constants.WARNING,'Usuário já cadastrado!')
            return redirect(reverse('login'))
        else:
            usuario = User.objects.create_user(username=email,first_name=nome,last_name=sobrenome,email=email,password=senha)
            usuario.save()
            messages.add_message(request,constants.SUCCESS,'Usuário cadastrado com sucesso!')
            return redirect(reverse('login'))
  
        
def sair(request):
    logout(request)
    return redirect(reverse('login'))


