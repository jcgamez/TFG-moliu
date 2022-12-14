from django.contrib import admin
from django.contrib.auth.models import Group

admin.site.site_header = "Administración de Moliu"
admin.site.unregister(Group)
