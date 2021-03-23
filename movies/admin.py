from django.contrib import admin
from.models import *
# Registrace modelů v administraci aplikace
admin.site.register(Genre)
admin.site.register(Film)
admin.site.register(Attachment)
