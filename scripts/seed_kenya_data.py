"""
Kenya Salon Seed Data Script
Run with: python manage.py shell < scripts/seed_kenya_data.py

Creates 3 salons with full Kenyan market data:
  - Salons, Staff, Clients, Service Categories, Services,
    Product Categories, Products (retail + consumable), Beverages
"""

import os
import django
from decimal import Decimal
from datetime import date

# ── Models ───────────────────────────────────────────────────────────────────
from salons.models import Salon
from staff.models import StaffMember
from clients.models import Client
from salon_services.models import ServiceCategory, Service
from inventory.models import ProductCategory, Product
from beverages.models import BeverageCategory, Beverage

print("🇰🇪  Starting Kenya salon seed data...\n")

# ─────────────────────────────────────────────────────────────────────────────
# HELPER
# ─────────────────────────────────────────────────────────────────────────────
def make_salon(name, phone, email, location, address):
    salon, created = Salon.objects.get_or_create(
        name=name,
        defaults=dict(phone=phone, email=email, location=location, address=address, is_active=True)
    )
    tag = "✅ Created" if created else "⏭  Exists"
    print(f"  {tag}: Salon → {name}")
    return salon


# ═════════════════════════════════════════════════════════════════════════════
# 1. SALONS
# ═════════════════════════════════════════════════════════════════════════════
print("── Salons ──────────────────────────────────────────────────────────────")

salon1 = make_salon(
    name="Glam Hub Beauty Lounge",
    phone="0712 345 678",
    email="glamhub@gmail.com",
    location="Westlands, Nairobi",
    address="Westlands Square, Ground Floor, Ring Road Westlands, Nairobi"
)
salon2 = make_salon(
    name="Nyumbani Salon & Spa",
    phone="0723 456 789",
    email="nyumbani.salon@gmail.com",
    location="Mombasa Road, Nairobi",
    address="Nextgen Mall, Ground Floor, Mombasa Road, Nairobi"
)
salon3 = make_salon(
    name="Coastal Glow Beauty Studio",
    phone="0741 567 890",
    email="coastalglow@gmail.com",
    location="Nyali, Mombasa",
    address="Nyali Centre, Ground Floor, Links Road, Nyali, Mombasa"
)

salons = [salon1, salon2, salon3]

# ═════════════════════════════════════════════════════════════════════════════
# 2. STAFF  (2–3 per salon)
# ═════════════════════════════════════════════════════════════════════════════
print("\n── Staff ───────────────────────────────────────────────────────────────")

STAFF_DATA = {
    salon1: [
        dict(full_name="Amina Wanjiru", role="stylist",        phone="0711 001 001", email="amina@glamhub.com",    commission_rate=Decimal("12.00"), hire_date=date(2022, 3, 15)),
        dict(full_name="Brenda Achieng", role="colorist",      phone="0711 001 002", email="brenda@glamhub.com",   commission_rate=Decimal("15.00"), hire_date=date(2022, 7, 1)),
        dict(full_name="Carol Njeri",    role="nail_tech",      phone="0711 001 003", email="carol@glamhub.com",    commission_rate=Decimal("10.00"), hire_date=date(2023, 1, 10)),
        dict(full_name="Diana Kamau",    role="manager",        phone="0711 001 004", email="diana@glamhub.com",    commission_rate=Decimal("0.00"),  hire_date=date(2021, 6, 1)),
    ],
    salon2: [
        dict(full_name="Faith Otieno",   role="stylist",        phone="0722 002 001", email="faith@nyumbani.com",   commission_rate=Decimal("12.00"), hire_date=date(2023, 2, 20)),
        dict(full_name="Grace Mwangi",   role="aesthetician",   phone="0722 002 002", email="grace@nyumbani.com",   commission_rate=Decimal("12.00"), hire_date=date(2023, 5, 1)),
        dict(full_name="Harriet Mutua",  role="receptionist",   phone="0722 002 003", email="harriet@nyumbani.com", commission_rate=Decimal("0.00"),  hire_date=date(2023, 8, 15)),
    ],
    salon3: [
        dict(full_name="Imani Hassan",   role="stylist",        phone="0741 003 001", email="imani@coastalglow.com",  commission_rate=Decimal("12.00"), hire_date=date(2022, 11, 1)),
        dict(full_name="Joyce Mwenda",   role="nail_tech",      phone="0741 003 002", email="joyce@coastalglow.com",  commission_rate=Decimal("10.00"), hire_date=date(2023, 3, 1)),
        dict(full_name="Khadija Omar",   role="colorist",       phone="0741 003 003", email="khadija@coastalglow.com",commission_rate=Decimal("15.00"), hire_date=date(2023, 6, 15)),
    ],
}

staff_map = {}  # salon → [staff members]
for salon, members in STAFF_DATA.items():
    staff_map[salon] = []
    for m in members:
        s, created = StaffMember.objects.get_or_create(salon=salon, full_name=m["full_name"], defaults=m)
        tag = "✅" if created else "⏭ "
        print(f"  {tag} {salon.name[:20]:<20} → {s.full_name} ({s.get_role_display()})")
        staff_map[salon].append(s)


# ═════════════════════════════════════════════════════════════════════════════
# 3. CLIENTS  (8–10 per salon, Kenyan names)
# ═════════════════════════════════════════════════════════════════════════════
print("\n── Clients ─────────────────────────────────────────────────────────────")

CLIENTS_DATA = {
    salon1: [
        ("Lydia Wairimu",    "0722 100 001", "lydia.wairimu@gmail.com",   date(1992, 4, 12)),
        ("Mercy Ndungu",     "0733 100 002", "mercy.ndungu@gmail.com",    date(1988, 8, 25)),
        ("Nancy Kipsang",    "0700 100 003", "nancy.kipsang@gmail.com",   date(1995, 1, 30)),
        ("Olivia Gitau",     "0712 100 004", "olivia.gitau@gmail.com",    date(1990, 6, 18)),
        ("Pauline Chebet",   "0723 100 005", "",                           date(1997, 11, 5)),
        ("Rose Auma",        "0741 100 006", "rose.auma@gmail.com",       date(1985, 3, 22)),
        ("Sandra Njoroge",   "0711 100 007", "sandra.njoroge@gmail.com",  date(1993, 7, 14)),
        ("Tabitha Waweru",   "0756 100 008", "",                           date(1999, 9, 9)),
    ],
    salon2: [
        ("Agnes Omondi",     "0722 200 001", "agnes.omondi@gmail.com",    date(1991, 2, 14)),
        ("Beatrice Kariuki", "0733 200 002", "beatrice.kariuki@gmail.com",date(1987, 10, 30)),
        ("Cynthia Njenga",   "0700 200 003", "",                           date(1996, 5, 20)),
        ("Doreen Ayoo",      "0712 200 004", "doreen.ayoo@gmail.com",     date(1994, 12, 1)),
        ("Eunice Wangari",   "0723 200 005", "eunice.wangari@gmail.com",  date(1989, 7, 8)),
        ("Fatuma Said",      "0741 200 006", "fatuma.said@gmail.com",     date(1998, 3, 15)),
        ("Gloria Kamau",     "0711 200 007", "",                           date(1993, 8, 27)),
        ("Hellen Otieno",    "0756 200 008", "hellen.otieno@gmail.com",   date(1986, 6, 11)),
    ],
    salon3: [
        ("Amina Salim",      "0741 300 001", "amina.salim@gmail.com",     date(1993, 1, 17)),
        ("Baraka Mwamba",    "0700 300 002", "",                           date(1990, 4, 5)),
        ("Chiku Hamisi",     "0722 300 003", "chiku.hamisi@gmail.com",    date(1997, 9, 23)),
        ("Dalilah Mwangi",   "0733 300 004", "dalilah.mwangi@gmail.com",  date(1988, 12, 8)),
        ("Eshe Karisa",      "0712 300 005", "eshe.karisa@gmail.com",     date(1995, 6, 30)),
        ("Fatuma Kombo",     "0723 300 006", "",                           date(1991, 2, 19)),
        ("Grace Masha",      "0741 300 007", "grace.masha@gmail.com",     date(1999, 7, 4)),
        ("Halima Rashid",    "0711 300 008", "halima.rashid@gmail.com",   date(1986, 10, 12)),
        ("Irene Odhiambo",   "0756 300 009", "irene.odhiambo@gmail.com",  date(1994, 3, 28)),
    ],
}

for salon, clients in CLIENTS_DATA.items():
    stylists = [s for s in staff_map[salon] if s.role == 'stylist']
    preferred = stylists[0] if stylists else None
    for i, (name, phone, email, bday) in enumerate(clients):
        c, created = Client.objects.get_or_create(
            salon=salon, phone=phone,
            defaults=dict(name=name, email=email, birthday=bday, preferred_worker=preferred, notes="")
        )
        tag = "✅" if created else "⏭ "
        print(f"  {tag} {salon.name[:20]:<20} → {c.name}")


# ═════════════════════════════════════════════════════════════════════════════
# 4. SERVICES  (categories + services per salon)
# ═════════════════════════════════════════════════════════════════════════════
print("\n── Services ────────────────────────────────────────────────────────────")

# (category, [(name, price_kes, duration_min, description)])
SERVICES_TEMPLATE = [
    ("Styling", [
        ("Blow Dry & Style",          800,  45, "Shampoo, blow dry and style to your preference"),
        ("Flat Iron / Silk Press",   2000,  60, "Full silk press using professional flat iron"),
        ("Tong Curls",               1500,  60, "Classic tong curl set for bouncy curls"),
        ("Blow Brush",               1200,  45, "Smooth blow-out using a round brush"),
        ("Hair Extension Wash & Set",2000,  90, "Wash, condition and style your hair extensions"),
    ]),
    ("Braiding", [
        ("Knotless Braids (Small)",  3500, 240, "Lightweight knotless box braids — small size"),
        ("Knotless Braids (Medium)", 2500, 180, "Knotless box braids — medium size"),
        ("Boho Braids",              3000, 210, "Bohemian braids with curly ends"),
        ("Cornrows (Simple)",         700,  60, "Basic cornrow pattern — straight back"),
        ("Stylish Cornrows",         1500,  90, "Creative cornrow design with pattern"),
        ("Twist Braids",             2000, 150, "Senegalese or Marley twist braids"),
    ]),
    ("Weaves & Wigs", [
        ("Quick Weave",              1500,  90, "Bonded weave installation"),
        ("Track & Sew",              2000, 120, "Traditional sew-in weave installation"),
        ("Frontal Sew-In",           3500, 180, "Lace frontal with sew-in weave"),
        ("Wig Installation",         2000,  60, "Wig prep, glue-down and styling"),
        ("Wig Customisation",        1500,  90, "Bleach knots, pluck and style your wig"),
    ]),
    ("Relaxer & Perm", [
        ("Relaxer Retouch",          1500,  75, "Touch up new growth — includes shampoo and condition"),
        ("Mega Growth Retouch",      2000,  75, "Mega growth relaxer retouch with conditioning treatment"),
        ("Curly Perm",               7000, 180, "Full curly perm transformation"),
        ("Curly Perm Retouch",       4500, 120, "Retouch for existing curly perm"),
    ]),
    ("Hair Colour", [
        ("Single Process Colour",    5000, 120, "All-over single colour application"),
        ("Highlights",               8000, 150, "Foil highlights for dimension and depth"),
        ("Balayage",                15000, 180, "Hand-painted balayage for a sun-kissed look"),
        ("Grey Coverage",            3000,  90, "Full grey coverage with permanent colour"),
        ("Toner / Gloss",            2500,  45, "Toning treatment to neutralise or enhance colour"),
        ("Henna Colour",             1000,  60, "Natural henna colour application"),
    ]),
    ("Treatments", [
        ("Deep Conditioning",        1500,  45, "Intensive moisture and protein conditioning mask"),
        ("Keratin Treatment",        8000, 180, "Professional keratin smoothing treatment — lasts 3 months"),
        ("Keratin Mask",             2000,  30, "Keratin-infused conditioning mask"),
        ("L'Oréal Absolute Repair",  5000, 120, "Professional bond repair treatment"),
        ("Metal Detox Treatment",    6000, 120, "Removes metal build-up that causes breakage"),
        ("Scalp Treatment",          1500,  45, "Dandruff or dry scalp targeted treatment"),
    ]),
    ("Nails", [
        ("Manicure (Basic)",          500,  30, "File, shape, cuticle care and polish"),
        ("Pedicure (Basic)",          800,  45, "File, shape, scrub, massage and polish"),
        ("Gel Manicure",             1500,  60, "Gel colour manicure that lasts 2–3 weeks"),
        ("Gel Pedicure",             2000,  75, "Gel colour pedicure — long lasting"),
        ("Acrylic Full Set",         3500, 120, "Full set acrylic nail extensions"),
        ("Acrylic Infill",           2000,  60, "Infill / fill for existing acrylics"),
        ("Nail Art (Per Nail)",       150,  30, "Custom nail art design — price per nail"),
    ]),
    ("Facials & Skin", [
        ("Classic Facial",           2500,  60, "Deep cleanse, exfoliate, tone and moisturise"),
        ("Brightening Hydra Facial", 4500,  75, "Hydrating facial for a glowing, even complexion"),
        ("Acne Facial",              3000,  60, "Targeted acne-clearing facial treatment"),
        ("Eyebrow Shaping",           300,  15, "Thread or wax brow shaping"),
        ("Eyebrow Tinting",           500,  20, "Brow tint to enhance natural colour"),
        ("Upper Lip Wax",             200,  10, "Quick and effective upper lip wax"),
    ]),
    ("Make-Up", [
        ("Natural / Day Make-Up",    2000,  60, "Light, everyday natural make-up look"),
        ("Full Glam Make-Up",        4000,  90, "Full glam — foundation, contour, lashes and lips"),
        ("Bridal Make-Up",           8000, 120, "Bridal make-up with trial included"),
        ("Cluster Lashes",           1200,  30, "Individual cluster lash application"),
        ("Lash Lift & Tint",         2500,  60, "Lift and tint your natural lashes"),
    ]),
    ("Microblading & Brows", [
        ("Microblading / Microshading",10000, 120, "Semi-permanent brow tattoo — lasts 12–18 months"),
        ("Brow Touch-Up",             5000,  60, "Touch-up for existing microbladed brows"),
        ("Ombre Powder Brows",       12000, 150, "Soft powder effect brow tattoo"),
    ]),
    ("Massage & Spa", [
        ("Swedish Massage (30 min)",  2500,  30, "Relaxing full-body Swedish massage"),
        ("Swedish Massage (60 min)",  4500,  60, "Full hour relaxing Swedish massage"),
        ("Deep Tissue Massage",       5000,  60, "Firm pressure deep tissue massage"),
        ("Hot Stone Massage",         6000,  75, "Relaxing massage using heated volcanic stones"),
        ("Back & Shoulder Massage",   2000,  30, "Targeted back and shoulder tension relief"),
    ]),
]

for salon in salons:
    for cat_name, services in SERVICES_TEMPLATE:
        cat, _ = ServiceCategory.objects.get_or_create(salon=salon, name=cat_name)
        for svc_name, price, duration, desc in services:
            s, created = Service.objects.get_or_create(
                salon=salon, name=svc_name,
                defaults=dict(category=cat, price=Decimal(str(price)), duration=duration, description=desc, is_active=True)
            )
            if created:
                print(f"  ✅ {salon.name[:20]:<20} → [{cat_name}] {svc_name} (KES {price})")

print(f"\n  Total services: {Service.objects.count()}")


# ═════════════════════════════════════════════════════════════════════════════
# 5. PRODUCTS  (retail + consumable)
# ═════════════════════════════════════════════════════════════════════════════
print("\n── Inventory Products ──────────────────────────────────────────────────")

# (category, type, name, description, cost, selling, stock, unit)
PRODUCTS_TEMPLATE = [
    # ── RETAIL (sold to clients) ─────────────────────────────────────────────
    ("Hair Care", "retail", [
        ("ORS Olive Oil Relaxer Kit",        "No-lye relaxer kit with conditioning treatment",           600, 950,  30, "unit"),
        ("Dark & Lovely Relaxer Kit",        "Professional relaxer for colour-treated hair",             550, 850,  25, "unit"),
        ("Cantu Shea Butter Leave-In",       "Leave-in conditioning repair cream, 453g",                700, 1100, 20, "unit"),
        ("Cantu Define & Shine Custard",     "Curl defining custard for natural hair, 370g",            650, 1050, 15, "unit"),
        ("Eco Styler Olive Oil Gel",         "Professional styling gel with olive oil, 473ml",          350, 550,  40, "unit"),
        ("Schwarzkopf Gliss Hair Serum",     "Hair repair serum for dry damaged hair, 75ml",            800, 1300, 20, "unit"),
        ("Keratin Infused Shampoo",          "Sulfate-free keratin shampoo, 500ml",                    1200, 1800, 15, "unit"),
        ("Keratin Conditioner",              "Keratin conditioner for smooth frizz-free hair, 500ml",  1200, 1800, 15, "unit"),
        ("Argan Oil Treatment",              "100% pure argan oil for shine and frizz control, 60ml",   900, 1500, 20, "unit"),
    ]),
    ("Skin Care", "retail", [
        ("Neutrogena Face Wash",             "Oil-free acne face wash, 175ml",                          700, 1100, 20, "unit"),
        ("Garnier Vitamin C Serum",          "Brightening vitamin C serum, 30ml",                      1500, 2200, 15, "unit"),
        ("Nivea Natural Glow Lotion",        "Even-tone body lotion with vitamin C, 400ml",             500,  850, 25, "unit"),
        ("Dove Body Lotion",                 "Deep moisturising body lotion, 400ml",                    400,  650, 30, "unit"),
        ("Black & White Fair & White Cream", "Lightening and brightening face cream, 50ml",             800, 1200, 20, "unit"),
        ("Sunscreen SPF 50",                 "Broad-spectrum mineral sunscreen, 50ml",                 1000, 1600, 15, "unit"),
    ]),
    ("Nail Products", "retail", [
        ("OPI Nail Polish Assorted",         "Long-lasting nail colour — various shades",               600,  950, 50, "unit"),
        ("Essie Base Coat",                  "Base coat for longer-lasting nail polish",                500,  800, 20, "unit"),
        ("Cuticle Oil Pen",                  "Nourishing cuticle oil for healthy nail growth",          350,  600, 30, "unit"),
        ("Nail Strengthener Treatment",      "Keratin nail hardener to prevent breakage",               600,  950, 25, "unit"),
    ]),
    ("Hair Accessories", "retail", [
        ("Satin Bonnet (Assorted Sizes)",    "Satin bonnet to protect hair overnight",                  200,  350, 60, "unit"),
        ("Wide-Tooth Detangling Comb",       "Wide-tooth comb for detangling wet natural hair",         150,  280, 50, "unit"),
        ("Micro-Fibre Hair Towel",           "Ultra-absorbent hair towel — reduces frizz",              400,  650, 30, "unit"),
        ("Scrunchies Pack x5",               "Gentle satin scrunchies — assorted colours",              200,  350, 40, "unit"),
        ("Bobby Pin Set",                    "100pc black bobby pin set",                               100,  180, 80, "unit"),
        ("Flexi Rods Set",                   "Flexi rod curling set — 18 pieces",                       350,  600, 25, "unit"),
    ]),
    # ── CONSUMABLE (used during services) ────────────────────────────────────
    ("Salon Consumables", "consumable", [
        ("Wella Koleston Permanent Colour",  "Professional permanent hair colour, 60ml tube",            450,    0, 500, "unit"),
        ("Wella Blondor Bleach Powder",      "Professional bleach powder, sold per gram",                  3,    0,5000, "gram"),
        ("L'Oréal Majirel Hair Colour",      "Permanent hair colour for grey coverage, 50ml",            400,    0, 300, "unit"),
        ("Keratin Treatment Solution",       "Professional Brazilian keratin smoothing, 1000ml",        8000,    0,5000, "ml"),
        ("Developer 20 Vol",                 "Cream developer 20 volume for colour, per ml",               2,    0,5000, "ml"),
        ("Developer 30 Vol",                 "Cream developer 30 volume for lightening, per ml",           2,    0,5000, "ml"),
        ("Salon Shampoo (Bulk)",             "Professional moisturising shampoo, per ml",                  2,    0,10000,"ml"),
        ("Deep Conditioner (Bulk)",          "Professional deep conditioner for treatments, per ml",       3,    0,10000,"ml"),
        ("Relaxer (Professional)",           "Professional no-lye relaxer, per application",            500,    0,  50, "unit"),
        ("Tinfoil Sheets",                   "Aluminium foil for highlights, per sheet",                   5,    0,2000, "unit"),
        ("Disposable Gloves (Box 100)",      "Vinyl gloves for colour and chemical services",            500,    0,  20, "unit"),
        ("Cotton Strips",                    "Neck cotton strips for chemical services",                  80,    0, 200, "unit"),
        ("Acrylic Powder (Clear)",           "Acrylic powder for nail extensions, per gram",               8,    0, 500, "gram"),
        ("Acrylic Liquid Monomer",           "Acrylic monomer for nail extensions, per ml",              10,    0, 500, "ml"),
        ("Nail Primer",                      "Nail prep primer for acrylics, 15ml",                     800,    0,  20, "unit"),
        ("Gel Top Coat",                     "UV/LED gel top coat, 15ml bottle",                        700,    0,  30, "unit"),
        ("Facial Cleanser (Professional)",   "Professional deep cleanse facial wash, per ml",             3,    0,2000, "ml"),
        ("Facial Mask (Clay)",               "Professional clay mask for deep pore cleansing, per gram",  5,    0,1000, "gram"),
        ("Massage Oil",                      "Professional relaxing massage oil blend, per ml",            4,    0,2000, "ml"),
        ("Waxing Strips",                    "Non-woven waxing strips for facial waxing",               200,    0, 500, "unit"),
    ]),
]

for salon in salons:
    for cat_name, ptype, products in PRODUCTS_TEMPLATE:
        cat, _ = ProductCategory.objects.get_or_create(salon=salon, name=cat_name)
        for name, desc, cost, selling, stock, unit in products:
            p, created = Product.objects.get_or_create(
                salon=salon, name=name,
                defaults=dict(
                    category=cat,
                    description=desc,
                    product_type=ptype,
                    unit_type=unit,
                    cost_price=Decimal(str(cost)),
                    selling_price=Decimal(str(selling)) if selling > 0 else Decimal("0.00"),
                    stock_quantity=float(stock),
                    is_active=True,
                )
            )
            if created:
                print(f"  ✅ {salon.name[:20]:<20} → [{ptype.upper()}] {name}")

print(f"\n  Total products: {Product.objects.count()}")


# ═════════════════════════════════════════════════════════════════════════════
# 6. BEVERAGES
# ═════════════════════════════════════════════════════════════════════════════
print("\n── Beverages ───────────────────────────────────────────────────────────")

# (category, name, size, cost, selling, stock)
BEVERAGES_TEMPLATE = [
    ("Soda", [
        ("Coca-Cola",    "300ml",  40,  80, 48),
        ("Coca-Cola",    "500ml",  60, 100, 24),
        ("Sprite",       "300ml",  40,  80, 36),
        ("Fanta Orange", "300ml",  40,  80, 36),
        ("Fanta Grape",  "300ml",  40,  80, 24),
        ("Stoney Ginger","300ml",  40,  80, 24),
        ("Pepsi",        "300ml",  40,  80, 24),
        ("Krest Tonic",  "300ml",  40,  80, 12),
        ("Mirinda",      "300ml",  40,  80, 24),
    ]),
    ("Water", [
        ("Dasani Water",  "500ml", 30,  60, 48),
        ("Keringet Water","500ml", 35,  70, 48),
        ("Evian Water",   "500ml", 80, 150, 12),
        ("Dasani Water",  "1000ml",50, 100, 24),
    ]),
    ("Juice", [
        ("Afia Mango",       "300ml", 50, 100, 24),
        ("Afia Orange",      "300ml", 50, 100, 24),
        ("Afia Tropical",    "300ml", 50, 100, 24),
        ("Delmonte Pineapple","300ml",55, 110, 24),
        ("Minute Maid Pulpy","300ml", 60, 120, 24),
        ("Sunny Fresh Apple","300ml", 50, 100, 12),
    ]),
    ("Energy Drinks", [
        ("Redbull",         "250ml", 150, 280, 12),
        ("Monster Energy",  "500ml", 180, 320, 12),
        ("Burn Energy Drink","250ml",120, 220, 12),
        ("Lucozade Boost",  "300ml",  90, 160, 12),
        ("Power Horse",     "250ml", 100, 180, 12),
    ]),
    ("Hot Drinks", [
        ("Nescafé Coffee",  "other",  30,  80, 100),
        ("Kericho Gold Tea","other",  20,  60, 100),
        ("Milo Hot Drink",  "other",  35,  90, 100),
        ("Malewa African Tea","other",25,  70, 100),
    ]),
    ("Milk & Yoghurt", [
        ("Brookside Drinking Yoghurt","300ml", 80, 140, 24),
        ("Yoplait Drinking Yoghurt",  "300ml", 90, 160, 12),
    ]),
]

for salon in salons:
    for cat_name, beverages in BEVERAGES_TEMPLATE:
        cat, _ = BeverageCategory.objects.get_or_create(salon=salon, name=cat_name)
        for name, size, cost, selling, stock in beverages:
            b, created = Beverage.objects.get_or_create(
                salon=salon, name=name, size=size,
                defaults=dict(
                    category=cat,
                    cost_price=Decimal(str(cost)),
                    selling_price=Decimal(str(selling)),
                    stock_units=stock,
                    low_stock_threshold=6,
                    is_active=True,
                )
            )
            if created:
                print(f"  ✅ {salon.name[:20]:<20} → [{cat_name}] {name} {size} (KES {selling})")

print(f"\n  Total beverages: {Beverage.objects.count()}")

# ═════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*60)
print("🎉  Kenya Seed Data Complete!")
print("═"*60)
print(f"  Salons    : {Salon.objects.count()}")
print(f"  Staff     : {StaffMember.objects.count()}")
print(f"  Clients   : {Client.objects.count()}")
print(f"  Services  : {Service.objects.count()}")
print(f"  Products  : {Product.objects.count()}")
print(f"  Beverages : {Beverage.objects.count()}")
print("═"*60)
