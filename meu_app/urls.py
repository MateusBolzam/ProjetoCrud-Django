from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    
    path('cadastro/', views.cadastro, name="cadastro"),
    path('login/', views.login, name="login"),
    path('home', views.home,name="home"),
    
    path('fornecedores/', views.fornecedor_crud, name='fornecedor_crud'),
    path('fornecedores/novo/', views.fornecedor_salvar, name='fornecedor_salvar'),
    path('fornecedores/<int:id>/editar/', views.fornecedor_editar, name='fornecedor_editar'),
    path('fornecedores/<int:id>/deletar/', views.fornecedor_delete, name='fornecedor_delete'),
    
    path('grupos/', views.grupo_list, name='grupo_list'),
    path('grupos/novo/', views.grupo_create, name='grupo_create'),
    path('grupos/<int:id>/editar/', views.grupo_update, name='grupo_update'),
    path('grupos/<int:id>/deletar/', views.grupo_delete, name='grupo_delete'),
    
    path('subgrupos/', views.subgrupo_crud, name='subgrupo_crud'),
    path('subgrupos/novo/', views.subgrupo_salvar, name='subgrupo_salvar'),
    path('subgrupos/<int:id>/editar/', views.subgrupo_editar, name='subgrupo_editar'),
    path('subgrupos/<int:id>/deletar/', views.subgrupo_delete, name='subgrupo_delete'),
    
    path('produtos/', views.produto_list, name='produto_list'),
    path('produtos/novo/', views.produto_create, name='produto_create'),
    path('produtos/<int:id>/editar/', views.produto_update, name='produto_update'),
    path('produtos/<int:id>/deletar/', views.produto_delete, name='produto_delete'),
    
    path('vendas/adicionar/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('vendas/carrinho/', views.ver_carrinho, name='ver_carrinho'),
    path('vendas/finalizar/', views.finalizar_venda, name='finalizar_venda'),
    path('vendas/concluida/', views.venda_concluida, name='venda_concluida'),
    path('vendas/realizadas/', views.vendas_realizadas, name='vendas_realizadas'),
    path('vendas/<int:pk>/', views.detalhes_venda, name='detalhes_venda'),
    
     path('vendas/visualizar/', views.visualizar_vendas, name='visualizar_vendas'),
]