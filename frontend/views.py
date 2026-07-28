import csv
import json
import urllib.parse
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.db import transaction, models
from django.db.models import Sum, Count, Avg, F, ExpressionWrapper, DecimalField
from django.http import HttpResponse
from django.utils.timezone import now
from datetime import timedelta, date

# Models
from sales.models import Sale, SaleItem
from clients.models import Client
from salon_services.models import Service, ServiceCategory
from inventory.models import (
    Product, 
    StockMovement, 
    HumanHair, 
    HairStockMovement
)
from beverages.models import Beverage, BeverageStock
from salons.models import Salon

try:
    from staff.models import StaffMember
    STAFF_ENABLED = True
except Exception:
    STAFF_ENABLED = False


def _get_salon():
    """Helper to retrieve the current salon context"""
    return Salon.objects.first()


# ─────────────────────────────────────────
# DASHBOARD V2 (Premium UI Logic with Growth Metrics)
# ─────────────────────────────────────────
@login_required
def dashboard(request):
    salon = _get_salon()
    if not salon:
        return render(request, 'dashboard.html', {})

    today = now().date()
    month_start = today.replace(day=1)
    # Simple logic for "Last Month" comparison
    last_month_start = (month_start - timedelta(days=1)).replace(day=1)
    
    # Base Querysets
    sales_all = Sale.objects.filter(salon=salon, is_paid=True)
    items_all = SaleItem.objects.filter(sale__salon=salon, sale__is_paid=True)
    hair_stock = HumanHair.objects.filter(salon=salon, is_active=True)

    # Accurately calculate item subtotal (price * quantity)
    total_expr = ExpressionWrapper(
        F("price") * F("quantity"),
        output_field=DecimalField(max_digits=12, decimal_places=2),
    )
    items_annotated = items_all.annotate(item_total=total_expr)

    # Calculate Current vs Previous Revenue for Trends
    rev_this_month = sales_all.filter(created_at__date__gte=month_start).aggregate(t=Sum('total_amount'))['t'] or 0
    rev_last_month = sales_all.filter(created_at__date__gte=last_month_start, created_at__date__lt=month_start).aggregate(t=Sum('total_amount'))['t'] or 0
    
    # Growth Percentage logic
    growth = 0
    if rev_last_month > 0:
        growth = ((rev_this_month - rev_last_month) / rev_last_month) * 100

    # --- ROW 1: PRIMARY KPIs ---
    stats = {
        'revenue_today': sales_all.filter(created_at__date=today).aggregate(t=Sum('total_amount'))['t'] or 0,
        'revenue_month': rev_this_month,
        'avg_sale': round(sales_all.filter(created_at__date__gte=month_start).aggregate(a=Avg('total_amount'))['a'] or 0, 0),
        'new_clients': Client.objects.filter(salon=salon, created_at__date__gte=month_start).count(),
        'growth': round(growth, 1),
    }

    # --- ROW 2: HUMAN HAIR KPI ---
    hair_items_month = items_annotated.filter(item_type='human_hair', sale__created_at__date__gte=month_start)
    hair_stats = {
        'revenue': hair_items_month.aggregate(t=Sum('item_total'))['t'] or 0,
        'bundles_sold': hair_items_month.aggregate(q=Sum('quantity'))['q'] or 0,
        'inventory_value': sum(h.stock_value for h in hair_stock),
        'low_stock_count': hair_stock.filter(bundles_in_stock__lte=F('low_stock_alert')).count(),
    }

    # --- ROW 3: CATEGORY REVENUE ---
    def get_rev(itype):
        return items_annotated.filter(item_type=itype, sale__created_at__date__gte=month_start).aggregate(t=Sum('item_total'))['t'] or 0

    cat_revenue = {
        'services': get_rev('service'),
        'products': get_rev('product_sale'),
        'beverages': get_rev('beverage'),
        'total_clients': Client.objects.filter(salon=salon).count(),
    }

    # --- TABLES & LISTS ---
    staff_performance = []
    if STAFF_ENABLED:
        staff_performance = items_annotated.filter(sale__created_at__date__gte=month_start, worker__isnull=False)\
            .values('worker__full_name', 'worker__role')\
            .annotate(revenue=Sum('item_total'), jobs=Count('id'))\
            .order_by('-revenue')[:5]

    # Query recent item sales for the Dashboard Live Sales Feed
    recent_activity = items_annotated.select_related('sale', 'sale__client').order_by('-sale__created_at')[:5]

    context = {
        'stats': stats,
        'hair_stats': hair_stats,
        'cat_revenue': cat_revenue,
        'staff_performance': staff_performance,
        'recent_activity': recent_activity,
        'recent_sales': sales_all.select_related('client').order_by('-created_at')[:5],
        'inventory_alerts': hair_stock.filter(bundles_in_stock__lte=F('low_stock_alert'))[:4],
        'chart_data': [
            float(cat_revenue['services']), 
            float(hair_stats['revenue']), 
            float(cat_revenue['products']), 
            float(cat_revenue['beverages'])
        ],
        'now': now()
    }
    return render(request, 'dashboard.html', context)


# ─────────────────────────────────────────
# POS DASHBOARD
# ─────────────────────────────────────────
@login_required
def pos_dashboard(request):
    salon = _get_salon()
    if not salon:
        return render(request, 'sales/pos.html', {})

    services = Service.objects.filter(salon=salon, is_active=True).select_related('category').order_by('category__name', 'name')
    products = Product.objects.filter(salon=salon, is_active=True)
    beverages = Beverage.objects.filter(salon=salon, is_active=True).select_related('category').order_by('name')
    clients = Client.objects.filter(salon=salon).order_by('name')
    staff = StaffMember.objects.filter(salon=salon, status='active').order_by('full_name') if STAFF_ENABLED else []

    human_hair = HumanHair.objects.filter(
        salon=salon, 
        is_active=True, 
        bundles_in_stock__gt=0
    ).select_related("texture").order_by("origin", "texture__name", "length_inch")

    return render(request, 'sales/pos.html', {
        'services': services, 
        'products': products,
        'human_hair': human_hair, 
        'beverages': beverages,
        'clients': clients, 
        'staff': staff,
    })


# ─────────────────────────────────────────
# CREATE SALE
# ─────────────────────────────────────────
@login_required
def create_sale(request):
    salon = _get_salon()
    if not salon or request.method != 'POST':
        return redirect('pos_dashboard')

    cart_data = request.POST.get('cart_data')
    try:
        cart = json.loads(cart_data)
    except:
        messages.error(request, 'Invalid cart data.')
        return redirect('pos_dashboard')

    with transaction.atomic():
        client_id = request.POST.get('client_id')
        client = Client.objects.filter(id=client_id).first() if client_id else None
        
        sale = Sale.objects.create(
            salon=salon, 
            user=request.user, 
            client=client,
            is_paid=True, 
            payment_method=request.POST.get('payment_method', 'cash'),
            discount_amount=Decimal(request.POST.get('discount', '0') or '0'),
            notes=request.POST.get('notes', '')
        )

        for item in cart:
            service = None; product = None; hair = None; bev = None
            itype, iid, qty = item.get('type'), item.get('id'), float(item.get('quantity', 1))
            
            worker_id = item.get('worker_id')
            worker = StaffMember.objects.filter(id=worker_id).first() if STAFF_ENABLED and worker_id else None

            if itype == 'service':
                service = Service.objects.filter(id=iid).first()
            elif itype in ['product', 'product_sale']:
                product = Product.objects.filter(id=iid).first()
                if product: StockMovement.create_movement(product, qty, 'out', 'sale', f'Sale #{sale.id}')
            elif itype == 'human_hair':
                hair = HumanHair.objects.filter(id=iid).first()
                if hair: HairStockMovement.create_movement(hair, int(qty), 'out', 'sale', f'Sale #{sale.id}')
            elif itype == 'beverage':
                bev = Beverage.objects.filter(id=iid).first()
                if bev: BeverageStock.objects.create(beverage=bev, quantity=int(qty), movement_type='out')

            SaleItem.objects.create(
                sale=sale, service=service, product=product, human_hair=hair, beverage=bev,
                worker=worker, name=item.get('name'), item_type=itype, 
                price=item.get('price'), quantity=qty
            )
            
        sale.update_total()

    messages.success(request, f'Sale #{sale.id} completed!')
    return redirect('sales_list')


# ─────────────────────────────────────────
# SALES LIST & REPORTS
# ─────────────────────────────────────────
@login_required
def sales_list(request):
    salon = _get_salon()
    period = request.GET.get('period', 'all')
    today = now().date()

    if not salon:
        return render(request, 'sales/list.html', {'sales': [], 'total_revenue': 0})

    sales = Sale.objects.filter(salon=salon, is_paid=True).select_related('client').order_by('-created_at')

    if period == 'today':
        sales = sales.filter(created_at__date=today)
    elif period == 'week':
        sales = sales.filter(created_at__date__gte=today - timedelta(days=today.weekday()))
    elif period == 'month':
        sales = sales.filter(created_at__date__gte=today.replace(day=1))

    total_revenue = sales.aggregate(t=Sum('total_amount'))['t'] or 0

    return render(request, 'sales/list.html', {
        'sales': sales, 'total_revenue': total_revenue, 'period': period
    })

@login_required
def reports(request):
    salon = _get_salon()
    if not salon: return render(request, 'reports.html', {})
    month_start = now().date().replace(day=1)
    
    items = SaleItem.objects.filter(sale__salon=salon, sale__is_paid=True, sale__created_at__date__gte=month_start)

    context = {
        'top_services': items.filter(item_type='service').values('name').annotate(revenue=Sum('price'), count=Count('id')).order_by('-revenue')[:10],
        'top_human_hair': items.filter(item_type='human_hair').values('name').annotate(revenue=Sum('price'), count=Count('id')).order_by('-revenue')[:10],
        'month_revenue': Sale.objects.filter(salon=salon, is_paid=True, created_at__date__gte=month_start).aggregate(t=Sum('total_amount'))['t'] or 0,
    }
    return render(request, 'reports.html', context)


# ─────────────────────────────────────────
# CLIENTS & EXPORTS
# ─────────────────────────────────────────
@login_required
def clients_list(request):
    salon = _get_salon()
    clients = Client.objects.filter(salon=salon).order_of_client = Client.objects.filter(salon=salon).order_by('name') if salon else []
    return render(request, 'clients/list.html', {'clients': clients})

@login_required
def add_client(request):
    salon = _get_salon()
    if request.method == 'POST' and salon:
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email', '')
        if name and phone:
            Client.objects.get_or_create(salon=salon, phone=phone, defaults={'name': name, 'email': email})
            messages.success(request, f'Client {name} added.')
    return redirect('clients_list')

@login_required
def client_detail(request, pk):
    """CRM profile for a single client: visit history, spend, preferred stylist."""
    salon = _get_salon()
    client = get_object_or_404(Client, pk=pk, salon=salon)

    sales = Sale.objects.filter(client=client, is_paid=True) \
        .prefetch_related('items').order_by('-created_at')

    total_spent = sales.aggregate(s=Sum('total_amount'))['s'] or 0
    visit_count = sales.count()
    last_visit = sales.first().created_at if sales.exists() else None

    # Most frequent stylist based on actual sale history
    top_stylist_row = SaleItem.objects.filter(sale__client=client, worker__isnull=False) \
        .values('worker__full_name') \
        .annotate(count=Count('id')) \
        .order_by('-count').first()
    top_stylist = top_stylist_row['worker__full_name'] if top_stylist_row else "None yet"

    return render(request, 'clients/detail.html', {
        'client': client,
        'sales': sales,
        'total_spent': total_spent,
        'visit_count': visit_count,
        'last_visit': last_visit,
        'top_stylist': top_stylist,
    })

@login_required
def export_vcf(request):
    salon = _get_salon()
    clients = Client.objects.filter(salon=salon) if salon else []
    lines = []
    for c in clients:
        lines.extend(["BEGIN:VCARD", "VERSION:3.0", f"FN:{c.name}", f"TEL;TYPE=CELL:{c.phone}", "END:VCARD", ""])
    response = HttpResponse("\n".join(lines), content_type='text/vcard')
    response['Content-Disposition'] = 'attachment; filename="clients.vcf"'; return response

@login_required
def export_csv(request):
    salon = _get_salon()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="clients.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Phone', 'Email'])
    for c in Client.objects.filter(salon=salon):
        writer.writerow([c.name, c.phone, c.email])
    return response

@login_required
def broadcast(request):
    salon = _get_salon()
    clients = Client.objects.filter(salon=salon) if salon else []
    return render(request, 'clients/broadcast.html', {'clients': clients})


# ─────────────────────────────────────────
# INVENTORY, SERVICES & AUTH
# ─────────────────────────────────────────
@login_required
def inventory_list(request):
    salon = _get_salon()
    if not salon: return render(request, 'inventory/list.html', {})
    return render(request, 'inventory/list.html', {
        'products': Product.objects.filter(salon=salon),
        'hair_stock': HumanHair.objects.filter(salon=salon),
        'beverages': Beverage.objects.filter(salon=salon),
    })

@login_required
def services_list(request):
    salon = _get_salon()
    services = Service.objects.filter(salon=salon) if salon else []
    return render(request, 'services/list.html', {'services': services})

@login_required
def custom_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')