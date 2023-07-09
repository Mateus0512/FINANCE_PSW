from django.db import models
from datetime import datetime


# Create your models here.
class Categoria(models.Model):
    categoria = models.CharField(max_length=50)
    essencial = models.BooleanField(default=False)
    valor_planejamento = models.FloatField(default=0)

    def __str__(self):
        return self.categoria
    
    def total_gasto(self):
        from extrato.models import Valores
        valores = Valores.objects.filter(categoria_id=self.id).filter(data__month=datetime.now().month).filter(tipo='S')
        total_valor = 0
        for valor in valores:
            total_valor += valor.valor
        return total_valor
    
    def calcula_percentual_gasto_por_categoria(self):
        return int((self.total_gasto() * 100)/ self.valor_planejamento)
    
    def total(self):
        from extrato.models import Valores
        valores = Valores.objects.all()
        total_valor = 0
        for valor in valores:
            total_valor += valor.valor
        return total_valor
    
    def valor_total_planejamento(self):
        total_valor = 0
        categorias = Categoria.objects.all()
        for categoria in categorias:
            total_valor+= categoria.valor_planejamento
        return total_valor
    
    
    def calcula_porcentagem_total(self):
        return int((self.total()*100)/self.valor_total_planejamento())


    
class Conta(models.Model):
    banco_choices = (
        ('BB','Banco do Brasil'),
        ('BR','Bradesco'),
        ('CE','Caixa Econômica'),
        ('IT','Itaú'),
        ('NU','Nubank'), 
        ('ST','Santander')      
    )
    tipo_choices = (
        ('PF','Pessoa Física'),
        ('PJ','Pessoa Jurídica')
    )
    apelido = models.CharField(max_length=50)
    banco = models.CharField(max_length=2,choices=banco_choices)
    tipo = models.CharField(max_length=2,choices=tipo_choices)
    valor = models.FloatField()
    icone = models.ImageField(upload_to='icones')

    def __str__(self):
        return self.apelido