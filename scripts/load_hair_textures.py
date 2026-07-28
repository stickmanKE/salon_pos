"""
load_hair_textures.py
─────────────────────
Loads common hair textures into the database.

Usage:
    python manage.py shell -c "exec(open('scripts/load_hair_textures.py', encoding='utf-8').read())"
"""

from inventory.models import HairTexture
from salons.models import Salon

salon = Salon.objects.first()
if not salon:
    print("No salon found.")
    exit()

TEXTURES = [
    'Straight',
    'Body Wave',
    'Loose Wave',
    'Deep Wave',
    'Water Wave',
    'Kinky Curly',
    'Kinky Straight',
    'Curly',
    'Afro Kinky',
    'Yaki Straight',
    'Natural Wave',
    'Jerry Curl',
]

print(f"Loading hair textures for: {salon.name}\n")
created = 0
for name in TEXTURES:
    obj, made = HairTexture.objects.get_or_create(salon=salon, name=name)
    if made:
        print(f"  + {name}")
        created += 1
    else:
        print(f"  ~ {name} (already exists)")

print(f"\nDone. {created} new textures added.")
print(f"Total textures: {HairTexture.objects.filter(salon=salon).count()}")
print("\nNext: Go to Admin → Inventory → Human Hair Stock → Add your bundles.")
