from django.shortcuts import render, redirect
from django.db import transaction
from .forms import UsuarioForm, CustomLoginForm
from django.contrib import messages
from django.urls import reverse
from .models import Usuario, Chamado
from .forms import ChamadoForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test


def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            tipo_usuario = form.cleaned_data['tipo_usuario']
            matricula = form.cleaned_data['matricula']
            password = form.cleaned_data['password']
            nome_usuario = form.cleaned_data['nome_usuario']
            email = form.cleaned_data['email']

            # Alteração para criar usuário com matrícula ou SIAPE conforme o tipo de usuário
            if tipo_usuario == 'Servidor':
                siape = form.cleaned_data['siape']
                Usuario.objects.create_user(matricula=matricula, password=password, siape=siape, nome_usuario=nome_usuario, email=email, tipo_usuario=tipo_usuario)
            else:
                Usuario.objects.create_user(matricula=matricula, password=password, nome_usuario=nome_usuario, email=email, tipo_usuario=tipo_usuario)

            messages.success(request, f'O usuário {nome_usuario} foi cadastrado com sucesso!')
            return redirect('cadastrar_usuario')
    else:
        form = UsuarioForm()

    return render(request, 'cadastrar_usuario.html', {'form': form, 'show_message': False})


def fazer_login(request):
    if request.method == 'POST':
        # Note que não estamos passando o request para o formulário aqui
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('matricula')
            password = form.cleaned_data.get('password')

            print(f"Matrícula: {username}, Senha: {password}")
            user = authenticate(request=request, username=username, password=password)
            print(f"Resultado do authenticate: {user}")

            if user is not None:
                login(request, user)
                messages.success(request, "Login foi efetuado com sucesso!")
                next_url = request.POST.get('next', None)
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('abrir_chamados')
            else:
                messages.error(request, "Credenciais inválidas. Tente novamente.")
        else:
            messages.error(request, "Formulário inválido. Verifique os campos e tente novamente.")
    else:
        form = CustomLoginForm()

    return render(request, 'fazer_login.html', {'form': form})


@login_required
def abrir_chamados(request):
    if request.method == 'POST':  
        form = ChamadoForm(request.POST, request.FILES)
        if form.is_valid():
            chamado = form.save(commit=False)
            chamado.usuario = request.user 
            chamado.save()
            messages.success(request, "Chamado criado com sucesso!")
            return redirect(reverse('dashboard_chamados', kwargs={'estado': 'novos'}))
    else:
        form = ChamadoForm()

    return render(request, 'abrir_chamados.html', {'form': form})


def dashboard_chamados(request, estado='novos'):
    if request.method == 'POST':
        # Obter dados do formulário
        codigo = request.POST.get('codigo', 0)
        tipo = request.POST.get('tipo', '')
        categoria = request.POST.get('categoria', '')
        titulo = request.POST.get('titulo', '')
        descricao = request.POST.get('descricao', '')
        prioridade = request.POST.get('prioridade', '')
        responsavel_id = request.POST.get('responsavel', '')

        # Verificar se o responsável selecionado é um Servidor Técnico
        try:
            responsavel = Usuario.objects.get(id=responsavel_id, tipo_usuario='Servidor')
        except Usuario.DoesNotExist:
            responsavel = None

        # Criar o objeto de chamado e salvar se o responsável for um Servidor válido
        if responsavel:
            chamado = Chamado(
                usuario=request.user,
                codigo=codigo,
                tipo=tipo,
                categoria=categoria,
                titulo=titulo,
                descricao=descricao,
                prioridade=prioridade,
                responsavel=responsavel,
            )
            chamado.save()

    # Obter todos os técnicos para exibição no formulário
    servidores = Usuario.objects.filter(tipo_usuario='Servidor')

    # Defina a condição para filtrar os chamados com base no estado
    if estado == 'novos':
        chamados = Chamado.objects.filter(usuario=request.user, estado='Novos')
    elif estado == 'em_andamento':
        chamados = Chamado.objects.filter(usuario=request.user, estado='Em andamento')
    elif estado == 'finalizados':
        chamados = Chamado.objects.filter(usuario=request.user, estado='Finalizados')
    else:
        # Se o estado não for reconhecido, exiba todos os chamados
        chamados = Chamado.objects.filter(usuario=request.user)

    return render(request, 'dashboard_chamados.html', {'servidores': servidores, 'chamados': chamados, 'estado_atual': estado})


@transaction.atomic
def atualizar_chamados(request):
    # Função para atualizar os chamados
    def atualizar_chamados_estado(chamados, novo_estado):
        for chamado in chamados.order_by('id')[:5]:
            chamado.estado = novo_estado
            chamado.save()

    # Obter todos os chamados em estado 'Novos' do usuário
    chamados_novos = Chamado.objects.filter(usuario=request.user, estado='Novos')

    # Verificar se há mais de 5 chamados em estado 'Novos'
    if chamados_novos.count() >= 5:
        # Atualizar os 5 chamados mais antigos para estado 'Em andamento'
        atualizar_chamados_estado(chamados_novos, 'Em andamento')

    # Obter todos os chamados em estado 'Em andamento' do usuário
    chamados_andamento = Chamado.objects.filter(usuario=request.user, estado='Em andamento')

    # Verificar se há mais de 5 chamados em estado 'Em andamento'
    if chamados_andamento.count() >= 5:
        # Atualizar os 5 chamados mais antigos para estado 'Finalizados'
        atualizar_chamados_estado(chamados_andamento, 'Finalizados')

    # Redirecionar de volta para o painel de chamados
    return redirect(reverse('dashboard_chamados'))