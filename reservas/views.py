from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import EspacoCoworking, Reserva, RecursosEspacoCoworking
from .forms import ReservaForm
from django.shortcuts import render

from django.shortcuts import render
from django.core.serializers import serialize
import json


def index(request):
    espacos = EspacoCoworking.objects.all()
   
    espacosJ = EspacoCoworking.objects.all()
    espacos_json = serialize('json', espacosJ)
    
    espacos_json = json.loads(espacos_json)
    #print(json.dumps(espacos_json))

    context = {
        'espacos': espacos,
        'espacosJ': json.dumps(espacos_json)

    }

    return render(request, 'reservas/index.html', context)


'''@login_required
def detalhe_espaco(request, espaco_id):
    # Garante que o espaço pertence ao usuário
    espaco = get_object_or_404(
        EspacoCoworking, id=espaco_id, proprietario=request.user)
   
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.espaco = espaco
            reserva.usuario = request.user
            
            reserva.save()
            messages.success(request, 'Reserva feita com sucesso!')
            return redirect('lista_espacos')
    else:
        form = ReservaForm()
    return render(request, 'reservas/detalhe_espaco.html', {'espaco': espaco, 'form': form})'''




@login_required
def detalhe_espaco(request, espaco_id):
    espaco = get_object_or_404(EspacoCoworking, id=espaco_id)
    recursos = RecursosEspacoCoworking.objects.filter(espaco_coworking_id=espaco_id)

    # Verifica se o usuário tem permissão para ver o espaço
    if espaco.proprietario != request.user and not is_coworking_admin(request.user):
        return render(request, '403.html', status=403)

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.espaco = espaco
            reserva.usuario = request.user

            # Obtém o recurso selecionado a partir do campo select no form
            recurso_id = request.POST.get('recurso')
            recurso = get_object_or_404(RecursosEspacoCoworking, id=recurso_id)
            reserva.recurso = recurso  # Associa o recurso à reserva

            reserva.save()
            messages.success(request, 'Reserva feita com sucesso!')
            return redirect('lista_espacos')
    else:
        form = ReservaForm()

    return render(request, 'reservas/detalhe_espaco.html', {'espaco': espaco, 'form': form, 'recursos': recursos})











def lista_espacos(request):
    #print("Lista_espacos!!!")
    espacos = EspacoCoworking.objects.all()
    return render(request, 'reservas/lista_espacos.html', {'espacos': espacos})

# View para registro de novos usuários


def register(request):
    #print("Achou a função!!!!1")
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Conta criada com sucesso para {username}!')
            login(request, user)
            return redirect('lista_espacos')
    else:
        form = UserCreationForm()
    return render(request, 'reservas/register.html', {'form': form})


def is_coworking_admin(user):
    return user.groups.filter(name='Administradores de Coworking').exists()


@user_passes_test(is_coworking_admin)
@login_required
def gerenciar_espacos(request):
   # print("Opaaa!")
    espacos = EspacoCoworking.objects.filter(proprietario=request.user)
    return render(request, 'reservas/gerenciar_espacos.html', {'espacos': espacos})













def newsletter_signup(request):
    if request.method == 'POST':
        # Lógica para processar o formulário de inscrição
        # Redirecione para a página inicial ou qualquer outra página desejada
        return redirect('index')
    # Renderize o template de inscrição (se necessário)
    return render(request, 'reservas/newsletter_signup.html')
