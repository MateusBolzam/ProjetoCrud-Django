# meu_app/forms.py

from django import forms
from .models import Fornecedor, Grupo, Subgrupo

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
        