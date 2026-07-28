from django.urls import path
from .views import (
    dashboard,
    pos_dashboard,
    create_sale,
    sales_list,
    clients_list,
    client_detail,
    add_client,
    export_vcf,
    export_csv,
    broadcast,
    inventory_list,
    services_list,
    reports,
    custom_logout,
)

urlpatterns = [
    # Dashboard
    path('', dashboard, name='dashboard'),
    path('dashboard/', dashboard, name='dashboard'),

    # POS
    path('pos/', pos_dashboard, name='pos_dashboard'),
    path('sales/create/', create_sale, name='create_sale'),

    # Sales & Reports
    path('sales/', sales_list, name='sales_list'),
    path('reports/', reports, name='reports'),

    # Clients
    path('clients/', clients_list, name='clients_list'),
    path('clients/add/', add_client, name='add_client'),
    path('clients/<int:pk>/', client_detail, name='client_detail'),

    # ── Exports ──────────────────────────────────
    path('clients/export/vcf/', export_vcf, name='export_vcf'),
    path('clients/export/csv/', export_csv, name='export_csv'),

    # ── Broadcast ────────────────────────────────
    path('clients/broadcast/', broadcast, name='broadcast'),

    # Inventory & Services
    path('inventory/', inventory_list, name='inventory_list'),
    path('services/', services_list, name='services_list'),

    # Auth
    path('logout/', custom_logout, name='custom_logout'),
]