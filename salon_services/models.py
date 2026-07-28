from django.db import models
from salons.models import Salon
from inventory.models import Product

class ServiceCategory(models.Model):
    # Added salon link to ensure categories are private to each business
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='service_categories')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Service Categories"

class Service(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='services')
    
    # Linked to Category, using SET_NULL so services survive if a category is deleted
    category = models.ForeignKey(
        ServiceCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='services'
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(null=True, blank=True, help_text="Duration in minutes")

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.price}"

    class Meta:
        ordering = ['name']

class ServiceProduct(models.Model):
    """
    Tracks how much of a specific inventory product is consumed 
    when a service is performed (e.g., 50ml of shampoo for a wash).
    """
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='product_usage')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    # Updated field name to quantity_used as per your request
    quantity_used = models.FloatField(help_text="Amount used per service (ml or units)")

    def __str__(self):
        return f"{self.service.name} uses {self.product.name} ({self.quantity_used})"