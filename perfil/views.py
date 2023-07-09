from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import Conta,Categoria
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import constants
from django.db.models import Sum
from . utils import calcula_total,calcula_equilibrio_financeiro
from extrato.models import Valores
from datetime import datetime
from contas.models import ContaPagar,ContaPaga
# Create your views here.
def home(request):
    DIA_ATUAL = datetime.now().day
    MES_ATUAL = datetime.now().month
    contas = Conta.objects.all()
    total_conta = calcula_total(contas,'valor')
    valores =  Valores.objects.filter(data__month=datetime.now().month)
    entradas = valores.filter(tipo='E')
    saidas = valores.filter(tipo='S')
    total_entradas = calcula_total(entradas,'valor')
    total_saidas = calcula_total(saidas,'valor')
    total = total_entradas-total_saidas
    percentual_gastos_essenciais,percentual_gastos_nao_essenciais = calcula_equilibrio_financeiro()
    contas_pagar = ContaPagar.objects.all()
    contas_pagas = ContaPaga.objects.filter(data_pagamento__month=MES_ATUAL).values('conta')
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

def gerenciar(request):
    contas = Conta.objects.all()
    bancos = contas[0].banco_choices
    categorias = Categoria.objects.all()
    total_conta = contas.aggregate(Sum('valor'))['valor__sum']

    return render(request,'gerenciar.html',{'contas':contas,'total_conta':total_conta,'categorias':categorias,'bancos':bancos})

def cadastrar_banco(request):
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')

    if len(apelido.strip())==0 or len(valor)==0:
        messages.add_message(request,constants.WARNING,'Preencha todos os campos')
        return redirect(reverse('gerenciar'))

    conta = Conta(apelido=apelido,banco=banco,tipo=tipo,valor=valor,icone=icone)
    conta.save()
    messages.add_message(request,constants.SUCCESS,'Conta cadastrada com sucesso')
    return redirect(reverse('gerenciar'))

def deletar_banco(request,id):
    conta = Conta.objects.get(id=id)
    conta.delete()
    messages.add_message(request,constants.SUCCESS,'Banco deletado com sucesso')
    return redirect(reverse('gerenciar'))

def cadastrar_categoria(request):
    nome = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))
    categoria = Categoria(categoria=nome,essencial=essencial)

    categoria.save()
    messages.add_message(request,constants.SUCCESS,'Categoria cadastrada com sucesso')
    return redirect(reverse('gerenciar'))



def update_categoria(request,id):
    categoria = Categoria.objects.get(id=id)
    categoria.essencial = not categoria.essencial 
    categoria.save()
    return redirect(reverse('gerenciar'))


def dashboard(request):
    dados = {}
    categorias =  Categoria.objects.all()
    for categoria in categorias:
        total = 0
        valores =  Valores.objects.filter(categoria=categoria)
        for valor in valores:
            total += valor.valor 
        dados[categoria.categoria] = total
    return render(request,'dashboard.html',{'labels':list(dados.keys()),'values':list(dados.values())})