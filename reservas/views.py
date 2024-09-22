from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import EspacoCoworking, Reserva, RecursosEspacoCoworking
from .forms import ReservaForm, EspacoCoworkingForm
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
    #if espaco.proprietario != request.user and not is_coworking_admin(request.user):
    #    return render(request, '403.html', status=403)

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




@login_required
def editar_espaco(request, pk):
    espaco = get_object_or_404(EspacoCoworking, pk=pk)

    # Verifica se o usuário logado é o proprietário do espaço
    if espaco.proprietario != request.user:
        return redirect('pagina_inicial')

    if request.method == 'POST':
        form = EspacoCoworkingForm(request.POST, request.FILES, instance=espaco)
        if form.is_valid():
            form.save()
            return redirect('detalhe_espaco', espaco_id=espaco.pk)
    else:
        form = EspacoCoworkingForm(instance=espaco)

    return render(request, 'editar_espaco.html', {'form': form})


@login_required
def editar_espaco_coworking(request, espaco_id=None):
    if espaco_id:  # Se o pk existir, estamos editando um espaço
        espaco = get_object_or_404(EspacoCoworking, pk=espaco_id)
    else:  # Se não houver pk, estamos criando um novo espaço
        espaco = None

    if request.method == 'POST':
        print('------ entrou no post')

        # Cria um dicionário a partir de request.POST
        post_data = request.POST.copy()  # Copia os dados para um dicionário mutável

        # Substitui a vírgula por ponto no campo preco_por_hora
        if 'preco_por_hora' in post_data:
            post_data['preco_por_hora'] = post_data['preco_por_hora'].replace(',', '.')

        if 'latitude' in post_data:
            post_data['latitude'] = post_data['latitude'].replace(',', '.')

        if 'longitude' in post_data:
            post_data['longitude'] = post_data['longitude'].replace(',', '.')        

        form = EspacoCoworkingForm(post_data, request.FILES, instance=espaco)
        
        print(form.errors)
        if form.is_valid():
         
            espaco = form.save(commit=False)

         
            espaco.proprietario = request.user  # Define o proprietário como o usuário logado
            espaco.save()
            return redirect('detalhe_espaco', espaco_id=espaco.pk)  # Redireciona para a página de detalhes
    else:
        form = EspacoCoworkingForm(instance=espaco)

    print(form.instance.preco_por_hora)

    print(form.instance.preco_por_hora)
    return render(request, 'reservas/editar_espaco_coworking.html', {'form': form})










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
