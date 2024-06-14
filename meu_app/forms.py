# meu_app/forms.py

from django import forms
from .models import Fornecedor, Grupo, Subgrupo,Produto,ItemVenda

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['nome_fantasia', 'nome_social', 'cnpj', 'endereco', 'telefone', 'email', 'vendedor']


class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['nome', 'descricao']
        
class SubgrupoForm(forms.ModelForm):
    class Meta:
        model = Subgrupo
        fields = ['nome', 'descricao', 'grupo']
        
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco_custo', 'preco_venda', 'peso', 'compra', 'vendas', 'fornecedor', 'grupo', 'sub_grupo']
        
class ItemVendaForm(forms.ModelForm):
    class Meta:
        model = ItemVenda
        fields = ['produto', 'quantidade']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
        }