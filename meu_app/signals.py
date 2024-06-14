# meu_app/signals.py

from django.dispatch import Signal, receiver
from .models import Venda, ItemVenda

# Definindo o sinal sem providing_args
venda_pronta = Signal()

# Conectando o sinal a um receptor
@receiver(venda_pronta)
def venda_concluida_handler(sender, **kwargs):
    venda = kwargs['venda']
    for item in venda.itens.all():
        produto = item.produto
        quantidade_vendida = item.quantidade
        
        # Atualizar o estoque do produto
        produto.estoque -= quantidade_vendida
        produto.vendas += quantidade_vendida
        produto.save()

        # Verificar se o estoque está baixo
        estoque_minimo = 100  # Defina aqui o valor mínimo de estoque para considerar como baixo
        if produto.estoque <= estoque_minimo:
            # Aqui você pode enviar um e-mail, uma notificação, etc.
            print(f"Alerta: Estoque baixo para o produto {produto.nome}. Estoque atual: {produto.estoque}")
