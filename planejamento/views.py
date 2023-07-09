from django.shortcuts import render
from perfil.models import Categoria
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

# Create your views here.
def definir_planejamento(request):
    categorias = Categoria.objects.all()
    return render(request,'definir_planejamento.html',{'categorias':categorias})

@csrf_exempt
def update_valor_categoria(request,id):
    novo_valor =  json.load(request)['novo_valor']
    categoria = Categoria.objects.get(id=id)
    categoria.valor_planejamento = novo_valor
    categoria.save() 
    return JsonResponse({'status': 'Sucesso'})


def ver_planejamento(request):
    categorias =  Categoria.objects.all()
    total = categorias[0].total()
    valor_total_planejamento = categorias[0].valor_total_planejamento()
    calcula_porcentagem_total = categorias[0].calcula_porcentagem_total()
    print(valor_total_planejamento)
    return render(request,'ver_planejamento.html',{'categorias':categorias,'total':total,'valor_total_planejamento':valor_total_planejamento,'calcula_porcentagem_total':calcula_porcentagem_total})