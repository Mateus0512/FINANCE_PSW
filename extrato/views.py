from django.shortcuts import render,redirect
from perfil.models import Categoria,Conta
from django.http import HttpResponse,FileResponse
from django.urls import reverse
from .models import Valores
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime
from django.template.loader import render_to_string
import os
from django.conf import settings
#from weasyprint import HTML
from io import BytesIO
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/')
def novo_valor(request):
    if request.method == 'GET':
        categorias = Categoria.objects.filter(usuario_id=request.user.id)
        contas = Conta.objects.filter(usuario_id=request.user.id)
        return render(request,'novo_valor.html',{'categorias':categorias,
                                                 'contas':contas})

    elif request.method == 'POST':
        valor = request.POST.get('valor')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        data = request.POST.get('data')
        conta = request.POST.get('conta')
        tipo = request.POST.get('tipo')

        valores = Valores(valor=valor,categoria_id=categoria,descricao=descricao,data=data,conta_id=conta,tipo=tipo,usuario_id=request.user.id)
        valores.save()

        conta = Conta.objects.get(id=conta)
        if tipo == 'E':
            conta.valor += float(valor)
            conta.save()
        else:
            conta.valor -= float(valor)
            conta.save()

        messages.add_message(request,constants.SUCCESS,'Entrada/Saida Cadastrada com sucesso.')
        return redirect(reverse('novo_valor'))

@login_required(login_url='/')
def view_extrato(request):
    categorias = Categoria.objects.filter(usuario_id=request.user.id)
    contas = Conta.objects.filter(usuario_id=request.user.id)
    valores = Valores.objects.filter(usuario_id=request.user.id).filter(data__month=datetime.now().month)
    conta_get = request.GET.get('conta')
    categoria_get = request.GET.get('categoria')


    if conta_get:
        valores = valores.filter(conta_id=conta_get)

    if categoria_get:
        valores = valores.filter(categoria_id=categoria_get)

    return render(request,'view_extrato.html',{'categorias':categorias,'contas':contas,'valores':valores})


def exportar_pdf(request):
    #valores = Valores.objects.filter(data__month=datetime.now().month)
    #path_template = os.path.join(settings.BASE_DIR,'templates/partials/extrato.html')
    #template_render = render_to_string(path_template,{'valores':valores})
    #path_output = BytesIO()
    #HTML(string=template_render).write_pdf(path_output)
    #path_output.seek(0)
    #return FileResponse(path_output,filename='extrato.pdf')
    pass