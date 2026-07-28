from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Service, ServiceCategory
from inventory.models import Product
from salons.utils import get_current_salon

@login_required
def pos_view(request):
    """The main POS checkout interface"""
    salon = get_current_salon(request)
    print("SALON:", salon)  # 🛠️ TEMP DEBUG
    
    if not salon:
        return render(request, "sales/pos.html", {"services": [], "products": []})

    # 1. Fetch Categories
    categories = ServiceCategory.objects.filter(salon=salon)

    # 2. Fetch Services (Ordered by category for template regrouping)
    services = Service.objects.filter(
        salon=salon, 
        is_active=True
    ).select_related('category').order_by('category__name', 'name')

    # 3. Fetch Products
    products = Product.objects.filter(
        salon=salon, 
        is_active=True
    )

    return render(request, "sales/pos.html", {
        "services": services,
        "products": products,
        "categories": categories,
    })

@login_required
def services_list(request):
    """The management page (Services Page) where you view/edit your service menu"""
    salon = get_current_salon(request)
    
    if not salon:
        return render(request, "services/list.html", {"services": [], "categories": []})

    categories = ServiceCategory.objects.filter(salon=salon)
    services = Service.objects.filter(
        salon=salon
    ).select_related('category').order_by('category__name', 'name')

    return render(request, "services/list.html", {
        "services": services,
        "categories": categories
    })