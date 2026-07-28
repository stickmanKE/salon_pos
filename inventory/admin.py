from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import (
    Product, ProductCategory, StockMovement, 
    HumanHair, HairTexture, HairStockMovement
)

# ── Product Category ─────────────────────────────────────────────
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'salon')
    search_fields = ('name',)
    list_filter = ('salon',)


# ── Product ──────────────────────────────────────────────────────
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'product_type',
        'selling_price', 'cost_price',
        'stock_quantity', 'stock_status',
        'is_active', 'created_at', 'updated_at',
    )
    list_filter   = ('salon', 'category', 'product_type', 'is_active')
    search_fields = ('name', 'description')
    list_editable = ('selling_price', 'stock_quantity', 'is_active')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Product Info', {
            'fields': ('salon', 'category', 'name', 'description', 'product_type', 'unit_type', 'is_active'),
        }),
        ('Pricing', {
            'fields': ('cost_price', 'selling_price'),
        }),
        ('Stock', {
            'fields': ('stock_quantity',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def stock_status(self, obj):
        if obj.stock_quantity <= 0:
            return mark_safe('<span style="color:#f44336;font-weight:bold">❌ Out of Stock</span>')
        if obj.stock_quantity < 5:
            # We format the string first, then wrap in format_html to avoid SafeString errors
            qty = "{:,.1f}".format(obj.stock_quantity)
            return format_html('<span style="color:#ff9800;font-weight:bold">⚠️ Low ({})</span>', qty)
        return mark_safe('<span style="color:#4caf50">✅ OK</span>')
    stock_status.short_description = 'Status'
    stock_status.admin_order_field = 'stock_quantity'


# ── Stock Movement ───────────────────────────────────────────────
@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display  = ('product', 'movement_type', 'quantity', 'source', 'reference', 'created_at')
    list_filter   = ('movement_type', 'source', 'created_at')
    search_fields = ('product__name', 'reference')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'


# ── Hair Texture ─────────────────────────────────────────────────
@admin.register(HairTexture)
class HairTextureAdmin(admin.ModelAdmin):
    list_display  = ('name', 'salon')
    search_fields = ('name',)
    list_filter   = ('salon',)


# ── Hair Stock Movement Inline ────────────────────────────────────
class HairStockMovementInline(admin.TabularInline):
    model   = HairStockMovement
    extra   = 1
    fields  = ('movement_type', 'bundles', 'source', 'reference', 'notes')
    readonly_fields = ()

    def get_extra(self, request, obj=None, **kwargs):
        return 0 if obj and obj.movements.exists() else 1


# ── Human Hair ───────────────────────────────────────────────────
@admin.register(HumanHair)
class HumanHairAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'origin', 'texture', 'length_inch',
        'selling_price', 'cost_price',
        'stock_badge', 'stock_value_display',
        'is_active', 'created_at',
    )
    list_filter   = ('origin', 'texture', 'is_active', 'salon')
    search_fields = ('name', 'origin', 'texture__name')
    list_editable = ('selling_price', 'is_active')
    
    readonly_fields = (
        'created_at', 'updated_at', 'stock_value', 
        'potential_revenue', 'potential_profit'
    )
    
    date_hierarchy  = 'created_at'
    inlines = [HairStockMovementInline]

    fieldsets = (
        ('Hair Identity', {
            'fields': ('salon', 'name', 'origin', 'texture', 'length_inch', 'is_active'),
        }),
        ('Pricing (per bundle)', {
            'fields': ('cost_price', 'selling_price'),
        }),
        ('Stock Status & Financials', {
            'fields': (
                'bundles_in_stock', 'low_stock_alert', 
                'stock_value', 'potential_revenue', 'potential_profit'
            ),
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def stock_badge(self, obj):
        if obj.is_out_of_stock:
            return mark_safe(
                '<span style="background:#f44336;color:white;'
                'padding:2px 10px;border-radius:12px;'
                'font-size:11px">Out of Stock</span>'
            )

        if obj.is_low_stock:
            return mark_safe(
                '<span style="background:#ff9800;color:white;'
                'padding:2px 10px;border-radius:12px;'
                'font-size:11px">Low Stock</span>'
            )

        return mark_safe(
            '<span style="background:#4caf50;color:white;'
            'padding:2px 10px;border-radius:12px;'
            'font-size:11px">In Stock</span>'
        )
    stock_badge.short_description = "Stock Status"

    def stock_value_display(self, obj):
        # FIX: We format the number into a string first. 
        # This prevents the 'f' ValueError when format_html treats the value as a SafeString.
        formatted_val = "{:,.0f}".format(obj.stock_value or 0)
        return format_html('KSh {}', formatted_val)
    stock_value_display.short_description = 'Stock Value'


# ── Hair Stock Movement ──────────────────────────────────────────
@admin.register(HairStockMovement)
class HairStockMovementAdmin(admin.ModelAdmin):
    list_display  = ('hair', 'movement_type', 'bundles', 'source', 'reference', 'created_at')
    list_filter   = ('movement_type', 'source', 'created_at')
    search_fields = ('hair__name', 'reference')
    readonly_fields = ('created_at',)
    date_hierarchy  = 'created_at'