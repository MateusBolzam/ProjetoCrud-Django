from django.db import models

# Create your models here.

class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nome
       
       
class Fornecedor(models.Model):
    
    nome_fantasia = models.CharField(max_length=100)
    nome_social = models.CharField(max_length=100)
    
    cnpj = models.IntegerField()
    
    endereco = models.CharField(max_length=100)
    telefone = models.IntegerField()
    email = models.CharField(max_length=100)
    
    vendedor = models.CharField(max_length=100) 
    
    def __str__(self):
        return self.nome_fantasia
    
class Grupo(models.Model):
    
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
    
class Subgrupo(models.Model):
    
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)
    
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nome
    
class Produto(models.Model):
    
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)
    
    preco_custo = models.IntegerField()
    preco_venda = models.IntegerField()
    
    peso = models.IntegerField()
    compra = models.IntegerField()
    vendas = models.IntegerField()
    
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    sub_grupo = models.ForeignKey(Subgrupo, on_delete=models.CASCADE)
    