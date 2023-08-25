from django.shortcuts import render
from perfil.models import Categoria
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def definir_planejamento(request):
    categorias = Categoria.objects.filter(usuario_id=request.user.id)
    return render(request,'definir_planejamento.html',{'categorias':categorias})

@csrf_exempt
def update_valor_categoria(request,id):
    novo_valor =  json.load(request)['novo_valor']
    categoria = Categoria.objects.get(id=id)
    categoria.valor_planejamento = novo_valor
    categoria.save() 
    return JsonResponse({'status': 'Sucesso'})

@login_required
def ver_planejamento(request):
    categorias =  Categoria.objects.filter(usuario_id=request.user.id)
    total_entrada = 0
    total_saida = 0
    valor_total_planejamento = 0
    calcula_porcentagem_total_entrada = 0
    calcula_porcentagem_total_saida = 0

    if categorias:
        total_entrada,total_saida = categorias[0].total()
        valor_total_planejamento = categorias[0].valor_total_planejamento()
        calcula_porcentagem_total_entrada,calcula_porcentagem_total_saida= categorias[0].calcula_porcentagem_total()

    print(calcula_porcentagem_total_entrada)
    print(calcula_porcentagem_total_saida)

    return render(request,'ver_planejamento.html',{'categorias':categorias,'total_entrada':total_entrada,'total_saida':total_saida,'valor_total_planejamento':valor_total_planejamento,'calcula_porcentagem_total_entrada':calcula_porcentagem_total_entrada,'calcula_porcentagem_total_saida':calcula_porcentagem_total_saida})