from django.contrib import admin

from flight.models import Crew, Airplane, AirplaneType, Flight

admin.site.register(Crew)
admin.site.register(Airplane)
admin.site.register(AirplaneType)
admin.site.register(Flight)
