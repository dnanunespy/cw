from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from .models import EspacoCoworking, Reserva, RecursosEspacoCoworking, ImagemEspacoCoworking
from .forms import ReservaForm, EspacoCoworkingForm
from .forms import RecursosEspacoCoworkingForm



from django.shortcuts import render

from django.shortcuts import render
from django.core.serializers import serialize
import json

from django.core.paginator import Paginator



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



#realizando reserva
@login_required
def detalhe_espaco(request, espaco_id):
    espaco = get_object_or_404(EspacoCoworking, id=espaco_id)
    recursos = RecursosEspacoCoworking.objects.filter(espaco_coworking_id=espaco_id)

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

    # Lista de horas inteiras de 00:00 até 23:00
    horas = ['{:02d}:00'.format(h) for h in range(24)]

    return render(request, 'reservas/detalhe_espaco.html', {
        'espaco': espaco,
        'form': form,
        'recursos': recursos,
        'horas': horas  # Passando a lista de horas para o template
    })


#editando reservas
@login_required
def listar_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user)
    return render(request, 'reservas/listar_reservas.html', {'reservas': reservas})

@login_required
def editar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reserva atualizada com sucesso!')
            return redirect('listar_reservas')
    else:
        form = ReservaForm(instance=reserva)
    return render(request, 'reservas/editar_reserva.html', {'form': form})

@login_required
def excluir_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)
    if request.method == 'POST':
        reserva.delete()
        messages.success(request, 'Reserva excluída com sucesso!')
        return redirect('listar_reservas')
    return render(request, 'reservas/excluir_reserva.html', {'reserva': reserva})





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
        espaco = EspacoCoworking()  # Cria uma nova instância sem pk

    if request.method == 'POST':
        print('------ entrou no post')

        # Cria um dicionário a partir de request.POST
        post_data = request.POST.copy()  # Copia os dados para um dicionário mutável

        # Substitui a vírgula por ponto nos campos de preço e coordenadas
        if 'preco_por_hora' in post_data:
            post_data['preco_por_hora'] = post_data['preco_por_hora'].replace(',', '.')

        if 'latitude' in post_data:
            post_data['latitude'] = post_data['latitude'].replace(',', '.')

        if 'longitude' in post_data:
            post_data['longitude'] = post_data['longitude'].replace(',', '.')

        # Formulário principal do espaço de coworking
        form = EspacoCoworkingForm(post_data, request.FILES, instance=espaco)
        print(form.errors)

        if form.is_valid():
            espaco = form.save(commit=False)
            espaco.proprietario = request.user  # Define o proprietário como o usuário logado
            espaco.save()  # Salva o espaço antes de adicionar imagens

            # Agora processa as múltiplas imagens carregadas
            imagens = request.FILES.getlist('imagens')
            for imagem in imagens:
                ImagemEspacoCoworking.objects.create(espaco=espaco, imagem=imagem)

            return redirect('administrar_espacos')  # Redireciona para a página de administração de espaços

    else:
        form = EspacoCoworkingForm(instance=espaco)

    return render(request, 'reservas/editar_espaco_coworking.html', {'form': form, 'espaco': espaco})


@login_required
def cadastrar_recurso_espaco(request, espaco_id):
    espaco = get_object_or_404(EspacoCoworking, pk=espaco_id)

    if request.method == 'POST':
        form = RecursosEspacoCoworkingForm(request.POST)
        if form.is_valid():
            recurso = form.save(commit=False)
            recurso.espaco_coworking = espaco
            recurso.save()
            return redirect('detalhe_espaco', espaco_id=espaco.id)
    else:
        form = RecursosEspacoCoworkingForm()

    return render(request, 'reservas/cadastrar_recurso.html', {'form': form, 'espaco': espaco})




@login_required
def excluir_imagem(request, imagem_id):
    if request.method == 'POST':
        imagem = get_object_or_404(ImagemEspacoCoworking, id=imagem_id)
        imagem.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)



def lista_espacos(request):
    # Obtém todos os espaços de coworking
    espacos = EspacoCoworking.objects.all()
    
    # Configura a paginação: 6 espaços por página (você pode ajustar esse valor)
    paginator = Paginator(espacos, 6)
    
    # Obtém o número da página atual a partir da URL (padrão é a primeira página)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Serializa os dados dos espaços para JSON
    espacos_json = serialize('json', espacos)

    # Contexto a ser passado para o template
    context = {
        'page_obj': page_obj,  # Passa os objetos paginados para o template
        'espacosJ': espacos_json  # Serializado diretamente para o template
    }
    
    return render(request, 'reservas/lista_espacos.html', context)


def lista_espacos_original(request):
    #print("Lista_espacos!!!")
    espacos = EspacoCoworking.objects.all()
    
    espacosJ = EspacoCoworking.objects.all()
    espacos_json = serialize('json', espacosJ)
    espacos_json = json.loads(espacos_json)

    context = {
        'espacos': espacos,
        'espacosJ': json.dumps(espacos_json)
    }
    return render(request, 'reservas/lista_espacos.html', context)


def administrar_espacos(request):
    #print("Lista_espacos!!!")
    espacos = EspacoCoworking.objects.filter(proprietario_id=request.user.id)
    return render(request, 'reservas/administrar_coworkings.html', {'espacos': espacos})



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
