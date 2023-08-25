from django.shortcuts import render,redirect
from django.urls import reverse
from perfil.models import Categoria
from . models import ContaPagar,ContaPaga
from django.contrib.messages import constants
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def definir_contas(request):
    if request.method == 'GET':
        categorias = Categoria.objects.filter(usuario_id=request.user.id)
        return render(request,'definir_contas.html',{'categorias':categorias})
    
    else:
        titulo = request.POST.get('titulo')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        dia_pagamento = request.POST.get('dia_pagamento')
        conta =  ContaPagar(titulo=titulo,categoria_id=categoria,descricao=descricao,valor=valor,dia_pagamento=dia_pagamento,usuario_id=request.user.id)
        conta.save()
        messages.add_message(request,constants.SUCCESS,'Conta cadastrada com sucesso!')
        return redirect(reverse('definir_contas'))
    
@login_required    
def ver_contas(request):
    MES_ATUAL = datetime.now().month
    DIA_ATUAL = datetime.now().day
    contas = ContaPagar.objects.filter(usuario_id=request.user.id)
    contas_pagas = ContaPaga.objects.filter(usuario_id=request.user.id).filter(data_pagamento__month=MES_ATUAL).values('conta')
    contas_vencidas = contas.filter(dia_pagamento__lt=DIA_ATUAL).exclude(id__in=contas_pagas)
    contas_proximas_vencimento = contas.filter(dia_pagamento__lte=DIA_ATUAL+5).filter(dia_pagamento__gt=DIA_ATUAL).exclude(id__in=contas_pagas)
    restantes = contas.exclude(id__in=contas_vencidas).exclude(id__in=contas_proximas_vencimento).exclude(id__in=contas_pagas)
    total_contas_vencidas = contas_vencidas.count()
    total_contas_proximas_vencimento = contas_proximas_vencimento.count()
    total_restantes = restantes.count()
    total_contas_pagas = contas_pagas.count()
    
    return render(request,'ver_contas.html',{'contas_vencidas':contas_vencidas,
                                             'contas_proximas_vencimento':contas_proximas_vencimento,
                                             'restantes':restantes,
                                             'total_contas_vencidas':total_contas_vencidas,
                                             'total_contas_proximas_vencimento':total_contas_proximas_vencimento,
                                             'total_restantes':total_restantes,
                                             'total_contas_pagas':total_contas_pagas})

@login_required
def pagar_conta(request):
    id_conta = request.POST.get('id_conta')
    data_pagamento = request.POST.get('dia_do_pagamento')
    conta_paga = ContaPaga(conta_id=id_conta,data_pagamento=data_pagamento)
    conta_paga.save()
    print(id_conta)
    messages.add_message(request,constants.SUCCESS,'Conta paga com sucesso!')
    return redirect(reverse('ver_contas'))