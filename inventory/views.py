from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Product, ProductCategory
from salons.utils import get_current_salon

@login_required
def products_page(request):
    """
    The main inventory/products list view.
    Filters products by the current user's salon and pre-loads categories.
    """
    salon = get_current_salon(request)
    
    if not salon:
        # Handle cases where the user isn't linked to a salon
        return render(request, 'inventory/list.html', {'products': []})

    # Optimized Query: 
    # 1. Filter by salon
    # 2. Use select_related to get category names in 1 database hit
    # 3. Filter for active products only (optional, depends on your preference)
    products = Product.objects.filter(
        salon=salon,
        is_active=True
    ).select_related('category').order_by('category__name', 'name')

    # Optional: Get categories for the sidebar or filter dropdown
    categories = ProductCategory.objects.filter(salon=salon)

    return render(request, 'inventory/list.html', {
        'products': products,
        'categories': categories,
        'salon': salon
    })