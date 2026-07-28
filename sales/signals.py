from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SaleItem


@receiver(post_save, sender=SaleItem)
def update_sale_total(sender, instance, **kwargs):
    instance.sale.total_amount = instance.sale.get_total
    instance.sale.save()