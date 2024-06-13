from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Fornecedor, Grupo, Subgrupo
from .forms import FornecedorForm, GrupoForm, SubgrupoForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from rolepermissions.roles import assign_role
from rolepermissions.decorators import has_role_decorator ,has_permission_decorator
from site_django.roles import Gerente, Vendedor
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