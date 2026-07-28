from django.contrib import admin
from .models import Service, ServiceCategory, ServiceProduct

# =========================
# INLINES
# =========================
class ServiceProductInline(admin.TabularInline):
    """
    Allows you to add/remove product usage (like shampoo amount) 
    directly on the Service edit page.
    """
    model = ServiceProduct
    extra = 1 

# =========================
# CATEGORY ADMIN
# =========================
@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    # display the salon so we know which business owns which category
    list_display = ('name', 'salon')
    search_fields = ('name',)
    list_filter = ('salon',)

# =========================
# SERVICE ADMIN
# =========================
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    # This attaches the product usage management to the service page
    inlines = [ServiceProductInline]

    list_display = (
        'name', 
        'category', 
        'formatted_price', 
        'duration', 
        'salon', 
        'is_active'
    )
    
    list_filter = ('category', 'salon', 'is_active')
    search_fields = ('name', 'description')
    list_editable = ('is_active',)
    ordering = ('name',)
    
    actions = ['mark_inactive']

    # Custom Methods
    def formatted_price(self, obj):
        # Displays KSh 1,500 instead of just 1500.00
        return f"KSh {obj.price:,.0f}"
    formatted_price.short_description = "Price"

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
    mark_inactive.short_description = "Hide selected services from POS"