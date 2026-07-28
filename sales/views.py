import json
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum

# Models
from .models import Sale, SaleItem
from clients.models import Client
from salon_services.models import Service
from inventory.models import Product, StockMovement
from salons.utils import get_current_salon


# 📌 POS DASHBOARD
@login_required
def pos_dashboard(request):
    """ View to handle the Point of Sale interface """
    salon = get_current_salon(request)

    services = Service.objects.filter(salon=salon)
    products = Product.objects.filter(salon=salon)
    clients = Client.objects.filter(salon=salon)

    return render(request, "sales/pos.html", {
        "services": services,
        "products": products,
        "clients": clients
    })


# 📌 SALES LIST VIEW
@login_required
def sales_list(request):
    salon = get_current_salon(request)

    if not salon:
        sales = Sale.objects.none()
        clients = Client.objects.none()
        total_revenue = 0
    else:
        sales = Sale.objects.filter(
            salon=salon,
            is_paid=True
        ).select_related('client').order_by('-created_at')

        clients = Client.objects.filter(
            salon=salon
        ).order_by('name')

        total_revenue = sales.aggregate(
            total=Sum('total_amount')
        )['total'] or 0

    context = {
        "sales": sales,
        "clients": clients,
        "total_revenue": total_revenue
    }

    return render(request, "sales/list.html", context)


# 📌 CREATE SALE
@login_required
def create_sale(request):
    salon = get_current_salon(request)

    if not salon:
        messages.error(request, "No salon assigned to your account.")
        return redirect("sales_list")

    if request.method == "POST":
        client_id = request.POST.get("client_id")
        cart_data = request.POST.get("cart_data")

        try:
            cart = json.loads(cart_data)
        except (json.JSONDecodeError, TypeError):
            messages.error(request, "Invalid cart data.")
            return redirect("pos_dashboard")

        with transaction.atomic():
            client = Client.objects.filter(id=client_id, salon=salon).first() if client_id else None

            sale = Sale.objects.create(
                salon=salon,
                user=request.user,
                client=client,
                is_paid=True
            )

            for item in cart:
                service, product = None, None
                item_type = item.get('type')
                item_id = item.get('id')

                if item_type == 'service':
                    service = Service.objects.filter(id=item_id, salon=salon).first()

                elif item_type in ['product', 'product_sale']:
                    product = Product.objects.filter(id=item_id, salon=salon).first()

                    if product:
                        StockMovement.create_movement(
                            product=product,
                            quantity=item.get('quantity', 1),
                            movement_type='out',
                            source='sale',
                            reference=f"Sale #{sale.id}"
                        )

                elif item_type == 'product_use':
                    product = Product.objects.filter(id=item_id, salon=salon).first()

                    if product:
                        StockMovement.create_movement(
                            product=product,
                            quantity=item.get('quantity', 1),
                            movement_type='out',
                            source='service',
                            reference=f"Service in Sale #{sale.id}"
                        )

                SaleItem.objects.create(
                    sale=sale,
                    service=service,
                    product=product,
                    name=item.get('name'),
                    item_type=item_type,
                    price=item.get('price'),
                    quantity=item.get('quantity', 1)
                )

            # 🔥 IMPORTANT
            sale.total_amount = sale.get_total
            sale.save()

        messages.success(request, f"Sale #{sale.id} completed successfully!")
        return redirect("sales_list")

    return redirect("sales_list")