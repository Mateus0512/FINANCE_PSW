from extrato.models import Valores
from datetime import datetime

def calcula_total(objeto,campo):
    total = 0
    for obj in objeto:
        total += getattr(obj,campo)

    
    return total


def calcula_equilibrio_financeiro(usuario):
    gastos_essenciais = Valores.objects.filter(usuario_id=usuario).filter(data__month=datetime.now().month).filter(tipo='S').filter(categoria__essencial=True)
    gastos_nao_essenciais = Valores.objects.filter(usuario_id=usuario).filter(data__month=datetime.now().month).filter(tipo='S').filter(categoria__essencial=False)
    total_gastos_essenciais = calcula_total(gastos_essenciais,'valor')
    total_gastos_nao_essenciais = calcula_total(gastos_nao_essenciais,'valor')
    total = total_gastos_essenciais + total_gastos_nao_essenciais
    try:
        percentual_gastos_essenciais = int((total_gastos_essenciais*100)/total)
        percentual_gastos_nao_essenciais = int((total_gastos_nao_essenciais*100)/total)
        return percentual_gastos_essenciais,percentual_gastos_nao_essenciais
    except:
        return 0,0
    
def bancos():
    banco_choices = (
        ('BB','Banco do Brasil'),
        ('BR','Bradesco'),
        ('CE','Caixa Econômica'),
        ('IT','Itaú'),
        ('NU','Nubank'), 
        ('ST','Santander')      
    )
    return banco_choices