"""
load_services.py
────────────────
Run this to load all Happy Hair Beauty Salon services into the database.

Usage:
    python manage.py shell < load_services.py

This script:
- Creates all service categories
- Creates every service with correct price
- Skips duplicates safely (won't create doubles if run again)
- Links each service to the first Salon in the database
"""

from salon_services.models import Service, ServiceCategory
from salons.models import Salon

# ── Get the salon ─────────────────────────────────────────────────
salon = Salon.objects.first()
if not salon:
    print("❌ No salon found. Create one in Admin first.")
    exit()

print(f"✅ Loading services for: {salon.name}")
print("─" * 50)

# ── Helper ────────────────────────────────────────────────────────
created_count = 0
skipped_count = 0

def add(category_obj, name, price):
    global created_count, skipped_count
    obj, created = Service.objects.get_or_create(
        salon=salon,
        name=name,
        category=category_obj,
        defaults={'price': price, 'is_active': True}
    )
    if created:
        created_count += 1
        print(f"  + {name} — KSh {price:,}")
    else:
        # Update price in case it changed
        if obj.price != price:
            obj.price = price
            obj.save(update_fields=['price'])
            print(f"  ~ {name} — updated to KSh {price:,}")
        else:
            skipped_count += 1

def category(name):
    obj, created = ServiceCategory.objects.get_or_create(salon=salon, name=name)
    if created:
        print(f"\n📂 {name} (new)")
    else:
        print(f"\n📂 {name}")
    return obj


# ════════════════════════════════════════════════════════════════
# WASH & BASIC
# ════════════════════════════════════════════════════════════════
cat = category("Wash & Basic")
add(cat, "Wash and blowdry",   500)
add(cat, "Wash and set",       800)
add(cat, "Trimming",           500)
add(cat, "Detangling",         500)


# ════════════════════════════════════════════════════════════════
# LEAVE-IN TREATMENT
# ════════════════════════════════════════════════════════════════
cat = category("Leave-In Treatment")
add(cat, "Olive leave-in",              1000)
add(cat, "Hawaiian silky",              1500)
add(cat, "Shea Butter American silky",  1500)
add(cat, "Cantu",                       1500)
add(cat, "Moisture African pride",      1500)
add(cat, "Mikalla leave-in",            1000)
add(cat, "Revlon leave-in",             2500)
add(cat, "Revlon anti-hair loss",       2500)
add(cat, "Mizani miracle milk",         3000)
add(cat, "Loreal vitamino leave-in",    2500)
add(cat, "Loreal curl expression leave-in", 2500)
add(cat, "Own treatment",               1000)


# ════════════════════════════════════════════════════════════════
# DEEP TREATMENT
# ════════════════════════════════════════════════════════════════
cat = category("Deep Treatment")
add(cat, "Mikalla deep treatment",          1500)
add(cat, "Keratin hair mask",               2000)
add(cat, "American Shea butter",            2000)
add(cat, "Mayoinase vital",                 2000)
add(cat, "Revlon mask",                     3000)
add(cat, "Curls and coils mizani",          4000)
add(cat, "Moisture fusion mizani",          4000)
add(cat, "Loreal scalp advance",            5000)
add(cat, "Loreal curl expression deep",     5000)
add(cat, "Loreal absolute repair",          5000)
add(cat, "Loreal absolute molecular",       7500)
add(cat, "Metal detox",                     8000)
add(cat, "Loreal vitamino color treatment", 4500)
add(cat, "Loreal curl expression treatment",4500)
add(cat, "Vitamino leave-in deep",          2500)


# ════════════════════════════════════════════════════════════════
# STYLING
# ════════════════════════════════════════════════════════════════
cat = category("Styling")
add(cat, "Hair extension wash and style", 1500)
add(cat, "Flat iron",                     1000)
add(cat, "Tong",                          1000)
add(cat, "Silk press",                    4500)
add(cat, "Blow brush",                    2500)


# ════════════════════════════════════════════════════════════════
# PERM
# ════════════════════════════════════════════════════════════════
cat = category("Perm")
add(cat, "Curly perm retouch", 5000)
add(cat, "Curly perm",         7000)   # starts from 7,000


# ════════════════════════════════════════════════════════════════
# KERATIN
# ════════════════════════════════════════════════════════════════
cat = category("Keratin")
add(cat, "Keratin retouch treatment", 5000)
add(cat, "Keratin virgin hair",       7000)  # starts from 7,000


# ════════════════════════════════════════════════════════════════
# WEAVING
# ════════════════════════════════════════════════════════════════
cat = category("Weaving")
add(cat, "Track and saw",           1500)
add(cat, "Traditional sew-in",      2000)
add(cat, "3-part sew-in",           3000)
add(cat, "Braidless sew-in",        4000)
add(cat, "4x4 Closure sew-in",      2500)
add(cat, "Frontal sew-in",          3000)
add(cat, "360 frontal sew-in",      3500)
add(cat, "Full head",               2000)
add(cat, "Microlinks",              7000)
add(cat, "Nano links",              10000)
add(cat, "Microlinks re-tightening",2500)
add(cat, "Wig installation",        2500)
add(cat, "Wig customization",       1000)


# ════════════════════════════════════════════════════════════════
# RELAXER SERVICE
# ════════════════════════════════════════════════════════════════
cat = category("Relaxer Service")
add(cat, "Partial retouch (own weave)", 1000)
add(cat, "Mega growth retouch",         2000)
add(cat, "Mega growth virgin",          4000)
add(cat, "Olive vitale retouch",        2500)
add(cat, "Olive vitale virgin",         4500)
add(cat, "Mizani retouch relaxed hair", 7500)
add(cat, "Mizani virgin hair",          9000)  # starts from 9,000
add(cat, "Own relaxer",                 1500)


# ════════════════════════════════════════════════════════════════
# BRAIDING
# ════════════════════════════════════════════════════════════════
cat = category("Braiding")
add(cat, "Knotless braids small",    2500)
add(cat, "Knotless braids medium",   1500)
add(cat, "Knotless braids long",     3000)
add(cat, "Boho braids",              2500)
add(cat, "Passion twist",            2000)
add(cat, "Artificial sister locks",  3000)
add(cat, "Cornrows",                 1200)
add(cat, "Cornrows with braids",     1500)
add(cat, "2 strand twist",           2000)
add(cat, "Stylish braids",           2500)
add(cat, "Human hair braiding",      5000)


# ════════════════════════════════════════════════════════════════
# NAILS
# ════════════════════════════════════════════════════════════════
cat = category("Nails")
add(cat, "Pedicure",                  800)
add(cat, "Manicure",                  500)
add(cat, "Pedicure gel",              1400)
add(cat, "Manicure gel",              1000)
add(cat, "Stick on",                  1000)
add(cat, "Builders on natural nails", 1000)
add(cat, "Tips builders",             2000)
add(cat, "Gum gel",                   2000)
add(cat, "Acrylics",                  3000)


# ════════════════════════════════════════════════════════════════
# FACIALS
# ════════════════════════════════════════════════════════════════
cat = category("Facials")
add(cat, "Brightening hydra facial", 3000)
add(cat, "Normal facial",            2000)


# ════════════════════════════════════════════════════════════════
# MICROSHADING
# ════════════════════════════════════════════════════════════════
cat = category("Microshading")
add(cat, "Semi-permanent brows", 10000)
add(cat, "Brows retouch",         5000)


# ════════════════════════════════════════════════════════════════
# COLOR
# ════════════════════════════════════════════════════════════════
cat = category("Color")
add(cat, "Basic color",                    7500)
add(cat, "Balayage bleach+toner+treatment",17000)
add(cat, "Toner/gloss",                    4500)
add(cat, "Heena",                          1000)
add(cat, "Grey coverage",                  2000)


# ════════════════════════════════════════════════════════════════
# MAKE-UP
# ════════════════════════════════════════════════════════════════
cat = category("Make-up")
add(cat, "Basic make-up",      2500)
add(cat, "Full make-up",       3500)
add(cat, "Cluster Lashes",     1200)
add(cat, "Eyebrow trimming",    200)


# ── Summary ───────────────────────────────────────────────────────
print("\n" + "═" * 50)
print(f"✅ Done!")
print(f"   Created : {created_count} services")
print(f"   Skipped : {skipped_count} (already existed)")
total = Service.objects.filter(salon=salon).count()
print(f"   Total in DB: {total} services")
print("═" * 50)
