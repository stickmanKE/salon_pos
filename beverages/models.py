from django.db import models
from salons.models import Salon


class BeverageCategory(models.Model):
    """e.g. Soda, Water, Juice, Energy Drink"""
    name = models.CharField(max_length=100)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='beverage_categories')

    class Meta:
        ordering = ['name']
        verbose_name = 'Beverage Category'
        verbose_name_plural = 'Beverage Categories'
        unique_together = ('salon', 'name')

    def __str__(self):
        return self.name


class Beverage(models.Model):
    """Individual drink product e.g. Coca-Cola 500ml, Sprite 300ml, Fanta Orange 500ml"""
    SIZE_CHOICES = [
        ('200ml', '200ml'), ('300ml', '300ml'), ('500ml', '500ml'),
        ('1000ml', '1 Litre'), ('2000ml', '2 Litres'), ('other', 'Other'),
    ]

    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='beverages')
    category = models.ForeignKey(
        BeverageCategory, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='beverages'
    )

    # Drink identity: name = "Coca-Cola", "Sprite", "Fanta Orange", "Mineral Water"
    name = models.CharField(max_length=100, help_text='e.g. Coca-Cola, Sprite, Fanta Orange')
    size = models.CharField(max_length=20, choices=SIZE_CHOICES, default='500ml')

    # Pricing
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Stock (number of bottles/cans)
    stock_units = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=5, help_text='Alert when stock falls below this')

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name', 'size']
        verbose_name = 'Beverage'
        verbose_name_plural = 'Beverages'

    def __str__(self):
        return f"{self.name} ({self.size})"

    @property
    def is_low_stock(self):
        return self.stock_units <= self.low_stock_threshold

    @property
    def total_stock_ml(self):
        try:
            ml = int(self.size.replace('ml', ''))
            return self.stock_units * ml
        except Exception:
            return self.stock_units


class BeverageStock(models.Model):
    """Stock movement log — records every stock in/out event"""
    MOVEMENT_TYPES = [('in', 'Stock In'), ('out', 'Stock Out')]
    SOURCE_TYPES = [
        ('sale', 'Sale'), ('purchase', 'Purchase'), ('adjustment', 'Adjustment'),
    ]

    beverage = models.ForeignKey(Beverage, on_delete=models.CASCADE, related_name='movements')
    quantity = models.IntegerField(help_text='Number of units (bottles/cans)')
    movement_type = models.CharField(max_length=10, choices=MOVEMENT_TYPES)
    source = models.CharField(max_length=20, choices=SOURCE_TYPES, default='sale')
    reference = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.quantity <= 0:
                raise ValueError('Quantity must be greater than zero')
            if self.movement_type == 'in':
                self.beverage.stock_units += self.quantity
            elif self.movement_type == 'out':
                if self.beverage.stock_units < self.quantity:
                    raise ValueError(
                        f'Not enough stock for {self.beverage.name}. '
                        f'Available: {self.beverage.stock_units}'
                    )
                self.beverage.stock_units -= self.quantity
            self.beverage.save(update_fields=['stock_units'])
        super().save(*args, **kwargs)

    @staticmethod
    def create_movement(beverage, quantity, movement_type, source='sale', reference=None):
        return BeverageStock.objects.create(
            beverage=beverage, quantity=quantity,
            movement_type=movement_type, source=source, reference=reference
        )

    def __str__(self):
        return f"{self.beverage.name} - {self.movement_type} ({self.quantity})"
