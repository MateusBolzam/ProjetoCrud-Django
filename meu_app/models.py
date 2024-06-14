from django.db import models
from django.utils import timezone
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
    
    preco_custo = models.FloatField()  
    preco_venda = models.FloatField() 
    
    peso = models.FloatField()
    
    compra = models.IntegerField()
    vendas = models.IntegerField()
    
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    sub_grupo = models.ForeignKey(Subgrupo, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nome
    
class Venda(models.Model):
    
    finalizado = models.BooleanField(default=False)
    
    data_hora = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def atualizar_total(self):
        self.total = sum(item.subtotal for item in self.itens.all())
        self.save()
    
class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        self.preco_unitario = self.produto.preco_venda
        self.subtotal = self.preco_unitario * self.quantidade
        super().save(*args, **kwargs)
        self.venda.atualizar_total()
        # Atualiza o estoque
        self.produto.vendas += self.quantidade
        self.produto.save()
        
    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade}"