# reservas/models.py
from django.db import models
from django.contrib.auth.models import User


class EspacoCoworking(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=200)
    frase_destaque = models.CharField(max_length=100, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    capacidade = models.IntegerField()
    preco_por_hora = models.DecimalField(max_digits=10, decimal_places=2)
   #foto = models.ImageField(upload_to='fotos/', blank=True, null=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    prioridade = models.IntegerField(default=0, blank=True, null=True)

    # DETALHES DO ESPAÇO 
    #descricao_espaco = models.TextField(blank=True, null=True)

    # DADOS DO ESPAÇO
    palavras_chave = models.TextField(blank=True, null=True, help_text='Separado por -')
    instagram = models.URLField(max_length=255, blank=True, null=True)
    facebook = models.URLField(max_length=255, blank=True, null=True)
    linkedin = models.URLField(max_length=255, blank=True, null=True)
    nome_espaco = models.CharField(max_length=255, blank=True, null=True)
    razao_social = models.CharField(max_length=255, blank=True, null=True)
    cep = models.CharField(max_length=20, blank=True, null=True)
    pais = models.CharField(max_length=100, blank=True, null=True)
    uf = models.CharField(max_length=2, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    logradouro = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=10, blank=True, null=True)
    complemento = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    foto_horizontal = models.ImageField(upload_to='fotos_espaco/', blank=True, null=True)

    # DADOS PESSOAIS
    nome_proprietario = models.CharField(max_length=255, blank=True, null=True)
    email_proprietario = models.EmailField(blank=True, null=True)
    telefone_proprietario = models.CharField(max_length=20, blank=True, null=True)
    nome_gerente = models.CharField(max_length=255, blank=True, null=True)
    email_gerente = models.EmailField(blank=True, null=True)
    telefone_gerente = models.CharField(max_length=20, blank=True, null=True)

    # DADOS BANCÁRIOS
    titular_conta = models.CharField(max_length=255, blank=True, null=True)
    banco = models.CharField(max_length=100, blank=True, null=True)
    agencia = models.CharField(max_length=20, blank=True, null=True)
    conta = models.CharField(max_length=20, blank=True, null=True)
    tipo_conta = models.CharField(max_length=50, blank=True, null=True)
    tipo_pix = models.CharField(max_length=50, blank=True, null=True)
    pix = models.CharField(max_length=100, blank=True, null=True)


    # DIFERENCIAIS OFERECIDOS
    cafe = models.BooleanField(default=False)
    cha = models.BooleanField(default=False)
    massagem = models.BooleanField(default=False)
    outros_diferenciais = models.CharField(max_length=255, blank=True, null=True)

    # SOBRE AS ÁREAS COMUNS
    wifi = models.BooleanField(default=False)
    acessibilidade = models.BooleanField(default=False)
    acesso24h = models.BooleanField(default=False)
    playground_kids = models.BooleanField(default=False)
    ar_condicionado = models.BooleanField(default=False)
    area_alimentacao = models.BooleanField(default=False)
    biblioteca = models.BooleanField(default=False)
    cabine_call = models.BooleanField(default=False)
    cozinha = models.BooleanField(default=False)
    espaco_pet = models.BooleanField(default=False)
    espaco_convivencia = models.BooleanField(default=False)
    lounge = models.BooleanField(default=False)
    galeria_arte = models.BooleanField(default=False)
    geladeira = models.BooleanField(default=False)
    gerador_eletricidade = models.BooleanField(default=False)
    jardim = models.BooleanField(default=False)
    quadro_branco = models.BooleanField(default=False)
    recepcao = models.BooleanField(default=False)
    sala_descompressao = models.BooleanField(default=False)
    sala_jogos = models.BooleanField(default=False)
    varanda = models.BooleanField(default=False)
    vestuario = models.BooleanField(default=False)
    velocidade_internet = models.CharField(max_length=50, blank=True, null=True)

    # OUTROS SERVIÇOS OFERECIDOS NO SEU ESPAÇO
    auditorio = models.BooleanField(default=False)
    cafeteria = models.BooleanField(default=False)
    coliving = models.BooleanField(default=False)
    espaco_eventos = models.BooleanField(default=False)
    estudio_gravacao = models.BooleanField(default=False)
    restaurante = models.BooleanField(default=False)

    # FOTOS
    fotos_area_comum = models.ImageField(upload_to='fotos_areas_comuns/', blank=True, null=True)
    fotos_area_compartilhada = models.ImageField(upload_to='fotos_areas_compartilhadas/', blank=True, null=True)
    fotos_salas_privativas = models.ImageField(upload_to='fotos_salas_privativas/', blank=True, null=True)
    outras_fotos = models.ImageField(upload_to='outras_fotos/', blank=True, null=True)


    # Definindo um relacionamento com o usuário como proprietário
    proprietario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Espaço de Coworking"
        verbose_name_plural = "Espaços de Coworking"
        ordering = ['prioridade']  # Ordena os espaços pelo nome de forma padrão


class ImagemEspacoCoworking(models.Model):
    espaco = models.ForeignKey(EspacoCoworking, related_name='imagens', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='fotos/')

    def __str__(self):
        return f"Imagem de {self.espaco.nome}"        





class RecursosEspacoCoworking(models.Model):
    espaco_coworking = models.ForeignKey(EspacoCoworking, on_delete=models.CASCADE, related_name='recursos')
    nome_recurso = models.CharField(max_length=100)
    descricao = models.TextField()
    quantidade = models.PositiveIntegerField()
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome_recurso} - {self.espaco_coworking.nome}"
    
    class Meta:
        verbose_name = "Recurso"
        verbose_name_plural = "Recursos"
        ordering = ['nome_recurso']  # Ordena os espaços pelo nome de forma padrão










class Reserva(models.Model):
    espaco = models.ForeignKey(EspacoCoworking, on_delete=models.CASCADE)
    usuario = models.ForeignKey( User, on_delete=models.CASCADE, blank=True, null=True)
    data_reserva = models.DateField()
    recurso = models.ForeignKey(RecursosEspacoCoworking, on_delete=models.CASCADE) 
    hora_inicio = models.TimeField(blank=True, null=True)
    hora_fim = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.espaco.nome} - {self.data_reserva} - {self.hora_inicio} to {self.hora_fim}"

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        # Ordena as reservas por data e hora
        ordering = ['data_reserva', 'hora_inicio']

    def save(self, *args, **kwargs):
        # Adicionar lógica para validação de reservas aqui, se necessário
        super().save(*args, **kwargs)
