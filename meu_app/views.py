import plotly.express as px
import plotly.graph_objs as go
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Fornecedor, Grupo, Subgrupo, Produto , ItemVenda, Venda
from .forms import FornecedorForm, GrupoForm, SubgrupoForm, ProdutoForm , ItemVendaForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from rolepermissions.roles import assign_role
from rolepermissions.decorators import has_role_decorator ,has_permission_decorator
from site_django.roles import Gerente, Vendedor
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from decimal import Decimal
from plotly.offline import plot
import plotly.offline as opy
import plotly.graph_objs as go
from .signals import venda_pronta
from django.utils.timezone import now

# Create your views here.

def cadastro(request):
    if request.method == "GET":
        return render(request, "cadastro.html")
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        role = request.POST.get('role')

        # Verifica se o username já está em uso
        user = User.objects.filter(username=username).first()
        if user:
            return render(request, "cadastro.html", {'error_message': 'Já existe um usuário com esse username'})

        # Cria o novo usuário
        user = User.objects.create_user(username, email, senha)

        # Associa a role escolhida ao novo usuário
        if role == 'Gerente':
            assign_role(user, Gerente)
        elif role == 'Vendedor':
            assign_role(user, Vendedor)

        return redirect('login')

def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)
        
        if user:
            login_django(request, user)
            return redirect('home')  # Certifique-se que 'home2' é o nome correto da sua rota
        else:
            return redirect('login')  # Certifique-se que 'login' é o nome correto da sua rota


def home(request):
        return render(request, "home.html")


# Fornecedor 
@login_required(login_url="/venda/login")
@has_role_decorator(Gerente)
def fornecedor_crud(request):
    fornecedores = Fornecedor.objects.all()
    return render(request, "fornecedor_list.html", {"fornecedores": fornecedores})

@login_required(login_url="/venda/login")
@has_role_decorator(Gerente)
def fornecedor_salvar(request):
    if request.method == "POST":
        form = FornecedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fornecedor_crud')  # Redireciona para a lista de fornecedores

    form = FornecedorForm()
    return render(request, "fornecedor_form.html", {"form": form})

@login_required(login_url="/venda/login")
@has_role_decorator(Gerente)
def fornecedor_editar(request, id):
    fornecedor = get_object_or_404(Fornecedor, id=id)
    if request.method == "POST":
        form = FornecedorForm(request.POST, instance=fornecedor)
        if form.is_valid():
            form.save()
            return redirect('fornecedor_crud')
    else:
        form = FornecedorForm(instance=fornecedor)
    return render(request, "fornecedor_form.html", {"form": form})

@login_required(login_url="/venda/login")
@has_role_decorator(Gerente)
def fornecedor_delete(request, id):
    fornecedor = get_object_or_404(Fornecedor, id=id)
    if request.method == "POST":
        fornecedor.delete()
        return redirect('fornecedor_crud')
    return render(request, "fornecedor_delete.html", {"fornecedor": fornecedor})


# Grupo

@login_required
@has_role_decorator(Gerente)
def grupo_list(request):
    grupos = Grupo.objects.all()
    return render(request, 'grupo_list.html', {'grupos': grupos})

@login_required
@has_role_decorator(Gerente)
def grupo_create(request):
    if request.method == "POST":
        form = GrupoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('grupo_list')
    else:
        form = GrupoForm()
    return render(request, 'grupo_form.html', {'form': form})

@login_required
@has_role_decorator(Gerente)
def grupo_update(request, id):
    grupo = get_object_or_404(Grupo, id=id)
    if request.method == "POST":
        form = GrupoForm(request.POST, instance=grupo)
        if form.is_valid():
            form.save()
            return redirect('grupo_list')
    else:
        form = GrupoForm(instance=grupo)
    return render(request, 'grupo_form.html', {'form': form})

@login_required
@has_role_decorator(Gerente)
def grupo_delete(request, id):
    grupo = get_object_or_404(Grupo, id=id)
    if request.method == "POST":
        grupo.delete()
        return redirect('grupo_list')
    return render(request, 'grupo_delete.html', {'grupo': grupo})

# SubGrupo

@login_required(login_url="/venda/login")
@has_role_decorator(Gerente)  # Decorator para verificar a permissão do usuário
def subgrupo_crud(request):
    subgrupos = Subgrupo.objects.all()
    return render(request, "subgrupo_list.html", {"subgrupos": subgrupos})

@login_required(login_url="/venda/login")
@has_role_decorator(Gerente)
def subgrupo_salvar(request):
    if request.method == "POST":
        form = SubgrupoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subgrupo_crud')  # Redireciona para a lista de subgrupos

    form = SubgrupoForm()
    return render(request, "subgrupo_form.html", {"form": form})

@login_required(login_url="/venda/login")
@has_role_decorator(Gerente)
def subgrupo_editar(request, id):
    subgrupo = get_object_or_404(Subgrupo, id=id)
    form = SubgrupoForm(instance=subgrupo)
    return render(request, "subgrupo_form.html", {"form": form})

@login_required(login_url="/venda/login")
@has_role_decorator(Gerente)
def subgrupo_update(request, id):
    subgrupo = get_object_or_404(Subgrupo, id=id)
    if request.method == "POST":
        form = SubgrupoForm(request.POST, instance=subgrupo)
        if form.is_valid():
            form.save()
            return redirect('subgrupo_crud')

    form = SubgrupoForm(instance=subgrupo)
    return render(request, "subgrupo_form.html", {"form": form})
@login_required(login_url="/venda/login")
@has_role_decorator(Gerente)
def subgrupo_delete(request, id):
    subgrupo = get_object_or_404(Subgrupo, id=id)
    if request.method == "POST":
        subgrupo.delete()
        return redirect('subgrupo_crud')
    return render(request, 'subgrupo_delete.html', {'subgrupo': subgrupo})

# Produtos

@login_required(login_url="/venda/login")
@has_role_decorator(Gerente)
def produto_list(request):
    produtos = Produto.objects.all()
    return render(request, "produto_list.html", {"produtos": produtos})

@login_required(login_url="/venda/login")
@has_role_decorator(Gerente)
def produto_create(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('produto_list')
    else:
        form = ProdutoForm()
    return render(request, "produto_form.html", {"form": form})

@login_required(login_url="/venda/login")
@has_role_decorator(Gerente)
def produto_update(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == "POST":
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('produto_list')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, "produto_form.html", {"form": form})

@login_required(login_url="/venda/login")
@has_role_decorator(Gerente)
def produto_delete(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == "POST":
        produto.delete()
        return redirect('produto_list')
    return render(request, "produto_delete.html", {'produto': produto})

def adicionar_ao_carrinho(request):
    if request.method == "POST":
        venda, created = Venda.objects.get_or_create(finalizado=False)
        form = ItemVendaForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.venda = venda
            item.save()
            return redirect('ver_carrinho')
    else:
        form = ItemVendaForm()
    return render(request, 'adicionar_carrinho.html', {'form': form})

@login_required(login_url="/venda/login")
def ver_carrinho(request):
    venda = get_object_or_404(Venda, finalizado=False)
    itens = venda.itens.all()
    return render(request, 'ver_carrinho.html', {'venda': venda, 'itens': itens})

@login_required(login_url="/venda/login")
def finalizar_venda(request):
    venda = get_object_or_404(Venda, finalizado=False)
    venda.finalizado = True
    venda.save()

    # Emitir sinal de venda concluída
    venda_pronta.send(sender=Venda, venda=venda)

    return redirect('venda_concluida')

@login_required(login_url="/venda/login")
def venda_concluida(request):
    return render(request, 'venda_concluida.html')

@login_required(login_url="/venda/login")
def vendas_realizadas(request):
    vendas = Venda.objects.filter(finalizado=True)
    return render(request, 'vendas_realizadas.html', {'vendas': vendas})

@login_required(login_url="/venda/login")
def detalhes_venda(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    itens = venda.itens.all()
    return render(request, 'detalhes_venda.html', {'venda': venda, 'itens': itens})



try:
    import plotly.express as px
    import plotly.graph_objs as go
    import pandas as pd
except ImportError as e:
    print(f"Erro de importação: {e}")

@login_required(login_url="/venda/login")
def visualizar_vendas(request):
    current_year = timezone.now().year

    # Gráfico de Linha: Custo Total e Venda Total Mensal do Ano Corrente
    vendas = Venda.objects.filter(data_hora__year=current_year, finalizado=True)
    vendas_mensais = vendas.annotate(mes=ExtractMonth('data_hora')).values('mes').annotate(
        total_venda=Sum('total'),
        total_custo=Sum('itens__produto__preco_custo')
    ).order_by('mes')

    meses = list(range(1, 13))
    total_venda = [0] * 12
    total_custo = [0] * 12

    for v in vendas_mensais:
        total_venda[v['mes'] - 1] = v['total_venda']
        total_custo[v['mes'] - 1] = v['total_custo']

    fig_linha = go.Figure()
    fig_linha.add_trace(go.Scatter(x=meses, y=total_venda, mode='lines+markers', name='Total Venda'))
    fig_linha.add_trace(go.Scatter(x=meses, y=total_custo, mode='lines+markers', name='Total Custo'))
    graph_linha = fig_linha.to_html(full_html=False)

    # Gráfico de Barras: Quantidade Vendida Mensal do Ano Corrente
    produtos_vendidos = ItemVenda.objects.filter(venda__data_hora__year=current_year, venda__finalizado=True).values(
        'produto__nome').annotate(total_vendido=Sum('quantidade')).order_by('produto__nome')

    nomes_produtos = [p['produto__nome'] for p in produtos_vendidos]
    quantidade_vendida = [p['total_vendido'] for p in produtos_vendidos]

    fig_barras = go.Figure()
    fig_barras.add_trace(go.Bar(x=nomes_produtos, y=quantidade_vendida, name='Quantidade Vendida'))
    graph_barras = fig_barras.to_html(full_html=False)

    # Gráfico de Dispersão: Percentual de Lucro dos Produtos Vendidos Mensal do Ano Corrente
    percentual_lucro = [
        (Decimal(venda.total) - Decimal(venda.itens.aggregate(Sum('produto__preco_custo'))['produto__preco_custo__sum'])) / Decimal(venda.total) * Decimal(100)
        for venda in vendas if venda.total > 0
    ]

    fig_dispersao = go.Figure()
    fig_dispersao.add_trace(go.Scatter(x=meses, y=percentual_lucro, mode='lines+markers', name='Percentual de Lucro'))

    # Atualizar layout do gráfico
    fig_dispersao.update_layout(
        title='Percentual de Lucro dos Produtos Vendidos Mensal',
        xaxis_title='Mês',
        yaxis_title='Percentual de Lucro (%)',
        legend_title='Legenda'
    )

    graph_dispersao = fig_dispersao.to_html(full_html=False)

    # Gráfico de Pizza: Top 3 Produtos Mais Vendidos em Quantidade Mensal do Ano Corrente
    top_produtos = produtos_vendidos[:3]
    top_produtos_nomes = [p['produto__nome'] for p in top_produtos]
    top_produtos_quantidade = [p['total_vendido'] for p in top_produtos]

    fig_pizza = px.pie(names=top_produtos_nomes, values=top_produtos_quantidade, title='Top 3 Produtos Mais Vendidos')
    graph_pizza = fig_pizza.to_html(full_html=False)

    current_year = timezone.now().year

    current_year = timezone.now().year

    # Gráfico de Barras e Linha: Grupos de Produtos Mais Vendidos com Meta
    grupos_vendidos = ItemVenda.objects.filter(
        venda__data_hora__year=current_year,
        venda__finalizado=True
    ).values('produto__grupo__nome').annotate(
        total_vendido=Sum('quantidade')
    ).filter(
        total_vendido__gte=10
    ).order_by('-total_vendido')[:4]

    nomes_grupos = [g['produto__grupo__nome'] for g in grupos_vendidos]
    quantidade_grupos = [g['total_vendido'] for g in grupos_vendidos]

    fig_barras_linha = go.Figure()
    fig_barras_linha.add_trace(go.Bar(x=nomes_grupos, y=quantidade_grupos, name='Quantidade Vendida', marker_color='blue'))

    # Adicionar linha de meta
    meta = 1000
    fig_barras_linha.add_trace(go.Scatter(x=nomes_grupos, y=[meta] * len(nomes_grupos), mode='lines', name='Meta', line=dict(color='red', dash='dash')))

    # Atualizar layout do gráfico
    fig_barras_linha.update_layout(
        title='Grupos de Produtos Mais Vendidos com Meta',
        xaxis_title='Grupo de Produtos',
        yaxis_title='Quantidade Vendida',
        legend_title='Legenda',
        barmode='group'
    )

    graph_barras_linha = opy.plot(fig_barras_linha, auto_open=False, output_type='div')

    #Tabela Analitica
    estoque_baixo_limite = 100
    produtos_estoque_baixo = Produto.objects.filter(estoque__lt=estoque_baixo_limite).order_by('-estoque')
        
    
    context = {
        'graph_linha': graph_linha,
        'graph_barras': graph_barras,
        'graph_dispersao': graph_dispersao,
        'graph_pizza': graph_pizza,
        'graph_barras_linha': graph_barras_linha,
        'produtos_estoque_baixo': produtos_estoque_baixo,
    }

    return render(request, 'visualizar_vendas.html', context)