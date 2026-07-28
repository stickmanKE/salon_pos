from django.contrib import admin
from .models import Salon


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'location', 'is_active', 'created_at')
    search_fields = ('name', 'phone', 'location')
    list_filter = ('is_active',)