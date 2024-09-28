from django import forms
from django.contrib import admin
from .models import EspacoCoworking, ImagemEspacoCoworking, RecursosEspacoCoworking, Reserva

class ImagemEspacoCoworkingInline(admin.TabularInline):
    model = ImagemEspacoCoworking
    extra = 1

class EspacoCoworkingAdminForm(forms.ModelForm):
    # Campo para upload de imagens múltiplas
    imagens = forms.FileField(required=False, label='Upload de Imagens', help_text="Selecione múltiplas imagens", widget=forms.FileInput)

    class Meta:
        model = EspacoCoworking
        fields = '__all__'

class EspacoCoworkingAdmin(admin.ModelAdmin):
    form = EspacoCoworkingAdminForm
    inlines = [ImagemEspacoCoworkingInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Pegando as imagens carregadas manualmente
        imagens = request.FILES.getlist('imagens')
        for imagem in imagens:
            # Salvando cada imagem no modelo ImagemEspacoCoworking
            ImagemEspacoCoworking.objects.create(espaco=obj, imagem=imagem)

admin.site.register(EspacoCoworking, EspacoCoworkingAdmin)
admin.site.register(Reserva)
admin.site.register(RecursosEspacoCoworking)
