import random
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

# Import Models
from salons.models import Salon
from clients.models import Client
from inventory.models import HumanHair, HairTexture, Product, ProductCategory
from sales.models import Sale, SaleItem
from salon_services.models import Service, ServiceCategory

def run():
    print("🚀 Starting Data Seeding...")

    # 1. Get the EXISTING Salon from your screenshot
    salon = Salon.objects.filter(name__icontains="Happy Hair").first()
    
    if not salon:
        print("❌ Error: Could not find 'Happy Hair Beauty Salon'. Please create it in Admin first.")
        return

    print(f"✅ Linked to Salon: {salon.name} (ID: {salon.id})")

    # CLEANUP: Optional - remove old seed data to prevent duplicates
    # Sale.objects.filter(salon=salon).delete()
    # Client.objects.filter(salon=salon).delete()

    # 2. Add 10 Clients
    names = [
        "Jane Mwangi", "Mary Kamau", "Faith Wambui", "Alice Otieno", 
        "Purity Muthoni", "Sarah Atieno", "Linda Moraa", "Nancy Achieng",
        "Esther Njeri", "Grace Wanjiru"
    ]
    client_objs = []
    for name in names:
        c, _ = Client.objects.get_or_create(
            salon=salon,
            name=name,
            defaults={'phone': f"07{random.randint(10000000, 99999999)}"}
        )
        client_objs.append(c)
    print(f"✅ Prepared {len(client_objs)} Clients")

    # 3. Add Hair Textures & 10 Human Hair Types
    textures = ["Straight", "Body Wave", "Deep Wave", "Kinky Curly", "Loose Wave"]
    texture_objs = []
    for t in textures:
        obj, _ = HairTexture.objects.get_or_create(salon=salon, name=t)
        texture_objs.append(obj)

    origins = ["brazilian", "peruvian", "vietnamese", "indian"]
    lengths = [18, 20, 22, 24, 26]

    hair_products = []
    for i in range(10):
        h, _ = HumanHair.objects.get_or_create(
            salon=salon,
            origin=random.choice(origins),
            texture=random.choice(texture_objs),
            length_inch=random.choice(lengths),
            defaults={
                'cost_price': random.randint(4000, 7000),
                'selling_price': random.randint(8000, 15000),
                'bundles_in_stock': random.randint(10, 20),
                'low_stock_alert': 2
            }
        )
        hair_products.append(h)
    print("✅ Added 10 Human Hair SKUs")

    # 4. Add Inventory Products (Retail)
    cat_prod, _ = ProductCategory.objects.get_or_create(salon=salon, name="Hair Care")
    products_data = [
        ("Organic Hair Serum", 800, 1500),
        ("Nairobi Foam Mousse", 1200, 2200),
        ("Edge Control Pro", 400, 950),
        ("Shea Butter Conditioner", 600, 1300),
    ]
    retail_items = []
    for name, cost, sell in products_data:
        p, _ = Product.objects.get_or_create(
            salon=salon,
            name=name,
            defaults={
                'category': cat_prod,
                'cost_price': cost,
                'selling_price': sell,
                'stock_quantity': random.randint(15, 40),
                'product_type': 'retail'
            }
        )
        retail_items.append(p)
    print("✅ Added Inventory Products")

    # 5. Add Services
    cat_serv, _ = ServiceCategory.objects.get_or_create(salon=salon, name="Styling")
    services_data = [
        ("Silk Press", 3500),
        ("Hair Installation", 5000),
        ("Wig Revamp", 2500),
        ("Wash & Set", 1500),
    ]
    service_objs = []
    for name, price in services_data:
        s, _ = Service.objects.get_or_create(
            salon=salon,
            name=name,
            defaults={'category': cat_serv, 'price': price}
        )
        service_objs.append(s)
    print("✅ Added Services")

    # 6. Generate Sales Data (ensure they are in the CURRENT month)
    print("📊 Generating Sales History for the dashboard...")
    now_date = timezone.now()
    
    for i in range(40):
        # Random date within the last 14 days
        random_day = now_date - timedelta(days=random.randint(0, 14), hours=random.randint(1, 8))
        client = random.choice(client_objs)
        
        sale = Sale.objects.create(
            salon=salon,
            client=client,
            is_paid=True,
            payment_method=random.choice(['cash', 'mpesa', 'mpesa', 'card']),
            created_at=random_day
        )

        # Add random items to sale
        for _ in range(random.randint(1, 3)):
            choice = random.choice(['service', 'product', 'hair'])
            
            if choice == 'service':
                item = random.choice(service_objs)
                SaleItem.objects.create(
                    sale=sale, item_type='service', service=item,
                    name=item.name, price=item.price, quantity=1
                )
            elif choice == 'product':
                item = random.choice(retail_items)
                SaleItem.objects.create(
                    sale=sale, item_type='product_sale', product=item,
                    name=item.name, price=item.selling_price, quantity=1
                )
            elif choice == 'hair':
                item = random.choice(hair_products)
                SaleItem.objects.create(
                    sale=sale, item_type='human_hair', human_hair=item,
                    name=item.name, price=item.selling_price, quantity=1
                )
        
        # Calculate total and force the date (auto_now_add hack)
        sale.update_total()
        Sale.objects.filter(id=sale.id).update(created_at=random_day)

    print("⭐ SUCCESS! All data linked to 'Happy Hair Beauty Salon'.")