from django.contrib import admin
from .models import Funcionario , Produto , Fornecedor ,Grupo , Subgrupo , Venda, ItemVenda
# Register your models here.

admin.site.register(Funcionario)

admin.site.register(Produto)
admin.site.register(Fornecedor)
admin.site.register(Grupo)
admin.site.register(Subgrupo)
admin.site.register(Venda)
admin.site.register(ItemVenda)