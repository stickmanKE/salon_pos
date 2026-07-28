from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from salons.models import Salon
from clients.models import Client

class Sale(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Cash'),
        ('mpesa', 'M-Pesa'),
        ('card', 'Card'),
        ('mixed', 'Mixed'),
    )

    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, default='cash', blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        # Calculate subtotal of all items then subtract discount
        subtotal = sum(item.price * Decimal(str(item.quantity)) for item in self.items.all())
        return subtotal - self.discount_amount

    def update_total(self):
        self.total_amount = self.get_total
        self.save()

    def __str__(self):
        return f"Sale #{self.id} - {self.salon.name if self.salon else 'No Salon'}"

    class Meta:
        ordering = ['-created_at']

class SaleItem(models.Model):
    ITEM_TYPES = (
        ('service', 'Service'),
        ('product_sale', 'Product Sale'),
        ('product_use', 'Product Used'),
        ('beverage', 'Beverage'),
        ('human_hair', 'Human Hair'),
    )

    sale = models.ForeignKey('Sale', on_delete=models.CASCADE, related_name='items')
    
    # Links to inventory/services
    service = models.ForeignKey('salon_services.Service', null=True, blank=True, on_delete=models.SET_NULL)
    product = models.ForeignKey('inventory.Product', null=True, blank=True, on_delete=models.SET_NULL)
    human_hair = models.ForeignKey('inventory.HumanHair', null=True, blank=True, on_delete=models.SET_NULL)
    beverage = models.ForeignKey('beverages.Beverage', null=True, blank=True, on_delete=models.SET_NULL)
    
    # Link to staff
    worker = models.ForeignKey('staff.StaffMember', null=True, blank=True, on_delete=models.SET_NULL, related_name='sale_items')

    name = models.CharField(max_length=255)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.FloatField(default=1)

    def save(self, *args, **kwargs):
        # Auto-fill name and price if not provided based on the item type
        if not self.name:
            if self.item_type == 'service' and self.service:
                self.name = self.service.name
                if not self.price: self.price = self.service.price
            elif self.item_type == 'human_hair' and self.human_hair:
                self.name = self.human_hair.name
                if not self.price: self.price = self.human_hair.selling_price
            elif self.item_type == 'beverage' and self.beverage:
                self.name = self.beverage.name
                if not self.price: self.price = self.beverage.selling_price
            elif self.product:
                self.name = self.product.name
                if not self.price: self.price = self.product.selling_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.quantity})"

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('mpesa', 'M-Pesa'),
        ('card', 'Card'),
    )

    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    reference = models.CharField(max_length=100, blank=True, help_text='M-Pesa code or card ref')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.method.upper()} KSh{self.amount} for Sale #{self.sale.id}"