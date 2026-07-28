from django.db import models
from salons.models import Salon

# =========================
# PRODUCT CATEGORY
# =========================
class ProductCategory(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='product_categories')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Product Categories'


# =========================
# PRODUCT
# =========================
class Product(models.Model):
    PRODUCT_TYPES = (('retail', 'Retail'), ('consumable', 'Consumable'))
    UNIT_TYPES = (('unit', 'Unit'), ('gram', 'Gram'), ('ml', 'Milliliters'))

    salon        = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='products')
    category     = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, blank=True)
    name         = models.CharField(max_length=255)
    description  = models.TextField(blank=True, null=True)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES, default='retail')
    unit_type    = models.CharField(max_length=20, choices=UNIT_TYPES, default='unit')

    cost_price    = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    stock_quantity = models.FloatField(default=0)
    is_active      = models.BooleanField(default=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.stock_quantity} {self.unit_type})"

    class Meta:
        ordering = ['-created_at']


# =========================
# STOCK MOVEMENT (General Products)
# =========================
class StockMovement(models.Model):
    product       = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements')
    quantity      = models.FloatField()
    movement_type = models.CharField(max_length=10, choices=[('in', 'Stock In'), ('out', 'Stock Out')])
    source        = models.CharField(max_length=20, choices=[('sale', 'Sale'), ('service', 'Service'), ('purchase', 'Purchase'), ('adjustment', 'Adjustment')])
    reference     = models.CharField(max_length=255, blank=True, null=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.quantity <= 0:
                raise ValueError('Quantity must be greater than zero')
            if self.movement_type == 'in':
                self.product.stock_quantity += self.quantity
            elif self.movement_type == 'out':
                if self.product.stock_quantity < self.quantity:
                    raise ValueError(f'Not enough stock for {self.product.name}')
                self.product.stock_quantity -= self.quantity
            self.product.save()
        super().save(*args, **kwargs)

    @staticmethod
    def create_movement(product, quantity, movement_type, source, reference=None):
        return StockMovement.objects.create(product=product, quantity=quantity, movement_type=movement_type, source=source, reference=reference)


# =========================
# HUMAN HAIR
# =========================
class HairTexture(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='hair_textures')
    name  = models.CharField(max_length=100)
    def __str__(self): return self.name

class HumanHair(models.Model):
    ORIGIN_CHOICES = [
        ('brazilian', 'Brazilian'), ('peruvian', 'Peruvian'), ('malaysian', 'Malaysian'),
        ('indian', 'Indian'), ('cambodian', 'Cambodian'), ('vietnamese', 'Vietnamese'),
        ('mongolian', 'Mongolian'), ('burmese', 'Burmese'), ('other', 'Other'),
    ]

    salon   = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='human_hair')
    texture = models.ForeignKey(HairTexture, on_delete=models.SET_NULL, null=True, blank=True, related_name='hair_items')
    name    = models.CharField(max_length=255, blank=True, help_text='Auto-filled if left blank')
    origin  = models.CharField(max_length=20, choices=ORIGIN_CHOICES, default='brazilian')
    length_inch = models.PositiveIntegerField(help_text='Length in inches')

    cost_price    = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    bundles_in_stock = models.PositiveIntegerField(default=0)
    low_stock_alert  = models.PositiveIntegerField(default=2)

    is_active  = models.BooleanField(default=True)
    notes      = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['origin', 'texture__name', 'length_inch']
        verbose_name = 'Human Hair'
        verbose_name_plural = 'Human Hair Stock'

    def save(self, *args, **kwargs):
        if not self.name:
            texture_name = self.texture.name if self.texture else 'Unknown Texture'
            self.name = f"{self.get_origin_display()} {texture_name} {self.length_inch}\""
        super().save(*args, **kwargs)

    @property
    def is_low_stock(self):
        return self.bundles_in_stock <= self.low_stock_alert and self.bundles_in_stock > 0

    @property
    def is_out_of_stock(self):
        return self.bundles_in_stock == 0

    @property
    def stock_value(self):
        cost = self.cost_price if self.cost_price is not None else 0
        return self.bundles_in_stock * cost

    @property
    def potential_revenue(self):
        price = self.selling_price if self.selling_price is not None else 0
        return self.bundles_in_stock * price

    @property
    def potential_profit(self):
        return self.potential_revenue - self.stock_value

    def __str__(self):
        return f"{self.name} — {self.bundles_in_stock} bundles"


# =========================
# HAIR STOCK MOVEMENT
# =========================
class HairStockMovement(models.Model):
    hair          = models.ForeignKey(HumanHair, on_delete=models.CASCADE, related_name='movements')
    bundles       = models.PositiveIntegerField(help_text='Number of bundles')
    movement_type = models.CharField(max_length=10, choices=[('in', 'Stock In'), ('out', 'Stock Out')])
    source        = models.CharField(max_length=20, choices=[('sale', 'Sale'), ('purchase', 'Purchase'), ('adjustment', 'Adjustment'), ('returned', 'Returned')])
    reference     = models.CharField(max_length=255, blank=True, help_text='e.g. Sale #12')
    notes         = models.TextField(blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.bundles <= 0:
                raise ValueError('Bundles must be greater than zero')
            
            if self.movement_type == 'in':
                self.hair.bundles_in_stock += self.bundles
            elif self.movement_type == 'out':
                if self.hair.bundles_in_stock < self.bundles:
                    raise ValueError(f'Not enough bundles for {self.hair.name}. Available: {self.hair.bundles_in_stock}')
                self.hair.bundles_in_stock -= self.bundles
            
            self.hair.save()
        super().save(*args, **kwargs)

    @staticmethod
    def create_movement(hair, bundles, movement_type, source, reference=None, notes=None):
        return HairStockMovement.objects.create(
            hair=hair, bundles=bundles, movement_type=movement_type, 
            source=source, reference=reference, notes=notes
        )

    def __str__(self):
        return f"{self.hair.name} — {self.movement_type} ({self.bundles} bundles)"