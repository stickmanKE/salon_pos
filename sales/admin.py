from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Count
from django.utils.timezone import now
from datetime import date, timedelta
from .models import Sale, SaleItem, Payment


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0
    fields = ['name', 'item_type', 'worker', 'quantity', 'price']
    readonly_fields = []
    autocomplete_fields = ['worker']


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    fields = ['method', 'amount', 'reference']


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'client', 'payment_badge', 'formatted_total',
        'discount_display', 'is_paid', 'item_count', 'created_at',
    ]
    list_filter = ['is_paid', 'payment_method', 'created_at', 'salon']
    search_fields = ['client__name', 'client__phone', 'id']
    readonly_fields = ['total_amount']
    inlines = [SaleItemInline, PaymentInline]
    ordering = ['-created_at']
    date_hierarchy = 'created_at'

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'

    def formatted_total(self, obj):
        return f"KSh {obj.total_amount:,.0f}"
    formatted_total.short_description = 'Total'

    def discount_display(self, obj):
        if obj.discount_amount:
            return format_html(
                '<span style="color:#e53e3e">-KSh {}</span>',
                f"{obj.discount_amount:,.0f}"
            )
        return '-'
    discount_display.short_description = 'Discount'

    def payment_badge(self, obj):
        colors = {'cash': '#4caf50', 'mpesa': '#2196f3', 'card': '#9c27b0', 'mixed': '#ff9800'}
        color = colors.get(obj.payment_method, '#9e9e9e')
        label = obj.get_payment_method_display() if obj.payment_method else 'N/A'
        return format_html(
            '<span style="background:{};color:white;padding:2px 10px;border-radius:12px;font-size:11px">{}</span>',
            color, label
        )
    payment_badge.short_description = 'Payment'

    def changelist_view(self, request, extra_context=None):
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        month_start = today.replace(day=1)

        def rev(qs):
            return qs.filter(is_paid=True).aggregate(t=Sum('total_amount'))['t'] or 0

        base = Sale.objects.filter(salon__isnull=False)

        extra_context = extra_context or {}
        extra_context['dashboard_stats'] = {
            'sales_today': base.filter(created_at__date=today).count(),
            'revenue_today': rev(base.filter(created_at__date=today)),
            'revenue_week': rev(base.filter(created_at__date__gte=week_start)),
            'revenue_month': rev(base.filter(created_at__date__gte=month_start)),
        }
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ['sale', 'name', 'item_type', 'worker', 'quantity', 'price']
    list_filter = ['item_type', 'worker']
    search_fields = ['name', 'worker__full_name', 'sale__id']
    autocomplete_fields = ['worker']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['sale', 'formatted_amount', 'method', 'reference', 'created_at']
    list_filter = ['method', 'created_at']
    search_fields = ['reference', 'sale__id']
    date_hierarchy = 'created_at'

    def formatted_amount(self, obj):
        return f"KSh {obj.amount:,.0f}"
    formatted_amount.short_description = 'Amount'
