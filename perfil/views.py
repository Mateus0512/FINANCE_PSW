from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import Conta,Categoria
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import constants
from django.db.models import Sum
from . utils import calcula_total,calcula_equilibrio_financeiro,bancos as lista_bancos
from extrato.models import Valores
from datetime import datetime
from contas.models import ContaPagar,ContaPaga
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='/')
def home(request):
    DIA_ATUAL = datetime.now().day
    MES_ATUAL = datetime.now().month
    contas = Conta.objects.filter(usuario_id=request.user.id)
    total_conta = calcula_total(contas,'valor')
    valores =  Valores.objects.filter(usuario_id=request.user.id).filter(data__month=datetime.now().month)
    entradas = valores.filter(tipo='E')
    saidas = valores.filter(tipo='S')
    total_entradas = calcula_total(entradas,'valor')
    total_saidas = calcula_total(saidas,'valor')
    total = total_entradas-total_saidas
    percentual_gastos_essenciais,percentual_gastos_nao_essenciais = calcula_equilibrio_financeiro(request.user.id)
    contas_pagar = ContaPagar.objects.filter(usuario_id=request.user.id)
    contas_pagas = ContaPaga.objects.filter(usuario_id=request.user.id).filter(data_pagamento__month=MES_ATUAL).values('conta')
    contas_vencidas = contas_pagar.filter(dia_pagamento__lt=DIA_ATUAL).exclude(id__in=contas_pagas).count()
    contas_proximas_vencimento = contas_pagar.filter(dia_pagamento__lte=DIA_ATUAL+5).filter(dia_pagamento__gt=DIA_ATUAL).exclude(id__in=contas_pagas).count()  
    return render(request,'home.html',{'contas':contas,
                                       'total_conta':total_conta,
                                       'total_entradas':total_entradas,
                                       'total_saidas':total_saidas,
                                       'percentual_gastos_essenciais':percentual_gastos_essenciais,
                                       'percentual_gastos_nao_essenciais':percentual_gastos_nao_essenciais,
                                       'contas_vencidas':contas_vencidas,
                                       'contas_proximas_vencimento':contas_proximas_vencimento,
                                       'total':total})

@login_required(login_url='/')
def gerenciar(request):
    contas = Conta.objects.filter(usuario_id=request.user.id)
    
    bancos = lista_bancos()
    categorias = Categoria.objects.filter(usuario_id=request.user.id)
    total_conta = contas.aggregate(Sum('valor'))['valor__sum']

    return render(request,'gerenciar.html',{'contas':contas,'total_conta':total_conta,'categorias':categorias,'bancos':bancos})

@login_required(login_url='/')
def cadastrar_banco(request):
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')

    if len(apelido.strip())==0 or len(valor)==0:
        messages.add_message(request,constants.WARNING,'Preencha todos os campos')
        return redirect(reverse('gerenciar'))

    conta = Conta(apelido=apelido,banco=banco,tipo=tipo,valor=valor,icone=icone,usuario_id=request.user.id)
    conta.save()
    messages.add_message(request,constants.SUCCESS,'Conta cadastrada com sucesso')
    return redirect(reverse('gerenciar'))

@login_required(login_url='/')
def deletar_banco(request,id):
    conta = Conta.objects.get(id=id)
    conta.delete()
    messages.add_message(request,constants.SUCCESS,'Banco deletado com sucesso')
    return redirect(reverse('gerenciar'))

@login_required(login_url='/')
def cadastrar_categoria(request):
    nome = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))
    categoria = Categoria(categoria=nome,essencial=essencial,usuario_id=request.user.id)

    categoria.save()
    messages.add_message(request,constants.SUCCESS,'Categoria cadastrada com sucesso')
    return redirect(reverse('gerenciar'))


@login_required(login_url='/')
def update_categoria(request,id):
    categoria = Categoria.objects.get(id=id)
    categoria.essencial = not categoria.essencial 
    categoria.save()
    return redirect(reverse('gerenciar'))

@login_required(login_url='/')
def dashboard(request):
    dados = {}
    categorias =  Categoria.objects.filter(usuario_id=request.user.id)
    for categoria in categorias:
        total = 0
        valores =  Valores.objects.filter(categoria=categoria)
        for valor in valores:
            total += valor.valor 
        dados[categoria.categoria] = total
    return render(request,'dashboard.html',{'labels':list(dados.keys()),'values':list(dados.values())})