from django.db import models
from django.contrib.auth.models import User
from salons.models import Salon


class StaffMember(models.Model):
    ROLE_CHOICES = [
        ('stylist', 'Stylist'),
        ('colorist', 'Colorist'),
        ('nail_tech', 'Nail Technician'),
        ('aesthetician', 'Aesthetician'),
        ('manager', 'Manager'),
        ('receptionist', 'Receptionist'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('on_leave', 'On Leave'),
    ]

    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='staff')
    user = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='staff_profile'
    )
    full_name = models.CharField(max_length=150)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='stylist')
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    hire_date = models.DateField(null=True, blank=True)
    commission_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00,
        help_text='Commission percentage e.g. 10.00 for 10%'
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['full_name']
        verbose_name = 'Staff Member'
        verbose_name_plural = 'Staff Members'

    def __str__(self):
        return f"{self.full_name} ({self.get_role_display()})"

    @property
    def is_active(self):
        return self.status == 'active'
