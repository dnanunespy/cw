from django.contrib import admin
from .models import EspacoCoworking, Reserva, RecursosEspacoCoworking

admin.site.register(EspacoCoworking)
admin.site.register(Reserva)
admin.site.register(RecursosEspacoCoworking)
