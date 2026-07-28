from django.db import models
from salons.models import Salon


class Client(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)

    # Basic Info
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    # NEW fields
    birthday = models.DateField(null=True, blank=True, help_text='Used for birthday promotions')
    preferred_worker = models.ForeignKey(
        'staff.StaffMember', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='preferred_clients',
        help_text='Preferred stylist/worker'
    )
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('salon', 'phone')
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def visit_count(self):
        return self.sale_set.filter(is_paid=True).count()

    @property
    def total_spent(self):
        from django.db.models import Sum
        return self.sale_set.filter(is_paid=True).aggregate(
            t=Sum('total_amount')
        )['t'] or 0
