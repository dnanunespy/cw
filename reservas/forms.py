# reservas/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Reserva
from .models import EspacoCoworking






# reservas/forms.py
class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = [ 'data_reserva', 'hora_inicio', 'hora_fim']
        widgets = {
            'data_reserva': forms.DateInput(attrs={'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fim': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        self.espaco = kwargs.pop('espaco', None)
        super(ReservaForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        data_reserva = cleaned_data.get('data_reserva')
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fim = cleaned_data.get('hora_fim')


        # Verifica se a data está no passado
        if data_reserva and data_reserva < timezone.now().date():
            print('Data passada!')
            raise ValidationError('Não é possível fazer reservas para datas passadas.')


        # Verifica se o horário de início é anterior ao horário de fim
        if hora_inicio and hora_fim and hora_inicio >= hora_fim:
            print('Hora errada!')
            raise ValidationError('O horário de início deve ser anterior ao horário de fim.')
       

        # Verifica conflitos de horário usando o espaço passado na view
        if data_reserva and hora_inicio and hora_fim:
            conflitos = Reserva.objects.filter(
                espaco=self.espaco,
                data_reserva=data_reserva,
                hora_inicio__lt=hora_fim,
                hora_fim__gt=hora_inicio
            )
            if conflitos.exists():
                print('Conflitou!')
                raise ValidationError('Já existe uma reserva para este horário.')

        return cleaned_data
    
 

class EspacoCoworkingForm(forms.ModelForm):
    # Campo para upload de múltiplas imagens
    imagens = forms.FileField(required=False, widget=forms.FileInput(), help_text="Selecione as imagens para upload")

    class Meta:
        model = EspacoCoworking
        fields = '__all__'
        exclude = ['proprietario']  # Não permita que o proprietário seja alterado        
