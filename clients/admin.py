from django.contrib import admin
from django.utils.html import format_html
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'salon', 'visit_count_display', 'total_spent_display', 'created_at')
    search_fields = ('name', 'phone', 'email')
    list_filter = ('salon', 'created_at')
    readonly_fields = ('created_at', 'visit_count_display', 'total_spent_display')

    def visit_count_display(self, obj):
        try:
            return obj.sale_set.filter(is_paid=True).count()
        except Exception:
            return 0
    visit_count_display.short_description = 'Visits'

    def total_spent_display(self, obj):
        try:
            from django.db.models import Sum
            total = obj.sale_set.filter(is_paid=True).aggregate(t=Sum('total_amount'))['t']
            total = float(total) if total else 0.0
            return format_html('KSh {:,.0f}', total)
        except Exception:
            return 'KSh 0'
    total_spent_display.short_description = 'Total Spent'

    