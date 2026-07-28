from django.contrib import admin
from django.utils.html import format_html
from .models import Beverage, BeverageCategory, BeverageStock


@admin.register(BeverageCategory)
class BeverageCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'salon']
    search_fields = ['name']
    list_filter = ['salon']


@admin.register(Beverage)
class BeverageAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'size', 'selling_price',
        'cost_price', 'stock_status', 'is_active',
    ]
    list_filter = ['category', 'size', 'is_active', 'salon']
    search_fields = ['name', 'category__name']
    list_editable = ['selling_price', 'is_active']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Product Info', {
            'fields': ('salon', 'name', 'category', 'size', 'is_active'),
        }),
        ('Pricing', {
            'fields': ('selling_price', 'cost_price'),
        }),
        ('Stock', {
            'fields': ('stock_units', 'low_stock_threshold'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def stock_status(self, obj):
        if obj.stock_units == 0:
            return format_html(
                '<span style="background:#f44336;color:white;padding:2px 10px;border-radius:12px;font-size:11px">Out of stock</span>'
            )
        elif obj.is_low_stock:
            return format_html(
                '<span style="background:#ff9800;color:white;padding:2px 10px;border-radius:12px;font-size:11px">Low: {}</span>',
                obj.stock_units,
            )
        return format_html(
            '<span style="background:#4caf50;color:white;padding:2px 10px;border-radius:12px;font-size:11px">{} units</span>',
            obj.stock_units,
        )
    stock_status.short_description = 'Stock'


@admin.register(BeverageStock)
class BeverageStockAdmin(admin.ModelAdmin):
    list_display = ['beverage', 'movement_type', 'quantity', 'source', 'reference', 'created_at']
    list_filter = ['movement_type', 'source', 'created_at']
    search_fields = ['beverage__name', 'reference']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
